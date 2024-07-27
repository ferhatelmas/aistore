//go:build !statsd

// Package stats provides methods and functionality to register, track, log,
// and StatsD-notify statistics that, for the most part, include "counter" and "latency" kinds.
/*
 * Copyright (c) 2018-2024, NVIDIA CORPORATION. All rights reserved.
 */
package stats

import (
	"encoding/json"
	"strings"
	"sync"
	ratomic "sync/atomic"
	"time"

	"github.com/NVIDIA/aistore/cmn/cos"
	"github.com/NVIDIA/aistore/cmn/debug"
	"github.com/NVIDIA/aistore/cmn/nlog"
	"github.com/NVIDIA/aistore/core/meta"
	"github.com/NVIDIA/aistore/memsys"
	jsoniter "github.com/json-iterator/go"
	"github.com/prometheus/client_golang/prometheus"
)

type (
	promDesc map[string]*prometheus.Desc

	coreStats struct {
		Tracker   map[string]*statsValue
		promDesc  promDesc
		sgl       *memsys.SGL
		statsTime time.Duration
		cmu       sync.RWMutex // ctracker vs Prometheus Collect()
	}
)

///////////////
// coreStats //
///////////////

// interface guard
var (
	_ json.Marshaler   = (*coreStats)(nil)
	_ json.Unmarshaler = (*coreStats)(nil)
)

func (s *coreStats) init(size int) {
	s.Tracker = make(map[string]*statsValue, size)
	s.promDesc = make(promDesc, size)

	s.sgl = memsys.PageMM().NewSGL(memsys.DefaultBufSize)
}

// vs Collect()
func (s *coreStats) promRLock()   { s.cmu.RLock() }
func (s *coreStats) promRUnlock() { s.cmu.RUnlock() }
func (s *coreStats) promLock()    { s.cmu.Lock() }
func (s *coreStats) promUnlock()  { s.cmu.Unlock() }

// init MetricClient client: StatsD (default) or Prometheus
func (*coreStats) initMetricClient(_ *meta.Snode, parent *runner) {
	nlog.Infoln("Using Prometheus")
	prometheus.MustRegister(parent) // as prometheus.Collector
}

// populate *prometheus.Desc and statsValue.label.stpr
func (s *coreStats) initProm(snode *meta.Snode) {
	id := strings.ReplaceAll(snode.ID(), ".", "_")
	for name, v := range s.Tracker {
		var variableLabels []string
		if isDiskMetric(name) {
			// obtain prometheus specific disk-metric name from tracker name
			// e.g. `disk.nvme0.read.bps` -> `disk.read.bps`.
			_, name = extractPromDiskMetricName(name)
			variableLabels = []string{diskMetricLabel}
		}
		label := strings.ReplaceAll(name, ".", "_")
		// prometheus metrics names shouldn't include daemonID.
		label = strings.ReplaceAll(label, "_"+id+"_", "_")
		v.label.stpr = strings.ReplaceAll(label, ":", "_")

		help := v.kind
		if strings.HasSuffix(v.label.stpr, "_n") {
			help = "total number of operations"
		} else if strings.HasSuffix(v.label.stpr, "_size") {
			help = "total size (bytes)"
		} else if strings.HasSuffix(v.label.stpr, "avg_rsize") {
			help = "average read size (bytes)"
		} else if strings.HasSuffix(v.label.stpr, "avg_wsize") {
			help = "average write size (bytes)"
		} else if strings.HasSuffix(v.label.stpr, "_ns") {
			v.label.stpr = strings.TrimSuffix(v.label.stpr, "_ns") + "_ms"
			help = "latency (milliseconds)"
		} else if strings.HasSuffix(v.label.stpr, "_ns_total") {
			help = "cumulative latency (nanoseconds)"
		} else if strings.Contains(v.label.stpr, "_ns_") {
			v.label.stpr = strings.ReplaceAll(v.label.stpr, "_ns_", "_ms_")
			if name == Uptime {
				v.label.stpr = strings.ReplaceAll(v.label.stpr, "_ns_", "")
				help = "uptime (seconds)"
			} else {
				help = "latency (milliseconds)"
			}
		} else if strings.HasSuffix(v.label.stpr, "_bps") {
			v.label.stpr = strings.TrimSuffix(v.label.stpr, "_bps") + "_mbps"
			help = "throughput (MB/s)"
		}

		fullqn := prometheus.BuildFQName("ais", snode.Type(), v.label.stpr)
		// e.g. metric: ais_target_disk_avg_wsize{disk="nvme0n1",node_id="fqWt8081"}
		s.promDesc[name] = prometheus.NewDesc(fullqn, help, variableLabels, prometheus.Labels{"node_id": id})
	}
}

