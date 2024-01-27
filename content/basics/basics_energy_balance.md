Title: Energy Balance "Standard Computational Model"    
header: The Basics: Intermediate Topics  
Date: 2024-01-28 12:00  
tags: intermediate topics, thermodynamics   
status: draft  
rights: CC-BY-NC-SA 4.0  

The "Aircraft Icing Handbook", DOT/FAA/CT-88/8-1, defines a "standard computational model" for the ice accretion process.  

Note that the relevant sections in DOT/FAA/CT-88/8-1, 1991 [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf) 
were affected by the perhaps little known update in 1993: [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA276499.pdf).  

Several errors and omissions were corrected in the update, so it is essential to consult the update. 
As the update only include certain affected pages, it makes it difficult to read this section 
as there is much interruption paging back and forth between sources. 
Here, the two sources are merged for easier reading. 
The cited references are also noted inline here. 

Note that the equation figures have AltText that may aid all readers, 
as the online digital reproductions are of poor quality in some cases. 

The term "standard computational model" has not seen wide use. 
Most recent literature refers to the "Messinger Model" or "Modified Messinger Model". 
That may or may not mean the "standard computational model" presented here. 
As noted below for calculating evaporation:  
>There are a variety of formulations of this term.  

That could also apply to several of the terms in the model.  

The "merged text" section below is from DOT/FAA/CT-88/8-1, 
but I have not used the usual quote block formatting to make it more readable.

### The merged text  

2.2.2.4 Physical Modeling of Ice Accretion Process  
 
The physical modeling of aircraft icing consists of (1) the modeling of the trajectories and
impingement of the supercooled water droplets and (2) the modeling of the behavior of the liquid
water formerly in the droplets once it is on a surface of the aircraft. Part (1) has been presented
above; the basic assumptions and equations go back to reference 2-2 and are widely accepted;
discussion centers on the formulation of numerical procedures. Part (2), which will now be discussed,
remains controversial. There exists what might be called a "standard computational model" which is
incorporated in various forms in a number of computer codes, the most widely used of which is
probably LEWICE (reference 2-39), developed under the direction of NASA Lewis Research Center.
 
However, a number of questions have been raised as to how accurately this model actually depicts the
surface behavior of the liquid water. NASA-Lewis (reference 2-40) has initiated efforts to "formulate
either changes to the existing model or an alternate model in order to see if ice shape predictions can
be improved." (However, LEWICE can presently give useful ice shape predictions for a fairly wide
range of conditions when used in conjunction with an appropriate roughness correlation; see the
discussion in Chapter IV, Section 2.) This section begins with a presentation of the standard
computational model; this is followed by a brief survey of the major criticisms of that model.  

The standard model assumes that if air temperature is not low enough for impinging droplets to
freeze upon impact, then the droplets are absorbed into a thin water film which flows away from the
stagnation line (or point). As it flows, it is cooled mainly by convection to the airstream until it
freezes, thus gradually changing the surface shape.  

This model is formulated computationally by dividing the airfoil surface into segments, and
associating a control volume with each segment. The water entering a control volume has two sources:
(1) water droplets impinging on the surface segment; (2) water "running back" from an adjacent
control volume closer to the stagnation point. (This "run back" water consists of all water which
entered the adjacent control volume but did not freeze.) An energy balance analysis is applied to each
control volume to determine the freezing fraction n, the fraction of the incoming water which freezes
for that control volume. If n = 1, then all incoming water freezes. If n < 1, then a fraction 1-n does
not freeze. This water will in turn run back into the adjacent control volume further away from the
stagnation point.  

The mass and energy balance analyses for a given control volume will now be presented in some
detail. The energy balance analysis was given its classic formulation by Messinger (reference 2-41),
whose work drew on earlier work by Tribus (reference 2-42). The presentation and notation used
here is based on reference 2-43.  

The mass balance for a control volume on the surface can be formulated as follows (figure 2-73).  

