# Automated Homework Grading System

I am a tutor for an introductory Python programming course for Data Science majors. In this class, we give out programming assignments to students to complete. For grading, we have automated tests for checking inputs and outputs of assignments, but we also have a style grade worth 15% of each assignment.

Grading style used to take an enormous amount of time. We currently have 300 students this quarter, and we have between 8-14 criteria to grade, depending on the assignment. This ranges from simple things like requiring their name, to much more complex things like using a one-line list comprehension.

## Original Idea and Prototype

Back in January of 2023, I started working on an idea to detect the use of recursion. I found a StackOverflow post that described a way to do it using the `bdb` library, which is used by the Python Debugger (`Pdb`).

```python
"""
Recursion Detector file, created by Bryce for DSC20
"""

from bdb import Bdb
import sys
import unittest


class RecursionDetector(Bdb):
    """
    Child class of Bdb used to detect recursion

    I have no idea how this works
    Overrides a few methods in the Bdb class
    """

    def __init__(self, *args):
        Bdb.__init__(self, *args)
        self.stack = set()

    def do_clear(self, arg):
        pass

    def user_call(self, frame, argument_list):
        code = frame.f_code
        if code in self.stack:
            raise RecursionDetected
        self.stack.add(code)

    def user_return(self, frame, return_value):
        self.stack.remove(frame.f_code)


class RecursionDetected(Exception):
    pass


def test_recursion(func, *args, **kwargs):
    """
    Checks if the given function is recursive

    See https://stackoverflow.com/questions/36662181/is-there-a-way-to-check-if-function-is-recursive-in-python

    :param func: the function to check
    :param *args: list of arguments passed to func
    :param **kwargs: keyword list of arguments passed to func
    :returns: True if function is recursive, False otherwise
    """
    detector = RecursionDetector()
    detector.set_trace()
    try:
        func(*args, **kwargs)
    except RecursionDetected:
        return True
    else:
        return False
    finally:
        sys.settrace(None)
```

This code would check the stack to see if a function was calling itself, and this could be integrated into our autograder.

## Next Steps

The issue with this code was dealing with submissions with broken recursion functions. Sometimes the student's code would have a broken base case, and the recursion would never end. For this reason, I wanted to move away from dynamic towards static analysis.

In March of 2023, I decided to continue by writing code to determine if a submission was avoiding the requirement to use a while loop. I found a library called `ast` which parses a Python file and generates a tree structure of nodes, where each node represents a state change in the code.

