Title: __Computer Freezing Rate Analysis Tools Examples    
header: The Basics: Intermediate Topics  
Date: 2024-03-04 16:00  
tags: intermediate topics, ice shape, LEWICE   
status: draft  
rights: CC-BY-NC-SA 4.0  

## Summary  

The LEWICE analysis at the nominal -4F does not predict complete freezing 
at the leading edge:  

![lewice2d_example2_2_thick_tf_-4.png](..%2Fimages%2Fbasics%2Flewice2d_example2_2_thick_tf_-4.png)

Here is the result at a colder temperature (-22F):  

![lewice2d_example2_2_thick_tf_m22.png](..%2Fimages%2Fbasics%2Flewice2d_example2_2_thick_tf_m22.png)  

Here are the computed ice shapes:

![lewice2d_example2_2_ice_tf_m25.png](..%2Fimages%2Fbasics%2Flewice2d_example2_2_ice_tf_m25.png)  

```text
Method                          Leading edge ice thick, inch
Handbook                        0.39
Standard Computational Model    0.393
LEWICE -4F                      0.32
LEWICE -22F                     0.39
```