func (s *coreStats) updateUptime(d time.Duration) {
	v := s.Tracker[Uptime]
	ratomic.StoreInt64(&v.Value, d.Nanoseconds())
}

func (s *coreStats) MarshalJSON() ([]byte, error) { return jsoniter.Marshal(s.Tracker) }
func (s *coreStats) UnmarshalJSON(b []byte) error { return jsoniter.Unmarshal(b, &s.Tracker) }

func (s *coreStats) get(name string) (val int64) {
	v := s.Tracker[name]
	val = ratomic.LoadInt64(&v.Value)
	return
}

func (s *coreStats) update(nv cos.NamedVal64) {
	v, ok := s.Tracker[nv.Name]
	debug.Assertf(ok, "invalid metric name %q", nv.Name)
	switch v.kind {
	case KindLatency:
		ratomic.AddInt64(&v.numSamples, 1)
		fallthrough
	case KindThroughput:
		ratomic.AddInt64(&v.Value, nv.Value)
		ratomic.AddInt64(&v.cumulative, nv.Value)
	case KindCounter, KindSize, KindTotal:
		ratomic.AddInt64(&v.Value, nv.Value)
	default:
		debug.Assert(false, v.kind)
	}
}

// log + StatsD (Prometheus is done separately via `Collect`)
func (s *coreStats) copyT(out copyTracker, diskLowUtil ...int64) bool {
	idle := true
	intl := max(int64(s.statsTime.Seconds()), 1)
	s.sgl.Reset()
	for name, v := range s.Tracker {
		switch v.kind {
		case KindLatency:
			var lat int64
			if num := ratomic.SwapInt64(&v.numSamples, 0); num > 0 {
				lat = ratomic.SwapInt64(&v.Value, 0) / num
				if !ignore(name) {
					idle = false
				}
			}
			out[name] = copyValue{lat}
		case KindThroughput:
			var throughput int64
			if throughput = ratomic.SwapInt64(&v.Value, 0); throughput > 0 {
				throughput /= intl
				if !ignore(name) {
					idle = false
				}
			}
			out[name] = copyValue{throughput}
		case KindComputedThroughput:
			if throughput := ratomic.SwapInt64(&v.Value, 0); throughput > 0 {
				out[name] = copyValue{throughput}
			}
		case KindCounter, KindSize, KindTotal:
			var (
				val     = ratomic.LoadInt64(&v.Value)
				changed bool
			)
			if prev, ok := out[name]; !ok || prev.Value != val {
				changed = true
			}
			if val > 0 {
				out[name] = copyValue{val}
				if changed && !ignore(name) {
					idle = false
				}
			}
		case KindGauge:
			val := ratomic.LoadInt64(&v.Value)
			out[name] = copyValue{val}
			if isDiskUtilMetric(name) && val > diskLowUtil[0] {
				idle = false
			}
		default:
			out[name] = copyValue{ratomic.LoadInt64(&v.Value)}
		}
	}
	return idle
}

// REST API what=stats query
// NOTE: not reporting zero counts
func (s *coreStats) copyCumulative(ctracker copyTracker) {
	for name, v := range s.Tracker {
		switch v.kind {
		case KindLatency:
			ctracker[name] = copyValue{ratomic.LoadInt64(&v.cumulative)}
		case KindThroughput:
			val := copyValue{ratomic.LoadInt64(&v.cumulative)}
			ctracker[name] = val

			// NOTE: effectively, add same-value metric that was never added/updated
			// via `runner.Add` and friends. Is OK to replace ".bps" suffix
			// as statsValue.cumulative _is_ the total size (aka, KindSize)
			n := name[:len(name)-3] + "size"
			ctracker[n] = val
		case KindCounter, KindSize, KindTotal:
			if val := ratomic.LoadInt64(&v.Value); val > 0 {
				ctracker[name] = copyValue{val}
			}
		default: // KindSpecial, KindComputedThroughput, KindGauge
			ctracker[name] = copyValue{ratomic.LoadInt64(&v.Value)}
		}
	}
}

func (s *coreStats) reset(errorsOnly bool) {
	if errorsOnly {
		for name, v := range s.Tracker {
			if IsErrMetric(name) {
				debug.Assert(v.kind == KindCounter || v.kind == KindSize, name)
				ratomic.StoreInt64(&v.Value, 0)
			}
		}
		return
	}

	for _, v := range s.Tracker {
		switch v.kind {
		case KindLatency:
			ratomic.StoreInt64(&v.numSamples, 0)
			fallthrough
		case KindThroughput:
			ratomic.StoreInt64(&v.Value, 0)
			ratomic.StoreInt64(&v.cumulative, 0)
		case KindCounter, KindSize, KindComputedThroughput, KindGauge, KindTotal:
			ratomic.StoreInt64(&v.Value, 0)
		default: // KindSpecial - do nothing
		}
	}
}

