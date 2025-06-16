# OOSpy Interpreter
OOSpy Interpreter (In the context of book: "Introduction to Electrical Engineering and Computer Science I by Leslie Kaelbling & figures by Dennis Freeman" which is used in MIT OCW SC 6.01 course) is a mixture of Scheme and Python.It also supports object oriented paradigm.
This interpreter only implements fundamental built-in functions which are addition, divison, multiplication, substraction, and comparison. The purpose of this project was to gain further insight on behaviour of computer programs and to understand the general idea behind an interpreter by building one.

# Basic Syntax
The syntax of spy is fully parenthesized prefix syntax. Prefix means that the name of the function or operation comes before its arguments. And it'll have parentheses around every sub-expression. So to write `7 - 3x`, we would write:

`(- 7 (* 3 x))`

## Assignment
`(set x 34)` will assign 34 to variable x.

`(set (attr object x) 43)` will assign 43 to attribute `x` of `object`

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

`(if <condition> <true body> <false body>` if the condition is true the `<true body>` will get executed if it's false then the `<false body>` will get executed. Here's an example:

`(if (= 6 6) (+ 1 1) (- 2 9))` 

This example will return 2 since the condition is true.

## Class Declaration
`(class <name> <parent> <body>)` `<parent>` can be `None` if the class has no parent.
Here's an example class declaration

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
Classes are implemented as functions not environments therefore they cannot be changed after declaration.

## Instantiating a Class

`(<class name>)` will return a class instance. `set` can be used to assign the instance to a variable like this:

`(set <object name> (<class name>)`

Here's an example for the class declared in previous section:

`(set point (Point)`

## Accessing Attributes

`(attr <object name> <attribute name>` is used for accessing attributes of objects.

You can change the values of attributes of an object this way:

`(set (attr <object name> <attribute name>) <new value>`

You can call class methods this way:

`((attr <object name> <method name>) <parameters>)`


## Class Method Calls

`((attr <object name> <method name>) <parameters>)` is used for calling class methods here's an example for `point` object declared couple sections before:

`((attr point init) 5 7)` this method call will set values of attributes x to 5 and y to 7 in point object.

# General Ideas Behind this Interpreter

## Binding Environments

Binding environments are tables that have names on one side and values associated with those names on the other side. Many aspects of the programming language are built upon environments these will be explained in next sections. 
Alongside key-value pairs environments have a parent property. When a key is not in the environment, parent environment is checked.
To implement an envrionment an hash map can be used.

| Key  | Value  |
|------|--------|
| a    | 9      |
| b    | 2.8    |
| foo  | -15    |

## Global Environment

Global environment contains the definitions of basic built-in functions `+` `-` `*` `/` and `=`. It is the parent of all other environments.

## Variables

`(set <name> <value>)` when interpreter reads these lines it sets the `<name>` to `<value>` in environment which statement is in.
For example `(set bar 39)` will set the value corresponding to `bar` key in the table to `39`. As a result we'd have a table that looked like this:

| Key  | Value  |
|------|--------|
| a    | 9      |
| b    | 2.8    |
| foo  | -15    |
| bar  | 39     |

## Procedures(Functions)

Procedures are objects, containing the parameter list procedure body and a pointer to the environment in which the procedure was declared. When a procedure is declared, interpreter binds the function name to function object created, in the binding environment. 
The procedure object looks like this:
```
{
  params_list: <list of parameters>
  body: <tokenized expression>
  env: <pointer to the environment in which the function is declared>
}
```

## Procedure Calls

When a procedure is called every argument is evaluated. Then a new environment is created for procedure and evaluated arguments are assigned to arguments stated in proceduere declaration. This environment has a parent environment which is the same as procedure object.

## Classes

Classes are primitive procedures that return binding environments. These binding environments have a parent and when a attribute is not in the environment the parent is checked for the attribute. If a class has no parent then it's parent is the global environment.


# How To Install And Run a Program
You need to get these files to your local machine in a folder. Then to run a program you need to open a terminal on that folder and type:

`python interpreter.py <path to your program>`

You can run the example "Averager.spy" program instead by typing:

`python interpreter.py Averager.spy`

It also have a shell which works in read execute print loop. There is an extra keyword "env" which lets you view the global environment.
To open that you can use the command:

`python interpreter.py`
