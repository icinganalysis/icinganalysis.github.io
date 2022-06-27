Title: Bilanin Pi Terms  
status: draft  




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




