title: airfoil impingement drop distribution  
Category: NACA  
tags: instruments  
status: draft  

###_"... it is believed that a comparison of the water-drop impingement over several different airfoils ... is of interest"_ [^1]  


#NACA-TN-1397, "A Method for Numerically Calculating the Area and Distribution of Water Impingement on the Leading Edge of an Airfoil in a Cloud."
  
#NACA-TN-2476, "An Empirical Method Permitting Rapid Determination of the Area, Rate, and Distribution of Water-Drop Impingement on an Airfoil of Arbitrary Section at Subsonic Speeds."  

#NACA-RM-E52B12, "Impingement of Water Droplets on an NACA 651-212 Airfoil at an Angle of Attack of 4°."  

##Abstract  
>The trajectories of droplets in the air flowing past an NACA 65<sub>1</sub>-212
airfoil at an angle of attack of 4° were determined. The collection
efficiency, the area of droplet impingement, and the rate of droplet
impingement were calculated from the trajectories and are presented herein
to cover the following range of conditions:  
```text
Variable                    Minimum value  Maximum value         
Droplet diameter (microns)  5              100                    
Airplane speed. (mph)       150            Critical flight speed  
Altitude (ft)               1000           35,000                 
Chord length (ft)           2              20                     
```

##Discussion  

###Is this an instrument?  

No.

These three publications discuss water drop impingement, 
without mentioning an instrument. 
One might wonder why 
these were included in the "Meteorological Instrument" section 
of [The Historical Selected Bibliography of NACA-NASA Icing Publications]({filename}The Historical Selected Bibliography of NACA-NASA Icing Publications.md), 
when there is also a large "Impingement of Cloud Droplets" section.  

However, the later NACA-TN-3338 does describe measuring a drop size 
distribution based on the impingement rates on a cylinder, 
measured with the dye tracer method in a wind tunnel,
and the method could be used for airfoils. 
While it was not developed in to a practical flight instrument, 
it is interesting. 

###Low cost, approximate impingement values  

A motivation for these three publications was that the use of a 
differential analyzer was expensive and time consuming. 
It is hard to design an ice protection system without knowing 
how much water is hitting where on an airfoil.  

>the designer is therefore
confronted with the desirability of employing a computation method,
preferably without the necessity of a differential analyzer, which
will provide some indication of the area and distribution of water
impingement.  

[^1]  

These three publications provide numerous tables, graphs, 
and an "equivalent cylinder" method 
to obtain approximate impingement values without the use 
of a differential analyzer. 


###Airfoils  

NACA-TN-1397:  
>12—percent—thick symmetrical Joukowski profile chosen to
simulate an NACA 0012 section. [^1]

NACA-TN-2476:  
>The five airfoil cases selected for the water-drop-trajectory
investigation are listed in the following table: [^2]  
![NACA-TN-2476 Table of airfoils](images/NACA-TN-2476/Table of airfoils.png)  
_["Do" is apparently short for "ditto", or "same as above".]_  

An advantage of the Joukowski airfoils for analysis was that the 
flow solution for a cylinder 
(an analytic function, for incompressible, inviscid flow) 
can be mapped onto a Joukowski airfoil section. 
[We might go into more detail on that in a post in the distant future.]  

NACA-RM-E52B12:  
As stated in the abstract above, a NACA 65<sub>1</sub>-212
airfoil at an angle of attack of 4° was analyzed over a broad range of conditions.  
>The NACA 65-series airfoil sections are particularly adaptable to airplanes 
having high-level flight speeds. An airfoil 12 percent thick was
chosen as adaptable to transport and cargo airplanes. An angle of attack
of 4° was chosen as being representative of low cruise attitude for a
turbojet-powered aircraft operated under conditions giving a relatively
large area of droplet impingement on the airfoil.  


###NACA-TN-1397 "equivalent" cylinder analysis  

