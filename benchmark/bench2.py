from __future__ import print_function

import random
import multiprocessing
from multiprocessing import Pool
import time
import bench2

def monte_carlo_pi_part(n):
    count = 0
    for i in range(n):
        x=random.random()
        y=random.random()

        if x*x + y*y <= 1:
            count=count+1

    return count

def GetPI(samples):
    np = multiprocessing.cpu_count()
    part_count=[int(samples/np) for i in range(np)]
    pool = Pool(processes=np)
    count=pool.map(monte_carlo_pi_part, part_count)
    return sum(count)/(samples*1.0)*4

if __name__=='__main__':
    pystart = time.time()
    pythonPi = GetPI(100000)
    pyend = time.time()
    gostart = time.time()
    gopi = bench2.GetPI(100000)
    goend = time.time()
    print("python", pyend - pystart)
    print("go", goend - gostart)
