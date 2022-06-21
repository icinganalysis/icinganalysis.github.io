Title: Ice Shapes and Their Effects  
Category: NACA  

###_"an irregular shape is developed due to the ice formation, which is ruinous to the aerodynamic efficiency of the airfoils"_ [^1]

![Figure_14 of NACA-TN-1598](images/naca-tn-1598/Figure_14_naca_tn_1598.png)  
>from NACA-TN-1598 [^2]

#Ice Shapes and Their Effects Thread

This thread will cover ice shapes and the aerodynamic effects of the ice.

This will primarily cover ice shapes on unprotected surfaces.

There are additional publications on ice shapes for deicing systems and propellers that will not be reviewed here. 

##Publications

###Review of the "Ice Shapes and Their Effects" thread so far

In this thread, we saw:

An almost "lost gem" of the NACA-era, [NACA-TN-313, "The Formation of Ice upon Airplanes in Flight"] with, in 1929: 
- Description of supercooled large drop (SLD) icing conditions  
- "Detect and exit" icing mitigation strategy  
- Natural icing flight tests of icephobic materials  
- Identification of different types of icing  

The effect of "protuberances" on an airfoil section lift and drag in [NACA-TR-446, "Airfoil Section Characteristics as Affected by Protuberances"]({filename}NACA-TR-446.md)  

The effects of simulated residual ice in [NACA-WR-L-292, "Effects of a Simulated Ice Formation on the Aerodynamic Characteristics of an Airfoil"]({filename}NACA-WR-L-292.md)     

Airplane levels effects of icing are measured, and broken into major components in [NACA-TN-1598, "Effects of Ice Formations on Airplane Performance in Level Cruising Flight"]({filename}NACA-TN-1598.md)   
  
Gray, Vernon H., and von Glahn, Uwe H.: Effect of Ice and Frost Formations on Drag of NACA 651_212 Airfoil for Various Modes of Thermal Ice Protection. NACA-TN-2962, 1953.   
>By "discriminating use of the data", drag results can be estimated using NACA-TR-446.  

von Glahn, Uwe H., and Gray, Vernon H.: Effect of Ice Formations on Section Drag of Swept NACA 63A-009 Airfoil with Partial-Span Leading-Edge Slat for Various Modes of Thermal Ice Protection. NACA-RM-E53J30, 1954.  
>The drag due to ice on a swept airfoil section is measured. 

Gray, Vernon H., and von Glahn, Uwe H.: Aerodynamic Effects Caused by Icing of an Unswept NACA 65A004 Airfoil. NACA-TN-4155, 1958  
and  
Gray, Vernon H.: Correlations Among Ice Measurements, Impingement Rates, Icing Conditions and Drag Coefficients for an Unswept NACA 65A004 Airfoil. NACA-TN-4151, 1958.  
>Correlations are develop between ice shapes, aerodynamic performance, and icing conditions.  

