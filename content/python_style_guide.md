title: Python coding style guide  
Date: 2022-04-21 13:00  
category: Python  
tags: python 

### _"Beautiful is better than ugly."_  

![Python programming logo. Two stylized, interlocking snakes with the word python.](images/python-logo-master-v3-TM.png)

## Summary

For the [Thermodynamics tread]({filename}thermodynamics.md) and on, I will be using this style guide. 
Previous code may eventually be upgraded to this.

## Python target version:  

Target python version 3.7, and the corresponding [Anaconda stack](https://www.anaconda.com/) (version 2021-11). 
Avoid modules with deprecation warnings (there are not many of them).
This is a balance between current installations and future-proofing. 
The goal is to be applicable for all 3.7+ uses. 

(Note: 3.10 is the latest available version, as of April 2022).

Code should be portable, and not use operating system specific functions. 

## General guidelines

- simple
    - use simple functions over classes
    - out-source complexity where possible
        - use built-in data structures (list, dict) 
        - use numpy and scipy, anything in the anaconda stack
    - promote reuse
        - anything used more than once should be put in an importable [module](https://docs.python.org/3.7/tutorial/modules.html)
        - use the "if \_\_name__ == '\_\_main\_\_:" block [idiom](https://docs.python.org/3.7/library/__main__.html) 
            - to have clean (no side effect) imports
            - include an example of how to use the module
        - lots of small modules are an asset
            - each module is easier to understand
            - a well focused, cohesive module is more likely to be reused
            - lots of imports are better than lots of bespoke code
    - do all internal calculations in SI units
        - use units_helpers for input/output conversion
        
- understandable
    - name things well
        - use named constants rather than just numeric values
        - long, descriptive variable and function names are an asset
        - use verbs for function names (calc_, find_, get_, ...)
        - use [namespaces](https://docs.python.org/3/glossary.html#term-namespace)
            - eschew the temptation to use "import *"
    - include [doc strings](https://peps.python.org/pep-0257/) for non-obvious functions
    - consider using [type annotations](https://docs.python.org/3.7/library/typing.html) (perhaps I should do more of that)
    - minimize comments
        - prefer doc strings, well named variables, and type annotations 
    - a consistent "look and feel" reduces the cognitive load
        - use the ["Black"](https://pypi.org/project/black/) file formatter (a super-set of [PEP 8](https://peps.python.org/pep-0008/))
        - imports order (consistency aids understanding):
            1. [Standard modules](https://docs.python.org/3.7/py-modindex.html) (in alphabetical order)
            2. Anaconda stack (numpy, scipy, etc.)
            3. icinganalysis modules
    - I consider [list comprehensions](https://docs.python.org/3.7/tutorial/datastructures.html#list-comprehensions) to be quite understandable (others may not)
    - limit file lengths to less than 1000 lines of code
        - while number of lines of code is a crude measure of complexity, it is adequate in many cases

## Version control

[Git](https://git-scm.com/) is used. 

Code is available at [https://github.com/icinganalysis/icinganalysis.github.io](https://github.com/icinganalysis/icinganalysis.github.io)

## License

The code is available under the [LGPL license](https://raw.githubusercontent.com/icinganalysis/icinganalysis.github.io/main/LICENSE)

## Verification

There are not yet any unit tests. They would probably be good idea. 

At the moment, the verification is out-sourced to the validation 
("If it works, it works"). 
However, this may miss edge-cases, 
and coincidences where one error offsets another error.

## Validation  

Code will have a comparison to test and NACA analysis data, 
which illustrate the degree of agreement. 
 
Users may determine if the degree of agreement is adequate for their use case. 

## The Zen of Python [https://peps.python.org/pep-0020/](https://peps.python.org/pep-0020/)

> Beautiful is better than ugly.  
Explicit is better than implicit.  
Simple is better than complex.  
Complex is better than complicated.  
Flat is better than nested.  
Sparse is better than dense.  
Readability counts.  
Special cases aren't special enough to break the rules.  
Although practicality beats purity.  
Errors should never pass silently.  
Unless explicitly silenced.  
In the face of ambiguity, refuse the temptation to guess.  
There should be one-- and preferably only one --obvious way to do it.  
Although that way may not be obvious at first unless you're Dutch.  
Now is better than never.  
Although never is often better than *right* now.  
If the implementation is hard to explain, it's a bad idea.  
If the implementation is easy to explain, it may be a good idea.  
Namespaces are one honking great idea -- let's do more of those!  


