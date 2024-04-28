Title: Aircraft Icing Intermediate Level   
header: The Basics: Intermediate Topics  
Date: 2024-04-08 12:00  
published: 2024-04-08 12:00  
tags: intermediate topics,  
rights: CC-BY-NC-SA 4.0  

![Figure 2-71. Effect of total temperature on the ice shape.](/images/FAA%20Handbook%20volume%201%2FFigure%202-71%20crop.png)  
_From "Aircraft Icing Handbook", DOT/FAA/CT-88/8-1 [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf)_  
 
## Summary  

After [The Basics]({filename}basics.md), 
you are ready for Intermediate level aircraft icing topics:  

- Using handbook analysis methods  
- Using computer icing analysis tools to produce ice shapes  
- Preliminary ice protection system sizing  

The Intermediate Level is a work in progress, as there may yet be many revisions and additions. 
However, it may be useful "as is" to some readers. 

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

<a name="intermediate-topics"></a>  
## Intermediate level topics   

### Water drop impingement  

- skill: use correlations to calculate water drop impingement on a surface  
    - [DOT/FAA/CT-88-1 Examples 2-1 through 2.4]({filename}intermediate_water_catch_examples.md)  
- skill: use equations of motion to calculate water drop impingement  
    - [Computer Impingement Analysis Tools Examples]({filename}intermediate_lewice_impingement.md): Run a 2D simulation, such as LEWICE    

### Ice formation  

- skill: calculate freezing rates  
    - [DOT/FAA/CT-88/8-1 heat balance examples]({filename}intermediate_heat_balance_examples.md)  
- skill: calculate ice shapes  
    - [Run a 2D simulation]({filename}intermediate_lewice_freezing.md), such as LEWICE  

### Introduction to accuracy and variance  
 
- skill: quantify ice shape differences  
    - [Introduction to Variations]({filename}intermediate_variance.md) calculate the expected difference between calculated ice shapes versus test,
and estimate the range of effects   

### Using icing conditions definitions  

- skill: use the Appendix C icing envelopes  
    - Identify conditions for "critical" ice shapes:   
[Using Appendix C for Ice Shape Analysis]({filename}intermediate_using_app_c.md)   

### Ice protection [in work]  
 
- skill: calculate heat required for thermal ice protection  
    - Anti-ice calculation theory    
    <!--
[Anti-Ice Heating Calculations Theory]({filename}intermediate_anti_ice_theory.md)  
  -->
    - ADS-4 "Aircraft A" Wing Anti-icing example  
    <!--
[Anti-Ice Heat Required Calculations]({filename}intermediate_anti_ice_heat_required.md)   
-->
    - Run a 2D simulation, such as LEWICE, and compare to the handbook values.  

## Items specifically deferred to the (yet to be written) Expert Level  

- 3D analysis (including swept wings)  
- Icing wind tunnel tests  
- Runback ice  
- Heat transfer coefficients  

## Related  

Back to [The Basics]({filename}basics.md).  
