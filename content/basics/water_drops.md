Title: Water Drops      
header: The Basics of Aircraft Icing
Date: 2024-01-15 14:00  
tags: basics, clouds, impingement  
status: draft  
rights: CC-BY-NC-SA 4.0

## DRAFT

The water that causes most aircraft in-flight icing is small drops in clouds. 
Average drop sizes are typically 10 to 50 ["Micrometers"]({filename}Nomenclature.md#micrometer) (μm) in diameter
(for comparison, a human hair is about 50 to 100 micrometers in diameter).

![drop sizes.png](/images%2Fdrop%20sizes.png)  
_Typical drop sizes, approximately proportional. Public Domain by Donald Cook._  

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
Calculations of the paths of water drops, termed water ["Drop Trajectories"]({filename}Nomenclature.md#drop-trajectory), 
are in some ways more complicated than the air flow calculations. 
There is no simple way to directly visualize water drop trajectories. 

Streamlines and water drop trajectories around a cylinder 
(airflow is from left to right, or, alternatively, the cylinder is moving from right to left through stationary air and water drops):  
![Figure 1 of NACA-TN-2903, a cylinder in cross flow with air flow lines and water drop trajectories impacting the cylinder](/images%2Fcylinder%20with%20flow%20lines.png)  
_from "Impingement of Cloud Droplets on Aerodynamic Bodies as Affected by Compressibility of Air Flow Around the Body". NACA-TN-2903, 1953 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19930083601)_  

As water drop trajectories diverge around an object, 
not all drops in the frontal view of the object impinge on the object. 
The fraction of water drops that do impinge is termed the water ["Collection Efficiency"]({filename}Nomenclature.md#collection-efficiency). 
Once drops impinge on a surface they tend to remain on the surface. 
The water collection efficiency can vary widely, 
depending on factors such as the water drop size and object size, airspeed, 
air pressure, and others. 
The water collection efficiency can also be zero for some cases 
(such as very small water drops, a very large object, and a low airspeed). 

Collection efficiency is the ratio of the area of impingement to the frontal area (Em or Percentage Catch in the figure below):  

![Figure II-3. Graphical representation of parameters used in trajectory work.](/images%2FModern%20Icing%20Technology%2FFigure%20II-3.png)   
_from "Modern Icing Technology" 1952 [deepblue.lib.umich.edu](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/7990/bad2682.0001.001.pdf?sequence=5)_  

The water drops do not impinge everywhere on a surface, they tend to 
only hit near the leading edge. The limits of where they hit is termed 
["Impingement Limits"]({filename}Nomenclature.md#impingement-limits). These can vary with conditions details such as airspeed and drop size.

In a particular cloud, not all water drops are the same size. 
The ["Langmuir Drop Size Distributions"]({filename}Nomenclature.md#langmuir-distribution) describe an idealized approximation of 
how the drop sizes vary in a cloud about an average or median drop size. 
It has seven bins, each with a representative drop size and fraction of the 
total water content in the cloud.  

![Table 1-1. LANGMUIR AND BLODGETT DROPLET SIZE DISTRIBUTIONS.](/images%2FFAA%20Handbook%20volume%201%2FTable%201-1.png)  
_from  "Aircraft Icing Handbook", DOT/FAA/CT-88/8-1 [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf)_  

Much study has been done on the conditions that cause icing on an aircraft in flight. 
The data were collected into graphs in design documents and certification requirements. 
They give expected values for intensity or concentration of supercooled water in g/m^3 
(["Liquid Water Content"]({filename}Nomenclature.md#liquid-water-content) or "LWC"), 
and mean or average drop size 
(["Mean Effective Drop Diameter"]({filename}Nomenclature.md#medd) "MED" or ["Median Volumetric Diameter"]({filename}Nomenclature.md#mvd) "MVD"). 
Other factors also have to be specified, such as temperature and altitude, 
for a complete definition. 

Part of the definition of ["Appendix C"]({filename}Nomenclature.md#appendix-c) icing conditions:  
![AppCfig1.png](/images%2FAppCfig1.png)  
_from Part 25 Appendix C (1964) [ecfr.gov](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-C/part-25/appendix-Appendix%20C%20to%20Part%2025)_  

["Continuous Maximum Icing Conditions"]({filename}Nomenclature.md#continuous-max) 
are for ["Stratus"]({filename}Nomenclature.md#stratus) or layer-type clouds, 
which can extend for several miles.  

["Intermittent Maximum Icing Conditions"]({filename}Nomenclature.md#intermittent-max) 
are for ["Cumulus"]({filename}Nomenclature.md#cumulus)  or "storm" type clouds, 
which extend over a lesser distance, but have more intense icing conditions.  

Regulations cover large drop icing conditions, 
termed ["Appendix O"]({filename}Nomenclature.md#appendix-o), were published in 2014. 
These have lWC values and extents roughly comparable to Continuous Maximum Icing Conditions, 
but have larger drop sizes. There are four detailed conditions definitions. 
The ["Freezing Drizzle"]({filename}Nomenclature.md#freezing-drizzle) definition includes drop sizes over 200 micrometers. 
The ["Freezing Rain"]({filename}Nomenclature.md#freezing-rain) definition includes drop sizes over 1000 micrometers. 
The larger drops can cause icing in locations where Appendix C 
size drops do not reach. 

## Resources  

Appendix C [ecfr.gov](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-C/part-25/appendix-Appendix%20C%20to%20Part%2025)

Appendix O [ecfr.gov](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-C/part-25/subpart-F/subject-group-ECFR3f07132c2c2d01e/section-25.1420)  

"Aircraft Icing Handbook", DOT/FAA/CT-88/8 [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf), 
Chapter 1, Sections 1 and 2.2.1 in particular.  
Also note that there was a perhaps little known update in 1993: [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA276499.pdf) The update contains only the updated pages. 
This worked fine when one printed the pages, punched holes, and manually substituted them into a three ring binder, 
but not so well in the digital age. 
I do not know of a pdf file that integrates the two into one.  

“Engineering Summary of Airframe Icing Technical Data”, FAA Technical Report ADS-4, 1963 [apps.dtic.mil](https://apps.dtic.mil/sti/citations/AD0608865)  
Chapter 2 in particular. This has more figures of impingement correlation than DOT/FAA/CT-88/8.

## Related  

This is part of [The Basics]({filename}basics.md) series.  
