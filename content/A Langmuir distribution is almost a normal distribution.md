Title: A Langmuir drop size distribution is (almost) a normal distribution   
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

[Normal distributions](https://en.wikipedia.org/wiki/Normal_distribution) show up many places in nature, 
so it is not surprising that drop sizes in clouds can approximate a normal distribution.  

In NACA-TN-2708 [^1], it was "presumed" that water-volume distribution with the
drop size is a Gaussian [normal] distribution:

> Drop-Size Distribution. - In the present report it is presumed,
following Howell (reference 6), that water-volume distribution with the
drop size is a Gaussian distribution, the breadth of which may be characterized 
by a modulus of distribution m that is defined by the relation:  
    m = (2)**0.5 * sigma / R_bar  
where simga is the standard deviation and R_bar is the volume median radius.
The distributions postulated by Langmuir (reference 7) and used in the
multicylinder method may be given numerical values as follows:

|Langmuir letter |A   |B   |C   |D   |E   |F   |G   |H   |J  |
|----------------|----|----|----|----|----|----|----|----|---|
|Modulus         |0.00|0.50|0.75|1.00|1.25|1.50|1.75|2.00|2.5|



NACA-TN-2708 [^1] noted that the Houghton and Radford data [^2] Langmuir [^2] used did fit a normal distribution well. 
The data were digitized, and the normal fit was confirmed, as shown below.

![](/images/naca-tn-2708/NACA-TN-2708_overlay.png)

Clark [^4] recommended a different fit of the Houghton and Radford data in the column denoted by (2) than that found by Langmuir (1).  
![Table IV. Ratios of Drop Radius to Volume Median Radius Corresponding to Percentile Divisions of Total Liquid Water in Clouds](/images/naca-tn-2708/table_iv_corrected_distrbutions.png) 


With normal distribution stdev=0.237 (fit to Houghton and Radford)

Percentile divisions of total liquid volume in clouds|Expected midpoint cumulative %|Drop size ratios to match midpoint cumulative % (normal distribution)Drop size ratios (Langmuir B)|Calculate cumulative volume (Langmuir B), %|Drop size ratios (Clark)|Calculate cumulative volume (Clark), %
---|---|---|---|---|---
0-5|2.5|0.54|0.56|3.2|0.53|2.4
5-15|10|0.7|0.72|11.9|0.69|9.5
15-35|25|0.84|0.84|25.0|0.91|35.2
35-65|50|1.0|1.0|50.0|1.0|50.0
65-85|75|1.16|1.17|76.3|1.09|64.8
85-95|90|1.3|1.32|91.2|1.31|90.5
95-100|97.5|1.46|1.49|98.1|1.47|97.6



With normal distribution stdev=0.25

Percentile divisions of total liquid volume in clouds|Expected midpoint cumulative %|Drop size ratios to match midpoint cumulative % (normal distribution)Drop size ratios (Langmuir B)|Calculate cumulative volume (Langmuir B), %|Drop size ratios (Clark)|Calculate cumulative volume (Clark), %
---|---|---|---|---|---
0-5|2.5|0.51|0.56|3.9|0.53|3.0
5-15|10|0.68|0.72|13.1|0.69|10.7
15-35|25|0.83|0.84|26.1|0.91|35.9
35-65|50|1.0|1.0|50.0|1.0|50.0
65-85|75|1.17|1.17|75.2|1.09|64.1
85-95|90|1.32|1.32|90.0|1.31|89.3
95-100|97.5|1.49|1.49|97.5|1.47|97.0



![]()

![](/images/naca-tn-2708/NACA-TN-2708_Figure_6.png)

> In the course of earlier work on the physical origin of the drop-
size distribution in clouds, the volume distribution diagram of Houghton
and Radford (reference 13) for fog drops was redrawn in the form shown
in figure 6 and the volume distribution found by Vonnegut, Cunningham,
and Katz (reference 14) in clouds was plotted on the same chart. Upon
comparing this chart with Langinuir's tables (reference 7), it was found
that his selections of the representative radii for the various sub-
divisions of the volume were in error. The matter was not pursued fur-
ther at the time, but as a part of the present study it was decided to
investigate the effect this error might have on the collection-efficiency
graphs, based on Langmuir's data, that have been used by virtually all
workers with the multicylinder method. The matter was not pursued further at the time, 
but as a part of the present study it was decided to
investigate the effect this error might have on the collection-efficiency
graphs, based on Langmuir's data, that have been used by virtually all
workers with the multicylinder method.


¯\\_(ツ)_/¯

##Notes:
[^1]: 
Howell, Wallace E.: Comparison of Three Multicylinder Icing Meters and Critique of Multicylinder Method. NACA-TN-2708, 1952.  
[^2]:
Houghton, H. G., and Radford, W. H.: On the Measurement of Drop Size and Liquid Water Content in Fogs and Clouds. Papers in Phys. Oceanography and Meteorol., M.I.T. and Woods Hole Oceanographic Inst., vol. VI, no. 4, Nov. 1938.
[^3]:  
[Mathematical Investigation of Water Droplet Trajectories]({filename}/Mathematical Investigation of Water Droplet Trajectories.md)  
[^4]:
Clark, Victor F.: The Multicylinder Method. Mt. Wash. Observatory Monthly Res. Bull., vol. II, no. 6, June 1946.
