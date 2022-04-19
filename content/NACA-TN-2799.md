Title: NACA-TN-2799  
Category: NACA  
tags: thermodynamics  
status: draft    

> ###_"Solution of the heat and mass transfer from a wetted surface is quite involved and tedious."_  

#"Simple Graphical Solution of Heat Transfer and Evaporation from Surface Heated to Prevent Icing" [^1]

![Figure 1](images/naca-tn-2799/Figure1.png) 

##Summary
Simplified ice protection equations allow graphical solutions.

##Key points

1. Simplified ice protection equations allow graphical solutions.
2. The effects of varying local surface pressure and velocity are included.


##Abstract

> Equations expressing the heat transfer and evaporation from wetted
surfaces during ice prevention have been simplified and regrouped to
permit solutions by simple graphical means. Working charts for quick
and accurate anti-icing calculations are also included. 
    
##Discussion

This 

> INTRODUCTION
Solution of the general problem of heat and mass transfer from a
wetted surface in forced convection is quite involved and tedious.
The calculations that often must be made point by point along a surface
are complex even after the basic variables and ambient conditions have
been determined. The method of solution customarily performed involves
several trial-and-error calculations that are intermediate'between the
final answer and the basic factors that define a particular anti-icing
situation.
This investigation was conducted at the NACA Lewis laboratory to
simplify the method. of calculating heat and mass transfer after the basic
factors (such as ambient temperature, rate of water interception, and
relative velocity) are known. Calculations will be greatly simplified by
a fundamental rearrangement of terms in the conventional equations, which
will eliminate the trial-and-error calculations and. permit a rapid.
graphical solution. The solution will be limited. to the normal range of
anti-icing conditions and. to the case of surface temperatures above
32° F with liquid-water interception by the surface.

> Heat transfer. - The heat transfer in forced convection from a surface 
subjected, to water impingement and. heated above 32° F has been represented 
by the total heat transferred. by convection and by evaporation
of surface water, plus the sensible heat change of the impinging water.
These heat-transfer processes are discussed in detail in references 1 to
5 and are summarized, in the following five conventional equations: 

![Equations 1 to 5](images/naca-tn-2799/Equations1to5.png) 

Readers may recognize forms of equations 1 through 4 from [NACA-ARR-5G13]({filename}NACA-ARR-5G13.md) [^2]. 

I think that equation (5) is a wet adiabatic calculation 
that assumes water drop temperatures are in equilibrium 
with the air as they approach a surface, 
although I could not find it in "references 1 to 5". 
I guess that I am not completely up on the "five conventional equations".

> (The symbols used herein are given in the appendix.)
A solution of equation (1) requires the prior calculation of equations 
(2) to (5). Because of the dependence of ed on td and of e1
on t1 , equations (2) and (5) are both trial-and-error solutions. In
order to eliminate these laborious calculations, a single equation will
be derived containing only a minimum mImber of basic variables.

> In order to obtain a simplified relation using the preceeding eight terms; 
the following assumptions are made:  
(1) In the air flow over a body, temperatures and pressures change
adiabatically too quickly to permit any change in the state of entrained
moisture; the local-stream vapor pressure (as shown in reference 2) is
then given by  
![Equation 6](images/naca-tn-2799/Equation6.png) 

Reference 2 is NACA-ARR-5G13. It is an alternative Not the only scenario presented) 
that was considered to the 
assumption that the water drops are in equilibrium with the air as they approach an object. 
![Equation 7](images/naca-tn-2799/Equation7.png) 
Equation 7 is an incompressible approximation of Bernoulli's Law.

    p/rho + v**2/2 = pl/rhol +vl**2/2
    v**2/2 - vl**2/2 = pl/rhol - p/rho
    v**2 - vl**2 = 2 * (pl/rhol - p/rho)
    assume that rho ~= rhol
    v**2 - vl**2 = 2 / rho * (pl - p)
    vl**2 = v**2 - 2 / rho * (pl - p)
    vl**2 = v**2 - 2 p / rho * (pl/p - p/p)
    vl**2 = v**2 - 2 p / rho * (pl/p - 1)
    
    p/rho = R*T
    
    vl**2 = v**2 - 2 * R * T * (pl/p - 1)
    T = 464 R = 257.77 K
    
    
    
    (v**2/2 - vl**2/2) / (2*32.2*778*0.24) = R * T * (pl/p - 1) / (2*32.2*778*0.24)
    
    T = p/(rho*R)
    
    rho lb-s^2/ft^4  !!?? 
    
    lbm/ft^3 / (ft/s^2) = lbm-s^2/ft^4   

