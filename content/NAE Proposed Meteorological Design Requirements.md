Title: The NAE Proposed Meteorological Design Requirements   
Date: 2023-05-31 12:00  
tags: Airplane Icing Information Course  

### _"It is observed that severe icing is not predicted over large areas."_  

## Introduction  

This is one of the shortest post that I have written, 
as it is more outlining a mystery, that I have not yet sorted out, than a full review.  

## Summary  

In [Conclusions of the Meteorology of Icing Clouds Thread]({filename}Conclusions%20of%20the%20Meteorology%20of%20Icing%20Clouds%20Thread.md#tracking-lwc-values), 
there is a time-line of how the NACA understanding of the icing conditions evolved, 
focussing on liquid water content (LWC) values. 

In Canada, icing research was also being performed by the National Aeronautical Establishment (NAE). 

Here, we will compare what was published in the 
University of Michigan Airplane Icing Information Course, in 1953,
to NACA data and the later Appendix C.

## Discussion 

### Smith, E. L.: "The Design of Fluid Anti-Icing Systems" (NAE) [^1]  

>3.3 Meteorological Conditions  
> 
>Figure 15 presents the meteorological design requirements proposed by the Low 
Temperature Laboratory of the N.A.E. 
It is observed that severe icing is not predicted over large areas. 
These curves may be cross plotted on fluid requirement 
curves (for example, Figures 7 to 10), assuming constant meteorological conditions 
to 20,000 ft., to determine the fluid requirements at various flight speeds and 
altitudes. If a control for fluid flow is provided, then the 3-mile extent curve 
will simply specify the maximum flow required, while the lower curves enable a 
prediction to be made of the maximum total quantity of fluid required for a given 
flight.

![Smith Figure 15. Proposed Meteorological Design Requirements 
for Aircraft Anti-Icing Equipment.](images%2FFraser%20Flight%2FSmith%20Figure%2015.png)  

### Fraser, Don: "Meteorological Design Requirements for Icing Protection Systems" (NAE) [^2]  

Fraser compares the NAE definition to the NACA values: 

![Figure 12. Comparison of Proposed and NACA Design Requirements.](images%2FFraser%20Flight%2FFigure%2012.png)  

Drop size information is given in Section 4.4. 
Figure 11b is referenced (not included here) which indicates the use of 
35 micrometer volume median drop diameter at an LWC value of 2 g/m^3. 
[This is from the errata sheet, the original text used Figure 7.] 
A size distribution is recommended that "corresponds roughly to the Langmuir and Blodgett Spectrum 'C'". 

Fraser Figure 12 has a separate line for freezing rain. 

### Comparison to an Appendix C icing condition  

As we did in 
[Conclusions of the Meteorology of Icing Clouds Thread]({filename}Conclusions%20of%20the%20Meteorology%20of%20Icing%20Clouds%20Thread.md#tracking-lwc-values) 
for data from several sources, 
we will see what LWC value this definition (designated as "N.A.E.") yields 
for a selected condition, Appendix C [^3] Figure 1
for "Continuous Maximum (Stratiform Clouds)" (upper left corner of the envelope):  

- Temperature = 32F, MVD = 15 micrometer, 17.4 nmi (20 mile) extent  

![Appendix C Figure 1. Continuous Maximum (Stratiform Clouds) 
Atmospheric Conditions 
Liquid Water Content vs. Mean Effective Drop Diameter](images%2FAppCfig1.png)  

The differing MVD value for the NAE definition makes this a bit of a strained, 
"apples and oranges" comparison, but I will also include the Appendix C 
values for 35 micrometers. 

| Source                     | Year | LWC, g/m^3    |
|----------------------------|------|---------------|
| Rodert                     | 1946 | 3.0           |
| NACA-TN-1391               | 1947 | 1.5           |
| NACA-TN-1393               | 1947 | 0.8           |
| NACA-TN-1424 A             | 1947 | 1.0           |
| NACA-TN-1424 B             | 1947 | 0.8           |
| NACA-TN-1855               | 1949 | 0.8           |
| N.A.E.                     | 1953 | 2.25 [30 MVD] |
| CAR 4b-2 (1964 Appendix C) | 1955 | 0.8  [15 MVD] |
| CAR 4b-2 (1964 Appendix C) | 1955 | 0.26 [35 MVD] |

This is a much different value than what NACA was converging on. 
Fraser cites NACA-TN-1855 (and NACA-TN-2569 and NACA-TN-2738), 
so at least some in the NAE were aware of them. 

Oleskiw [^5] summarizes the flight tests and instruments used. 

As we saw in the 
[Conclusions of the Meteorological Instruments Thread]({filename}Conclusions%20of%20the%20Meteorological%20Instruments%20Thread.md), 
the National Research Council (Canada) had arrived at a similar instrumentation suite to that used by NACA by 1952 [^6].    

![Table 1 of Pettit.](/images/K G Pettit/Table of instruments.png)  

So, differences in instruments does not appear to be an explanation for the strikingly different results. 

## Conclusions  

I have not been able to find the actual data that the NAE used to determine the values. 

The NAE publications show a diversity of opinions in 1953 about what icing design conditions should be 
compared to the NACA publications. 

## Notes  

[^1]: Smith, E. L.: The Design of Fluid Anti-Icing Systems. Engine Laboratory, National Aeronautical Research Establishment, Ottawa, Canada, Lecture No. 11, University of Michigan Airplane Icing Information Course, 1953.  (32 pages) (includes errata sheet)  
[^2]: Fraser, Don: Meteorological Design Requirements for Icing Protection Systems. Low Temperature Laboratory, NAE, Ottawa, Canada, Lecture No. 12a, University of Michigan Airplane Icing Information Course, 1953.  (36 pages) 
[^3]: “Airworthiness Standards: Transport Category Airplanes”, CFR 14, Part 25, Appendix C, Washington, DC, 2021 [Appendix C ecfr.gov](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-C/part-25/appendix-Appendix%20C%20to%20Part%2025)  
[^4]:
"AIRPLANE AIRWORTHINESS - TRANSPORT CATEGORIES MISCELLANEOUS AMENDMENTS", Civil Air Regulations Amendment 4b-2, July, 1955. 
[stacheair.com](http://www.stacheair.com/data/At%20Work%209B%20Repair%20Station%20CD/Data%20Info/CAR%27s/CAR%20Part%20%204b/PDF/Part%2004b-02.pdf)  
[^5]: Oleskiw, M. M. "A review of 65 years of aircraft in-flight icing research at NRC." Canadian Aeronautics and Space Journal 47.3 (2001): 259-268. [researchgate.net](https://www.researchgate.net/publication/44057561_A_Review_of_65_Years_of_Aircraft_In-Flight_Icing_Research_at_NRC)  
[^6]: Pettit, K. G.: "'The Rockcliffe Ice Wagon' and its role in Canadian icing research." Publ. R. Met. Soc. Canad. Branch, Toronto 2 (1951). [cmosarchives.ca](http://cmosarchives.ca/RMS/r0205.pdf)  
