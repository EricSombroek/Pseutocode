[![Build Status](https://travis-ci.com/PatWg/Pseutocode.svg?branch=master)](https://travis-ci.com/PatWg/Pseutocode)

# General description

This project defines a grammar for a programming language based on pseudocode.
The main objective of this language is to be as close as possible to a natural
language (and in particular English), so that instructions could be both
_spoken_ and intelligible for someone without any programming background.

After having defined this pseudocode, we are also capable of translating it into
valid Python instructions.

# Prerequisites

- astor
- textX
- pytest (for unit tests)

`pip install astor textX pytest` or `pip install -r requirements.txt`

# Usage

Python code can be generated through the command line this way : `python pseudotopy_cl.py INPUT_FILE`.
This will print out the generated code based on the pseudocode of the input file.

The available flags are :
 - `-a` `--ast` : Prints the generated Python AST
 - `-e` `--exec` : Executes the generated Python code
 - `-q` `--quiet` : Don't print the generated Python code
 - `-h` `--help` : Shows a help message
 
 # Testing
 
 To run unit tests, run `pytest` at the root of the project.

# Syntax

## Variable declaration

To declare a variable, use the keyword `declare` followed by the name of the variable

```
declare myVar
```

## Variable assignment

To assign a value to variable, you can use either the `=` operator or the keyword `equals`.
So these two lines are equivalent:

```
a = 2
a equals 2
```

You can put any expression on the right side of the equal, but only one variable on the left side, like so:

```
a = 56 modulo 3
b = a power 2
```

## Arithmetic operators

Like many things in our pseudocode, the basic arithmetic operators have aliases so they can be pronounced and remembered easily.

| Sum  | Subtraction | Multiplication | Division   | Modulo | Exponentiation         |
| ---- | ----------- | -------------- | ---------- | ------ | ---------------------- |
| +    | -           | \*             | /          | %      | \*\*                   |
| plus | minus       | times          | divided by | module | power, to the power of |

As an example, these two instructions are equivalent:

```
var equals a plus ( b  power (c divided by (d modulo 3)) times minus 4
var equals a + ( b  ** (c / (d % 3)) * -4
```

## If statements

All of the following are legal ways to open an if statement.

```
if <expression> :
if <expression> then:
if <expression> then :
if <expression> then
```

There is only one way to close it though, which is by using the keyword

```
endif
```

Usage example:

```
if 2 + 4 == 6 then :
    show "Hello world"
endif
```

## Comparison operators

In pseudocode, the common comparisons operators also have aliases so they can be pronounced easily:

| Equality    | Inequality                             | Greater         | Greater or equal       | Lower         | Lower or equal       |
| ----------- | -------------------------------------- | --------------- | ---------------------- | ------------- | -------------------- |
| ==          | !=                                     | >               | >=                     | <             | <=                   |
| is equal to | is not equal to <br> is different from | is greater than | is greater or equal to | is lower than | is lower or equal to |

As an example, all these expressions are equivalent:

```
a != 3
a is not equal to 3
a is different from 3
```

## Logical operators

The 3 basic logical operators are implemented in pseudocode.

| AND | OR   | NOT |
| --- | ---- | --- |
| and | or   | not |
| &&  | \|\| | !   |

The AND operator can be used by either the keyword `and` or `&&`.

The OR operator can be used by either the keyword `or` or `||`.

The NOT operator can be used by either the keyword `not` or `!`.

Examples :

```
a is equal to 4 and b is lower than a
a equals 2
isOdd equals a modulo 2 is different from 0
if not isOdd then :
    show "it is even"
endif
```
