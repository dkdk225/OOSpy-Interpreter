# OOSpy Interpreter
OOSpy Interpreter (In the context of book: "Introduction to Electrical Engineering and Computer Science I by Leslie Kaelbling & figures by Dennis Freeman" which is used in MIT OCW SC 6.01 course) is a mixture of Scheme and Python.It also supports object oriented paradigm.
This interpreter only implements fundamental built-in functions which are addition, divison, multiplication, substraction, and comparison. The purpose of this project was to gain further insight on behaviour of computer programs and to understand the general idea behind an interpreter by building one.

# Table of Contents

- [Basic Syntax](#basic-syntax)
  - [Assignment](#assignment)
  - [Basic Built-In Functions](#basic-built-in-functions)
  - [Compound Expressions](#compound-expressions)
  - [Function Definition](#function-definition)
  - [Function Call](#function-call)
  - [If Statements](#if-statements)
  - [Class Definition](#class-definition)
  - [Instantiating a Class](#instantiating-a-class)
  - [Accessing Attributes](#accessing-attributes)
  - [Class Method Calls](#class-method-calls)
- [General Ideas Behind this Interpreter](#general-ideas-behind-this-interpreter)
  - [Binding Environments](#binding-environments)
  - [Global Environment](#global-environment)
  - [Variables](#variables)
  - [Procedures(Functions)](#proceduresfunctions)
  - [Procedure Calls](#procedure-calls)
  - [Classes](#classes)
  - [Primitive Procedures](#primitive-procedures)
- [How To Install And Run a Program](#how-to-install-and-run-a-program)
  
<a name="basic-syntax"></a>
# Basic Syntax
The syntax of spy is fully parenthesized prefix syntax. Prefix means that the name of the function or operation comes before its arguments. And it'll have parentheses around every sub-expression. So to write `7 - 3x`, we would write:

`(- 7 (* 3 x))`

<a name="assignment"></a>
## Assignment
`(set x 34)` will assign 34 to variable x.

`(set (attr object x) 43)` will assign 43 to attribute `x` of `object`

<a name="basic-built-in-functions"></a>
## Basic Built-In Functions
`+`, `-`, `*`, `/`, `=` are basic builtin functions here's an example for each function:
- `(+ 5 3)` will **add** the values and return the result: 8
- `(- 5 3)` will **substract** the second value from the first and return the result: 2
- `(* 5 3)` will **multiply** the values and return the result: 15
- `(/ 5 3)` will **divide** the first value with second value return the result: 1.6666666666666667
- `(= 5 3)` will compare both numbers and return `True` if they're the same otherwise it'll return `False`

<a name="compound-expressions"></a>
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

<a name="function-definition"></a>

## Function Definition
`(def <function name> <function parameters> <function body>)` Function body should be a single expression. A compound expression should be used when needed. Here's an example for function definition:

`(def cube (x) (* x (* x x))` is a function that would return the cube of given parameter `x`

<a name="function-call"></a>

## Function Call
`(<function name> <parameters>)` function name and parameters can be expressions to be evaluated, here's an example function call of `cube` which was declared in previous section:

`cube 4`


<a name="if-statements"></a>

## If Statements

`(if <condition> <true body> <false body>` if the condition is true the `<true body>` will get executed if it's false then the `<false body>` will get executed. Here's an example:

`(if (= 6 6) (+ 1 1) (- 2 9))` 

This example will return 2 since the condition is true.

<a name="class-definition"></a>

## Class Definition
`(class <name> <parent> <body>)` `<parent>` can be `None` if the class has no parent.
Here's an example class definition:

```
(class Point None
  (begin
    (def init (self x y)
      (set (attr self x) x)
      (set (attr self y) y)
    )
  )
)
```
Classes have no specially named methods that gets called automatically. So after instantiating the `Point` class `init` method has to be called manually.
Classes are implemented as functions not environments therefore they cannot be changed after definition.

<a name="instantiating-a-class"></a>

## Instantiating a Class

`(<class name>)` will return a class instance. `set` can be used to assign the instance to a variable like this:

`(set <object name> (<class name>)`

Here's an example for the class declared in previous section:

`(set point (Point)`

<a name="accessing-attributes"></a>

## Accessing Attributes

`(attr <object name> <attribute name>` is used for accessing attributes of objects.

You can change the values of attributes of an object this way:

`(set (attr <object name> <attribute name>) <new value>`

You can call class methods this way:

`((attr <object name> <method name>) <parameters>)`

<a name="class-method-calls"></a>

## Class Method Calls

`((attr <object name> <method name>) <parameters>)` is used for calling class methods here's an example for `point` object declared couple sections before:

`((attr point init) 5 7)` this method call will set values of attributes x to 5 and y to 7 in point object.

<a name="general-ideas-behind-this-interpreter"></a>

# General Ideas Behind this Interpreter

<a name="binding-environments"></a>

## Binding Environments

Binding environments are tables that have names on one side and values associated with those names on the other side. Many aspects of the programming language are built upon environments these will be explained in next sections. 
Alongside key-value pairs environments have a parent property. When a key is not in the environment, parent environment is checked.
To implement an envrionment an hash map can be used.

| Key  | Value  |
|------|--------|
| a    | 9      |
| b    | 2.8    |
| foo  | -15    |

<a name="global-environment"></a>

## Global Environment

Global environment contains the definitions of basic built-in functions `+` `-` `*` `/` and `=`. It is the parent of all other environments.

<a name="variables"></a>

## Variables

`(set <name> <value>)` when interpreter reads these lines it sets the `<name>` to `<value>` in environment which statement is in.
For example `(set bar 39)` will set the value corresponding to `bar` key in the table to `39`. As a result we'll have a table that looks like this:

| Key  | Value  |
|------|--------|
| a    | 9      |
| b    | 2.8    |
| foo  | -15    |
| bar  | 39     |

<a name="proceduresfunctions"></a>

## Procedures(Functions)

Procedures are objects, containing data about the procedure defined. Data contained is, parameter list procedure body and a pointer to the environment in which the procedure was declared. When a procedure is declared, interpreter binds the function name to function object created, in the binding environment. 
The procedure object looks like this:
```
{
  params_list: <list of parameters>
  body: <tokenized expression>
  env: <pointer to the environment in which the function is declared>
}
```
<a name="procedure-calls"></a>

## Procedure Calls

When a procedure is called every argument is evaluated. Then a new environment is created for procedure and evaluated arguments are assigned to arguments stated in proceduere definition. This environment has a parent environment which is the same as procedure object.

<a name="classes"></a>

## Classes

Classes are primitive procedures that return binding environments. These binding environments have a parent and when a attribute is not in the environment the parent is checked for the attribute. If a class has no parent then it's parent is the global environment.

<a name="primitive-procedures"></a>

## Primitive Procedures

Primitive procedures are like built-in functions in python. They are built in into the interpreter and determine the limits of the language. For example addition is a primitive function if the interpreter didn't know how to add it wouldn't be possible to write some logic with other programming components to add 2 numbers.


<a name="how-to-install-and-run-a-program"></a>

# How To Install And Run a Program
You need to get these files to your local machine in a folder. Then to run a program you need to open a terminal on that folder and type:

`python interpreter.py <path to your program>`

You can run the example "Averager.spy" program instead by typing:

`python interpreter.py Averager.spy`

It also have a shell which works in read execute print loop. There is an extra keyword "env" which lets you view the global environment.
To open that you can use the command:

`python interpreter.py`
