Title: USA 35-B Airfoil Impingement Data       
header: The Basics: Intermediate Topics  
Date: 2024-04-29 14:00  
tags: intermediate topics, analysis tools, LEWICE   
status: draft  
rights: CC-BY-NC-SA 4.0  

![usa35b.png](/images%2FIntermediate%2Fusa35b.png)  
_Public domain image by Donald Cook._  

## Prerequisites  

This information relates to [Anti-Ice Heat Required Calculations]({filename}intermediate_anti_ice_heat_required.md).  

## Introduction  

ADS-4 uses the USA 35-B airfoil in the "Aircraft A" example in section 4.1.4. 
It does not provide impingement data for that airfoil, 
but uses an approximation:  

> Modified inertia parameter Ko = 0.0238  
> The ratio of projected airfoil height to chord h/C= 0.1225 (at alpha = -1.7), based on measured values for USA 35-B airfoil  
> Collection efficiency can be obtained from Figure 2-7 for a 12 per cent
> Joukowski airfoil at a zero-deg. angle of attack  
> EM = 0.135  
> Water catch WM = 2.95 lb/hr-ft.span  
>
>The limits of impingement can be found from Figures 2-15 and 2-16 using
> a 15 per cent Joukowski airfoil at alpha = 2 deg. to represent the USA 35-B airfoil
> at alpha = -1.6 deg.
> The Joukowski airfoil was used because of the profile similarity to the USA 35-B airfoil
> for which no data was available.
> See Paragraph 2.3.4 for an explanation of airfoil matching procedures.  
> SU/C = 0.04 SL/C = 0.02  
> SU = 2.7 in. SL = 1.3 in.  

The airfoil coordinates are available at https://m-selig.ae.illinois.edu/ads/coord/usa35b.dat. 
If you plot the points from usa35b.dat (34 points), 
you can see that LEWICE has interpolated more points (108 points) using splines, 
and the individual panels are not readily visible on this scale.  

![usa35b_with_points.png](/images%2FIntermediate%2Fusa35b_with_points.png)  
_Public domain image by Donald Cook._  

When LEWICE is run with the USA 35-B airfoil for the ADS-4 4.1.4.1 conditions, 
slightly different impingement data results are found:  

![USA35B Airfoil AOA=-1.6 em](/images%2FIntermediate%2FUSA35B%20Airfoil%20AOA%3D-1.6%20em.png)  
_Public domain image by Donald Cook._  

![USA35B Airfoil AOA=-1.6 beta_max](/images%2FIntermediate%2FUSA35B%20Airfoil%20AOA%3D-1.6%20beta_max.png)  
_Public domain image by Donald Cook._  

![USA35B Airfoil AOA=-1.6 sl_su](/images%2FIntermediate%2FUSA35B%20Airfoil%20AOA%3D-1.6%20sl_su.png)  
_Public domain image by Donald Cook._  

The LEWICE results are similar to the Joukowski airfoil approximation.
See [Anti-Ice Heat Required Calculations]({filename}intermediate_anti_ice_heat_required.md#lewice-imingement) 
for examples. 

You may note the non-smooth nature of the LEWICE results for impingement limits. 
This is a feature of the methods that use surface panels to approximate smooth airfoil surfaces. 
Figures in ADS-4 that appear to be smooth were likely either smoothed with engineering judgement, 
or sparsely calculated and the interpolated smoothly.  

These results here may be used by readers who do not have access to LEWICE to perform some of the analysis in 
[Anti-Ice Heat Required Calculations]({filename}intermediate_anti_ice_heat_required.md). 
They are listed in the file 
[USA 35-B Airfoil AOA=-1.6.dat](/images%2FIntermediate%2FUSA%2035-B%20Airfoil%20AOA%3D-1.6.dat).  

## Resources  

- "Engineering Summary of Airframe Icing Technical Data", ADS-4 [apps.dtic.mil](https://apps.dtic.mil/sti/citations/AD0608865)  

- User's Manual for LEWICE Version 3.2 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20080048307)  

## Related  

Back to [Intermediate Topics]({filename}intermediate.md#intermediate-topics)  
