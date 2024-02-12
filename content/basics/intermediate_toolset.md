Title: __Analysis Toolset    
header: The Basics: Intermediate Topics  
Date: 2024-01-28 12:00  
tags: intermediate topics, analysis tools   
status: draft  
rights: CC-BY-NC-SA 4.0  

## Summary  

You will have to choose a toolset to perform the example analyses. 

Example calculations are provided in the Python programming language, 
and using the NASA-provided LEWICE code. 

## Introduction  

You are highly encouraged to perform the analysis described in the examples (and not just read the examples). 
Some examples can be accomplished with hand calculations, while other require computational capabilities. 

You need to select your toolset. 

### Consider your current and future uses  

A toolset is an investment of your time and resources. 
By performing the calculation of the examples used here, 
you will build your personal and software capabilities and skills.  

Your toolset at a particular time may not be entirely your choice. 
Your company, institution, or customer may have policies on which kinds of software are 
required, encouraged, discouraged, or prohibited. 
You may have signed an agreement that any 
software you developed on paid time is someone else's property. 

However, you may not work at the same place your entire career, 
so consider having a portable toolset. 

### Bespoke analysis  

For the example cases, 
code written in the Python programming language is provided, via
[github.com/icinganalysis](https://github.com/icinganalysis/icinganalysis.github.io/tree/main/icinganalysis), 
under the [LGPL license](https://raw.githubusercontent.com/icinganalysis/icinganalysis.github.io/main/LICENSE). 
Software under the LGPL license may or may not be usable for your use case.

While I am not a lawyer, I will call attention to a part of the LGPL license:  

>NO WARRANTY
> 
>  15. BECAUSE THE LIBRARY IS LICENSED FREE OF CHARGE, THERE IS NO
WARRANTY FOR THE LIBRARY, TO THE EXTENT PERMITTED BY APPLICABLE LAW.
EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR
OTHER PARTIES PROVIDE THE LIBRARY "AS IS" WITHOUT WARRANTY OF ANY
KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE
LIBRARY IS WITH YOU.  SHOULD THE LIBRARY PROVE DEFECTIVE, YOU ASSUME
THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

The LGPL license is not entirely unique in this respect, 
as I have seen similar language for some commercial software. 
For any software that you use, you should be familiar with the license. 

I have found the python programming language to be the most productive, portable, 
interoperable, and reusable option of those that I have used 
(C, Fortran, Java, Javascript, Matlab, spreadsheets with code extensions, and a few others). 
However, you may opt for (or be mandated to use) a different toolset.
(For the few cases where high performance computation is really required, I use FORTRAN.)

If you opt for a different toolset, some example input files are provided in a .csv format, 
which any toolset can presumably read. 

### Computational Fluid Dynamics (CFD) analysis with icing capabilities  

Examples are included here using the NASA-provided LEWICE analysis tool. 
An advantage of LEWICE is that most analyses run quickly (on the order of minutes or less), 
even on lower capability platforms (such as my 10-year-old laptop). 

LEWICE is directly available for "U.S. Release Only". 
There are other, similar non-commercial tools, some with similar by-country restrictions, 
that presumably yield similar results.  

If you are not in the U.S.A., for LEWICE consider LewInt, which has a broader licensing agreement, 
from [americankestrelco.com](https://americankestrelco.com/LewInt.html):  
>LewInt integrates the ice accretion code LEWICE (version 3.2.2) with American Kestrel's user interface, icing analysis tools, and automated plotting. LEWICE 3.2.2 is a validated ice accretion code developed by NASA Glenn Research Center.  
A new license agreement, with NASA Glenn, allowing distribution of LEWICE version 3.2.2 was executed on 6/11/14. American Kestrel is accepting new international orders for the integrated ice accretion suite LewInt, including LEWICE version 3.2.2.  
LEWICE version 3.2.2 is made available under a copyright license from the U.S. Government, National Aeronautics and Space Administration or NASA.  
LewInt is a try-before-you-buy package. The download listed below is a fully functioning version of LewInt with LEWICE. 
The software comes with a 15 day trial period but includes some reminders that pop up everytime LewInt and LEWICE is run. Once down loaded and installed the trial version can be converted to a purchased version by inputing a software key.  

It is possible to complete the examples here within a 15-day period. 

There several other commercial icing analysis tools available, 
but the cost of a license may be prohibitive to beginners (some offer student licenses). 
The computing hardware performance requirements may be challenging 
(they run well on a high-performance cloud computing system, but not so much on my 10-year-old laptop). 
These tools are, in general, fundamentally 3D based.  

### Two-dimensional analysis (only) is used here  

There are situations where three-dimensional tools have clear advantages. 
The examples from the Aircraft Icing Handbook are two-dimensional. 
So, two-dimensional analysis is adequate for those cases.  

It is beyond this scope to explain how to use the wide variety of 3D codes now available. 

### Select the right tool for the task  

You might have access to a three-dimensional computational fluid dynamics code 
with icing simulation capabilities. If so, you are encouraged to try it on the examples here. 
You will have to use some creative constraints to run the equivalent 2D cases here. 
You may find that much time is required to set up the analysis. 
Also, the results may not be exactly the same as the examples, and are not necessarily more accurate. 

The handbook analysis methods and bespoke code are still used today, 
as in many situations they yield accurate enough results in much less time than more complex methods.  
