Title: Bilanin Pi Terms  
status: draft  

###_"An unfortunate fact is that if proposed additional scaling parameters prove to be what is required to conduct improved subscale tests, icing wind tunnel subscale tests are likely to be even more restrictive."_  


```text

Primary Units
L            length
M            mass
τ            time
Temperature  T
angle        radian

Note that force can be expressed as
F ∝ M L / τ^2 


Table 1 

           Description                  Units
Lengths
δi      ice thickness                   L
d       drop diameter                   L
ℓ       mean distance between drops     L
C       chord                           L
s       surface distance along airfoil  L

Densities
ρa      air                             M / L^3
ρw      water                           M / L^3
ρi      ice                             M / L^3

Viscosity
νa      air                             L^2 / τ
νw      water                           L^2 / τ

Thermal
ka      thermal conductivity air        M L / (τ^3 T)
kw      thermal conductivity water      M L / (τ^3 T)
ki      thermal conductivity ice        M L / (τ^3 T)
Cpa     specific heat air               M L / (τ^2 T)
Cpa     specific heat water             M L / (τ^2 T)
Cpa     specific heat ice               M L / (τ^2 T)
hfs     latent heat of fusion           M L / τ^2
Ta      air temperature                 T
Tf      freezing temperature            T

Surface tension
σw/a    water/air                       M / τ^2
γ       contact angle                   radian *

Velocity
U∞      air speed                       M / τ


* original had M / τ^2

```

Pi terms

δ<sub>i</sub> / c = f(π1, ..., π18)  

π1 = τ U<sub>∞</sub> / C  

π2 = s / C  

π3 = d / C

π4 = d / ℓ  

π5 = ρ<sub>a</sub> / ρ<sub>w</sub>  

π6 = ρ<sub>i</sub> / ρ<sub>w</sub>  

π7 = Cp<sub>a</sub> / Cp<sub>w</sub>

π8 = Cp<sub>w</sub> / Cp<sub>i</sub>    
  
π9 = k<sub>a</sub> / k<sub>w</sub>  

π10 = k<sub>w</sub> / k<sub>i</sub>  

π11 = ν<sub>a</sub> / ν<sub>w</sub>  

π12 = γ  

π13 = Cp<sub>a</sub> ρ<sub>a</sub> ν<sub>a</sub> / k<sub>w</sub>  

π14 = T<sub>f</sub> / T<sub>a</sub>

π15 = h<sub>fs</sub> / (Cp<sub>a</sub> T<sub>a</sub>)

π16 = U<sub>∞</sub><sup>2</sup> / (Cp<sub>a</sub> T<sub>a</sub>)  

π17 = U<sub>∞</sub> C / ν<sub>a</sub>  

π18 = ρ<sub>a</sub> U<sub>∞</sub><sup>2</sup> C / σ<sub>w/a</sub>


Proposed additions:  

π19 = p<sub>vapor</sub> / p<subs>a</sub>

π20 = p<sub>vapor at freezing</sub> / p<sub>vapor</sub>

Where:  
p<sub>vapor</sub> is vapor pressure at ambient temperature  
p<sub>vapor at freezing</sub> is vapor pressure at the freezing (melting) temperature  


"While aircraft size and speed have increased, tunnel facilities have not, 
thus making subscale geometric tests a necessity"



>The difficulty of conducting full-scale icing tests has long been appreciated. 
Testing in an icing wind tunnel has been undertaken for decades. 
While aircraft size and speed have increased, tunnel facilities have not, making subscale geometric tests a necessity. 
Scaling laws governing these tests are almost exclusively based on analysis
performed over 30 years ago and have not been rigorously validated. 
The following work reviews past scaling and suggests revision to these analyses based on recent experimental observation. 
It is also suggested, based on the analysis contained herein, 
that current ice accretion predictive technologies, as LEWICE, 
when utilized in the glaze ice accretion regime, 
may need upgrading to more accurately estimate the rate of ice buildup on aerodynamic surfaces.


