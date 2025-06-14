# OOSpy Interpreter
OOSpy Interpreter (In the context of book: "Introduction to Electrical Engineering and Computer Science I by Leslie Kaelbling & figures by Dennis Freeman" which is used in MIT OCW SC 6.01 course) is a mixture of Scheme and Python.It also supports object oriented paradigm.
This interpreter only implements fundamental built-in functions which are addition, divison, multiplication, substraction, and comparison. The purpose of this project was to gain further insight on behaviour of computer programs and to understand the general idea behind an interpreter by building one.

# Basic Syntax
The syntax of spy is fully parenthesized prefix syntax. Prefix means that the name of the function or operation comes before its arguments. And it'll have parentheses around every sub-expression. So to write `7 - 3x`, we would write:

`(- 7 (* 3 x))`

## Assignment
`(set x 34)` will assign 34 to variable x.

## Basic Built-In Functions
`+`, `-`, `*`, `/`, `=` are basic builtin functions here's an example for each function:
- `(+ 5 3)` will **add** the values and return the result: 8
- `(- 5 3)` will **substract** the second value from the first and return the result: 2
- `(* 5 3)` will **multiply** the values and return the result: 15
- `(/ 5 3)` will **divide** the first value with second value return the result: 1.6666666666666667
- `(= 5 3)` will compare both numbers and return `True` if they're the same otherwise it'll return `False`

## Compound Expressions
In Spy the body of a function definition, and the branches of an if expession, are expected to be a single expression;
in order to evaluate multiple expressions in one of those locations, there needs to be a grouping functionality, here's an example how that would look:

```
(begin
  (set x 4)
  (set y 43)
  (+ x y)
)
  ```

The value of a compound expression is the value of it's last component/expresson, and for this example that would be:

`4 + 43 = 47`

## Function Definition
`(def <function name> <function parameters> <function body>)` Function body should be a single expression. A compound expression should be used when needed. Here's an example for function definition:

`(def cube (x) (* x (* x x))` is a function that would return the cube of given parameter `x`

## Function Call
`(<function name> <parameters>)` function name and parameters can be expressions to be evaluated, here's an example function call of `cube` which was declared in previous section:

`cube 4`

## If Statements

`(if <condition> <true body> <false body>` if the condition is true the `<true body>` will get executed if it's false then the `<false body>` will get executed

## Class Declaration

## Class Method Calls

# General Ideas Behind this Interpreter

# How To Install And Run a Program
You need to get these files to your local machine in a folder. Then to run a program you need to open a terminal on that folder and type:

`python interpreter.py <path to your program>`

You can run the example "Averager.spy" program instead by typing:

`python interpreter.py Averager.spy`

It also have a shell which works in read execute print loop. There is an extra keyword "env" which lets you view the global environment 