Gray, Vernon H.: Correlation of Airfoil Ice Formations and Their Aerodynamic Effects With Impingement and Flight Conditions. SAE preprint No. 225 (paper presented at SAE National Aeronautics Meeting), October 1957, [https://archive.org/details/nasa_techdoc_19670083891/page/n19/mode/2up](https://archive.org/details/nasa_techdoc_19670083891/page/n19/mode/2up).  
and  
Gray, Vernon H.: Prediction of Aerodynamic Penalties Caused by Ice Formations on Various Airfoils. NASA-TN-D-2166, 1964.  [https://archive.org/details/nasa_techdoc_19810068590](https://archive.org/details/nasa_techdoc_19810068590)  
>A more general correlation of drag due to ice on an airfoil is developed.  

Wilder, Ramon W.: "Techniques used to determine Artificial Ice Shapes and Ice Shedding, Characteristics of Unprotected Airfoil Surfaces" in Anon., "Aircraft Ice Protection", the report of a symposium held April 28-30, 1969, by the FAA Flight Standards Service; Federal Aviation Administration, 800 Independence Ave., S.W., Washington, DC 20590. [https://apps.dtic.mil/sti/pdfs/AD0690469.pdf](https://apps.dtic.mil/sti/pdfs/AD0690469.pdf).  
>Glaze ice shape correlations for two commercial aircraft airfoils are developed.  

Summary of the "Ice Shapes and Their Effects" thread


##Discussion  

We will look at recent data to address some questions:  
1. Does leading edge freezing fraction correlate to airfoil ice shape parameters?  
2. How well do LEWICE results compare to the ice shapes data that we have seen?  

NASA-TM-107374 and NACA-TR-446  



###Correlation to freezing fraction 

In the review of NACA-TN-4155, it was noted:

We can see elements of a "freezing fraction" calculation from Messinger [^4] in equations (1) and (2)
from above. 

    θ = 483 w^0.5 (Em/(32-t_o)^(1/3) - 72 - 58 (1 - 1/1.35^αi), deg   (1)
    
    h = 4.35X10-4 τ V_o (w β_m)*0.5 (32-t_o)^0.3   (2)

LWC (w) and a water catch efficient term (E_m or β_m) are in both, and a temperature difference. 

From Messinger (equations re-arranged), we also see a water catch rate and a temperature difference:

    mw = LWC * β * V_o  or mw = LWC * E_m / length * V_o

    n = ((hc * (ts - ta)) + (Le * hc * 0.7 / cp * (pvs - pv) / p) + (mw * cpw * (ts - ta)) 
          -(hc * (r * u**2 / 2 / cp))-(mw * (u**2 / 2))) / (Lf * mw)

In the [Conclusions of the Icing Thermodynamics Thread]({filename}thermodynamics_thread_wrap_up.md) 
it was noted that 
[NASA/CR-2005-213852](https://ntrs.nasa.gov/api/citations/20050215212/downloads/20050215212.pdf)  
treated the airfoil leading edge as a cylinder with a diameter equal to twice the leading edge radius of curvature 
for calculating leading edge freezing fraction. 
We will use that here. 

For the cases in NACA-TN-4151 Table II, 
the leading edge equivalent cylinder freezing fractions were calculated. 
A Langmuir "D" drop size distribution was assumed. 

A fitting function of the form 

    A * freezing_fraction + B * aoa + C = theta_upper_horn_measured 
was used to determine the best fit coefficient values of A and B and C. 

The results of this are compared to the values from equation (1) below:  

![](images/ice_shapes_wrap_up/thetas fits.png)  

Both fits have some variance, but the one using freezing fraction 
has a slightly better fit. 

A similar fit was made for ice height with the addition 
of a water catch term:

    A * freezing_fraction * water_catch + B * aoa + C = theta_upper_horn_measured 

![](images/ice_shapes_wrap_up/ffcyl hs fit.png)  

The results are comparable between equation (2) values 
and the fit with freezing fraction. 

To summarized, calculated equivalent cylinder leading edge freezing fraction 
correlates as well to the ice shape height and theta as 
the icing conditions equations (1) and (2). 
They convey very similar information. 

I view this even more validation of Uwe von Glahn's assertion that 
**"The collection of ice by the cylinders is similar to the collection of ice by airplane components"** [^4] from 1955.  

###Comparison to LEWICE 2D  

In the [Conclusions of the Cylinder Thread]({filename}cylinder_thread_wrap_up.md) 
and [Conclusions of the Icing Thermodynamics Thread]({filename}thermodynamics_thread_wrap_up.md) 
comparisons to LEWICE 2D were made. 

We will do so again here, 
but with the caution that the cases in NACA-TN-4151 
are perhaps not a "fair" test. 
The thin NACA 65A004 airfoil had separation at higher angles of attack, 
The (default) potential flow solution was used to run LEWICE.
Potential flow will not model the separation correctly 
(and frankly, any CFD method will be challenged). 

The NACA 65A004 airfoil used in NACA-TN-4151 was not included in the LEWICE validation set, 
nor any other 4% thickness airfoils. 

Also, the LEWICE 2D manual notes that:  
>The range of angle of attack values in the validation database is -4 to +7 degrees.

and the 8, 10, and 11 degree AOA cases exceed that.

We will probably learn more about the limitations of potential flow 
than the capabilities of LEWICE 2D. 

LEWICE 2D calculations are compared to NACA-TN-4151 Table II 
values below.  

There is some correlation of upper horn angle at higher values, 
but poor correlation at lower theta values, 
many of which are at higher AOA values where there is separation. 

![](images/ice_shapes_wrap_up/l2d theta_.png)  

LEWICE was run with the default ice density of 917 kg/m^3. 
For ice height, the upper bound is not exceed 
but the LEWICE 2D values tend to be low. 
Using a lower ice density (or expeditiously increasing icing time) 
would move the LEWICE 2D value up to a better average, 
but would not improve the scatter. 

![](images/ice_shapes_wrap_up/l2d hs.png)  

##What is still used today 

###Protuberance effects

The "protuberance" effect data from NACA-TR-446 in perpetuated in Brumby,
which in addition to NACA-TR-446 collected several other studies and 
summarized them on a series of graphs. 

2] Brumby RE. Wing Surface Roughness – Cause & Effect. D.C. Flight Approach, Jan. 1979. pp. 2-7. 

These are still used today for purposes like in NACA-TR-446 of
"the prediction of the effects of short span protuberances" 
such as spoilers, and the effect of repairs such as external doublers. 

Protuberances had renewed interest after supercooled large drop (SLD) icing 
was recognized as a potential threat to current aircraft. 
Large drop icing can form in area different from smaller drops, 
and if ice forms aft of a protection system it can produce different shapes. 
the "Forward Facing Quarter Round" has been used as a stand-in for such ice. 

![](images/DOT-FAA-AR-00-14/Figure 7.png)  
>Figure 7 from DOT/FAA/AR-00-14.

You can find a more detail discussion at
Bragg, Michael B., Andy P. Broeren, and Leia A. Blumenthal. "Iced-airfoil aerodynamics." Progress in Aerospace Sciences 41.5 (2005): 323-362.  http://icing.ae.illinois.edu/papers/05/Iced%20Airfoil%20Aerodynamics.pdf  

###Icing conditions parameters  

As we saw above, the "empirical" icing conditions parameters in NACA-TN-4151 
anticipated and correlate to equivalent leading edge freezing fraction values. 

This gets used in 

NASA/CR-2004-212875 and NASA/CR-2005-213852

![NASA/CR-2005-213852 Figure 3](images/freezing_fractions/NASA_CR_2005_213852_Figure3.png)  

###Ice shape parameters

While there is no completely agreed upon "standard" set of parameters to describe an ice shape, 
the values from NACA-TN-4151 get perpetuated in the LEWICE user's manual,
and these (with the addition of icing limits) are probably the closest thing we have to a "standard" set:

NASA/CR—2008-214255
User’s Manual for LEWICE Version 3.2
November, 2008
https://ntrs.nasa.gov/api/citations/20080048307/downloads/20080048307.pdf

![](images/ice_shapes_wrap_up/LEWICE manual figure 18.png)  

However, the validation report used a modified definition for theta:

NASA/CR-1998-208687
A Summary of Validation Results for LEWICE 2.0
december, 1998
![](images/ice_shapes_wrap_up/LEWICE validation fig 16.png)  

##Notes  
[^1]: Carroll, Thomas, and McAvoy, William H.: The Formation of Ice upon Airplanes in Flight. NACA-TN-313, 1929.   
[^2]: Preston, G. Merritt, and Blackman, Calvin C.: Effects of Ice Formations on Airplane Performance in Level Cruising Flight. NACA-TN-1598, 1948.  

