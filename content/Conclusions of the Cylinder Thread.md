Title: Conclusions of the Cylinder Thread   
Date: 2022-04-04 12:00  
Category: NACA  
tags: cylinders  

## _"The collection of ice by the cylinders is similar to the collection of ice by airplane components." [^1]_  

![Figure 1 of NACA-TN-2903, depicting a cylinder in cross flow with air flow lines and water drop trajectories impacting the cylinder](images/cylinder with flow lines.png)

# Conclusions of the Cylinders Thread 

## Summary  
Data from the post-NACA era are used to resolve open questions 

## Key points
1. The Cylinders thread is summarized
2. Post-NACA era data is used to resolve some open questions.
3. NACA era data that are still used today are summarized

## Discussion

### Review of the Cylinders thread so far

In the Cylinders thread, we saw:

- A pioneering analysis of water drop impingement on a cylinder ([NACA-TN-779]({filename}NACA-TN-779.md)) 
- The most cited aircraft icing publication, with more detail of water drop impingement on a cylinder, and the rotating multicylinder instrument
(["Mathematical Investigation of Water Droplet Trajectories"]({filename}Mathematical Investigation of Water Droplet Trajectories.md)) 
- In flight icing measurements and an icing severity index ([NACA-TN-1393]({filename}NACA-TN-1393.md))
- An additional way to estimate drop size on a fixed cylinder ([NACA-TN-1424]({filename}NACA-TN-1424.md)) 
- Nine icing instruments compared ([NACA-RM-A9C09]({filename}NACA-RM-A9C09.md))
- The ability of the multicylinder method to determine drop distribution was questioned several times, including [NACA-TN-1904]({filename}NACA-TN-1904.md) 
- a comparison test of three similar multicylinders that found differences ([NACA-TN-2708]({filename}NACA-TN-2708.md)) 
- ["A Langmuir B drop size distribution is almost a normal distribution"]({filename}A Langmuir B distribution is almost a normal distribution.md) 
- The effect of compressibility on impingement calculation was found to be "negligible" ([NACA-TN-2903]({filename}NACA-TN-2903.md))  
- An analysis method to "more precisely" calculate water drop impingement was presented ([NACA-TN-2904]({filename}NACA-TN-2904.md)) 
- Data analysis methods can affect multicylinder results ([NACA-RM-E53D23]({filename}NACA-RM-E53D23.md)) 
- The effect of incomplete freezing on multicylinder results was quantified ([NACA-TR-1215]({filename}NACA-TR-1215.md)) 
- A pioneering dye-tracing impingement test method was used ([NACA-TN-3338]({filename}NACA-TN-3338.md)) 

And several programs in the Python programming language are available to reproduce the results in several cases [^2]. 

## Open questions

We will look at some data from the post-NACA era to help resolve these questions. 

1. differences in analysis methods between Langmuir and Blodgett [^3], and NACA-TN-2904 (which one is more accurate?)
2. the accuracy of the multicylinder method
3. How representative are Langmuir drop size distributions of natural and artificially produced drop size distributions?

## Post-NACA era data

### NASA-CR-4257 [^4]

This reference certainly merits a more complete review, but for now we will settle for a summary. 

In this publication, a dye-tracer method similar to NACA-TN-3338 was used on a 6 inch cylinder for two test cases. 
Water drop impingement rates were measured and presented as beta curves. 
The repeatability of the results was estimated as +/-10%.
There are also beta curves determined by water drop trajectory analysis (the "Breer" method).

[Note: I have worked with one of the authors, Marlin Breer.]

Two cases were measured, at 20.36 and 16.45 MVD.

![Figure 6.6A](images/nasa-cr-4257/Figure_6_6a.png)  

![Figure 6.6B](images/nasa-cr-4257/Figure_6_6b.png)  

Detailed drop size distributions were measured using a "Fiber Optics Particle Sizing System". 
30 bin data were published 
(although some larger drop size bins had zero water, 
so they are effectively 23 to 27 bin data). 
They were compared to a Langmuir D distribution.
(Nozzle pressure ratios corresponding to the cases above).

![Figure E9](images/nasa-cr-4257/FigureE9_pr_0_65.png) 

![Figure E6](images/nasa-cr-4257/FigureE6_pr0_8_rot.png)

### LEWICE [^5]

