# Google Summer Of Code 2017 
![GSoC2017](/img/googlesummerofcode.png)

# Final Report

## Project Updating gopy to support Python3 and PyPy

## Student
[Dong-hee Na](https://github.com/corona10) / Chugnam National University

## Mentors
[Sebastien Binet](https://github.com/sbinet) / CERN-HSF

[Alexandre Claude](https://github.com/alclaude) / CERN-HSF

## Abstract
gopy is an tool which generates (and compiles) a Python extension module from a go package. Although gopy provides powerful features of Go, gopy only supported CPython2. So I proposed updating gopy to support Python3 and PyPy by using CFFI.

CFFI is C Foreign Function interface for Python. It interacts with almost any C Code from Python. While ctypes is not perfectly compatible with PyPy.

In terms of Go API can be exposed by C API which is called Cgo. this project is focused on calling Go package C API through CFFI. Through this approach, it can interact with most of existing Python compilers.

Generate CFFI codes for gopy can be done by 3 phases. First, generating wrapped Go package code. Second, Analyze which interfaces should be exposed and generate C definition functions by rule based naming. Third, Generate a wrapper Python codes which Python compiler will import.

## Supported Features.

A. Basic types
   
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
   
B. Detect functions returning a Go error and make them pythonic (raising an Exception)

```
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

## Special thanks to
* [Haeun Kim](https://github.com/haeungun/)

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


## Blog Posts:
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
