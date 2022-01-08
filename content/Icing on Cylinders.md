Title: Icing on Cylinders   
Category: NACA
tags: cylinder

> ##"The collection of ice by the cylinders is similar to the collection of ice by airplane components." [^1]


![Figure 1 of NACA-TR-1215, depicting a cylinder in cross flow with air flow lines and water drop trajectories impacting the cylinder](images/naca-tr-1215/figure1a.png)

The cylinder has a wide range of current uses in aviation:  
- Meteorological instruments for flight and icing wind tunnel tests  
- Aircraft in-flight ice detectors and indicators  
- Structural elements (such as landing gear and cables)  
- An approximation of an airfoil leading edge (used in thermal design and icing wind tunnel test conditions determination[^2])   

Icing conditions measurements with instruments based on cylinders were key to developing the 
current aircraft flight in icing certification regulations.

One hundred and thirty-two NACA publications related to aircraft icing were 
identified in ["The Historical Selected Bibliography of NACA-NASA Icing Publications"]({filename}/The Historical Selected Bibliography of NACA-NASA Icing Publications.md), 
and categorized into 16 topics.

Publications related to icing on a cylinder will include several of the 16 topics, 
such as “Meteorology of Icing Clouds”, “Meteorological Instruments” 
and “Impingement of Cloud Droplets” (as cylinders were and still are used as icing measurement instruments), 
as well as “Heat Transfer”. With a firm foundation in those concepts, 
one may then move on to other topics, including ice protection.

The cylinder is geometrically simple, but is aerodynamically complex in such areas as flow separation, and so it will present worthy challenges. 

##The Cylinder Thread (_key points noted_)

These reviews will focus on water drop impingement and icing on cylinders. 
However, as cylinders were important instruments for meteorological measurements, some measurement results will be included. 
The accuracy of the cylinder when used as an instrument for determining icing conditions will be re-evalutated several times 
in the publications. 
While such instruments had limitations, the were often the best available technology at the time. 
(There may be a thread in the future devoted to measurements of the icing environment). 

Some typical multicylinder meteorological instruments (from [^3]):
![Multicyllnder cloud meters used in comparative study at
Mount Washington Observatory](/images/naca-tn-2708/figure_1.png)

###[NACA-TN-779 “Aerodynamic Heating and Deflection of Drops by an Obstacle in an Airstream in Relation to Aircraft Icing"]({filename}/NACA-TN-779.md)  
>   1. The effect of aerodynamic heating is predictable  
>   2. Water drop impingement on a cylinder is calculated  

###["Mathematical Investigation of Water Droplet Trajectories"]({filename}/Mathematical Investigation of Water Droplet Trajectories.md)  
>   1. The Langmuir drop size distributions are defined
>   2. The water drop impingement terms E, Beta, K, and Ko are defined
>   3. The use of cylinders of different sizes and detailed calculations to determine water drop sizes

###[Implementation of cylinder impingement correlations in Python]({filename}/Implementation of cylinder impingement correlations in Python.md)  
>   1. The cylinder impingement correlations were implemented and reproduced values from "Mathematical Investigation of Water Droplet Trajectories"
>   2. A subtlety about calculations with drop size distributions is noted.

###[A Detailed Comparison of Water Drop Impingement Calculations]({filename}/A Detailed Comparison of NACA-TN-779 and Mathematical Investigation of Water Droplet Trajectories.md)  
>   1. There are differences in conditions in Table IV(a) of "Mathematical Investigation of Water Droplet Trajectories" compared to NACA-TN-779.
>   2. When the conditions are revised to match, the comparison with NACA-TN-779 data improves.

###[Implementation of multicylinder calculations in Python]({filename}/Implementation of multicylinders cylinders.md)
>  1. A manual method of multicylinder calculation is illustrated.  
>  2. The drop median effect diameter is reproduced well from a multicylinder example in "Mathematical Investigation of Water Droplet Trajectories"  

###[NACA-TN-1393 “A Flight Investigation of the Meteorological Conditions Conducive to the Formation of Ice on Airplanes"]({filename}/NACA-TN-1393.md)  
>   1. The accuracy of multicylinder instruments used to determine liquid water content and median water drop size is assessed. 
>   2. An icing intensity index as related to the ice growth rate on a 3 inch diameter cylinder is detailed. 
>   3. Results from the methods of Tribus & Tessman and Langmuir & Blodgett agree well for cylinder analysis. 
>   4. "Tentative" values for icing design conditions were determined. 
>   5. An effect of distance on icing conditions is noted. 