For instance, a statement like `if a == 2:` would be converted into an `If` node, with a `test` sub-node that has more sub-nodes for `a` and `2`. Documentation (here)[https://docs.python.org/3/library/ast.html#ast.If]

Using this library, I successfully made a check for students not using while loops.

```python
"""
Contact Bryce for help

Useful ast classes
statements = {
    'loop': (ast.For, ast.While),  # Detect For and While loops
    'comp': (ast.comprehension),   # Detect ALL comprehensions
    'global': (ast.Global),        # Detect global vars, for recursion
    'func_def': (ast.FunctionDef), # Detect helper functions. Note the
                                   #     original counts as 1
    'lambda': (ast.Lambda),        # Detect lambda expressions
    ''
}
"""

from unittest import TestCase
from gradescope_utils.autograder_utils.decorators import weight, visibility
from timeout_decorator import timeout

import ast
import inspect

# Change to lab/hw function
from lab02 import correct_state


class TestRestrictions(TestCase):
    @timeout(30)
    @weight(0)
    def test_q3_loop(self):
        banned_states = [ast.For, ast.comprehension, ast.Lambda] # Change this
        banned_functions = ['map', 'filter'] # Change this
        func = correct_state # Change this to lab/hw function
        # Change this to represent the student's mistake
        msg = 'Possible for-loop or list comprehension detected in Q3!'

        # In ast, a node is a single python instruction
        nodes = ast.walk(ast.parse(inspect.getsource(func)))
        # Create list of T/F, true if bad, false if good
        node_check_list = []

        # First, check states
        for state in banned_states:
            for node in nodes:
                node_check_list.append((type(node) == state))
        # Next, check names of functions used
        name_nodes = [n for n in nodes if (type(n) == ast.Name)]
        for function in banned_functions:
            for node in name_nodes:
                node_check_list.append(node.id == function)
        cond = sum(node_check_list) > 0
        self.assertTrue(cond, msg=msg)
        print('All required restrictions passed!')
```

## Ambitious Next Steps

With this proof-of-concept working, my next goal was to automate as many style and restriction checks as possible. This includes this list:

1. Illegal imports
2. Missing Name/ID
3. Missing docstring
4. Line limits crossed
5. Meaningless variable name
6. Magic number usage
7. Bad variable style (snake_case)
8. Missing doctests
9. Uses One Line List Comprehension
10. Uses only List Comprehension
11. Uses only Map/Filter/Lambda
12. Uses only recursion
13. Does not use helper functions
14. Does not use global variables

Most of these were relatively easy to implement using the AST module. Checking for illegal imports, name and ID, line limits, and others involved a few short lines of code for parsing.

The more complicated ones, like Uses One Line List Comprehension, took a lot more work. The vast majority of solving this was to write all cases so that I could test it as comprehensively as possible. I went through and gathered a bunch of one-line list comprehensions from student submissions and put them all into a doctest for testing.

```python
    """
    >>> def case_double_lc(lst):
    ...     my_magic_var = 50
    ...     x = [p for p in 'example']
    ...     return [(str(i // 100) + ' dollar(s) and ' + str(i % 100) + \
    ' cents') for i in lst]
    >>> check_is_one_line_lc(case_double_lc)
    False
    >>> def case_tuple(lst):
    ...     minimum, cent = 50, 100
    ...     return sum([i // cent for i in lst if (i > cent * minimum)])
    >>> check_is_one_line_lc(case_tuple)
    True
    >>> def case_num_multiply(ages):
    ...     min_age = 21*12.5
    ...     return len([age for age in sublst for sublst in ages if \
    age >= min_age])
    >>> check_is_one_line_lc(case_num_multiply)
    True
    >>> def case_multiple_nums_multiplied(times):
    ...     min_time = 5*24*60*60
    ...     return len([time for time in times if time > min_time])
    >>> check_is_one_line_lc(case_multiple_nums_multiplied)
    True
    >>> def case_string_concat(names, time_of_day):
    ...     greeting = " it is " + time_of_day
    ...     return [name + greeting for name in names]
    >>> check_is_one_line_lc(case_string_concat)
    False
    >>> def case_asserts(names):
    ...     assert type(names) == list
    ...     assert all([len(name) > 1 for name in names])
    ...     return [names[0] for name in names]
    >>> check_is_one_line_lc(case_asserts)
    True

    ...
    """
```

## Verification

In order to verify that my style and restriction checker was working as intended, I decided against using it right away. For the Sprint 2023 quarter, I slowly introduced each of the features and constantly cross-checked the outputs to manual grading done by the tutors. By the end of the quarter, however, we were crunched on time for one of the last assignments, so we decided to rely on the style checker. By that point, it was refined enough to be deployed, and since then, we have used it for grading style on homework.

![Gradescope style checker](images/style%20checker%20gradescope.png)


## Why not use an existing style checker?

The advantages of using a custom-built style checker over a library like `Pylint` is for many reasons. First, `Pylint` lacks any way to perform checks for things like List Comprehension and Lambda usage, which are specific requirements for our course. Additionally, a custom-built style checker allows us to have more control over the checks and customize them to fit our needs.

Another advantage is that a custom-built style checker can be integrated seamlessly into our autograder system. This format uses the exact same structure as our existing correctness tests, so it easily incorporates into our existing test suite. We can also easily extend it to include additional checks or modify existing ones based on the needs of the course.


