// Package transform provides utilities to initialize and use transformation pods.
/*
 * Copyright (c) 2018-2020, NVIDIA CORPORATION. All rights reserved.
 */
package transform

import (
	"github.com/NVIDIA/aistore/3rdparty/glog"
	"github.com/NVIDIA/aistore/cluster"
	"github.com/NVIDIA/aistore/cmn"
)

var (
	tar2TfSpec = []byte(`
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: tar2tf
  name: tar2tf
  annotations:
    communication_type: "hrev://"
    wait_timeout: 60s
spec:
  containers:
    - name: server
      image: aistore/tar2tf:latest
      imagePullPolicy: Always
      ports:
        - containerPort: 80
`)
)

func InitTar2TF(t cluster.Target) error {
	if targetsNodeName == "" {
		glog.Warning("Not a kubernetes deployment. tar2tf transformation won't be available")
		return nil
	}

	msg, err := ValidateSpec(tar2TfSpec)
	cmn.AssertNoErr(err)
	msg.ID = cmn.GenUUID() // Doesn't have to be the same cluster-wide.
	return StartTransformationPod(t, msg, cmn.Tar2Tf)
}