![Equations 8 and 9](images/naca-tn-2799/Equations8and9.png) 

![Equations 10 to 15](images/naca-tn-2799/Equations10to15.png) 

The text from Figure 1:

    Solutions:  q/ha = τ1 - τ2  + K(τ3 -τ4) + τ5, F
                 Mev = (hs K/1066)(τ3 - τ4), lb/(hr)(ft^2)
                     Abscissa         Sloping line
    τ1 = Intersection  Mw/ha    and     ts - to
    τ2 = Intersection  Mw/ha    and       vo
    τ3 = Intersection   pl      and       ts
    τ4 = Intersection   po      and       to
    τ5 = Intersection   pl      and       po
    Example:    
    Let:  
    ha = 50 Btu/(hr)(ft^2)(F)  
    Mw = 35 lb/(hr)(ft^2)  
    ts = 80 F 
    to = 20 F  
    vo = 700 ft/s  
    p0  = 12 in. Hg  
    pl  = 16 in. Hg 
    Then: 
    Mw/ha = 0.7  
        q = 50(102 - 41.4 - 179.5 - 23.5 - 6.8) =
            10,490 BTU/(hr)(ft^2)
      Mev = (50/1066)(179.5 - 23.5) = 
            7.32 lb/(hr)(ft^2)
            
    Figure 1. - Graphical solution of anti-icing heat and mass transfer from surface subject to impingement and heated above freezing.
    (A 17 1/2 x 22 inch print of this figure is attached.) 
    
