Title: Computer Impingement Analysis Tools Examples    
header: The Basics: Intermediate Topics  
Date: 2024-04-8 17:00  
tags: intermediate topics, water catch, LEWICE   
status: draft  
rights: CC-BY-NC-SA 4.0  

![LEWICE 1990 Figure 4.2. Definition of total and local collection efficiency.](/images%2Fbasics%2FLEWICE%201990%20Figure%204_2.png)  
_from Users Manual for the NASA Lewis Ice Accretion Prediction Code (LEWICE) (1990 version) [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19900011627)_  

## Prerequisites  

You need to complete the [Aircraft Icing Handbook Water Catch Examples]({filename}intermediate_water_catch_examples.md).  

You need to select a computerized tool to work with. 
See [Analysis Toolset]({filename}intermediate_toolset.md) 
for obtaining LEWICE, and some other options.  

## Aircraft Icing Handbook Example 2-2  
                                       
>Example 2-2  
This example illustrates the estimation of the impingement parameters E, β, h, Su and SL
using graphical data (reference 2-12). The graphical data is all presented with Ko as the independent
variable. Much data is available in this form.  
> 
>The conditions of Example 2-1 for a NACA 0012 airfoil are assumed: thus Ko = 0.05. It also is
assumed for simplicity that the angle of attack, α, is 0 degrees. From figure 2-11, E, the total
impingement efficiency, is estimated to be 0.23 for these conditions. So about 23 percent of the water
in the projected frontal area of the airfoil, with height h = .120c (found using figure 2-12), impinges
on the airfoil. The maximum impingement efficiency for Ko = 0.05 and a = 0 degrees is estimated
from figure 2-13 to be β_max = 0.68. At a = 0 degrees, the upper and lower limits of impingement are
identical. From figure 2-14 at Ko = 0.05, SU = SL = .04. Therefore, water droplets will impinge on
the airfoil leading edge only back approximately 4 percent of chord. (Note that this example assumes
a "monodispersed" cloud, that is, a cloud in which all the droplets are of the same size. More realistic
approaches are discussed in the following section.)

## Aircraft Icing Handbook Example 2-3  

>This example is a repetition of Example 2-2 except that this time the impingement parameters
will be found using the entire droplet spectrum. It is assumed that the droplet median volume
diameter (MVD) is 20 im (the droplet size used in Example 2-2) and the cloud droplet spectrum can
be represented by a Langmuir D distribution. The droplet sizes representing the seven size bins in
the distribution are calculated using table I-1 (discussed in Section 1.2.6). Table 2-1 shows the droplet
sizes δ, the proportion δ_v of total droplet volume associated with each δ, and also the values of Re, 
K, and Ko for each δ. 
 
![Table 2-1.png](/images%2FFAA%20Handbook%20volume%201%2FTable%202-1.png)  

>Using these values of Ko and figure 2-11, a value E(δ) is associated with each
δ, as shown in the third column of table 2-2. Note that equation 2-23 can also be written as  

![Equation 2-25.png](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-25.png)  

>Thus E is calculated as an average value of the E(δ) weighted by volume using the Δv's. Table 2-2
shows that a value E = 0.24 is obtained, little different from the value E = 0.23 for the MVD. This
is well within the accuracy of reading numbers from the figure.  

![Table 2-2.png](/images%2FFAA%20Handbook%20volume%201%2FTable%202-2.png)  
 
>Considering this droplet size distribution and using equation 2-21, β_max can be calculated for a
surface length location of S = 0 (stagnation point). For the special case of a symmetric airfoil at zero
degrees angle of attack, where β_max occurs at S = 0 for all Ko, equation 2-21 can be used directly to
determine β_max. In table 2-2 the calculation of β_max at S = 0 is summarized in the last two colum's,
obtained from figure 2-11. Here again the value of β_max = 0.65 is close to the value for the MVD
droplet size, where β_max = 0.68.
> 
>The maximum limits can be found from Ko,max and figure 2-14. For the 44.4 micron droplet size,
Ko,max =0.176 and from the figure SU = SL = 0.11, or 11 percent of the chord length.
Estimates of the size of a pneumatic ice protection boot have been made by using an MVD of 20
microns and twice that diameter (40 microns) to determine the maximum extent of significant droplet
catch. This comes to about 10% of the airfoil chord on the critical upper surface.
Ten percent coverage of the upper surface is consistent with statistical measurements of upper surface icing made
in the USSR (reference 2-13). 

>Comparison of Example 2-2 and 2-3 suggests that, except for the limits of impingement.
impingement parameters calculated using the MVD may give a reasonably good approximation to those
calculated over an entire droplet distribution. 
> 
>This property of the MVD supplies the main
justification for its wide use as the "representative" droplet size for a supercooled cloud in the study
of aircraft icing. The error introduced in impingement calculations by its use rather than use of the
full droplet spectrum is discussed in reference 2-14 and 2-15.  

A solution using LEWICE is detailed here. 
The details of other methods may differ, 
but most impingement analysis programs use similar inputs. 

For the airfoil definition, 
the LEWICE software distribution includes an example with a NACA0012 airfoil file 
NACA0012.XYD.  

This example solution used the default potential flow solver included with LEWICE 
(LEWICE does have the option to include an externally determined flow solution). 
With the default potential flow solver, 
the surface grid is automatically determined (so no explicit, user-directed griding step is required).  