This reference also certainly merits a more complete review, but for now we will settle for a summary. 

The LEWICE computer program calculates water drop impingement rates on a body.
(It can also calculate ice shapes). 

LEWICE uses, by default, a compressible, potential flow solution 
(users have an option to use a separately determined flow solution). 
Drop trajectories are calculated by releasing drops upstream, 
and seeing where they impinge (not unlike the methods in NACA-TN-779, Langmuir-Blodgett, and NACA-TN-2904).

We will use it to get calculated water impingement rate values to compare to other data.

### Comparison of impingement calculation methods

We can use the detailed drop distribution data from NASA-CR-4257 to calculate water catch rate curves on the cylinder. 

The NACA-TN-2904 method tends to give higher values for both the maximum Beta value 
and the total water catch Em value, compared to the test and to the other analysis methods. 

The LEWICE and Langmuir-Bodgett analyses agree well with each other, 
and agree fairly well with the test values (within the +/-10% variation). 
The Breer method trends slightly lower.

![Comparison to Figure 6.6A](images/nasa-cr-4257/nasa_cr_4257_beta_comparison_fig6_6A.png)  

![Comparison to Figure 6.6B](images/nasa-cr-4257/nasa_cr_4257_beta_comparison_fig6_6B.png)  

The results are compared in tables below. 
The theta_max values for the Breer method may not have been digitized well by me, 
as they were difficult to discern from the figures. 
 
| Method                | Em    | Beta_max | Theta_max (degrees) |
|-----------------------|-------|----------|---------------------|
| Test Figure 6.6A      | 0.380 | 0.540    | 69.9                |
| Breer analysis        | 0.352 | 0.520    | 81.2                |
| LEWICE                | 0.373 | 0.556    | 81.6                |
| NACA-TN-2904          | 0.397 | 0.620    | 82.0                |
| Langmuir and Blodgett | 0.376 | 0.540    | 81.7                |

| Method                | Em    | Beta_max | Theta_max (degrees) |
|-----------------------|-------|----------|---------------------|
| Test Figure 6.6B      | 0.245 | 0.430    | 63.2                |
| Breer analysis        | 0.259 | 0.445    | 69.9                |
| LEWICE                | 0.288 | 0.480    | 79.8                |
| NACA-TN-2904          | 0.308 | 0.549    | 80.9                |
| Langmuir and Blodgett | 0.287 | 0.461    | 80.2                |

While I am inclined to view the Langmuir and Blodgett method as more accurate than the NACA-TN-2904 method, 
I would like to see more impingement data to determine it with more confidence. 
There is more cylinder test data that I am aware of, but as ice shapes, 
not direct impingement measurements, so the question may be not completely resolved. 

### Multicylinder method measurement accuracy

Alas, cylinders of different diameters were not included in NASA-CR-4257. 
However, three different cylinder diameters were included in NACA-TN-3338. 
We will take another look at that data, and analyze it as multicylinder data.

I wonder why NACA-TN-3338 did not use the "go-to" method of the multicylinder analysis. 
This was perhaps a lost opportunity for a drop size comparison that would not require technology beyond what was available. 
Author von Glahn was familiar with the multicylinder instrument. 
He was an author of NACA-RM-E51B12, which noted the use of multicylinders 
in the calibration of the icing tunnel: 
> Cloud droplet sizes and liquid-water contents in the tunnel
were measured by the rotating-multicylinder method and were in the
range of natural icing conditions. 

While the cylinders were not rotating, that does not limit the applicability of the method, 
as the main reason for rotating the cylinders is to make any ice accretion stay close to a cylindrical shape,
rather than some other shape for which the impingement characteristics are not known. 
With the dye-tracer method, the surface shape does not change. 

We will use the Python tools previously developed for multicylinders, 
using the Langmuir and Blodgett, and the NACA-TN-2904 implementations. 

![Figure 20](images/naca-tn-3338/Figure20.png) 

I digitized only one set of values for each cylinder diameter. 
Industrious readers may wish to clone the software repository, 
digitize more cases, and see if the results below still hold up. 

Note the small and subtle difference between MED and MVD from AC 20-73A [^6]:

>Appendix C icing conditions: 14 CFR parts 25, Appendix C and 29, Appendix C certification
icing condition standard for approving ice protection provisions on aircraft. The conditions are
specified by altitude, temperature, liquid water content (LWC), representative drop size (mean
effective diameter (MED)), and cloud horizontal extent.

