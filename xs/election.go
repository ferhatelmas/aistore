// Package runners provides implementation for the AIStore extended actions.
/*
 * Copyright (c) 2018-2020, NVIDIA CORPORATION. All rights reserved.
 */
package xs

import (
	"github.com/NVIDIA/aistore/cluster"
	"github.com/NVIDIA/aistore/cmn"
	"github.com/NVIDIA/aistore/cmn/cos"
	"github.com/NVIDIA/aistore/cmn/debug"
	"github.com/NVIDIA/aistore/xaction"
	"github.com/NVIDIA/aistore/xaction/xreg"
)

type (
	eleFactory struct {
		xact *Election
	}
	Election struct {
		xaction.XactBase
	}
)

// interface guard
var (
	_ cluster.Xact       = (*Election)(nil)
	_ xreg.GlobalFactory = (*eleFactory)(nil)
)

func (*eleFactory) New(_ xreg.XactArgs) xreg.GlobalEntry { return &eleFactory{} }

func (p *eleFactory) Start(_ cmn.Bck) error {
	args := xaction.Args{ID: xaction.BaseID(cos.GenUUID()), Kind: cmn.ActElection}
	p.xact = &Election{XactBase: *xaction.NewXactBase(args)}
	return nil
}

func (*eleFactory) Kind() string                         { return cmn.ActElection }
func (p *eleFactory) Get() cluster.Xact                  { return p.xact }
func (*eleFactory) PreRenewHook(_ xreg.GlobalEntry) bool { return true }
func (*eleFactory) PostRenewHook(_ xreg.GlobalEntry)     {}

func (*Election) Run() { debug.Assert(false) }