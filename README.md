# Google Summer Of Code 2017 
![GSoC2017](/img/googlesummerofcode.png)

## Organization
![CERN-HSF](/img/cern-hsf.png)

# Final Report
  * [Updating gopy to support Python3 and PyPy](#updating-gopy-to-support-python3-and-pypy)
  * [Mentors](#mentors)
  * [Student](#student)
  * [Supported Features.](#supported-features)
  * [Benchmark](#benchmark)
  * [Limitations](#limitations)
  * [Conclusion](#conclusion)
  * [Pull Requests](#pull-requests)
  * [Blog Posts](#blog-posts)
  * [Special thanks to](#special-thanks-to)


## Updating gopy to support Python3 and PyPy
gopy is an tool which generates (and compiles) a Python extension module from a go package. Although gopy provides powerful features of Go, gopy only supported CPython2. So I proposed updating gopy to support Python3 and PyPy by using CFFI.

CFFI is C Foreign Function interface for Python. It interacts with almost any C Code from Python. While ctypes is not perfectly compatible with PyPy.

In terms of Go API can be exposed by C API which is called Cgo. this project is focused on calling Go package C API through CFFI. Through this approach, it can interact with most of existing Python compilers.

Generating CFFI codes for gopy can be done by 3 phases. First, generate wrapped Go package code. Second, Analyze which interfaces should be exposed and generate C definition functions by rule based naming. Third, Generate a wrapper Python codes which Python compiler will import.

[Proposal slide](slide/gsoc_cern_talks_gopy.pdf)

## Mentors
[Sebastien Binet](https://github.com/sbinet) / [CERN-HSF](http://hepsoftwarefoundation.org/)

[Alexandre Claude](https://github.com/alclaude) / [CERN-HSF](http://hepsoftwarefoundation.org/)

## Student
[Dong-hee Na](https://github.com/corona10) / [Chugnam National University](http://www.cnu.ac.kr)

## Supported Features.

**A. Basic types**
   
```go
package simple
   
func Add(i, j int) int {
        return i + j
}

func Bool(b bool) bool {
        return b
}

func Comp64Add(i, j complex64) complex64 {
        return i + j
}

```
simple package can be easily imported by Python.
And Python can call each of Go functions which use basic types parameters and basic types return values.
   
```python
import simple
   
a = simple.Add(5,3)
b = simple.Bool(True)
c = simple.Comp64Add(3+5j, 2+2j)
```
   
**B. Detect functions returning a Go error and make them pythonic (raising an Exception)**

```go
package pyerrors

import "errors"

// Div is a function for detecting errors.
func Div(i, j int) (int, error) {
        if j == 0 {
                return 0, errors.New("Divide by zero.")
        }
        return i / j, nil
}
```
Go supports returning error types to detect error has occurred.
By using gopy and cffi engine it can be detected on Python side by the pythonic way.

```python
def div(a, b):
    try:
        r = pyerrors.Div(a, b)
        print("pyerrors.Div(%d, %d) = %d"% (a, b, r))
    except Exception as e:
        print(e)

div(5,0)
div(5,2)
```

**C. Go struct**

```go
type S struct{}

func (S) Init() {}
func (S) Upper(s string) string {
        return strings.ToUpper(s)
}

func FuncTest(item S) {}

func (this S) MethodTest(item S1) {}

type S1 struct {
        private int
}

type S2 struct {
        Public  int
        private int
}
```

Go’s structs are typed collections of fields. They’re useful for grouping data together to form records.
By using gopy and cffi engine, a user can import Go' structs and use its method and fields.

```python
import structs

print("s = structs.S()")
s = structs.S()
print("s = %s" % (s,))
print("s.Init()")
s.Init()
print("s.Upper('boo')= %r" % (s.Upper("boo"),))

print("s1 = structs.S1()")
s1 = structs.S1()
print("s1 = %s" %(s1,))
```

**D. Constants**

```go
package consts

const (
        C1 = "c1"
        C2 = 42
        C3 = 666.666
)
```

Constants are a read-only variable of Go.
gopy supports constants of Go by accessing `Get` methods.

```python
import consts

print("c1 = %s" % consts.GetC1())
print("c2 = %s" % consts.GetC2())
print("c3 = %s" % consts.GetC3())
```

**E. Variables**
```go
package vars

var (
        V1 = "v1"
        V2 = 42
        V3 = 666.666
)

var (
        V4 string  = "c4"
        V5 int     = 42
        V6 uint    = 42
        V7 float64 = 666.666
)
```

gopy with CFFI engine supports accessing variables by `Get/Set` methods.

```python
import vars

print("Initial values")
print("v1 = %s" % vars.GetV1())
print("v2 = %s" % vars.GetV2())
print("v3 = %s" % vars.GetV3())
print("v4 = %s" % vars.GetV4())
print("v5 = %s" % vars.GetV5())
print("v6 = %s" % vars.GetV6())
print("v7 = %s" % vars.GetV7())
```

**F. Arrays**
```go
package arrays

func IntSum(a [4]int) int {
        sum := 0
        for i := 0; i < len(a); i++ {
                sum += a[i]
        }
        return sum
}

func CreateArray() [4]int {
        return [4]int{1, 2, 3, 4}
}
```
An array is a fixed size elements arrangement.
gopy with CFFI engine supports Go's arrays.
It supports random accessing of arrays. Also, it supports arrays as function arguments.

```python
import arrays

a = [1,2,3,4]
b = arrays.CreateArray()
print ("Python list:", a)
print ("Go array: ", b)
print ("arrays.IntSum from Python list:", arrays.IntSum(a))
print ("arrays.IntSum from Go array:", arrays.IntSum(b))
```

**G. Slices**
```go
package slices

func IntSum(s []int) int {
        sum := 0
        for _, value := range s {
                sum += value
        }
        return sum
}

func CreateSlice() []int {
        return []int{1, 2, 3, 4}
}
```
A slice is a dynamically-sized, flexible view into the elements of an array. 
gopy with CFFI engine supports Go's slices.
It supports basic slices operations.
Also, it supports slices as function arguments.

```python
import slices

a = [1,2,3,4]
b = slices.CreateSlice()
print ("Python list:", a)
print ("Go slice: ", b)
print ("slices.IntSum from Python list:", slices.IntSum(a))
print ("slices.IntSum from Go slice:", slices.IntSum(b))
```
**H. maps**
```go
package maps

import (
        "sort"
)

func Sum(t map[int]float64) float64 {
        sum := 0.0
        for _, v := range t {
                sum += v
        }

        return sum
}

func New() map[int]float64 {
        return map[int]float64{
                1: 3.0,
                2: 5.0,
        }
}
```
A map is a key/value data structure of Go.
This feature is supported by CFFI engine.
A user can pass the parameter Python dict as a map parameter also.

```python
from __future__ import print_function
import maps

a = maps.New()
b = {1: 3.0, 2: 5.0}
print('maps.Sum from Go map:', maps.Sum(a))
print('maps.Sum from Python dictionary:', maps.Sum(b))
```

**I. Named types**

```go
package named

type Float float32

// Value returns a float32 value
func (f Float) Value() float32 { return float32(f) }

type X float32
type XX X
type XXX XX
type XXXX XXX

// Value returns a float32 value
func (x X) Value() float32 { return float32(x) }

// Value returns a float32 value
func (x XX) Value() float32 { return float32(x) }

// Value returns a float32 value
func (x XXX) Value() float32 { return float32(x) }

// Value returns a float32 value
func (x XXXX) Value() float32 { return float32(x) }
```
Go supports to define user custom typed with named.
By using gopy, it can be used by package method.

```python
import named

print("v = named.Float()")
v = named.Float()
print("v = %s" % (v,))
print("v.Value() = %s" % (v.Value(),))

print("x = named.X()")
x = named.X()
print("x = %s" % (x,))
print("x.Value() = %s" % (x.Value(),))

print("x = named.XX()")
x = named.XX()
print("x = %s" % (x,))
print("x.Value() = %s" % (x.Value(),))
```

**J. Unnamed types**

```go
package hi

var (
        IntSlice = []int{1, 2}                      // A slice of ints
        IntArray = [2]int{1, 2}                     // An array of ints
)
```

Go supports to define user custom typed with unnamed.
By using gopy, it can be used by calling package method.

```python

import hi
a = hi.GetIntArray()
print(a)
print(a[0])
print(a[1])
print(len(a))
```

**K. Go documentation extraction**

```go
package extract


const (
        PI float64  = 3.14
)

// Type S1 has a public field 
type S1 struct {
        Public int
}

// Add is function which returns sum of two variables.
func Add(a int, b int) int {
        return a + b
}
```

Go supports a documentation feature through Godoc.
It is a similar feature with Python's Pydoc.
gopy also migrate Go's documentation for the vars, functions, and types into Pydoc.
Here is the example.

```python
root@180a6474ebba:~/go/src/github.com/go-python/gopy/_examples/extract# pypy 
Python 2.7.10 (5.1.2+dfsg-1~16.04, Jun 16 2016, 17:37:42)
[PyPy 5.1.2 with GCC 5.3.1 20160413] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>> import extract
>>>> dir(extract)
['Add', 'GetGSoC', 'GetPI', 'S1', 'SetGSoC', '_PY3', '__builtins__', '__cached__', '__doc__', '__file__', '__name__', '__package__', '_cffi_backend', '_cffi_helper', 'collections', 'ffi', 'os', 'sys']
>>>> print(extract.Add.__doc__)
Add(int a, int b) int

Add is function which returns sum of two variables.

>>>> print(extract.GetGSoC.__doc__)
returns extract.GSoC
>>>> print(extract.SetGSoC.__doc__)
sets extract.GSoC
>>>> print(extract.S1.__doc__)
Type S1 has a public field

>>>> 
```

## Benchmark

**A. FindElementOfIndex Test**

* [Python code](/benchmark/bench1.py)
* [Go code](/benchmark/bench1.py)

```go
package bench1

func FindElementIdx(arrays []int, value int) int {
        for idx, v := range arrays {
                if v == value {
                        return idx
                }
        }

        return -1;
}
```

```python
def FindElementIdx(numbers, value):
   for idx, v in enumerate(numbers):
      if v is value:
          return idx

   return -1
```

| Python Interpreter | Python time elapsed(sec)| gopy time elapsed (sec)  |
|:------------------:|----------------------|--------------------|
| Python2            | 0.0396955013275      | 3.74620819092      |
| Python3            | 0.043562889099121094 | 3.0519542694091797 |
| PyPy               | 0.00602054595947     | 2.59648394585      |


**B. Calculating PI with Monte Carlo method Test**

* [Python code](/benchmark/bench2.py)
* [Go code](/benchmark/bench2.py)

```go
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
```
```python
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
```

| Sample Counts | CPython2 elapsed (sec) |  gopy elapsed (sec) |
|:-------------:|:----------------------:|:------------------:|
| 10            |        0.009872        |      0.001530      |
| 100           |        0.004988        |      0.000714      |
| 1000          |        0.006712        |      0.00076       |
| 10000         |        0.006253        |      0.000823      |
| 100000        |        0.020241        |      0.002766      |
| 1000000       |        0.132703        |      0.016841      |

*CPython2 VS gopy benchmark*

| Sample Counts | PyPy elapsed (sec) | gopy elapsed (sec) |
|:-------------:|:------------------:|:-----------------:|
| 10            |     0.013827     |      0.001615     |
| 100           |       0.00939      |      0.000846     |
| 1000          |      0.009166      |      0.000682     |
| 10000         |      0.020542      |      0.000975     |
| 100000        |      0.020035      |      0.002385     |
| 1000000       |      0.034196      |      0.012172     |

*PyPy VS gopy benchmark*

| Sample Counts | CPython3 elapsed (sec) | gopy elapsed(sec) |
|:-------------:|:----------------------:|:-----------------:|
| 10            |        0.0018612       |      0.001381     |
| 100           |        0.008366        |      0.000763     |
| 1000          |        0.007015        |      0.000777     |
| 10000         |        0.010334        |      0.000897     |
| 100000        |        0.023466        |      0.002581     |
| 1000000       |        0.117782        |      0.016638     |

*CPython3 VS gopy benchmark*

### Benchmark Analysis
As you can see `FindElementOfIndex Test`, Although Go run itself as compiled program, Communication overhead between Python VM and Go is not cheap. For example, If Python passes the parameters with Python list or dict, It converts them into Go objects such as Slices or Arrays. This operation is done by deep copying and its cost is very heavy. If we can solve this issue by the more efficient way.(e.g referencing elements). Communication overhead could be reduced. And the other side, if we see the result of `Calculating PI with Monte Carlo method Test`, Python can solve highly heavy multi-threaded calculation faster than pure Python calculation by using gopy. It means that we can solve this kind of calculation with the power of the goroutine and elapsed times can be reduced through gopy.

## Limitations
* [Need to fix cgo policy for using gopy on production mode.](https://github.com/go-python/gopy/issues/103)
* [Go interfaces is not yet fully supported.](https://github.com/go-python/gopy/issues/114)
* Need to support more types.

## Conclusion
For this Google Summer of Code 2017, I and Sebastien did a lot of things for gopy project.
We added a CFFI engine for gopy. And now, gopy supports PyPy and Python3. Also, Python can use lots of Go's feature though gopy including Slice, Arrays, and maps.
And this was the main task of Google Summer Of Code 2017.
gopy is not always the best answer for Python. because there is a communication overhead between Python VM and Go.
However, if Python needs to calculate heavy task with a multi-threaded method, Using gopy will provide tremendous performance improvements with the power of goroutine. It was also proved by our benchmark result.

There are a lot of experimental project for between Go and other languages. And we believe gopy is one of the successful projects for that objective. However, There are few things to solve for gopy to be used in real world production. And removing cgocheck policy is one of the things.

Although Google Summer of Code 2017 is ended, I am going to contribute gopy project to use this project for real world production. And I hope more people join gopy project also. I and Sebastien always welcome those people.

And finally, I am really thanks to Sebastien. He gave me a chance to participate in Google Summer of Code 2017.
His highly contributing for Go community leads a lot of projects including gopy, I hope that we can work together even after Google Summer of Code 2017.


## Pull Requests
* [bind: make sure GODEBUG=cgocheck=0 for Go>=1.6](https://github.com/go-python/gopy/pull/91)
* [gopy,bind: add boilerplate code for cffi support](https://github.com/go-python/gopy/pull/93)
* [bind, gencffi: Remove generating builders and support Vars and Consts.](https://github.com/go-python/gopy/pull/98)
* [gencffi: Detect functions returning a Go error](https://github.com/go-python/gopy/pull/105)
* [gopy: go-1.9 requires exactly one main package for c-shared libs](https://github.com/go-python/gopy/pull/109)
* [gencffi: Support bool types](https://github.com/go-python/gopy/pull/111)
* [cffi: Support struct types.](https://github.com/go-python/gopy/pull/113)
* [cffi: Let Python3 handles string as ASCII.](https://github.com/go-python/gopy/pull/115)
* [cffi: Support complex number types.](https://github.com/go-python/gopy/pull/116)
* [cffi: Support named type + Pass 'seq.go' test.](https://github.com/go-python/gopy/pull/120)
* [cffi: Support unnamed types and pass hi.go](https://github.com/go-python/gopy/pull/123)
* [cffi: Implement wrapping of functions with slices/arrays of builtin arguments](https://github.com/go-python/gopy/pull/129)
* [cffi: Updates README.md](https://github.com/go-python/gopy/pull/133)
* [cffi: Support built-in maps.](https://github.com/go-python/gopy/pull/137)


## Blog Posts
* [My Google Summer Of Code 2017 project with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Accepted/)
* [[GSoC 2017] Community bonding period with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-community-bonding/)
* [[GSoC 2017] Coding period Week1 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week1/)
* [[GSoC 2017] Coding period Week2 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week2/)
* [[GSoC 2017] Coding period Week3 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week3/)
* [[GSoC 2017] Coding period Week4 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week4/)
* [[GSoC 2017] Coding period Week5 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week5/)
* [[GSoC 2017] Coding period Week6 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week6/)
* [[GSoC 2017] Coding period Week7 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week7/)
* [[GSoC 2017] Coding period Week8 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week8/)
* [[GSoC 2017] Coding period Week9 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week9/)
* [[GSoC 2017] Coding period Week10 with gopy@CERN-HSF](http://corona10.github.io/GSoC2017-Week10/)

## Special thanks to
* [Haeun Kim](https://github.com/haeungun/)