Here is a subset of the Pi terms (see the paper for the full set).


```text
Primary Units
L            length
M            mass
τ            time
Temperature  T

Note that force can be expressed as
F ∝ M L / τ^2 

Table 1 (omitting substance properties)

           Description                  Units
Lengths
δi      ice thickness                   L
d       drop diameter                   L
ℓ       mean distance between drops     L
C       chord                           L
s       surface distance along airfoil  L

Densities
ρa      air                             M / L^3

Viscosity
νa      air                             L^2 / τ
νw      water                           L^2 / τ

Thermal
Cpa     specific heat air               M L / (τ^2 T)
hfs     latent heat of fusion           M L / τ^2
Ta      air temperature                 T
Tf      freezing temperature            T

Surface tension
σw/a    water/air                       M / τ^2

Velocity
U∞      air speed                       M / τ
```


Pi terms

(substance properties omitted)

δ<sub>i</sub> / c = f(π1, ..., π18)  

π1 = τ U<sub>∞</sub> / C  

π2 = s / C  

π3 = d / C

π4 = d / ℓ  

π14 = T<sub>f</sub> / T<sub>a</sub>

π15 = h<sub>fs</sub> / (Cp<sub>a</sub> T<sub>a</sub>)

π16 = U<sub>∞</sub><sup>2</sup> / (Cp<sub>a</sub> T<sub>a</sub>)  

π17 = U<sub>∞</sub> C / ν<sub>a</sub>  

π18 = ρ<sub>a</sub> U<sub>∞</sub><sup>2</sup> C / σ<sub>w/a</sub>


>The next three parameters π16 through π18 result that the free stream velocity vary as:  
 
>>U<sub>∞</sub> ~ const, U<sub>∞</sub> ~ 1/C, U<sub>∞</sub> ~ 1/sqrt(C)

>respectively, in an attempt to keep the Mach,
Reynolds and Weber numbers constant between 
tests. Obviously, this is not possible and not 
surprisingly __the π method has failed to provide a 
scaling methodology which can be used to test 
subscale aerodynamic components__. 

[Emphasis added.]

>This, however, does not preclude seeking 
approximate scaling methodologies which is the 
subject of the discussion that follows.  


There is a review of scaling methods, similar to that in [AEDC-TR-83-30]({filename}AEDC-TR-83-30.md),
defining A<sub>c</sub>, Φ, Θ, b, and n in slightly different forms:  

>The freezing fraction n is defined as the mass freezing/mass water incoming. 
Note that Eq. (4) is nondimensional, __exact__


>>d(δ<sub>i</sub>/C) / d(τ U<sub>∞</sub>/C) = LWC β n / ρ<sub>i</sub> &nbsp;&nbsp;&nbsp;&nbsp; (4)

>and __scaled ice accretion exactly requires__ that  

>>LWC β / ρ<sub>i</sub> τ U<sub>∞</sub> / C = A<sub>c</sub> n = constant

>or that A<sub>c</sub>, the accumulation parameter, and n
each be held constant which is what is normally attempted. 

[Emphasis in the original]


>The freezing fraction has been computed by several investigators using a
model propoosed by Messinger in 1951 (Ref. 11). If
evaporation is neglected in this model...  

[Eq. 5 not included herein]

[this results in] the functional form of freezing fraction used in the SIMICE code 
(Ref. 12). 

Later it is noted that the freezing fractions determined by SIMICE are much lower than those
determined experimentally, and this is not surprising, as evaporation was neglected. 

>Obviously, something is very wrong here, since at 
the lower freezing fractions differs from the measured value 
by a factor of 2.3. The problem is that the 
freezing fraction n in Equ. 5 is not being 
computed sufficiently accurately using the
Messinger formulation. 

This may be why I have not been able to find the SIMICE code.  






