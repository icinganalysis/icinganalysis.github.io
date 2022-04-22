Title: Let's Build a 1D Water Drop Trajectory Simulation  
category: Diversions  
tags: impingement  
status: draft  

![Figure 1 of NACA-TN-2903, depicting a cylinder in cross flow with air flow lines and water drop trajectories impacting the cylinder](images/cylinder with flow lines.png)  


#Let's build a 1D water drop trajectory simulation  

##Discussion  

We are going to start with a one dimensional simulation along the stagnation line. 
This will keep the implementation simple to be readily understood. 
This may not seem very useful, but it has applications: 

1. determine the drop size that will not impinge on a cylinder. 
2. icing wind tunnel center-line simulation. 

When we add water drop evaporation rates, we will have something like the AEDC1DMP (Arnold Engineering Development Center 1 Dimensional Multi-Particle) code, 
but it will be the "one dimensional single particle code". 

We will use the dimensionless coordinate system from Figure 1 above (from NACA-TN-2903). 

We will use python syntax, where exponentiation is "**". 

"u" is the dimensionless airspeed. 

For incompressible potential flow, 
The airspeed approaching a cylinder is (from L&B):


![](images/Mathematical Investigation of Water Droplet Trajectories/equations23and24.png)  


For y = 0 (the stagnation line or center-line), this simplifies to:

    ux = 1 - 1 / x**2
    
The coefficient of drag, Cd, for a sphere, where R is Reynolds number, is (from L&B)

![](images/Mathematical Investigation of Water Droplet Trajectories/equation22.png)  

![](images/Mathematical Investigation of Water Droplet Trajectories/equation4.png)  
![](images/Mathematical Investigation of Water Droplet Trajectories/equation6.png)  
![](images/Mathematical Investigation of Water Droplet Trajectories/equation12.png)  

Let us go implement the equations. 







is the AEDC1DMP 
(Arnold Engineering Development Center 1 Dimensional Multi-Particle) code described in [^3].

[^3]: 
Schulz, R. J.: Second Report for Research and Modeling of Water Particles in Adverse Weather Simulation Facilities. TASK REPORT 97-03, AEDC, July, 1998, https://apps.dtic.mil/sti/pdfs/ADA364922.pdf  

