from __future__ import print_function
import random
import time
import bench1

def FindElementIdx(numbers, value):
   for idx, v in enumerate(numbers):
      if v is value:
          return idx

   return -1

if __name__ == "__main__":
    python = 0.0
    go = 0.0
    for i in range(1000):
        numbers = list(range(1, 1000))
        random.shuffle(numbers)
        gostart = time.time()
        goidx = bench1.FindElementIdx(numbers, 555)
        goend = time.time()
        pystart = time.time()
        pyidx = FindElementIdx(numbers, 555)
        pyend = time.time()
        python += (pyend-pystart)
        go += (goend-gostart)

    print("Python:", python)
    print("gopy:", go)
