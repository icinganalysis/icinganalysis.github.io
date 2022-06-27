Title: NACA-TN-3024-revisited  
Category: NACA  
tags: thermodynamics  

> ###_"evaporation losses are ... very small (less than 1 percent) in the case of smaller obstacles (of icing-rate-measurement-cylinder size)."_  

#"Maximum Evaporation Rates of Water Droplets Approaching Obstacles the Atmosphere under Icing Conditions" Evaporation calculations [^1]

![Figure 1. Motional relationships among air-stream, droplet, and obstacle.](images/naca-tn-3024/Figure1.png)  

##Summary
Less that 1% of drops evaporate approaching an obstacle for most cases.

##Key points

1. Equations are detailed for the evaporation of water drops approaching an obstacle.  
2. The equations were coded into a python program.  
3. Less that 1% of drops evaporate approaching an obstacle for most cases.  
4. A water drop that approaches on the stagnation line but does not impinge is predicted to evaporate away. 

[NACA-TN-3024]({filename}NACA-TN-3024.md) was reviewed previously, 
herein we will concentrate on comparing our own code to the results in NACA-TN-3024.

##Abstract

> When a closed body or a duct envelope moves through the atmosphere,
air pressure and temperature rises occur ahead of the body or, under ram
conditions, within the duct. If cloud water droplets are encountered,
droplet evaporation will result because of the air-temperature rise and
the relative velocity between the droplet and stagnating air. It is
shown that the solution of the steady-state psychrometric equation provides 
evaporation rates which are the maximum possible when droplets are
entrained in air moving along stagnation lines under such conditions.
Calculations are made for a wide variety of water droplet diameters,
ambient conditions, and flight Mach numbers. Droplet diameter, body
size, and Mach number effects are found to predominate, whereas wide
variation in ambient conditions are of relatively small significance in
the determination of evaporation rates.  
The results are essentially exact for the case of movement of droplets 
having diameters smaller than about 30 microns along relatively long
ducts (length at least several feet) or toward large obstacles (wings),
since disequilibrium effects are then of little significance. Mass losses
in the case of movement within ducts will often be significant fractions
(one-fifth to one-half) of original droplet masses, while very small droplets 
within ducts will often disappear even though the entraining air is
not fully stagnated. Wing-approach evaporation losses will usually be of
the order of several percent of original droplet masses.  
Two numerical examples are given of the determination of local evaporation 
rates and total mass losses in cases involving cloud droplets
approaching circular cylinders along stagnation lines. The cylinders
chosen were of 3.95-inch (10.0+ cm) diameter and 39.5-inch 100+ cm)
diameter. The smaller is representative of icing-rate measurement cylinders, 
while with the larger will be associated an air-flow field similar
to that ahead of an airfoil having a leading-edge radius comparable with
that of the cylinder. It is found that the losses are less than 5 percent. 
It is concluded that such losses are, in general, very small
(less than 1 percent) in the case of smaller obstacles (of icing-rate-measurement-cylinder 
size); the motional dynamics are such, however, that
exceptions will occur by reason of failure of very small droplets (moving
along stagnation lines) to impinge upon obstacle surfaces. In such
cases, the droplets will evaporate completely.  

    
##Discussion

>The general literature in the field of evaporation from droplets is
extensive, but few studies of the particular problem of droplets approaching 
obstacle under icing conditions have been made. Both Hardy (ref. 4)
and Langmuir (ref. 5) have considered certain aspects of the question;
both analyses took into account the fact that the droplet will not, in
general, be in instantaneous psychrometric equilibrium with its surroundings. 
In both cases, the conclusion was reached that total evaporative
losses from droplets actually reaching obstacle surfaces are of the order
of several percent for the particular sets of conditions of their analyses. 
In both investigations, however, the ranges of droplet size, air
temperature and pressure, body size, and flight Mach number were rather
restricted.

