# Google Summer Of Code 2017 
![GSoC2017](/img/googlesummerofcode.png)

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
## Benchmark


## Limitations
* [Need to fix cgo policy for using gopy on production mode.](https://github.com/go-python/gopy/issues/103)
* [Go interfaces is not yet fully supported.](https://github.com/go-python/gopy/issues/114)
* Need to support more types.

## Conclusion

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
