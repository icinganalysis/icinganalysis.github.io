Title: A Brief Digression on Unit Systems  
Date: 2022-04-24 12:00  
Category: NACA  
tags: thermodynamics, about, diversions    

>_"I'm burning through the sky, yeah  
Two hundred degrees, that's why they call me Mister Fahrenheit  
I'm travelling at the speed of light  
I wanna make a supersonic woman of you"_  
from Queen, "Don't Stop Me Now"  

#A Brief Digression on Unit Systems

##Preferred units (primary SI units):

    mass: kg
    force: N
    length: m
    tk: temperature, K
    time: seconds, s
    p: air static pressure, Pa (N/m^2)
    u: free-stream air speed, m/s
    altitude: pressure altitude, m
    energy: J or N-m
##Icing specific, entrenched exceptions:  

    d_drop: water drop diameter, micrometer (1e-6 m)
    lwc: liquid water content, g/m^3
    

##A note about mass and force:  

To keep unit consistency in Newton's second law, a unit system constant "gc" is introduced.  

Force = mass * acceleration / gc

In SI units gc = 1 kg-m/(N-s^2)  
N = kg * m/s^2 / (kg-m/N-s^2) = N  

As the value is 1, gc might not be explicitly be included in calculations in SI units,
but it is always implicitly there.

In "US customary" units, gc = 32.174 lbm-ft/(lbf-s^2).  
It must be explicitly included in any calculation involving force, mass and acceleration. 
 
The archaic mass unit "slug" was sometimes used (1 slug = 32.174 lbm) to help "alleviate" this,
by making the gc value numerically 1, so if it is omitted it has no apparent effect.  

     gc = 1 slug-ft/lbf-s^2
     
However, I have seen errors of a factor of 32.174, regardless of whether slugs or lbm were used. 

Sometimes a unique unit appears, such as this from NACA-TN-2799:
    
    ⍴  density, (lb)(s^2)/ft^4

This is slug / ft^3, in disguise.    
    
See an excellent discussion about gc in "Fundamentals of Classical Thermodynamics", Van Wylen and Sonntag, Second Edition, John Wiley and Sons, 1973. 

##A note about thermal energy

In SI units, thermal energy and any other energy units are the same. 
For thermal energy, the Joule "J" is conventionally used. 
For mechanical energy, the unit N-m may be used, but it is, by definition, the same as a Joule. 

In "US customary" units, thermal energy is typically in BTU (British Thermal Units).  
To complicate matters, there is more than one BTU definition. 
See https://en.wikipedia.org/wiki/British_thermal_unit. 
Herein, the IT BTU is used.

    1 BTU = 778.16926 lbf-ft 
    
In the NACA publications, this is commonly rounded to 778.