>A complete treatment of the problem would require:
(1) use of the equations of motion of a droplet of liquid in a (compressible) gas, 
the equations to take into account in some way changes of
drag coefficient with Mach number;
(2) use of the equations governing the dynamic thermal behavior of
a volatile sphere under quite general conditions of changing heat and
mass-transfer rate including, in some instances, radiation effects; and
(3) coverage of wide ranges of obstacle size and shape, droplet
size, flight Mach number, and flight ambient air conditions.  

>The unavailability of a suitable high-speed calculator made it
necessary, however, to restrict in some manner the scope of the calculations. 

For point (1), we developed compressible flow relationships in 
["The AEDC 1-Dimensional Multi-Phase code (AEDC1DMP) and the iasd1dmp]({filename}aedci1mp.md).
The drag coefficient used is a function of Reynolds number, but not Mach. 
While the flow Mach numbers considered in NACA-TN-3024 included high values (0.75), 
the relative drop-to-air Mach values were lower (<0.3), so we will consider
Mach independence to be "good enough". 

For point (2), we will leave out radiation effects. 
For large drops, the temperature distribution within a drop caused by dynamic changes may be important, 
but for smaller drops (<100 micrometer) a constant temperature approximation is "good enough". 

For point (3), we wrote our equations to use a general air speed function as an input, 
so we just need a unique airspeed function for each "obstacle".

And fortunately, "a suitable high-speed calculator" is now widely available, 
the modern personal computer 
(although mine is an 8-year-old laptop, which some may not count as modern). 

>Since the subject of droplet evaporation, insofar as aircraft are
concerned, is of interest chiefly in connection with icing, radiation
effects could be ignored (since all temperature levels involved are low).
Further, it was decided to consider that a droplet remains in instantaneous 
psychrometric equilibrium with its immediate surroundings,
and its internal temperature was to be taken as uniform. Certain quantitative 
aspects of this assumption are scrutinized in the body of the report and in appendix B; 
a qualitative justification of the procedure is,
however, given here.  

>If evaporation occurs at all, it will occur principally as a result
of a droplet temperature rise, with which a droplet-surface vapor-pressure
rise will be concomitant. Therefore, maximum evaporation rates will occur,
In virtually all cases, in the vicinities of body stagnation points. If,
now, bodies and flight conditions (wing attitudes, for example) are considered 
such that air flows in the vicinities of stagnation points are
essentially symmetrical about such points, then the trajectory of a droplet 
originally on a stagnation line will essentially coincide with the
line. For the sake of simplicity, then, let attention be confined to
histories of droplets moving along such lines. Air temperature and pressure 
will rise monotonically. The droplet instantaneous position will
always be ahead of that of the air with which, at an arbitrary previous
time, it was in contact, although a quasi-static mass-transfer analysis
does not demand such motion. More importantly, with or without evaporation 
the interior droplet temperature will always lag behind the rising
surface temperature, and both the mean droplet temperature and the surface 
temperature will always be less than the local equilibrium (psychrometric) value; 
all droplet temperatures will rise monotonically. It is
possible to conclude that both the actual local time rate of evaporation
and the actual total loss of liquid will be less than those calculated
on the basis of psychrometric calculations in the case of stagnation
streamline droplet motion. It therefore follows that the present quasi-static 
calculations set upper bounds to the loss rates and total losses
for motion along stagnation lines.

We will also restrict our analysis to the stagnation line. 
However, we will not use the "quasi static" assumption, and 
will use the water drop relative speed, mass transfer, and heat transfer 
developed in ["The AEDC 1-Dimensional Multi-Phase code (AEDC1DMP) and the iads1dmp]({filename}aedci1mp.md). 

For the cylinder case in NACA-TN-3024, I used the airspeed calculation from 
Langmuir and ["Let's Build a 1D Water Drop Trajectory Simulation"](build_a_1d_drop_motion_simulation.md) . 

This is incorporated into the file "naca_tn_3024.py" [^2]. 

The Mach values calculated herein are similar, 
but not identical to the values in NACA-TN-3024 Figure 8. 
NACA-TN-3024 did not describe how the airspeed values were calculated. 
Presumably, they would be the same as in Langmuir and Blodgett [^3], which was referenced. 
The airspeed calculations herein were from Langmuir and Blodgett, 
but the values are visibly different. 

![Comparison to Figure 8 Mach values](images/naca-tn-3024/naca_tn_3024_mach.png)  

The evaporation rates compared to Figure 9 values are similar in magnitude, 
but not in detail. 
However, either result meets the "less than 1 percent" LWC change. 

![Comparison to Figure 9 LWC change values](images/naca-tn-3024/naca_tn_3024_lwc_change.png)  


The results above were for a water drop that impinges on the obstacle. 
NACA-TN-3024 considers cases where the drop never impinges:  
>Evaporative losses may be as high as several percent in the case
of small droplets approaching larger obstacles, such as wings, except
that there is always a possibility that the droplet will never reach the
airfoil. (In the latter case, it will, of course, evaporate completely
if it has been approaching along the stagnation line). 

To test this I used a case from ["Let's Build a 1D Water Drop Trajectory Simulation"](build_a_1d_drop_motion_simulation.md), 
where K=0.125, and the drop should theoretically never impinge on the cylinder. 
This requires a rather small drop for this condition (about 1.5 micrometer diameter).

I used a final distance for the cylinder of 1e-30 
(recall that we built the cylinder water drop motion simulation to handle very close approaches, 
and that we do not have infinite time to wait for a solution.)
The water drop is predicted to dwell very close to the cylinder:  
![Simulation time](images/naca-tn-3024/naca_tn_3024_time_k0_125.png)  

The water drop is predicted to be evaporating:  
![Simulated water drop diameter](images/naca-tn-3024/naca_tn_3024_d_drop_k0_125.png)  

The boundary conditions have essentially stabilized at the end of the time simulation. 
The local airspeed is essentially zero, so the local static pressure and temperature are constant. 
As the local static pressure is constant, the local vapor concentration and pressure will be constant. 
The water drop relative air velocity is essentially zero, so the heat and mass Nusselt numbers are constant at 2. 
The heat and mass transfer coefficients are inversely proportional to drop diameter, 
so those values will increase as the drop evaporates further.
So, the prediction that the drop will eventually evaporate is supported if it does not impinge. 

##Conclusions

NACA-TN-3024 stated that the "quasi-static" calculations set an upper bound:

>It therefore follows that the present quasi-static 
calculations set upper bounds to the loss rates and total losses
for motion along stagnation lines.

The comparison to Figure 9 values above support that conclusion. 

The conclusion of "less than 1 percent" LWC change due to evaporation is supported. 

In the post-NACA era, most sources assume (often tacitly) zero loss due to evaporation of drops approaching an obstacle. 

The basic equations required to do the calculations implemented in iads1dmp.py were available in the NACA era. 
I was surprised at how what I had to implement in the python code was just "plumbing" to join together the 
referenced equations and to do the integration, and not new or different equations. 
The key difference in 1953 was the "unavailability of a suitable high-speed calculator."

##Citations

NACA-TN-3024 cites 16 publications:  

- Guibert, A. G., Janssen, E., and Robbins, W. M.: Determination of Rate, Area, and Distribution of Impingement of Waterdrops on Various Airfoils from Trajectories Obtained on the Differential Analyzer. NACA-RM-9A05, 1949.  
- Bergrun, Norman R.: A Method for Numerically Calculating the Area and Distribution of Water Impingement on the Leading Edge of an Airfoil in a Cloud. NACA-TN-1397, 1947.  
- Langmuir, Irving, and Blodgett, Katherine B.: A Mathematical Investigation of Water Droplet Trajectories. Tech. Rep. No. 5418, Air Materiel Command, AAF, Feb. 19, 1946. (Contract No. W-33-038-ac-9151 with General Electric Co.)  
- Hardy, J. K.: Evaporation of Drops of Liquid. Rep. No. Mech. Eng. 1, British R.A.E., Mar. 1947.  
- Langmuir, Irving: The Cooling of Cylinders by Fog Moving at High Velocities. General Electric Co., Mar. 1945.  
- Schmidt, Ernst, and Wenner, Karl: Heat Transfer over the Circumference of a Heated Cylinder in Transverse Flow. NACA-TM-1050, 1943.  
- Frossling, Nils: Uber die Verdiinstung Fallender Tropfen. Gerl. Beitr. Geophys., Bd. 52, Heft 1/2, 1938, pp. 170-216.  
- Homann, F. (D. C. Ipsen, trans.): The Effect of High Viscosity on the Flow Around a Cylinder and Around a Sphere. Rep. No. RE-150-88, Inst. Eng. Res., Univ. Calif., Berkeley (Calif.), July 17, 1951. (Contract NAw-6004.)  
- Kaplan, Carl: The Flow of a Compressible Fluid Past a Sphere. NACA-TN-762, 1940.  
- Goff, John A., and Gratch, Serge: The Saturation Pressure of Water below 600 C. Rep. No. 4546, Thermodynamics Research Lab., Univ. of Pennsylvania, Jan. 1948. (Navy contract NObs-2477.)  
- Williams, Glenn Carber: Heat Transfer, Mass Transfer, and Friction for Spheres. SC. D. Thesis, M.I.T., 1942.  
- Ingebo, Robert D.: Vaporization Rates and Heat-Transfer Coefficients for Pure Liquid Drops. NACA-TN-2368, 1951.  
- Boelter, L. M. K., Cherry, V. H., Johnson, H. A., and Martinelli, R. C.: Heat Transfer Notes. Univ. Calif. Press (Berkeley and Los Angeles), 1948.  
- Dorsey, N. Ernest: Properties of Ordinary Water-Substance. Reinhold Pub. Corp. (New York), 1940.  
- Carslaw, H. S., and Jaeger, J. C.: Conduction of Heat in Solids. Clarendon Press (Oxford), 1947.  
- Jakob, Max: Heat Transfer. Vol. I. John Wiley & Sons, Inc., 1949.  

NACA-TN-3024 is cited 2 times by publications in the NACA Icing Publications Database [^4]:

- Brun, Rinaldo J., Lewis, William, Perkins, Porter J., and Serafini, John S.: Impingement of Cloud Droplets and Procedure for Measuring Liquid-Water Content and Droplet Sizes in Supercooled Clouds by Rotating Multicylinder Method. NACA-TR-1215, 1955. (Supersedes NACA TN’s 2903, 2904, and NACA-RM-E53D23)  
- Coles, Willard D.: Icing Limit and Wet-Surface Temperature Variation for Two Airfoil Shapes under Simulate High-Speed Flight Conditions. NACA-TN-3396, 1955.  

NACA-TN-3024 is cited 6 times in the literature [^5].

##Notes: 

[^1]: 
Lowell, Herman H.: Maximum Evaporation Rates of Water Droplets Approaching Obstacles the Atmosphere under Icing Conditions. NACA-TN-3024, 1953  
[^2]:
Langmuir, Irving, and Blodgett, Katherine B.: "Mathematical Investigation of Water Droplet Trajectories". Report. No. RL-224, January 1945, in "The Collected Works of Irving Langmuir", Vol. 10, 1961. Note: Neither Langmuir nor Bodgett are specifically credited in this publication.
[^3]: [https://github.com/icinganalysis/icinganalysis.github.io](https://github.com/icinganalysis/icinganalysis.github.io)  
[^4]: 
[NACA Icing Publications Database]({filename}naca icing publications database.md)  
[^5]: 
https://scholar.google.com/scholar?hl=en&as_sdt=0%2C48&q=Maximum+Evaporation+Rates+of+Water+Droplets+Approaching+Obstacles+the+Atmosphere+under+Icing+Conditions&btnG=  
