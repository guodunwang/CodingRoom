package main

import (
	"fmt"
	"sync"
	"testing"
)

func TestCounter(t *testing.T) {
	var counter int64 // 计数值

	var wg sync.WaitGroup

	for i := 0; i < 64; i++ {
		go func() {
			for i := 0; i < 1000000; i++ {
				counter++
			}

			wg.Done()
		}()
	}

	wg.Wait()

	if counter != 64000000 {
		t.Errorf("counter should be 64000000, but got %d", counter)
	}
}

// 下面写一个main版本的

func main() {
	var counter int64 // 计数值

	var wg sync.WaitGroup
	var mu sync.Mutex

	wg.Add(64)
	for i := 0; i < 64; i++ {
		go func() {
			for i := 0; i < 1000000; i++ {
				mu.Lock()
				counter++
				mu.Unlock()
			}
			wg.Done()
		}()
	}
	wg.Wait()

	fmt.Println(counter) // 在这儿的时候，counter还是0。到了下面, counter就是别的值了。

	if counter != 64000000 {
		fmt.Printf("counter should be 64000000, but got %d \n", counter)
	}
}