Since there is a graphical solution, I guess there is no need for a python implementation :( 

Let us write the equations in (mostly) SI units:    

I will attempt to standardize (mostly) to the nomenclature of "Manual of Scaling Methods" [^2]. 

Description| symbol | Messinger symbol
---|---|---
air specific heat at constant pressure | cp | cp
unit system gravitation factor | gc = 1 kg-m/(N-s^2) | g, acceleration due to gravity, 32.2 ft/sec^2
heat transfer coefficient| hc| ha
ambient static pressure | p | p
mass flux rate of water (mass/unit_area/time) | mw | Mw
ambient water vapor pressure | pv | eo
surface water vapor pressure | pvs | el
recovery factor | r | R
ambient air static temperature| ta | to
surface temperature | ts | ts
latent heat of evaporation | Le | Le
latent heat of freezing | Lf | Lf
free stream airspeed | u | V

Calculations here will be in SI units, with the exceptions of:  
- LWC, g/m^3  
- drop diameter, micrometer   

A curious unit appears in the description of density:
![rho term](images/naca-tn-2799/term_rho.png) 

From the units on g:
![g term](images/naca-tn-2799/term_g.png) 

I infer that the mass in the density is the archaic unit "slug" in disguise
(see [A Brief Digression on Unit Systems]({filename}brief-digression-on-units.md)).  

    slug = 32.2 lbm / (32.2 ft/s^2) => lbm-s^2/ft units 
    (missing the unit system constant "gc")
    
    density = slug / vol = lbm-s^2/ft / (ft^3) = lbm-s^2/ft^4
    
So, the tau values become (in units K):  

    τ1 = (ts - ta) * (1 + wm * cpw / ha)    
    τ2 = u**2 / 2 * (r / cp + wm / ha)  
    τ3 = 0.7 * Le / cp * (pvs / pl)  
    τ4 = 0.7 * Le / cp * (pv / po)  
    τ5 = (1-r) * R_AIR * ta / (2 *cp) * (1 - pl / p)  [evaluated at 464R, 257.77K, r=0.85]  
    
    
The τ5 term is a dry approximation, as I do not want to unwind all of equation (5),
and, after Messinger's comments about the "datum" temperature, the literature will soon lose interest. 
The term is small, anyway.
    
##Conclusions  

>From 

##Citations

NACA-TN-2799 cites 12 publications:

- Neel, Carr B., Jr., Bergrun, Norman R., Jukoff, David, and Schlaff, Bernard A.: The Calculation of the Heat Required for Wing Thermal Ice Prevention in Specified Icing Conditions. NACA-TN-1472, 1947.  
- Hardy, J. K.: Kinetic Temperature of Wet Surfaces A Method of Calculating the Amount of Alcohol Required to Prevent Ice, and the Derivation of the Psychrometric Equation. NACA-ARR-5G13, 1945  
- Gelder, Thomas F., and Lewis, James P.: Comparison of Heat Transfer from Airfoil in Natural and Simulated Icing Conditions. NACA-TN-2480, 1951.  
- Gray, Vernon H., and Campbell, B. G.: A Method for Estimating Heat Requirements for Ice Prevention on Gas-Heated Hollow Propeller Blades. NACA-TN-1494, 1947.  
- Brunt, David: Physical and Dynamical Meteorology. Univ. Press (Cambridge), 2nd ed., 2nd reprint, Chap. III, 1944, pp. 49-68.  
- Boelter, L. M. K., Martinelli, R. C., Romie, F. E., and Morrin, E. H.: An Investigation of Aircraft Heaters, Part XVIII - A Design Manual for Exhaust Gas and Air Heat Exchangers. NACA-ARR-5A06, 1945.  
- Boelter, L. M. K., Grossman, L. M., Martinelli, R. C., and Morrin, E. H.: An Investigation of Aircraft Heaters, Part XIX - Comparison of Several Methods of Calculating Heat Losses from Airfoils. NACA-TN-1453, University of California, 1947.  
- Johnson, H. A., and Rubesin, M. W.: Aerodynamic Heating and Convective Heat Transfer - Summary of Literature Survey. Trans. ASME, vol. 71, no. 5, July 1949, pp. 447-456.  
- Frick, Charles W., Jr., and McCullough, George B.: A Method for Determining the Rate of Heat Transfer from a Wing or Streamline Body. NACA-WR-A-40, Dec. 1942.  
- Scherrer, Richard: The Effects of Aerodynamic Heating and Heat Transfer on the Surface Temperature of a Body of Revolution in Steady Supersonic Flight. NACA-TR-917, 1948. (Formerly NACA-TN-1300.)  
- Drexel, Roger E., and McAdams, William H.: Heat-Transfer Coefficients for Air Flowing in Round Tubes, In Rectangular Ducts, and around Finned Cylinders. NACA-ARR-4F28, 1945.  
- Lowdermilk, Warren H., and Grele, Milton D.: Influence of Tube-Entrance Configuration on Average Heat-Transfer Coefficients and Friction Factors for Air Flowing in an Inconel Tube. NACA-RM-E50E23, 1950.  

NACA-TN-1472 is cited once by publications in the NACA Icing Publications Database [^7]:

- Lewis, James P.: An Analytical Study of Heat Requirements for Icing Protection of Radomes. NACA-RM-E53A22, 1953.  

NACA-TN-1472 is cited 6 times in the literature [^8].

##Notes: 

[^1]: 
Gray, Vernon H.: Simple Graphical Solution of Heat Transfer and Evaporation from Surface Heated to Prevent Icing. NACA-TN-2799, 1952.  
[^2]: Hardy, J. K.: Kinetic Temperature of Wet Surfaces A Method of Calculating the Amount of Alcohol Required to Prevent Ice, and the Derivation of the Psychrometric Equation. NACA-ARR-5G13, 1945  

[https://github.com/icinganalysis/icinganalysis.github.io](https://github.com/icinganalysis/icinganalysis.github.io)  
[^7]: 
[NACA Icing Publications Database]({filename}naca icing publications database.md)  
[^8]: 
https://scholar.google.com/scholar?hl=en&as_sdt=0%2C48&q=Simple+Graphical+Solution+of+Heat+Transfer+and+Evaporation+from+Surface+Heated+to+Prevent+Icing&btnG=  
