# Command Line Interface

* Successful installation will expose `console-calculator` entrypoint.
* This is an `argparse` application.

## Examples

Here are few examples of CLI to get help and sample uses.

### Getting help

Use `--help` flag to get details.

#### Primary entry point

```console
$ console-calculator --help
usage: console-calculator [-h] {binary,general} ...

calculator for console

positional arguments:
  {binary,general}  types of arithmetic expressions
    binary          basic binary operations
    general         standard simplification problems

options:
  -h, --help        show this help message and exit
```

#### Supported Commands

This has two commands:
  * `binary`
  * `general`

##### Binary operation

```console
$ console-calculator binary --help
usage: console-calculator binary [-h] first_number operator second_number

positional arguments:
  first_number   first number
  operator       arithmetic operator
  second_number  second number

options:
  -h, --help     show this help message and exit
```

##### Expression evaluation

```console
$ console-calculator general --help
usage: console-calculator general [-h] expression

positional arguments:
  expression  infix expression

options:
  -h, --help  show this help message and exit
```

### Sample usage

Use CLI to calculate arithmetic expressions.

#### Binary operation

```console
$ console-calculator binary 1 + 2
Result = 3.0
```

#### Expression evaluation

```console
$ console-calculator general "4 - 5 * (6/7)"
Result = -0.2857142857142856
```