![Figure 2-73. Control volume mass balance for an ice surface.](/images%2FFAA%20Handbook%20volume%201%2FFigure%202-73.png)  

Let M"Imp denote the mass flux per unit time due to impinging water droplets,
M"Run in and M"Run out denote mass flow per unit area per unit time into and out of the control
volume due to liquid run back, and M"ice denote the mass of ice formed per unit area per unit time.
Then the mass balance for the control volume is:  
![Equation 2-33 corrected. M"Ice = M"Ice + M"Runin - M"Runout - M"Evap](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-33%20corrected.png)   

The term M"Imp is given by:  
![Equation 2-34. M"Imp = V∞ LWC β](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-34.png)  
V∞ is the freestream velocity. However, if the local velocity at the edge of the boundary layer is
available, that velocity should be used rather than the freestream velocity. This procedure is followed,
for example, in the ice accretion code LEWICE. β is the local collection efficiency for the control
volume.  

It is convenient to define a term M"Incoming by:  
![Equation 2-35. M"Incoming = M"Imp + M"Runin](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-35.png)  
Then the freezing fraction n for the control volume is defined by:  
![Equation 2-36. n = M"Ice / M"Incoming](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-36.png)  
where M"ice is the incoming mass which freezes.  

The energy balance for a control volume on the surface can be formulated as follows (figure 2-74).  
 ![Figure 2-74. Modes of energy transfer for an accreting ice surface.](/images%2FFAA%20Handbook%20volume%201%2FFigure%202-74.png)  

First, the main heat source terms (those that release heat into the control volume) are given.  

Let Q"Freeze denote the freezing of the incoming water. Then  
![Equation 2-37. Q"Freeze = n M"Incoming Lf](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-37.png)  
where Lf is the heat of fusion.

Let Q"AeroHeat denote the aerodynamic heating. Then  
![Equation 2-38. Q"AeroHeat = hc rc V∞^2 / (2 CpAir)](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-38.png)  
where hc is the local heat transfer coefficient, rc is a recovery factor, and CpAir
is the specific heat of air.  

Let Q"DropletK.E. denote the kinetic energy of the incoming droplets. Then:
![Equation 2-39. Q"DropletKE = M"Imp V∞^2 / 2](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-39.png)  

Let Q"IceCool denote the cooling of the ice to the surface temperature TSurf. Then  
![Equation 2-40. Q"IceCool = n M"ice (Tf - Tsurf)](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-40.png)  
where Tf is the ice/water equilibrium temperature (32 F). Note that if n < 1, TSurf = Tf and so this term equals 0.

Define Q"Source by:  
![Equation 2-41. Q"Source = Q"Freeze + Q"AeroHeat + Q"DropletKE + Q"IceCool](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-41.png)  

Next, the main heat sink terms (those that remove heat from the control volume) are given.

Let Q"conv denote the convective cooling term. Then  
![Equation 2-42. Q"Conv = hc (Tsurf - T∞)](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-42.png)  
where T∞ is the freestream temperature. If the local temperature at the edge of the boundary layer
is available, that temperature should be used in this term rather than the freestream temperature. This
is also done in LEWICE.  

Note: The term Q"Conv is often defined by  
![Equation 42b. Q"Conv = hc (Tsurf - Tr)](/images%2FFAA%20Handbook%20volume%201%2FEquation%2042b.png)  
where the "recovery temperature" Tr is given by  
![Equation 42c. Tr = T∞ + hc rc V∞^2 / (2 CpAir)](/images%2FFAA%20Handbook%20volume%201%2FEquation%2042c.png)  
In this formulation the term Q"AeroHeat is omitted from equation (2-41). In subsequent calculations
in this section, Q"AeroHeat is retained and equation (2-42) is used to calculate Q"Conv.  

Let Q"DropWarm denote the droplet warming term. Then  
![Equation 2-43. Q"DropWarm = M"Imp Cw (TSurf - T∞)](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-43.png)  
where Cw is the specific heat of water.  

Let Q"Evap denote the heat loss due to evaporation. There are a variety of formulations of this
term. The approach used here is based on reference 2-44 and 2-U1 and employs the form of the Reynolds analogy. 

M"Evap is given by  
![Equation 2-44. M"Evap = g ΔB](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-44.png)  
where g is the mass transfer coefficient and ΔB is the evaporative driving potential dependent on the
vapor concentration difference between the surface and the edge of the boundary layer.
These quantities are given by:  
![Equation 2-45. g = hc / CpAir (Pr/Sc)^0.667](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-45.png)  
![Equation 2-46. ΔB = B1 / B2](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-46.png)  
![Equation 2-47a. B1 = PV,Surf / TSurf - (Po / P∞) (Pv,∞ / Ts)](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-47a.png)  
![Equation 2-47b. B2 = 1/ 0.0622 (Po / To) - (PV,Surf / TSurf)](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-47b.png)  
The Prandtl number Pr, Schmidt number Sc, and specific heat of air Cp air should be evaluated at the
film temperature (To + Tsurf)/2. PV,surf is the vapor pressure at the surface and Pv,∞ is the free
stream vapor pressure. The equations assume that Po and To the free stream pressure and temperature
at the edge of the boundary layer are available; if they are not, the corresponding freestream values
are used. 0.622 is the ratio of the molecular weight of water to that of dry air. The heat loss due to
evaporation is now given by:  
![Equation 2-48. Q"evap = M"Evap Lv](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-48.png)  
Lv is the heat of vaporization.  

If the freezing fraction is equal to 1 and the surface temperature Tsurf is to be computed, then
Q"Evap should be replaced by the heat loss due to sublimation, denoted by Q"Subl. This is given by  
![Equation 2-49. Q"Subl = M"Subl Ls](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-49.png)  
where M"Subl denotes the mass flux due to sublimation per unit time and Ls denotes the heat of
sublimation. In some programs, M"Subl is computed using the same formulas as M"Evap. 

Define Q"Sink by:  
![Equation 2-50. Q"Sink = Q"conv + Q"DropWarm + Q"Evap](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-50.png)  

The energy balance equation is:  
![Equation 2-51. Q"Source + Q"Sink = 0](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-51.png)  

The control volume freezing fraction is calculated as follows: Assume that the equilibrium
temperature, Tsurf, is Tf. With this assumption, all quantities in the energy balance except n can be
evaluated. Now solve for n. If the calculation yields a value of n between 0 and 1 inclusive, the
calculation is complete. If n is calculated to be larger than 1, assume that n = 1 and that the excess
over 1 was because Tsurf is actually smaller than Tf. So set n equal to 1 in the energy balance
equation, which is now solved iteratively (since several quantities depend on Tsurf) for Tsurf. If n
is calculated to be smaller than 0, similar reasoning leads to setting n equal to 0 and solving iteratively
for Tsurf, which will now be larger than Tf.  

A major source of uncertainty in calculating n using this equation arises from the uncertainty in
the computation of the heat transfer coefficient h. If n is calculated in the stagnation region of a
cylinder, it is common to use the heat transfer correlation for a smooth cylinder (given, for example,
in reference 2-45).  

If n is to be calculated in the stagnation region of an airfoil, the same correlation
is sometimes used with radius equal to the radius of curvature of the airfoil. As the ice accretes, the
shape changes and the surface roughness also changes, perhaps increasing dramatically. This can have
a profound effect on the heat transfer coefficient.   

Airfoil ice accretion codes must include an algorithm to calculate the heat transfer coefficient
over the entire airfoil (See Chapter IV, Section 2). If it is a time-stepping code such as LEWICE, it
must be able to calculate the heat transfer coefficient for an iced airfoil. An integral boundary layer
method is typically used (See references 2-39 and 2-46). These methods generally include roughness
terms, but a standard method for describing ice roughness has not yet been developed. NASA Lewis
has conducted experiments to determine heat transfer coefficient distributions for ice shapes
(references 2-47, 2-48). This data is essential to evaluate heat transfer coefficient algorithms. it
appears that all existing algorithms introduce substantial uncertainty into the calculation.  

[See the original for the rest of the text.]

## References  

2-2 Langmuir. I. and Blodgett, K., "A Mathematical Investigation of Water Droplet Trajectories," AAFTR 5418, February 1946. [books.google.com](https://books.google.com/books?hl=en&lr=&id=mJySYM32cHUC&oi=fnd&pg=PA11&dq=Katherine+Blodgett+icing&ots=QYP5gFyEiz&sig=djzAHtpIZuT_OlbopRsNYyUhUdc#v=onepage&q=Katherine%20Blodgett%20icing&f=false)   

2-39 Ruff, G. A. and Berkowitz, B. M., "Users Manual for the NASA Lewis Ice Accretion Prediction Code (LEWICE)," NASA CR 185129. [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19900011627)  

2-40 Shaw, R. J., "NASA's Aircraft Icing Analysis Program," NASA TM 88791, Sept. 1986. [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19920013862)  

2-41 Messinger, B. L., "Equilibrium Temperature ef an Unheated Surface as a Function of Airspeed," Journal of Aeronautical Sciences, January 1953 (Vol. 20, No. 1). [arc.aiaa.org](https://arc.aiaa.org/doi/10.2514/8.2520) [payment or institutional access required]  

2-42 Tribus, M.V., et. al., "Analysis of Heat Transfer over a Small Cylinder in Icing Conditions on Mount Washington," American Society of Mechanical Engineers Transactions, Vol. 70, 1949, pp. 871-876. [asme.org](https://asmedigitalcollection.asme.org/fluidsengineering/article-abstract/70/8/971/1152987/Analysis-of-Heat-Transfer-Over-a-Small-Cylinder-in?redirectedFrom=fulltext) [payment or institutional access required]    

2-43 "An experimental and theoretical study of the ice accretion process during artificial and natural icing conditions" DOT/FAA/CT-87/17 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19880011759)  

2-44 Analysis and Verification of the Icing Scaling Equations [AEDC-TR-85-30 Vol. 1 (Revised)](https://apps.dtic.mil/sti/tr/pdf/ADA167976.pdf)  

2-45 Kreith, F., Principles of Heat Transfer, Intext Educational Publishers, New York, 1973, third edition [archive.org](https://archive.org/details/principlesofheat0000krei_n7j4) [online borrowing with registration]  

2-U1 Sogin, H. H., "A Design Manual for Thermal Anti-icing Systems". ADC Technical Report 54-313, Dec. 1954. [ntrl.ntis.gov](https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/AD090156.xhtml)    

2-46 Makkonen, L., "Heat Transfer and Icing of a Rough Cylinder," Cold Regions Science Vol. 10, 1985, pp. 105-116. [cambridge.org](https://www.cambridge.org/core/journals/annals-of-glaciology/article/effect-of-roughness-on-the-rate-of-ice-accretion-on-a-cylinder/B110D4683F3D3AE616A0D2ADB70076FB)  

2-47 Van Fossen, G. J.; Simoneau, R. J.; Olsen, W. A.; and Shaw, R. J., "Heat Transfer
Distributions around Nominal Ice Accretion Shapes Formed on a Cylinder in the NASA
Lewis Icing Research Tunnel," NASA TM 83557, Jan. 1984. [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19840006395)  

2-48 Poinsatte, P. E.; Van Fowsen, G. J.; and DeWitt, K. J., "Convective Heat Transfer
Measurements from a NACA 0012 Airfoil in Flight and in the NASA Lewis Icing
Research Tunnel," NASA TM 102448, Jan. 1990. [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19900004434)  