A file case.inp defines icing conditions and other inputs. 
Values are in metric units, see the manual that was included with the LEWICE software distribution for full details. 
Some default values are explicitly included below, such as DSMN. 

```text
Aircraft Icing Handbook Example 2-3
&LEW20
ITIMFL =  1
TSTART =  0.0
TSTOP  =  300.0
IBOD   =  1
IFLO   =  1
DSMN   =  0.000400
NPL    =  24
RHOP   =  1000.000000
IGRID  =  0
IBOE   =  0
IDEICE =  0
IHTC   =  0
&END
&DIST
FLWC   =  0.05000, 0.10000, 0.20000, 0.30000, 0.20000, 0.10000, 0.05000
DPD    =  6.20000, 10.40000, 14.20000, 20.00000, 27.40000, 34.80000, 44.40000
&END
&ICE1
CHORD  =  0.9449
AOA    =  0.000
VINF   =  102.89
LWC    =  0.500
TINF   =  241.483
PINF   =  69681.6
RH     =  100.0
SREF   =  1
&END
&LPRNT
FPRT   =  2
HPRT   =  2
BPRT   =  1
EPRT   =  2
MPRT   =  2
TPRT   =  2
IDBF   =  0
KWARN  =  0
&END
&RDATA
&END
&BOOT
&END
```

For a Langmuir distribution, the user includes in the input file data for the 7 bins in the
FLWC (bin fraction of total liquid water content) and DPD (bin drop diameter in micrometers) values: 

```text
FLWC   =  0.05000, 0.10000, 0.20000, 0.30000, 0.20000, 0.10000, 0.05000
DPD    =  6.20000, 10.40000, 14.20000, 20.00000, 27.40000, 34.80000, 44.40000
```

LEWICE outputs numerous result files. The one of interest here is beta.dat. 
The distribution weighted-average calculation is automatically included. 

LEWICE does not directly report the Em value. 
You can calculate that by using the Aircraft Icing Handbook equations 2-16 and 2-18.  


![Equation 2-16](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-16.png)  

![Equation 2-18](/images%2FFAA%20Handbook%20volume%201%2FEquation%202-18.png)

The Beta curve was numerically integrated. 

![lewice2d_example2_2_beta_tf_15](/images%2Fbasics%2Flewice2d_example2_2_beta_tf_15.png)
_Public Domain by Donald Cook_  

The LEWICE results are similar to the Handbook values, 
but not exactly the same.  

```text
Example 2-3      Handbook  LEWICE
Em               0.24      0.251
Beta_max         0.65      0.642
Su/c (and Sl/c)  0.10      0.10
```

## Resources  

"Aircraft Icing Handbook", DOT/FAA/CT-88/8-1 [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA238039.pdf)  
Also note that there was a perhaps little known update in 1993: [apps.dtic.mil](https://apps.dtic.mil/sti/pdfs/ADA276499.pdf)  
The update contains only the updated pages. 
This worked fine when one printed the pages, punched holes, and manually substituted them into a three ring binder, 
but not so well in the digital age. 

[Aircraft Icing Handbook Merged Sections]({filename}intermediate_merged_handbook.md) 
merges some affected sections from the handbook and the update.  

The NASA-provided Icing Research Software (LEWICE, LEWICE 3D) [www1.grc.nasa.gov](https://www1.grc.nasa.gov/aeronautics/icing/software/)  

## References (Handbook format)  

2-2 Langmuir. I. and Blodgett, K., "A Mathematical Investigation of Water Droplet Trajectories," AAFTR 5418, February 1946. [books.google.com](https://books.google.com/books?hl=en&lr=&id=mJySYM32cHUC&oi=fnd&pg=PA11&dq=Katherine+Blodgett+icing&ots=QYP5gFyEiz&sig=djzAHtpIZuT_OlbopRsNYyUhUdc#v=onepage&q=Katherine%20Blodgett%20icing&f=false)   

2-12 Bragg, M. B. and Gregorek, G. M., "An Analytical Evaluation of the Icing Properties of Several Low and Medium Speed Airfoils," AIAA Paper No. 83-109, January 1983. [arc.aiaa.org](https://arc.aiaa.org/doi/10.2514/6.1983-109)  

2-13 Trunov, 0., "Icing of Aircraft and the Means of Preventing It," English Translation, FTD-M7-65-490, p. 105, 1965.

2-14 Chang, H-P; Frost, W; Shaw, R. J.; and Kimble, K. R., "Influence of Multidrop Size Distribution on Icing Collection Efficiency," AIAA-83-0100, paper presented at the 21st Aerospace Scienzes Meeting, Jan. 1983. [arc.aiaa.org](https://arc.aiaa.org/doi/10.2514/6.1983-110)  

2-15 Papadakis, M.; Elangovan, R.; Freund, Jr., 0. A.; Breer, M.; Zumwalt, G. W..; and Whitmer, L., "An Experimental Method for Measuring Water Droplet Impingement Efficiency on Two- and Three-Dimensional Bodies," NASA CR 4257, DOT/FAA/CT-87/22, November 1989. [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19900067654)  

## Related  

Back to [Intermediate Topics]({filename}intermediate.md#intermediate-topics)  
