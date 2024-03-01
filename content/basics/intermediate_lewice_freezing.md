Title: __Computer Freezing Rate Analysis Tools Examples    
header: The Basics: Intermediate Topics  
Date: 2024-03-04 16:00  
tags: intermediate topics, ice shape, LEWICE   
status: draft  
rights: CC-BY-NC-SA 4.0  

## Summary  

## Prerequisites  

You need to complete the [Aircraft Icing Handbook Water Catch Examples]({filename}intermediate_water_catch_examples.md).  

You need to select a computerized tool to work with. 
See [Analysis Toolset]({filename}intermediate_toolset.md) 
for obtaining LEWICE, and some other options.  

I make several comments here about some unique features of the LEWICE code. 
Some readers may consider these to be quirks, unexpected behaviors, or bugs. 
However, do not interpret these comments as recommending against the use of LEWICE. 
LEWICE is the most well characterized code available, 
and the LEWICE validation report shows that the behaviors do not have noticeable 
negative effects in the overall ice shape agreement. 
They are more evident for "edge cases", such as when comparing stagnation line values. 

It is a testament to NASA that the LEWICE code and source code are publicly available
(at least in the USA), so you can investigate the reasons for unexpected behaviors.  

I have used commercial codes. 
While they may not have the identical behaviors detailed here, 
they have their own unexpected behaviors. 
You generally cannot access the source code, 
and the developers may or may not be able to explain the behaviors.  

## Aircraft Icing Handbook Example 2-4  

>The mass of ice accretion on the NACA 0012 section will be calculated. Using the same flight
conditions as Example 2-1. and the droplet size distribution and value from Example 2-3:  

```text
Airfoil                         c = 3.1 foot chord NACA 0012  
Flight Speed:                   V = 200 kt  
Airfoil projected height:       h = 0.12 at alpha = 0  
Liquid Water Content:           LWC = 0.4 g/m^3
Ambient Temperature:            T = -4 F
Collection efficiency:          E = 0.24  
Maximum impingement efficiency: Beta_max = 0.65  
Icing time:                     tau = 5 minutes  
``` 

The LEWICE analysis at the nominal -4F does not predict complete freezing 
at the leading edge:  

![lewice2d_example2_2_thick_tf_-4.png](..%2Fimages%2Fbasics%2Flewice2d_example2_2_thick_tf_-4.png)

Here is the result at a colder temperature (-22F):  

![lewice2d_example2_2_thick_tf_m22.png](..%2Fimages%2Fbasics%2Flewice2d_example2_2_thick_tf_m22.png)  

Here are the computed ice shapes:

![lewice2d_example2_2_ice_tf_m25.png](..%2Fimages%2Fbasics%2Flewice2d_example2_2_ice_tf_m25.png)  

The ice calculated at -22F agrees well with the ice thickness from the handbook example.  

```text
Method                          Leading edge ice thick, inch
Handbook                        0.39
Standard Computational Model    0.393
LEWICE -4F                      0.32
LEWICE -22F                     0.39
```

## 20 cm diameter cylinder example  

The icing time was not specified, 
so we will assume the same value as example 2-4.  

![Table 2-5 to 2-8 LEWICE 300 s prt1.png](..%2F..%2Ficinganalysis%2Flewice%2Fhandbook_20cm_cylinder%2FTable%202-5%20to%202-8%20LEWICE%20300%20s%20prt1.png)  

The results do not appear to agree well. 
Many of the LEWICE results are that the freezing fraction is 1, 
while the Table 2-5 to 2-8 values show a range of results.  

## A partial explanation  

The integral boundary layer method implementation used in LEWICE has results that agree reasonably well 
with the stagnation line results from the Standard Computational Model. 
So, differing heat transfer coefficient values are only a small component in the differences. 
Here is the Table 2-5-a case at -8C temperature:  

![Table 2-5 LEWICE -8C htc full scale.png](..%2F..%2Ficinganalysis%2Flewice%2Fhandbook_20cm_cylinder%2FTable%202-5%20LEWICE%20-8C%20htc%20full%20scale.png)  

However, the stagnation line (S=0) Beta value differs from that calculated using the Standard Computational Model:  
 
![Table 2-5 LEWICE beta.png](..%2F..%2Ficinganalysis%2Flewice%2Fhandbook_20cm_cylinder%2FTable%202-5%20LEWICE%20beta.png)  

The LEWICE manual [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20080048307) states:  

>The icing model, which was first developed by Messinger, is used to calculate the ice growth rate at each point on the surface of the geometry.  

The LEWICE implementation adds a heat term to the Messinger heat balance for conduction to the surface where ice is forming
(the unnamed, first term in the equation below):  

![21_17_2 Energy Balance Equation Requirements.png](..%2Fimages%2Fbasics%2F21_17_2%20Energy%20Balance%20Equation%20Requirements.png)  

While the manual is not explicit, this is a transient heat term that changes with time
(you have to review the code to get the details). 
The time step used affects the analysis. 

## Resources  

User's Manual for LEWICE Version 3.2 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20080048307)  
Note that a "manual.pdf" file comes with the LEWICE software distribution (apparently for version 3.0), 
and a file "Lew32manual_changes.doc". 
I find it easier to just use the Version 3.2 manual.  




