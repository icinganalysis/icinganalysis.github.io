title: The Effects of Humidity in Icing Wind Tunnel Tests   
Date: 2022-08-16 12:00  
category: icing tunnels  
tags: icing tunnel, python  

### _"a condition of supersaturation, which promotes the growth of frost deposits"_  

## Summary  
Supersaturated humidity can affect icing wind tunnel results.  

## Key Points  
1. Some observations of supersaturated humidity conditions were made in the NACA-era.  
2. Supersaturation was associated with frost on test article afterbodies.  
3. Recirculating icing wind tunnel conditions are calculated to tend to be supersaturated.  
4. Some potential effects of supersaturation are calculated.  

## A brief primer on humidity  

A measurement of water vapor in the air is humidity. 
Relative humidity is the most common measure. 
In everyday life 30% to 60% relative humidity is generally considered to be comfortable. 
Lower humidities feel dry, and higher humidities feel wet or "humid".

The most water vapor that can usually exist at a given static temperature is termed
"saturated", and that condition has 100% relative humidity. 
Given sufficient time and condensation surfaces, 
any surplus vapor above this value will condense as liquid water. 

Natural icing conditions tend to be near 100% relative humidity, 
and are often slightly "supersaturated", to say 102% or 105%. 
This is due to some complex physics of small water drops and surface tension
[some of which is discussed in ["Super-Cooled Water Droplets in Rising Currents of Cold Saturated Air"]({filename}Langmuir Rising Currents.md)]. 

The rapidly changing conditions in the flow circuit of an icing wind tunnel 
can lead to significantly supersaturated conditions in the test section 
(much greater than 100% relative humidity). 
Some icing wind tunnels do not have direct control over humidity, 
and some do not routinely measure humidity. 

Supersaturation may be challenging to measure in an icing wind tunnel, 
as some instruments do not indicate values above 100% relative humidity, 
and readings may be affected by the impingement of water drops.

## Discussion

Three NACA publications mention supersaturated conditions in an icing wind tunnel. 

### Supersaturated icing wind tunnel conditions

I found four publications that mentioned the humidity in the NACA-era IRT. 
Three of the four described it at supersaturated, and note the effect on frost formations. 
None of the four described if the humidity was measured, inferred, or assumed. 
(I have measured supersaturated humidity levels in an icing wind tunnel, 
and have observed the frost on afterbodies.)

#### NACA-RM-E50I08 [^1]  

[Emphasis added]  
>A calibration of the water content of the tunnel air was made just
upstream of the vane duct for the range of air temperatures. The variation 
in liquid-water content is shown in figure 3 as measured by standard 
rotating-cylinder technique when the water flow through the nozzles
was held constant and the air temperature varied. __The air was saturated
at all temperatures prior to sprays__ and the velocity was constant;
therefore, the liquid-water content should also have been approximately
constant.  
![Figure 3. Variation of indicated liquid-water content with air total 
temperature for constant spray water input. Air velocity, 280 miles per hour; 
mean droplet diameter, 10-15 microns.](images/naca-rm-e50i08/Figure 3.png)  

I infer from "The air was saturated at all temperatures prior to sprays" 
that some effort was made to achieve saturated conditions. 

#### NACA-RM-E53C27 [^2]
[Emphasis added]  
>In figure 4(b) runback deposits have begun to collect directly impinging 
droplets and are growing forward and outward. The deposits aft of the heated
forward section are caused by impingement upon frost particles. The airfoil 
invariably frosted as soon as water sprays began, __probably because
of air-stream turbulence and supersaturation of the tunnel air, which is
not the usual case in flight__.  
![Figure 4b. Characteristic ice deposits with mariginal operation of de-icing system.
> ](images/naca-rm-e53c27/Figure 4b.png)  


#### [NACA-TN-2962]({filename}NACA-TN-2962.md) [^3]  
>For studies of the effect of afterbody frost formations on the drag
of the airfoil, no heat was furnished to the afterbody. Frost formed on
the afterbody because of air-stream turbulence and the supersaturated
condition of the tunnel air.  