>The designer of a heated wing, desiring to know the rate and
area of water impingement on the leading edge in a specified cloud at
a given flight speed, might assume that the impingement limit be
identical to that for a cylinder with a radius equal to the wing
leading-edge radius. There is some question, however, as to the
accuracy of this assumption for the larger drop sizes and for wing
sections with small leading-edge radii. The designer is therefore
confronted with the desirability of employing a computation method,
preferably without the necessity of a differential analyzer, which
will provide some indication of the area and. distribution of water
impingement.  
In this report, the water-drop trajectory equations used in
reference 3 have been modified to establish a step-by-step integration 
method applicable to any two-dimensional flow for which the
streamline velocity components are known or can be approximated. If
drop trajectories for a large range of airspeeds and drop diameters
are required, the computation time is large, arid the desirability of
access to a differential analyzer becomes evident. The integration
method presented herein, however, does permit the calculation of
any desired number of trajectories without resort to an analyzer; and
it also provides a means for estimating the error which will be
incurred by replacing the airfoil by a cylinder with a radius equal
to the leading-edge radius of the airfoil. In addition, water-impingement 
data over the entire airfoil surface can be obtained by
the integration method.
...

>With the set of trajectories calculated by the step—by—step
process and presented in figure 6, a comparison can be made between
the impingement of water drops on the Joukowski airfoil and its
equivalent cylinder, for a small range in drop sizes. Such a comparison
is made in figure 10, where the airfoil was used as the basis for
comparison. For area of impingement, the equivalent cylinder can be
used without much error to a drop—size diameter of aproximately 20
microns. However, for rate of impingement, appreciable difference
is not encountered until drop diameters are above 3O microns. It is
of interest to note that meteorological data obtained in flight
(reference 5) indicate a mean-effective drop-size diameter 2 for
cumulus clouds of 15 to 25 microns. Furthermore, mean-effective drop
diameters as high as 50 microns have been measured in clouds of the
altostratus category. Since, in accordance with the definition of
mean-effective drop diameter, half the water contained in a cloud
sample is composed of drops larger than the mean-effective diameter,
it is apparent that the use of an equivalent cylinder may be subject
to considerable error when applied to typical icing conditions in
which large drop-size diameters have been observed.

![Figure 6 from NACA-TN-1397](images/naca-tn-1397/Figure 6.png)  
_Figure 6 from NACA-TN-1397_  

![Figure 10 from NACA-TN-1397](images/naca-tn-1397/Figure 10.png)  
_Figure 10 from NACA-TN-1397_  

The "Conclusions" state:
```text
2. The rate and area of water-drop impingement on an NACA 0012
airfoil having an 8-foot chor& is approximated with reasonable
accuracy by the impingement on a cylinder of radius equal to the
leading-edge radius of the airfoil for only drop diameters below 20
microns at speeds of about 200 miles per hour and at an altitude of
7000 feet.
```

###NACA-TN-2476  

152 pages  


###Inferring a drop size distribution  

In the conclusions of NACA-TN-1397, it was stated:  
```
4. The area and distribution of water-drop impingement on an
airfoil in motion through a cloud of known drop-size distribution can
be obtained by calculating the area and distribution of impingement
for each drop-size range present.
```

This procedure can be reversed, as detailed in NACA-TN-3338 [^4], 
to determine a drop size distribution, if one has measured impingement data. 
To briefly outline, a drop size distribution is assumed, 
and the impingement for the largest drop size bin calculated. 
This is compared to the measured impingement rate 
for the area near the impingement limits to calculate 
the fraction of total water in that drop size bin. 
This is then repeated for each size bin. 


1397
differential analyzer
"equivalent cylinder"


NACA-RM-E52B12  
"mechanical analog"


Bergrun, Norman R.: A Method for Numerically Calculating the Area and Distribution of Water Impingement on the Leading Edge of an Airfoil in a Cloud. NACA-TN-1397, 1947.  
Bergrun, Norman R.: An Empirical Method Permitting Rapid Determination of the Area, Rate, and Distribution of Water-Drop Impingement on an Airfoil of Arbitrary Section at Subsonic Speeds. NACA-TN-2476, 1951.  
Brun, Rinaldo J., Serafini, John S., and Moshos, George J.: Impingement of Water Droplets on an NACA 651-212 Airfoil at an Angle of Attack of 4°. NACA-RM-E52B12, 1952.  
von Glahn, Uwe H., Gelder, Thomas F., and Smyers, William H., Jr.: A Dye-Tracer Technique for Experimentally Obtaining Impingement Characteristics of Arbitrary Bodies and a Method for Determining Droplet Size Distribution. NACA-TN-3338, 1955.  
