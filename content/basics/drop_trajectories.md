Title: The Motions of Water Drops    
header: The Basics of Aircraft Icing
Date: 2023-12-2 12:00  
tags: basics  
status: draft  
rights: CC-BY-NC-SA 4.0

# DRAFT

Calculating the amount of water that hits or impinges on the surface 
of an airplane as it flies through a cloud 
is an important step that is required to calculate ice shapes, 
and to determine the amount of ice protection required.

Air flow around an airfoil in flight can be idealized as streamlines, 
which may be parallel far from an object, but bend around an object close to it. 
Mathematical models are available to calculate streamlines. 
Streamlines can be visualized in a wind tunnel using smoke traces 
(a source that makes a thin line of smoke that shows how the airflow bends). 

Water drops tend to follow streamlines far from an object, 
but due to their momentum, diverge from streamlines near an object. 
Calculations of the paths of water drops, termed "Water Drop Trajectories", 
are in some ways more complicated than the air flow calculations. 
There is no simple way to directly visualize water drop trajectories. 

Streamlines and water drop trajectories around a cylinder 
(airflow is from left to right, or, alternatively, the cylinder is moving from right to left through stationary air and water drops):  
![Figure 1 of NACA-TN-2903, a cylinder in cross flow with air flow lines and water drop trajectories impacting the cylinder](..%2Fimages%2Fcylinder%20with%20flow%20lines.png)  
_from NACA-TN-2903, 1953._  

As water drop trajectories diverge around an object, 
not all drops in the frontal view of the object impinge on the object. 
The fraction of water drops that do impinge is termed the "Water Collection Efficiency". 
Once drops impinge on a surface they tend to remain on the surface. 
The water collection efficiency can vary widely, 
depending on factors such as the water drop size and object size, airspeed, 
air pressure, and others. 
The water collection efficiency can also be zero for some cases 
(such as very small water drops, a very large object, and a low airspeed). 

Collection efficiency is the ratio of the area of impingement to the frontal area:  
![Figure II-3. Graphical representation of parameters used in trajectory work.](..%2Fimages%2FModern%20Icing%20Technology%2FFigure%20II-3.png)   
_from ["Modern Icing Technology" (1952)](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/7990/bad2682.0001.001.pdf?sequence=5)_  

The water drops do not impinge everywhere on a surface, they tend to 
only hit near the leading edge. The limits of where they hit is termed 
"Impingement Limits". These can vary with conditions details such as airspeed and drop size.

In a particular cloud, not all water drops are the same size. 
The "Langmuir Drop Size Distributions" describe an idealized approximation of 
how the drop sizes vary in a cloud about an average or median drop size. 
It has seven bins, each with a representative drop size and fraction of the 
total water content in the cloud. 

## Resources  

[The Aircraft Icing Handbook, DOT/FAA/CT-88/8](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf), 
Volume 1, Chapter 1, Section 2.2.1 in particular. Note that much of that section is in the 
perhaps little known update from 1993: [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA276499.pdf). 
The update contains only the updated pages. 
This worked fine when one printed the pages, punched holes, and manually substituted them into a three ring binder, 
but not so well in the digital age. 
I do not know of a pdf file that integrates the two into one.  

[“Engineering Summary of Airframe Icing Technical Data”, FAA Technical Report ADS-4, 1963](https://apps.dtic.mil/sti/citations/AD0608865)  
Chapter 2 in particular. This has more figures of impingement correlation figures than DOT/FAA/CT-88/8.

## Related  

This is part of [The Basics]({filename}basics.md) series.  


