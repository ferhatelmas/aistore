package hrw_bench

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"testing"

	"github.com/OneOfOne/xxhash"
)

type hashFuncs struct {
	name      string
	hashF     func(string, []node) int
	countObjs []int
}

// Duplicated on purpose to avoid dependency on any DFC code.
func randFileName(src *rand.Rand, nameLen int) string {
	const (
		letterBytes   = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
		letterIdxBits = 6                    // 6 bits to represent a letter index
		letterIdxMask = 1<<letterIdxBits - 1 // All 1-bits, as many as letterIdxBits
		letterIdxMax  = 63 / letterIdxBits   // # of letter indices fitting in 63 bits
	)

	b := make([]byte, nameLen)
	// A src.Int63() generates 63 random bits, enough for letterIdxMax characters!
	for i, cache, remain := nameLen-1, src.Int63(), letterIdxMax; i >= 0; {
		if remain == 0 {
			cache, remain = src.Int63(), letterIdxMax
		}
		if idx := int(cache & letterIdxMask); idx < len(letterBytes) {
			b[i] = letterBytes[idx]
			i--
		}
		cache >>= letterIdxBits
		remain--
	}

	return string(b)
}

// Duplicated on purpose to avoid dependency on any DFC code.
func randNodeId(randGen *rand.Rand) string {
	randIp := ""
	for i := 0; i < 3; i++ {
		randIp += strconv.Itoa(randGen.Intn(255)) + "."
	}
	randIp += strconv.Itoa(randGen.Intn(255))
	cksum := xxhash.ChecksumString32S(randIp, xxHashSeed)
	nodeId := strconv.Itoa(int(cksum & 0xfffff))
	randPort := strconv.Itoa(randGen.Intn(65535))
	return nodeId + ":" + randPort
}

func getRandNodeIds(numNodes int, randGen *rand.Rand) []node {
	nodes := make([]node, numNodes)
	for i := 0; i < numNodes; i++ {
		id := randNodeId(randGen)
		xhash := xxhash.NewS64(xxHashSeed)
		xhash.WriteString(id)
		seed := xxhash.ChecksumString64S(id, xxHashSeed)
		nodes[i] = node{
			id:          id,
			idDigestInt: xorshift64(seed),
			idDigestXX:  xhash,
		}
	}
	return nodes
}

func writeOutputToFile(t *testing.T, hashFunc hashFuncs, numNodes int) {
	counts := fmt.Sprintf("%v", hashFunc.countObjs)
	countsStr := fmt.Sprintf("%s/%d %s\n", hashFunc.name, numNodes, counts[1:len(counts)-1])
	fmt.Printf(countsStr)
	fileName := fmt.Sprintf("nodes-%d.log", numNodes)
	f, err := os.OpenFile(fileName, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
	if err != nil {
		t.Errorf("Unable to open file to dump output. Values: [%s]", countsStr)
		return
	}
	defer f.Close()
	_, err = f.WriteString(countsStr)
	if err != nil {
		t.Errorf("Unable to write output to file. Values: [%s]", countsStr)
		return
	}
}

func get3DSlice(numRoutines, numFuncs, numNodes int) [][][]int {
	perRoutine := make([][][]int, numRoutines)
	for w := 0; w < numRoutines; w++ {
		perFunc := make([][]int, numFuncs)
		for p := range perFunc {
			perFunc[p] = make([]int, numNodes)
		}
		perRoutine[w] = perFunc
	}
	return perRoutine
}

func xorshift64(x uint64) uint64 {
	x ^= x >> 12 // a
	x ^= x << 25 // b
	x ^= x >> 27 // c
	return x * 2685821657736338717
}