###[NACA-TN-1424 "A Further Investigation of the Meteorological Conditions Conducive to Aircraft Icing"]({filename}/NACA-TN-1424.md)  
>  1. Two methods for determining drop size distributions are compared.
>  2. The difference in water drop concentration around an aircraft body is proposed as an explanation for results from the two methods.
>  3. A temperature dependence of icing conditions is noted.

<!--###[NACA-RM-A9C09 "A Review of Instruments Developed for the Measurement of the Meteorological Factors Conducive to Aircraft Icing"]({filename}/NACA-RM-A9C09.md)  
>  1. Nine instruments, including the fixed cylinder and rotating mulitcylinder, are qualitatively assessed.
>  2. "The [multicylinder] method has assumed the position of a standard against which other instruments are calibrated, and is apt to remain so..."
>  3. The effect of mass measurements errors on multicylinder results were assessed.
>  4. "A reliable method for the measurement of drop-size distribution should be developed"-->

<!--###[NACA-TN-1904 "Observations of Icing Conditions Encountered in Flight During 1948"]({filename}/NACA-TN-1904.md)  
>  1. The average liquid water content varies over distance traveled in icing.
>  2. The value of the multicylinder method for determining drop size distributions is questioned.  -->

NACA-RM-A9C09 "A Review of Instruments Developed for the Measurement of the Meteorological Factors Conducive to Aircraft Icing" _(planned)_  

NACA-TN-1904 "Observations of Icing Conditions Encountered in Flight During 1948" _(planned)_  

<!--  defer to meteorology thread
NACA-TN-2306 "Meteorological Analysis of Icing Conditions Encountered in Low-Altitude Stratiform Clouds" _(planned)_  -->

NACA-TN-2708 "Comparison of Three Multicylinder Icing Meters and Critique of Multicylinder Method" _(planned)_  

<!--NACA-TN-2738 "A Probability Analysis of the Meteorological Factors Conducive to Aircraft Icing in the United States" _(planned)_  -->
NACA-TN-2903 "Impingement of cloud droplets on aerodynamic bodies as affected by compressibility of air flow around the body" _(planned)_  

NACA-TN-2904 "Impingement of water droplets on a cylinder in an incompressible flow field and evaluation of rotating multicylinder method for measurement of droplet-size distribution, volume-median droplet size, and liquid-water content in clouds" _(planned)_  

NACA-RM-E53D23 "Procedure for Measuring Liquid-Water Content and Droplet Sizes in Super-cooled Clouds by Rotating Multicylinder Method" _(planned)_  

NACA-TR-1215 "Impingement of Cloud Droplets and Procedure for Measuring Liquid-Water Content and Droplet Sizes in Supercooled Clouds by Rotating Multicylinder Method" _(planned)_  

NACA-TN-3338 "A Dye-Tracer Technique for Experimentally Obtaining Impingement Characteristics of Arbitrary Bodies and a Method for Determining Droplet Size Distribution" _(planned)_  

Python cylinder analysis updated with ambient temperature effects _(planned)_  

##Other

[Blast from the Past: NACA Icing Publications](index.html)  
[The Historical Selected Bibliography of NACA-NASA Icing Publications]({filename}/The Historical Selected Bibliography of NACA-NASA Icing Publications.md)  
[NACA Icing Publications Database]({filename}/naca icing publications database.md)  

[Blog (to see the latest)](/blog.html)

##Notes:
[^1]: 
von Glahn, Uwe H.: The Icing Problem, presented at Ottawa AGARD Conference. AG 19/P9, June 10-17 1955, reprinted in Selected Bibliography of NACA-NASA Aircraft Icing Publications, NASA-TM-81651, August, 1981  I could not locate this on the NTRS. It is available at (https://core.ac.uk/reader/42858720) (circa November, 2021)  
[^2]:
Anderson, David N., Manual of Scaling Methods. NASA/CR-2004-212875, March 2004. https://ntrs.nasa.gov/citations/20040042486 .  
[^3]: 
Howell, Wallace E.: Comparison of Three Multicylinder Icing Meters and Critique of Multicylinder Method. NACA-TN-2708, 1952.  
