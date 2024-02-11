Title: Intermediate Level   
header: The Basics: Intermediate Topics  
Date: 2024-01-28 12:00  
tags: intermediate topics,  
status: draft  
rights: CC-BY-NC-SA 4.0  

## Summary 

After [The Basics]({filename}basics.md), you are ready for Intermediate level aircraft icing topics:  

- Using handbook analysis methods  
- Using computerized icing analysis tools  
- Preliminary ice protection system sizing  

### Prerequisite: Select your toolset  

You are encouraged to run code to reproduce the examples used here. 
By doing so, you can build your personal and software capabilities and skills.  

Example calculations are provided here in the Python programming language, 
and using the NASA-provided LEWICE code. 

There are several reasons why you may choose to use a different toolset. 
See [Analysis Toolset]({filename}intermediate_toolset.md) for more details and options.

## Every analysis is an approximation  

We can also say that every test is an approximation:  

> In these procedures, simplifying assumptions are required to
make analyses possible, imperfect simulations are required, and demonstration tests are not always
sufficiently specific or well correlated. Thus, engineering judgement must be used to provide the
conservativeness required in design, analysis, and test to compensate for uncertainties.  
> 
>_from "Aircraft Icing Handbook"," DOT/FAA/CT-88/8-1 [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf)_  

Whether an analysis or test is "good enough" requires experience and engineering judgement. 
Seeing many comparisons between analysis and test can help give the experience required to make informed judgements. 
Also, experience informs what type of simplifying assumptions are likely to be valid, 
if the assumptions are to be reliably "conservative" 
(will give results that are predictably too high or too low, 
depending on which direction is considered "conservative").  

The examples here will show where credible methods yield similar, 
but not identical, results.  

## Intermediate level topics  

### water drop impingement  

- skill: use correlations to calculate water drop impingement on a surface
    - [DOT/FAA/CT-88-1 Examples 2-1 through 2.4]({filename}intermediate_water_catch_examples.md)  
- skill: use equations of motion to calculate water drop impingement  
    - [Computerized Impingement Analysis Tools Examples]({filename}intermediate_lewice_impingement.md): Run a 2D simulation, such as LEWICE [www1.grc.nasa.gov](https://www1.grc.nasa.gov/aeronautics/icing/software/)    

### ice formation  

- skill: calculate freezing rates  
    - [DOT/FAA/CT-88/8-1 heat balance examples]({filename}intermediate_heat_balance_examples.md)  
- skill: calculate ice shapes  
    - Run a 2D simulation, such as LEWICE [www1.grc.nasa.gov](https://www1.grc.nasa.gov/aeronautics/icing/software/)    

### ice protection  

- Skill: calculate heat required for thermal ice protection  
    - DOT/FAA/CT-88/8-1 5.3.1.1 Wing Hot Air Anti-icing calculation  
    - Run a 2D simulation, such as LEWICE [www1.grc.nasa.gov](https://www1.grc.nasa.gov/aeronautics/icing/software/), and compare to the handbook values.  

<!--

 
Other Skills  

comparison of analysis to test  
reverse engineering/inferring values  
simplifying problems  
estimation  
every calculation is an estimate or approximation  
Python for the win!  

>the characteristic length used in the calculation of Ko is a matter of convention and the
conventional choice is not always obvious


I was initially hired as a thermal analyst (decades ago), 
and once they found out that I also knew some physics of drops they asked 
"Can you run this LEWICE program?"



### Yes to 1D and 2D analysis, no to 3D here  

Three-dimensional (3D) analysis offers many challenges. 
Surface geometry files have several formats. 
Creating a quality 3D analysis grid is often "half the battle" for achieving a reliable result. 
Output files from computational fluid dynamics (CFD) analysis can be very large, 
and even larger with water drop trajectory data is included. 
Displaying and interpreting 3D data can be difficult. 

As this series is about icing, we will focus on that, 
and use 1D and 2D analysis that illustrate the principles. 
1D and 2D geometry should be tractable for anyone with an engineering, math, or science background. 
You will have to go somewhere else to learn the 3D geometry skills. 

### Potential flow is good enough  

Different CFD programs have different approximations for modeling (RANS, DES, etc.). 
The cases for icing calculations where those make a significant difference are few and far between. 
The examples here will use LEWICE with the default potential flow solver. 

A case where those differing approximations might make a difference is calculating the aerodynamic effects of ice. 
I would describe the current state of the art for that, with any solver, as very approximate. 
It is hard enough to get an accurate result without ice, let alone with ice. 
We will not delve further into that topic here.  
-->



