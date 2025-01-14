// Package fs provides mountpath and FQN abstractions and methods to resolve/map stored content
/*
 * Copyright (c) 2018-2024, NVIDIA CORPORATION. All rights reserved.
 */
package fs

import (
	"runtime"
	"time"

	"github.com/NVIDIA/aistore/cmn/cos"
	"github.com/NVIDIA/aistore/sys"
)

// common throttling constants

const MaxThrottlePct = 60

const (
	Throttle1ms   = time.Millisecond
	Throttle10ms  = 10 * time.Millisecond
	Throttle100ms = 100 * time.Millisecond

	throttleBatch  = 0x1f // a.k.a. unit or period
	throMiniBatch  = 0x1f >> 1
	throMicroBatch = 0x1f >> 2
)

func IsThrottle(n int64) bool      { return n&throttleBatch == throttleBatch }
func IsMiniThrottle(n int64) bool  { return n&throMiniBatch == throMiniBatch }
func IsMicroThrottle(n int64) bool { return n&throMicroBatch == throMicroBatch }

// - max disk utilization across mountpaths
// - max (1 minute, 5 minute) load average
func ThrottlePct() (int, int64, float64) {
	var (
		load    = sys.MaxLoad()
		util    = GetMaxUtil()
		cpus    = runtime.NumCPU()
		maxload = max(cpus>>1, 1) // NOTE: artificially reducing (halving) `maxload` to report 100% earlier
	)
	if load >= float64(maxload) {
		return 100, util, load
	}
	ru := cos.RatioPct(100, 2, util)
	rl := cos.RatioPct(int64(10*maxload), 1, int64(10*load))
	return int(max(ru, rl)), util, load
}