>>NOTE: In Appendix C, the term “mean effective diameter” refers to
what is now called the “median volume diameter (MVD).” The MED
of Appendix C was determined by using rotating multi-cylinders and
assuming a Langmuir distribution.

So, I will use MED when reporting multicylinder results.

| Multicylinder Method                 | MED (micrometer) | LWC (g/m^3) | Best Fit Type |
|--------------------------------------|------------------|-------------|---------------|
| Langmuir and Blodgett (original)     | 18.8             | 0.458       | E             |
| NACA-TN-2904                         | 21.1             | 0.381       | E             |
| Langmuir and Blodgett (k_phi_unique) | 21.5             | 0.413       | E             |

When the distributions determined by the multicylinder methods are run in LEWICE, 
the measured mass rate values are reproduced well for the Langmuir and Blodgett methods, 
and less well for the NACA-TN-2904 multicylinder method. 

![Water catch rates calculated with Langmuir multicylinder fit](images/naca-tn-3338/Langmuir E original_6.png) 

![Water catch rates calculated with NACA-TN-2904 multicylinder fit](images/naca-tn-3338/Langmuir E NACA-TN-2904_6.png) 

![Water catch rates calculated with Langmuir multicylinder_k_phi_unique fit](images/naca-tn-3338/Langmuir E k_phi_unique_6.png)

So, a drop distribution determined by the multicylinder method 
(which is driven by cylinder Em values) 
can be used to reproduce well the composite water catch, built from Beta curves. 
 
This is an illustration of the applicability and accuracy of the multicylinder distribution measurements, 
at least over the range of cylinder sizes used (2, 4, and 6 inch diameter, in this case).

The comparisons above also add weight to the view that the Langmuir and Blodgett methods are more accurate than those of NACA-TN-2904. 

### A surprise from NACA-TN-3338

NACA-TN-3338 presented (at least) three drop distributions to represent the same test drop distribution. 
While I was sceptical of them, I ran them in LEWICE, 
and the Example from NACA-TN-3338 did an excellent job of reproducing the measured masses. 

![Water catch rates calculated with NACA-TN-3338 Example distribution](images/naca-tn-3338/Example_6.png)

When we plot the cumulative LWC vs. drop size for the distributions 
they may not appear to be very "similar", but three of them yielded very similar 
impingement analysis results. 
The NACA-TN-2904 distribution may appear similar to the "Langmuir_k_phi_unique" line, 
(see ["Implementation of cylinder impingement correlations in Python"]({filename}Implementation of cylinder impingement correlations in Python.md))
but the "Langmuir_k_phi_unique" line yielded a significantly better water catch result. 
So, I caution against reading too much into distribution plot comparisons for their 
relative effects on water catch. 

![Comparison of distributions](images/naca-tn-3338/distributions.png)

### <a name="drop_size_distributions"></a> Natural drop size distributions

We will apply the multicylinder method to a measured natural icing drop size distribution from FAA-RD-80-24 [^7]. 
(Once again, this reference merits a more thorough review, but we will settle for a brief summary for now). 

![FAA-RD-80-24 Figure 20](images/FAA_RD_80_24/Figure20.png)

I selected the 6000 ft data.
Alas, there was not a multicylinder instrument included in this test, 
so we will again use LEWICE to get the cylinder masses to use for the fitting. 
I used the cylinder diameters from NACA-RM-AC9C09 "Set A": 0.125, 0.5, 1.25, and 3 inch.

![Langmuir distribution fits to Figure 20 data](images/FAA_RD_80_24/RD80_mc_fits.png)

As in the prior examples, Beta curves were calculated with LEWICE. 
The Langmuir C best fit reproduces the measure test distribution ("ASSP") 
Beta curves very well, 
and the Langmuir E fit works well. 

![Calculated beta curve for the cylinders with distibutions](images/FAA_RD_80_24/RD80_betas.png)

So, even if multicylinder distributions may not appear to be similar to a 
more detailed, measured natural distribution, they can be used to reproduce impingement values 
quite well. 
The apparent difference in drop size distributions made 
little effective difference in impingement. 
For this case, at least, a Langmuir C fit or a Langmuir E fit both work well.
For me, this mitigates the concern expressed in NACA-TN-2904 and several other places of: 
> ... the inherent extreme insensitivity of the rotating multicylinder method to
differences in droplet size distributions ...

