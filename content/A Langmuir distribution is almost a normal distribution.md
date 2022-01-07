Title: A Langmuir distribution is (almost) a normal distribution   
Category: python tools
tags: cylinder
status: draft

> ###"Upon comparing this chart with Langmuir's tables (reference 7), it was found that his selections of the representative radii for the various sub-divisions of the volume were in error." [^1]

##Summary  
The Langmuir drop size distribution are almost normal distributions.

##Key points
1. The Langmuir drop size distribution are almost normal distributions.  
2. Perhaps it was originally intended that they be exactly normal distributions.

##Discussion

###Normal drop size distributions

Alas, I do not have access to a [differential analyzer](https://en.wikipedia.org/wiki/Differential_analyser) as was used in [^1], 
so I will have to use a modern, digital computer. Also, we will not be integrating the water drop equations of motion; 
we will be using the data in [^1] to determine water drop impingement on a cylinder.

The Anaconda distribution of Python version 3.7 was used [^2], 
as this includes the third party modules matplotlib, numpy, and scipy.

The drag for a sphere and the drop range parameter values from Table I are implemented in the file langmuir_blodgett_table_i.py in the github repository [^3].
The values for cylinder water catch efficiency Em Table II are implemented in the file langmuir_blodgett_table_ii.py. 
A 2D interpolation of Table II values was used. 

Other correlations were considered, as detailed in the file, but the
interpolation was selected as the most accurate over the entire range of parameters (K, Phi) considered. 
The range of values in Table II are rather broad, and should fit every combination of drop size and cylinder diameter 
of interest in aviation.
 
In the file langmuir_cylinder.py, several functions are implemented to calculate dimensionless values such as K and Phi 
from dimensional values, such as airspeed, drop size, and cylinder diameter. 
The Langmuir drop size distributions are implemented. 
The calculated cylinder water catch efficiency Em values compare to Table XI values quite well.

![comparison to Table XI values](images/Implementation of cylinder impingement correlations in Python/calculation_verification_table_XI_k_phi=1000_log.png)

###A subtlety about implementing drop size distributions

As noted in NACA-TR-1215 [^4], for drop size distributions Langmuir and Blodgett used an approximation, 
using the k\*phi value for the MVD for every drop size bin when calculating the weighted Em value. 
This means essentially that for part of the calculation (the k\*phi value) the MVD drop size was used for every bin, 
and for the other part (the k value) the drop size was unique for each bin.
A more technically correct implementation is to have a unique k\*phi value for each bin (both the k and the k\*phi parts). 
I could not find in Langmuir and Blodgett where they were explicit about this detail of their method, 
and it was an astute observations made in NACA-TR-1215 to notice this. 
A comparison to Table XI values verifies that the "k\*phi value for the MVD" method was used.

<!--- note the the "*" in k*phi is escaped k\*phi to prevent unwanted formatting between "*"s --->

Both methods were implemented herein. 
There are only a small differences between values calculated with the two implementations. 

![comparison of two implementations](images/Implementation of cylinder impingement correlations in Python/compare_em_distribution_with_and_without_k_phi_mvd_k_phi=1000.png)

I doubt that the approximation was a source of any significant errors in analysis using the 
Langmuir-Blodgett methods.

The "unique k\*phi for each bin" method is considered more technically correct, 
and will be used hereafter (unless noted otherwise).

##Notes:
[^1]:  
[Mathematical Investigation of Water Droplet Trajectories]({filename}/Mathematical Investigation of Water Droplet Trajectories.md)  
[^2]:
Anon: Anaconda Software Distribution. version 2021-11 (Python 3.7), Anaconda Inc. Available at: https://www.anaconda.com/  
[^3]: [https://github.com/icinganalysis/icinganalysis.github.io](https://github.com/icinganalysis/icinganalysis.github.io)  
[^4]: Brun, Rinaldo J., Lewis, William, Perkins, Porter J., and Serafini, John S.: Impingement of Cloud Droplets and Procedure for Measuring Liquid-Water Content and Droplet Sizes in Supercooled Clouds by Rotating Multicylinder Method. NACA-TR-1215, 1955. (Supersedes NACA TN’s 2903, 2904, and NACA-RM-E53D23)  
