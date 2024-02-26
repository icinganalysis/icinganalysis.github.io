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

The ice calculated at -22F agrees well with the ice thickness from the handbook.  

```text
Method                          Leading edge ice thick, inch
Handbook                        0.39
Standard Computational Model    0.393
LEWICE -4F                      0.32
LEWICE -22F                     0.39
```