A Langmuir distribution representation of an icing condition may not be the actual distribution, 
but it is a functionally representative distribution. 

## NACA era data that are still used today

### Langmuir drop size distributions

A version of the drop distributions was published in 1944, 
and the more often cited version was published in 1946. 
See ["Mathematical Investigation of Water Droplet Trajectories"]({filename}Mathematical Investigation of Water Droplet Trajectories.md) 
and ["A Langmuir B drop size distribution is (almost) a normal distribution"]({filename}A Langmuir B distribution is almost a normal distribution.md) 
 
![Table IX](images/Mathematical Investigation of Water Droplet Trajectories/distributions.png) 

More than 70 years later, they are still in use. 
From FAA AC 20-73A, "Aircraft Ice Protection" [^6]: 

![Table I-1](images/ac2073a/LangmuirD.png)

### Terminology 
Many of the terms still in use were in Langmuir and Blodgett:  
 
![K terms](images/Mathematical Investigation of Water Droplet Trajectories/K_terms.png)

From the "Aircraft Icing Handbook" DOT/FAA/CT-88/8-1 [^8]:

![K terms](images/faa_ct_88_k_terms.png)

### Correlations

The impingement correlations form Langmuir and Blodgett, 
and NACA-TN-2904 were summarized 
and are available in plots such as this from the "Aircraft Icing Handbook" [^8]:

![Figure 2-44](images/FAA_CT_fig2_44.png)

Langmuir and Blodgett correlation formulas are also used, as in the from 
"An Appraisal of the Single Rotating Cylinder Method of Liquid Water Content Measurement" [^9]:

![Page A2](images/LTR-LT-92_correlations.png)

### Approximation of an airfoil leading edge 

The "Manual of Scaling Methods" [^10] details the use Langmuir and Blodgett correlations for 
a cylinder as an approximation of an airfoil leading edge: 

![equation 3.5](images/Manual of scaling methods/terms1.png) 
![equation 3.8](images/Manual of scaling methods/terms2.png) 
![Figure 3.3.2](images/Manual of scaling methods/terms3.png) 

### Icing conditions in regulations

The "Aircraft Icing Handbook" [^8] summarizes data used to develop icing regulations. 
We have reviewed three of these:  
[NACA-TN-1393]({filename}NACA-TN-1393.md), 
[NACA-TN-1424]({filename}NACA-TN-1424.md), 
and [NACA-TN-1904]({filename}NACA-TN-1904.md). 

One may note that the later cylinder publications are not included, 
notably [NACA-TN-2904]({filename}NACA-TN-2904.md) and 
[NACA-TR-1215]({filename}NACA-TR-1215.md).

The implications of this is that much of the data used was multicylinder data, 
processed with the methods of Langmuir and Blodgett, 
and not the "more precisely" calculated methods in NACA-TN-2904. 
NACA-TN-2904 was published too late to directly influence the icing regulations. 

![Figure 3-1](images/Derivation of FAR standards.png)

The citation on the figure "Reference 3-12" is NACA-TN-2569, 
but the figure is not to be found there, 
and NACA-TN-2569 was published before the icing regulations were published. 
I have not found where the figure was originally from. 

NACA-TN-1855 (and others) are cited directly in the US icing regulations: 

![Appendix C Figure 1. Continuous Maximum (Stratiform Clouds) 
Atmospheric Conditions 
Liquid Water Content vs. Mean Effective Drop Diameter](/images%2FAppCfig1.png)  

### Cylinder icing thermodynamics for icing indication and detection

NACA-TR-1215 studied several flight icing data cases, 
and found some were affected by not all of the available water freezing. 
An analysis of the freezing rates agreed well with the observed values: 

![Figure 24b](images/naca-tr-1215/Fig24small.png)

"An Appraisal of the Single Rotating Cylinder Method of Liquid Water Content Measurement" [^9] shows a similar effect, 
plotted in a different format: 

![Fig. 3](images/LRT-LT-92Fig3.png)

## Conclusion

Langmuir was widely acknowledged in the post-NACA era, including by another often cited author of aircraft icing publications 
(B.L. Messinger, 1969 [^11]):
> Thanks to the basic work of Dr. Irving Langmuir and his associates in the early
194O's, we came to understand the physics of the behavior of cloud particles in 
the aerodynamic flow field of an airplane.