////////////
// runner //
////////////

// interface guard
var (
	_ prometheus.Collector = (*runner)(nil)
)

// NOTE naming convention: ".n" for the count and ".ns" for duration (nanoseconds)
// compare with coreStats.initProm()
func (r *runner) reg(_ *meta.Snode, name, kind string) {
	v := &statsValue{kind: kind}
	// in StatsD metrics ":" delineates the name and the value - replace with underscore
	switch kind {
	case KindCounter:
		debug.Assert(strings.HasSuffix(name, ".n"), name) // naming convention
		v.label.comm = strings.TrimSuffix(name, ".n")
		v.label.comm = strings.ReplaceAll(v.label.comm, ":", "_")
	case KindTotal:
		debug.Assert(strings.HasSuffix(name, ".total"), name) // naming convention
		v.label.comm = strings.ReplaceAll(v.label.comm, ":", "_")
	case KindSize:
		debug.Assert(strings.HasSuffix(name, ".size"), name) // naming convention
		v.label.comm = strings.TrimSuffix(name, ".size")
		v.label.comm = strings.ReplaceAll(v.label.comm, ":", "_")
	case KindLatency:
		debug.Assert(strings.Contains(name, ".ns"), name) // ditto
		v.label.comm = strings.TrimSuffix(name, ".ns")
		v.label.comm = strings.ReplaceAll(v.label.comm, ".ns.", ".")
		v.label.comm = strings.ReplaceAll(v.label.comm, ":", "_")
	case KindThroughput, KindComputedThroughput:
		debug.Assert(strings.HasSuffix(name, ".bps"), name) // ditto
		v.label.comm = strings.TrimSuffix(name, ".bps")
		v.label.comm = strings.ReplaceAll(v.label.comm, ":", "_")
	default:
		debug.Assert(kind == KindGauge || kind == KindSpecial)
		v.label.comm = name
		v.label.comm = strings.ReplaceAll(v.label.comm, ":", "_")
		if name == Uptime {
			v.label.comm = strings.ReplaceAll(v.label.comm, ".ns.", ".")
		}
	}
	r.core.Tracker[name] = v
}

func (*runner) IsPrometheus() bool { return true }

func (r *runner) Describe(ch chan<- *prometheus.Desc) {
	for _, desc := range r.core.promDesc {
		ch <- desc
	}
}

func (r *runner) Collect(ch chan<- prometheus.Metric) {
	if !r.StartedUp() {
		return
	}
	r.core.promRLock()
	for name, v := range r.core.Tracker {
		var (
			val int64
			fv  float64

			variableLabels []string
		)
		copyV, okc := r.ctracker[name]
		if !okc {
			continue
		}
		val = copyV.Value
		fv = float64(val)
		// 1. convert units
		switch v.kind {
		case KindCounter, KindTotal:
			// do nothing
		case KindSize:
			fv = float64(val)
		case KindLatency:
			millis := cos.DivRound(val, int64(time.Millisecond))
			fv = float64(millis)
		case KindThroughput:
			fv = roundMBs(val)
		default:
			if name == Uptime {
				seconds := cos.DivRound(val, int64(time.Second))
				fv = float64(seconds)
			}
		}
		// 2. convert kind
		promMetricType := prometheus.GaugeValue
		if v.kind == KindCounter || v.kind == KindSize || v.kind == KindTotal {
			promMetricType = prometheus.CounterValue
		}
		if isDiskMetric(name) {
			var diskName string
			diskName, name = extractPromDiskMetricName(name)
			variableLabels = []string{diskName}
		}
		// 3. publish
		desc, ok := r.core.promDesc[name]
		debug.Assert(ok, name)
		m, err := prometheus.NewConstMetric(desc, promMetricType, fv, variableLabels...)
		debug.AssertNoErr(err)
		ch <- m
	}
	r.core.promRUnlock()
}

// extractPromDiskMetricName returns prometheus friendly metrics name
// from disk tracker name of format `disk.<disk-name>.<metric-name>`
// it returns, two strings:
//  1. <disk-name> used as prometheus variable label
//  2. `disk.<metric-name>` used for prometheus metric name
func extractPromDiskMetricName(name string) (diskName, metricName string) {
	diskName = strings.Split(name, ".")[1]
	return diskName, strings.ReplaceAll(name, "."+diskName+".", ".")
}

func (r *runner) Stop(err error) {
	nlog.Infof("Stopping %s, err: %v", r.Name(), err)
	r.stopCh <- struct{}{}
	close(r.stopCh)
}