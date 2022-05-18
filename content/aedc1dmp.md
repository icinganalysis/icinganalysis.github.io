Title: AEDC1DMP  
category: Diversions  
tags: impingement  
status: draft  

![Figure 1 of NACA-TN-2903, depicting a cylinder in cross flow with air flow lines and water drop trajectories impacting the cylinder](images/cylinder with flow lines.png)  


#The AEDC 1-Dimensional Multi-Phase code (AEDC1DMP)  

##Discussion  

>5.3.2 Nominal Test Conditions in a Full-Scale Icing Facility

>The duct or wind tunnel geometry assumed for test case 2 is shown in Figure 14. This
wind tunnel like configuration has a large inlet and a steep contraction section, to minimize flow
disturbances. Icing spray nozzles are assumed to be put in the plane of the large inlet. The test
section is located at x = 46 ft, so that the state of the water particles injected at the inlet of the
wind tunnel should be in kinetic and thermal equilibrium with the air flow by the time they reach
the test section. The tunnel has a large contraction ratio (inlet flow area divided by test section
flow area), hence, the range of permissible inlet air flow velocities is small, ranging from near 0
to about 45 ft per second. At the higher inlet air velocities, the test section has reached near-
choking, or sonic flow conditions. Generally, icing tests are conducted at air flow or flight-
simulating speeds in the range of a few hundred miles per hour. Therefore, a nominal set of inlet
test conditions was defined for the representative calculation made with AEDC1DMP. The
nominal test conditions are listed below.

![](images/build_a_1d_drop_motion_simulation/Table2AEDC.png)  
![](images/build_a_1d_drop_motion_simulation/Figure14AEDC.png)  

Equations were implemented in the file "iads1dmp.py" for the iads1dmp 
("Icing Analysis Developmental Software 1 Dimensional Multi-Phase" code, 
an homage to AEDC1DMP and the python lower case file naming convention). 
Incompressible flow equations were used. 

The drop velocity values agree well with the AEDC1DMP results. 
![](images/build_a_1d_drop_motion_simulation/iads1dmp_velocity.png)   

The temperature values agree well for the 50 micrometer case, 
but not as well as for the 500 micrometer case, although the end points match well. 
The iads1dmp used the heat transfer correlation from NACA-TN-3024 for a sphere. 
I suspect that the AEDC1DMP may have used a different heat transfer coefficient
(the coefficient used is not give in the reference). 

![](images/build_a_1d_drop_motion_simulation/iads1dmp_temperature.png)  

The drop sizes change slightly as the travel. 
Most of the change occurs near the pot of the spray, where the drops are hot. 
![](images/build_a_1d_drop_motion_simulation/iads1dmp_drop_size.png)   

We will call this "good enough" to proceed. 





is the AEDC1DMP 
(Arnold Engineering Development Center 1 Dimensional Multi-Phase) code described in [^3].

[^3]: 
Schulz, R. J.: Second Report for Research and Modeling of Water Particles in Adverse Weather Simulation Facilities. TASK REPORT 97-03, AEDC, July, 1998, https://apps.dtic.mil/sti/pdfs/ADA364922.pdf  