[Emphasis added]  
>The afterbody __frost formations obtained in icing tunnels are
believed to be caused by turbulence of the air stream, which deposits
minute droplets on the surfaces, and by a condition of supersaturation,
which promotes the growth of frost deposits__. The initial frost deposit
on an afterbody appears immediately upon starting a spray cloud through
the tunnel and takes the form of a latticework of pinhead size crystalline 
deposits on both upper and lower surfaces of the airfoil
(fig. 26(a)). As the frost formation increases in size with time in the
icing condition, water droplets begin to impinge directly on the frost
pinnacles (fig. 26(b)). The deposition of droplets on the frost pinnacles 
causes small featherlike formations composed of ice and frost
particles to grow forward into the air stream (fig. 26(c)). These
feathers increase in size and may reach a length of several inches and
protrude as much as 1 inch in a direction normal to the air stream
(fig. 26(d)).  
![Figure 26. Typical frost formation and growth on airfoil afterbody.
> ](images/naca-tn-2962/Figure 26.png)  

#### NACA-RM-E53E07 [^4]  
[Emphasis added]  
>Photographs of ice on the ram inlet and the carburetor screen at
the end of the icing periods are shown in figure 6. At the higher
liquid-water-content condition (fig. 6(a)), a rough-glaze-ice formation
which built outward from the inlet was obtained on the rain-Inlet lips.
Little or no ice was observed inside the rain duct. Downstream of the
ram inlet, almost the entire scoop including the alternate-inlet ramp
was covered by a frost-like formation. __This frost icing is believed to
result from a combination of super saturation in the tunnel__ and turbulent 
deposit of small drops caused by the presence of rough ice formations 
on the ram-inlet lips.  
![Figure 6. Ice formed on ram inlet and carburetor screen at two icing conditions. 
Airspeed, 180 miles per hour; tunnel-air total temperature, 25 F; angle of attack, 
0 degree; initial mass-flow ratio, 0.35.](images/naca-rm-e53e07/Figure 6.png)  

### Water vapor analysis of an icing wind tunnel  

In the review ["The AEDC 1-Dimensional Multi-Phase code (AEDC1DMP) and the iads1dmp"]({filename}aedc1dmp.md) 
the water spray drop evaporation was calculated, 
as well as the amount of vapor in the tunnel flow. 

For that case, the tunnel modeled was assumed to have control over the humidity. 

For cases of recirculating flow icing wind tunnels without humidity control, 
the flow in the constant area section upstream of the contraction into the test section
tends to have 100% relative humidity (see [^5]). 
The flow then goes through the contraction into the test section. 
The static temperature lowers, but the vapor does not have time 
condense out to equilibrium, so the relative humidity climbs. 

Two test conditions from NACA-TN-2962 were modeled with the iads1dmp.py program, 
as shown below. 
The water drop size was listed at "10 to 16" micrometers, so I just picked 15 micrometer.
The test airspeed for each was 180 MPH (about 80 m/s). 

I used the example icing wind tunnel dimensions in [^6]. 
The facility is not named, but it is of comparable size (but not identical) to the IRT. 

At the 180 MPH airspeed, the test section relative humidity is calculated to be about 120%. 
Higher airspeeds were also considered. 
At higher airspeeds, the relative humidity can be much higher.  

![Calculated humidity values](images/naca-tn-2962/naca_tn_2962_humidity_compare_rhs.png)  

### Ice shape analysis with LEWICE2D [^7]  

