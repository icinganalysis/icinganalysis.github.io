Title: Intermediate Level   
header: The Basics: Intermediate Topics  
Date: 2024-03-04 12:00  
tags: intermediate topics,  
status: draft  
rights: CC-BY-NC-SA 4.0  

![Figure 2-71. Effect of total temperature on the ice shape.](..%2Fimages%2FFAA%20Handbook%20volume%201%2FFigure%202-71%20crop.png)  
_From "Aircraft Icing Handbook", DOT/FAA/CT-88/8-1 [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf)_  

## Summary 

After [The Basics]({filename}basics.md), you are ready for Intermediate level aircraft icing topics:  

- Using handbook analysis methods  
- Using computer icing analysis tools  
- Preliminary ice protection system sizing  

## Prerequisite: Select your toolset  

You are encouraged to run code to reproduce the examples used here. 
By doing so, you can build your personal and software capabilities and skills.  

Example calculations are provided here in the Python programming language, 
and using the NASA-provided LEWICE code. 

There are several reasons why you might use a different toolset. 
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
    - [Computer Impingement Analysis Tools Examples]({filename}intermediate_lewice_impingement.md): Run a 2D simulation, such as LEWICE [www1.grc.nasa.gov](https://www1.grc.nasa.gov/aeronautics/icing/software/)    

### ice formation  

- skill: calculate freezing rates  
    - [DOT/FAA/CT-88/8-1 heat balance examples]({filename}intermediate_heat_balance_examples.md)  
    - Run a 2D simulation, such as LEWICE [www1.grc.nasa.gov](https://www1.grc.nasa.gov/aeronautics/icing/software/)  
- skill: calculate ice shapes  
    - Run a 2D simulation, such as LEWICE [www1.grc.nasa.gov](https://www1.grc.nasa.gov/aeronautics/icing/software/)  

### Using icing conditions definitions  

- skill: use the Appendix C icing envelopes  
  - Identify conditions that yield the maximum freezing rate for given geometries and flight conditions   

### ice protection  

- Skill: calculate heat required for thermal ice protection  
    - DOT/FAA/CT-88/8-1 5.3.1.1 Wing Hot Air Anti-icing calculation  
    - Run a 2D simulation, such as LEWICE [www1.grc.nasa.gov](https://www1.grc.nasa.gov/aeronautics/icing/software/), and compare to the handbook values.  

## Related  

Back to [The Basics]({filename}basics.md).  

<!--

 
Other Skills  

comparison of analysis to test  
reverse engineering/inferring values  
simplifying problems  
estimation  
Python for the win!  

>the characteristic length used in the calculation of Ko is a matter of convention and the
conventional choice is not always obvious


I was initially hired as a thermal analyst (decades ago), 
and once they found out that I also knew some physics of drops they asked 
"Can you run this LEWICE program?"
-->