After a quick review of scaling methods, similar to that in [AEDC-TR-83-30]({filename}AEDC-TR-83-30.md), 
it is stated:  
>__It is again emphasised that if Ac and n are accurately computed analytically and
held constant between two tests, the prediction of 
ice accreation and scaling of the tests__ is a proven technology.  

[Emphasis in the original]



A "zeroth-order expansion" analysis in distance from the stagnation
point is performed, resulting in 

>At 200 ft/sec, the film thickness on a cylinder with 
2R = 1 inches is estimated to be 
δ<sub>w</sub>(o) ~ 0.001 inches or about 25 μm which is 
nearly the diameter of the drop impacting the surface. 

>The above analysis, while admittedly
approximate, does confirm that a thin film is 
anticipated over the ice when conditions of low 
freezing fraction are anticipated. These films
may modify the freezing fraction as described by 
Messinger in a very direct way by providing
surface roughness which will augment the heat
transfer, as well as provide thermal resistance 
through which the latent heat of fusion must pass. 
Also, splach back from this layer cannot be
ruled out. It should be noted that the Weber 
number, based on dynamic air pressure for a layer 
of this thickness, is of the order of 10<sup>2</sup> which 
suggests that the stripping of this film by the 
airstream may also occur.  


> It is significant to note at this time that 
Olsen (Ref. 20) has photographed the microphysics
of accretion at a stagnation point, and had
confirmed the presence of liquid and run back at 
the stagnation region. This work, however, 
indicates that liquid beading is also observed 
indicating that the surface tension neglected in the
above analysis plays an important role. While
from the photographs it is difficult to estimate
the height of the droplets, it is clear that when
surface tension is acting, the film thickness
estimates are low and perhaps an effective droplet
height at least an order of magnitude larger can 
be argued. This liquid roughness, and upon 
freezing, ice roughness is known to greatly affect 
the local convection heat transfer rate (Ref. 21). 
Detailed obeservations of the stagnation 
region have recently been made by Hansman et al. 
(Ref. 22) and are discussed at this meeting. 


There is an interesting reformation of Messinger's freezing fraction equation:  

n = (dM<sub>i</sub> / dt) / (LWC U<sub>∞</sub>d<sup>2</sup>)
= (Cp<sub>w</sub> (T<sub>∞</sub> - T<sub>f</sub>) / h<sub>fs</sub>) - q<sub>am</sub> / (h<sub>fs</sub> LWC U<sub>∞</sub>d<sup>2</sup>) + Cp<sub>w</sub> (1-n) δ<sub>w</sub>q<sub>am</sub> / (2 h<sub>fs</sub> k<sub>w</sub> d<sup>2</sup>)

>The first two terms are the freezing fraction as
described by Messinger. The last term which is 
proportional to the film thickness reduces the 
freezing fraction as a consequence of the presence 
of the film. 

##Conclusions

>It is argued that improve ice accretion scaling may require a better match in Reynolds 
Number and more accurate consideration of the physics of water film and droplet dynamics on the 
airfoil surface. Additional scaling parameters are proposed which require that the surface tension 
phenomenon be more accurately accounted for in wind tunnel tests. An unfortunate fact is that if 
proposed additional scaling parameters prove to be what is required to conduct improved subscale tests, 
icing wind tunnel subscale tests are likely to be even more restrictive.  

>Lastly, the phenomenon of droplet splash back cannot be ruled out and there is little justification
to go to the great care in computing the impact of droplets with a surface if significant
splash back occurs. It is strongly recommended that test be conducted in the near
future which can examone the question of splash back.  



##Citations

cites 22 publications:

Duhnham, R. E., Bezos, G. M., Gentry, C. L.: Two-Dimensional Wind Tunnel Tests of a Transport Type Airfoil in Water Spray. AIAA-85-0258, January, 1985.  
Feo, A.: Rotating Arms Applied to Studies of Single Angular Drop Impacts. AIAA-87-0257, January, 1985.  
- Bragg, M. B., Gregorek, G. M., and Shaw, R. J.: "An Analytical Approach to Airfoil Icing." AIAA Paper No. 81-0403, Presented at the 19th Aerospace Sciences Meeting, January 12-15, 1981.  
Papadakis, M., Elangovan, R. Freund, G. A. Jr., Breer, M. D.: Experimental Water Droplet Impingement Data on Two-Dimensional Airfoils, Axisymmetric Inlet and Boeing 737-300 Engine Inlet. AIAA-87-0097, January, 1987.  
Guibert, A. G., Janssen, E., and Robbins, W. M.: Determination of Rate, Area, and Distribution of Impingement of Waterdrops on Various Airfoils from Trajectories Obtained on the Differential Analyzer. NACA-RM-9A05, 1949.  
Ruff, G. A.: Development of an Analytical Ice Accretion Prediction Method (LEWICE). Sverdrup Technology, Inc., LeRC Group Progress Report, February, 1986.  
MacAurthur, C. D.: Numerical Simulation of Airfoil Ice Accretion. AIAA-83-0112, January, 1983.  
- Lozowski, E. P., Stallabrass, J. R., and Hearty, P. F.: "The Icing of an Unheated Nonrotating Cylinder in Liquid-Water Droplet-Ice Crystal Clouds." National Research Council of Canada (NCR) Report LTR-LT-88, February 1979.  
Bilanin, A. J.: Scaling Laws for Testing Airfoils Under Heavy Rainfall. Journal of Aircraft, Vol. 24, No. 1, January, 1987.  
Department of Transportation Federal Aviation Administration "Aircraft Ice Protection," Advisory Circular 20-73, April 21, 1971.
Messinger, B. L.: Equilibrium Temperature of an Unheated Icing Surface as a Function of Airspeed. Preprint No. 342, Presented at I.A.S. Meeting, June 27-28, 1951.  
Ruff, Gary A.: Analysis and Verification of the Icing Scaling Equations. AEDC-TR-85-30 Vol. II, March, 1986.   
Hauger, H. H., and Englar, K. G.: Analysis of Model Testing in an Icing Wind Tunnel. Douglas Aircraft Company, Inc. Report No. SM14933, 1954.   
Sibley, P. J. and Smith, R. E., Jr.: "Model Testing in an Icing Wind Tunnel." Lockheed Aircraft Corporation, Report No. LR10981, 1955.  
Dodson, E. O.: "Scale Model Analogy for Icing Tunnel Testing." Boeing Airplane Company, Transport Division, Document No. D66-7976, March 1962.  
Jackson, E. T.: Development Study: The Use of Scale Models in an Icing Wind Tunnel to Determine Ice Catch on a Prototype Aircraft with Particular Reference to Concorde. British Aircraft Corporation (Operating) Ltd., Filton Division, SST/B75/RMMcK/242, July, 1967.  
Armand, C. et. al.: "Techniques and Facilities Used at the Onera Modane Centre for Icing Tests." North Atlantic Treaty Organization Advisory Group for Aerospace Research and Development, AGARD-AF-127, November 1978.  
Ruff, Gary A.: Analysis and Verification of the Icing Scaling Equations. AEDC-TR-85-30 Vol. I (revised), 1985  
Schlichting, D.: Boundary-Layer Theory. McGraw-Hill Book Company, New York, NY, 1968.  
- Olsen, W., Shaw, J., and Newton, J. "Ice Shapes and the Resulting Drag Increase for a NACA 0012 Airfoil." NASA-TM-83556, January 1984.  
Achenbach, E.: The Effect of Surface Roughness on the Heat Transfer from a Circular Cylinder to the Cross Flow of Air. International Journal of Heat Mass Transfer, Vol. 20, 1977.  
Hansman, J. R., Jr., and Turnock, S. R.: Investigation of Surface Water Behavior During Glaze Ice Accretion. AIAA-88-0015, January, 1988.  




Bilanin, Alan J.: Proposed Modifications to Ice Accretion/Icing Scaling Theory. AIAA-88-0203, Janurary, 1983.  




