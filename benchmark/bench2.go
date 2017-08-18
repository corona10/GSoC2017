package bench2

import (
        "math"
        "math/rand"
        "runtime"
        "sync"
        "time"
)

func monte_carlo_pi(reps int, result *int, wait *sync.WaitGroup) {
        var x, y float64
        count := 0
        seed := rand.NewSource(time.Now().UnixNano())
        random := rand.New(seed)

        for i := 0; i < reps; i++ {
                x = random.Float64() * 1.0
                y = random.Float64() * 1.0

                if num := math.Sqrt(x*x + y*y); num < 1.0 {
                        count++
                }
        }

        *result = count
        wait.Done()
}

func GetPI(samples int) float64 {
        cores := runtime.NumCPU()
        runtime.GOMAXPROCS(cores)

        var wait sync.WaitGroup

        counts := make([]int, cores)

        wait.Add(cores)

        for i := 0; i < cores; i++ {
                go monte_carlo_pi(samples/cores, &counts[i], &wait)
        }

        wait.Wait()

        total := 0
        for i := 0; i < cores; i++ {
                total += counts[i]
        }

        pi := (float64(total) / float64(samples)) * 4
        return pi
}
