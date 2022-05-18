Title: AEDC1DMP  
category: Diversions  
tags: impingement  
status: draft  

![iads1dmp velocity](images/build_a_1d_drop_motion_simulation/iads1dmp_velocity.png)   

#The AEDC 1-Dimensional Multi-Phase code (AEDC1DMP) and the iasd1dmp

##Abstract 

The AEDC1DMP is described in "Second Report for Research and Modeling of Water Particles in Adverse Weather Simulation Facilities" [^1]. 

>1.0 INTRODUCTION TO THE RESEARCH  
This report describes a continuation of research into the modeling of water particle
freezing for application to adverse weather simulation facilities. The research was initiated in
FY1996 to investigate the physics of freezing of submillimeter supercooled water particles or
droplets in both natural and artificial or simulated adverse weather environments. The first phase
of the research was reported and discussed in a report [1] and a paper [2]. The work has
continued into FY1997 and has been expanded to include work done to model three-dimensional
ice accretions on surfaces, as well as modeling the near field of water spray clouds produced by
air-atomized water spray nozzles. Because of the increased scope of the work, a single report
cannot cover all of the work phases. Therefore, the present report covers only the continued
research and development of water particulate freezing models and their application in a one-
dimensional multiphase flow code to predict water spray freezing in ducted air flows.

There is considerable information on water drop freezing calculations, 
that will not be described herein. 

Our immediate goal is data to use for comparison with the code developed in this post. 

##Discussion  

>5.0 EVALUATION OF AEDC1DMP CODE ON REPRESENTATIVE DUCT FLOW CASES  
5.1 Baseline Case of Ducted. Two-Phase Flow  
The base case computed for a comparison purpose was a ducted flow with a "single"
water spray station at its inlet.
In the code AEDC1DMP, the water is assumed to enter the airflow at up to ten different
injection stations that are separated, axially in the duct. Each injection station is capable of
putting in a given amount of water, in a given sized water particle with its specified velocity and
temperature. When all of the injection stations are bunched close together, axially, in the duct,
they can be used to model a single spray station with a spray droplet size distribution
characterized by ten discrete drop sizes. This was the approach taken in the previous study [1] to
examine the freezing of two-phase, ducted flows representative of both full-scale and 
research-scale icing test facilities.

>5.3.2 Nominal Test Conditions in a Full-Scale Icing Facility

>The duct or wind tunnel geometry assumed for test case 2 is shown in Figure 14. This
wind tunnel like configuration has a large inlet and a steep contraction section, to minimize flow
disturbances. Icing spray nozzles are assumed to be put in the plane of the large inlet. The test
section is located at x = 46 ft, so that the state of the water particles injected at the inlet of the
wind tunnel should be in kinetic and thermal equilibrium with the air flow by the time they reach
the test section. The tunnel has a large contraction ratio (inlet flow area divided by test section
flow area), hence, the range of permissible inlet air flow velocities is small, ranging from near 0
to about 45 ft per second. At the higher inlet air velocities, the test section has reached 
near-choking, or sonic flow conditions. Generally, icing tests are conducted at air flow or 
flight-simulating speeds in the range of a few hundred miles per hour. 
Therefore, a nominal set of inlet
test conditions was defined for the representative calculation made with AEDC1DMP. 
The nominal test conditions are listed below.

![Table 2](images/build_a_1d_drop_motion_simulation/Table2AEDC.png)  
![Table 2 part 2](images/build_a_1d_drop_motion_simulation/Table2_part2.png)  
![Figure 14](images/build_a_1d_drop_motion_simulation/Figure14AEDC.png)  

Our goal is to develop enough capability to predict water drop airspeed, 
temperature, and evaporation rates. 

Equations were implemented in the file "iads1dmp.py" [^2] for the iads1dmp 
("Icing Analysis Developmental Software 1 Dimensional Multi-Phase" code, 
an homage to AEDC1DMP and the python lower case file naming convention). 

As this was flow in a duct, not flow around a cylinder, 
a different airspeed function was used 
than for the "cylinder_drop_1d_trajectory_shift.py" from ["Let's Build a 1D Water Drop Trajectory Simulation"]({filename}build_a_1d_drop_motion_simulation.md). 
The changing duct area was put into a table, 
and the local airspeed calculated with compressible flow relationships. 

The heat and mass transfer relationships from [NACA-TN-3024]({filename}NACA-TN-3024.md) [^3] were used.  

![Nu_h](images/naca-tn-3024/Nu_h.png)  
![Nu_m](images/naca-tn-3024/Nu_m.png)  

As a time stepping integration method was used, 
convergence with the dimensionless time step tau was checked using the calculated final drop temperature.  

![iads1dmp tau sensitivity](images/build_a_1d_drop_motion_simulation/iads1dmp_tau_sensitivity.png)  

The calculated drop velocity values agree well with the AEDC1DMP results. 
![iads1dmp velocity](images/build_a_1d_drop_motion_simulation/iads1dmp_velocity.png)   

The water leaving the spray nozzles is heated, 
so a water drop has a rapid initial temperature drop. 
The calculated temperature values agree well for the 50 micrometer case, 
but not as well as for the 500 micrometer case, although the end points match well. 
The iads1dmp used the heat transfer correlation from NACA-TN-3024 for a sphere. 
I suspect that the AEDC1DMP may have used a different heat transfer coefficient
(the coefficient used is not give in the reference). 

![iads1dmp temperature](images/build_a_1d_drop_motion_simulation/iads1dmp_temperature.png)  

The drop sizes change slightly during the travel as water evaporates. 
Most of the change occurs near the point of the spray, where the drops are hot. 
![iads1dmp drop size](images/build_a_1d_drop_motion_simulation/iads1dmp_drop_size.png)   

##Conclusions

Unfortunately, "Second Report for Research and Modeling of Water Particles in Adverse Weather Simulation Facilities" 
did not include actual test data for comparison, 
but it did have analysis results for comparison. 

We will call this "good enough" to proceed. 


##Notes:

This is part of the [Water drop evaporation thread]({filename}water_drop_evaporation_thread.md), 
which you may want to review if you came here via a direct link. 

[^1]: 
Schulz, R. J.: Second Report for Research and Modeling of Water Particles in Adverse Weather Simulation Facilities. TASK REPORT 97-03, AEDC, July, 1998, https://apps.dtic.mil/sti/pdfs/ADA364922.pdf  
[^2]: [https://github.com/icinganalysis/icinganalysis.github.io](https://github.com/icinganalysis/icinganalysis.github.io)  
[^3]: 
Lowell, Herman H.: Maximum Evaporation Rates of Water Droplets Approaching Obstacles the Atmosphere under Icing Conditions. NACA-TN-3024, 1953  