Humidity has some effect on the calculated heat and mass balance in icing calculations. 
[However, note that vapor pressure or humidity was specifically omitted from
[Bilanin's Pi Terms]({filename}bilanin_pi_terms.md)].

I do not know of a test where different humidity levels were used to 
measure the effects on ice shapes. 

We will use LEWICE2D to calculate some different ice shapes at different relative humidities. 
LEWICE2D does not predict the formation of frost on the afterbody due to supersaturation 
(the program was not intended to do so), 
but it does predict differences in the main, leading edge region ice shape.

I selected the case from NACA-TN-2962 Figure 27 at T_total = 25F for comparisons.
This had an 8-foot chord 65<sub>1</sub>-212 airfoil at 5 degrees angle of attack. 
This test did not report an unheated ice shape for this specific condition. 
It did include "General types of primary ice" in Figure 2. 
The conditions selected here are probably closest to case (c):

![Figure 2 of NACA-TN-2962. General types of primary icing observed on airfoil leading edge.
](images/naca-tn-2962/Figure 2.png)   

At the nominal airspeed of 180 MPH, 
the effect of supersaturation on the ice shape as calculated by
LEWICE2D is small.

![Ice at 180 MPH and T_total=25F.](images/naca-tn-2962/naca_tn_2962_humidity_lewice_180mph.png)  

At the 350 MPH, 
the effect of supersaturation on the ice shape is small, 
but more readily discernible than for the 180 MPH case. 

![Ice at 350 MPH and T_total=25F.](images/naca-tn-2962/naca_tn_2962_humidity_lewice_350mph.png)  

It we analyze at higher total temperatures, ice is still predicted 
(but only about 1 mm ice thickness for this 20 minute long exposure)
(I have observed ice formation at total air temperatures greater than 0C in an icing wind tunnel). 

![Ice at 180 MPH and T_total=34F.](images/naca-tn-2962/naca_tn_2962_humidity_lewice_4_5c_180mph.png)  

At the higher airspeed, ice is predicted to form at a rather warm total air temperature of 40F 
(I have not observed ice formation at total air temperatures as warm as 40F in an icing wind tunnel). 
There is a notable difference between the ice shape at 100% relative humidity and the calculated 213% relative humidity
(the ice shape at 213% relative humidity is barely visible, even on an expanded plot). 

![Ice at 350 MPH and T_total=40F.](images/naca-tn-2962/naca_tn_2962_humidity_lewice_4_5c_350mph.png)  

In most cases the effect of supersaturation is small. 
However, if one is attempting to demonstrate the presence or absence of ice
at temperature near the maximum for ice formation, 
a case such as the one above may not give a completely accurate answer in an icing wind tunnel,
as the relative humidity is different than the assumed 100%.

## Conclusions  

The observations of supersaturated conditions in the NACA-era IRT 
(however that was determined)
are supported by more recent analysis and test measurements. 

As many test facilities cannot control humidity, 
icing wind tunnel users should consider measuring test section humidity during tests. 
An instrument that is capable of reading above 100% relative humidity or the 
saturated vapor pressure should be used (some instruments are not capable).

Analysis methods that can use humidity values above 100% should be used 
for comparison to icing wind tunnel test results 
(some can only use 100% relative humidity).

If humidity cannot be measured during a test, 
analysis methods such as the AEDC1DMP and the iads1dmp.py can be used. 

Some tests, 
such as determining the maximum temperature for ice accumulation, 
and determining the absence or presence of ice near the maximum temperature, 
may be particularly sensitive to the effects of test section humidity. 

## Notes

[^1]: Gray, Vernon H., and Bowden, Dean T.: Icing Characteristics and Anti-Icing Heat Requirements for Hollow and Internally Modified Gas-Heated Inlet Guide Vanes. NACA-RM-E50I08, 1950.  
[^2]: Gray, Vernon H., and von Glahn, Uwe H.: Effect of Ice and Frost Formations on Drag of NACA 65<sub>1</sub>-212 Airfoil for Various Modes of Thermal Ice Protection. NACA-TN-2962, 1953 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19810068586).    
[^3]: Gray, Vernon H., and Bowden, Dean T.: Comparison of Several Methods of Cyclic De-Icing of a Gas-Heated Airfoil. NACA-RM-E53C27, 1953. [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19810068601)  
[^4]: Lewis, James P.: Investigation of Aerodynamic and Icing Characteristics of Flush Alternate-Inlet Induction-Systems Air Scoop. NACA-RM-E53E07, 1953.  
[^5]: Cook, Donald E.: Maximum Temperature for Ice Accumulation Calculations. AIAA-2005-655, January, 2005.   
[^6]: 
Schulz, R. J.: Second Report for Research and Modeling of Water Particles in Adverse Weather Simulation Facilities. TASK REPORT 97-03, AEDC, July, 1998, [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA364922.pdf)  
[^7]: 
[software.nasa.gov](https://software.nasa.gov/software/LEW-18573-1), [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19990021235)    