Langmuir frankly eclipsed the many efforts of NACA on the icing of cylinders 
and the multicylinder instruments, 
including the "more precisely" calculated NACA-TN-2904.

The bulk of the flight data that icing regulations were developed from were from multicylinder instruments, 
the data of which was processed with methods from Langmuir and Blodgett. 
This quote from NACA-RM-E53D53 over-states the situation a bit, but it was not far from the reality of the time:  

> The meteorological data obtained with the multicylinder method are the only data available for the design of ice-protection equipment for aircraft

I call the development of the rotating multicylinder instrument a crowning achievement of the 
NACA-era.  

Much effort went into estimating the potential errors of the multicylinder method, 
particularly identifying the distribution type (A, B, C, D, E).
As shown in examples above, calculated impingement values were affected to a limited 
extent by the use of a C or an E distribution, supporting the continued use of the 
distributions as "representative". 

NACA-TR-1215 was important in identifying cases were all the available water may not freeze, 
and is a good introduction to [icing thermodynamics]({filename}/thermodynamics.md). 

## Related

A version of this post that was presented to the 
SAE AC-9C Aircraft Icing Technology Committee [^12] 
is [available as a pdf](images/cylinder_thread_wrap_up/SAE presentation Cook.pdf). 

The next thread in the NACA review series is the [Thermodynamics Thread]({filename}thermodynamics.md).  

## Notes:
[^1]: 
von Glahn, Uwe H.: The Icing Problem, presented at Ottawa AGARD Conference. AG 19/P9, June 10-17 1955, reprinted in Selected Bibliography of NACA-NASA Aircraft Icing Publications, NASA-TM-81651, August, 1981.  
I could not locate this on the NTRS. It is available at [core.ac.uk](https://core.ac.uk/reader/42858720) (circa August, 2023)  
[^2]: [https://github.com/icinganalysis/icinganalysis.github.io](https://github.com/icinganalysis/icinganalysis.github.io)   
[^3]:
Langmuir, Irving, and Blodgett, Katherine B.: A Mathematical Investigation of Water Droplet Trajectories. Tech. Rep. No. 5418, Air Materiel Command, AAF, Feb. 19, 1946. (Contract No. W-33-038-ac-9151 with General Electric Co.)  
[^4]: 
Papadakis, M., Elangovan, R., Freund, G. A. Jr., Breer, M., Zumwalt, G. W., Whitier, L.,:
"An Experimental Method for Measuring" Water Droplet Impingement Efficiency on Two- and Three-Dimensional Bodies", NASA-CR-4257, DOT/FAA/CT-87/22, 1987.  
[^5]: 
[software.nasa.gov](https://software.nasa.gov/software/LEW-18573-1), [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19990021235)  
[^6]: Anon.:"Aircraft Ice Protection", FAA AC 20-73A, [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-73A.pdf)  
[^7]: Jeck, Richard K: "Icing Characteristics of Low Altitude, Supercooled Layer Clouds", FAA-RD-80-24, May, 1980.  
[^8]: “Aircraft Icing Handbook, Volume I.” DOT/FAA/CT-88/8-1 (1991) [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf) .  
Also note that there was a perhaps little known update in 1993 (that did not affect the pages of interest herein): [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA276499.pdf)  
[^9]: 
Stallabrass, J. R.:"An Appraisal of the Single Rotating Cylinder Method of Liquid Water Content Measurement", LTR-LT-92, November, 1978.  
[^10]: 
Anderson, David N., Manual of Scaling Methods. NASA/CR-2004-212875, March 2004. [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20040042486)    
[^11]:
Messinger, B. L.:"Airframe Design for Protection Against Icing" in 
Anon., "Aircraft Ice Protection", the report of a symposium held April 28-30, 1969, by the FAA Flight Standards Service; 
Federal Aviation Administration, 800 Independence Ave., S.W., Washington, DC 20590.  
I could not find this on the NTRS or on the FAA site. 
It is available at [DTIC](https://apps.dtic.mil/sti/pdfs/AD0690469.pdf).  
[^12]: More information at [sae.org](https://www.sae.org/works/committeeHome.do?comtID=TEAAC9C)  

