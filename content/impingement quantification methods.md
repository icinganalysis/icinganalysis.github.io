title: Water Drop Impingement Quantification  
category: impingement  
Date: 2023-10-05 12:00  
tags: impingement  
status: draft

# DRAFT

### _"One of the first essentials ... is a method for estimating or calculating the area over which water will strike the wing, and the distribution of water impingement over that area"_  

![Figure 5. Relationship of water-drop trajectories to streamline field about a symmetrical Joukowki airfoil 12 percent thick.](images%2Fnaca-tn-1397%2FFigure%205.png)  
_Figure 5 of NACA-TN-1397_  

## Summary  

Several methods were used to quantify the water-drop impingement on a surface, such as a wing. 

## Discussion

We already saw in the [Icing on Cylinders thread]({filename}Icing%20on%20Cylinders.md) calculations made for impingement on a cylinder. 
The technique was expanded in NACA-TN-1397 to include Joukowski type airfoils. 
This allowed a transformation of the flow solution around a cylinder to be mapped into airfoil coordinates, 
and then used to solve for water drop trajectory calculations, similar to those used for cylinders. 

NACA-TN-1397 said one could calculate "the trajectory a single drop without the utilization of a differential analyzer". 
We saw the differential analyzer in the [Icing on Cylinders thread]({filename}Icing%20on%20Cylinders.md), 
in particular detail in [NACA-TN-2904]({filename}NACA-TN-2904.md). 
However, the example given (Table II) has 32 columns with 37 rows of values (over 1000 values total), 
many of which are complex values to 6 digits that require manual table look-ups and subsequent calculation. 
And many trajectory calculations are required to determine "the distribution of water impingement over that area". 
So, access to a differential analyzer could greatly increase the number of analyses accomplished.  

![Table II. COMPUTATION OF A WATER-DROP TRAJECTORY (Ru^2 = 9.15 x 10^3; K = 0.0581)](images%2Fnaca-tn-1397%2FTable%20II.png)  
_Table II from NACA-TN-1397 (part 1 of 4)._  

A differential analyzer was a potentially general purpose computer, 
that could be re-arranged to perform different integrations. 
The "Water-drop-trajectory analog" was, apparently, purpose-built to solve the drop trajectory differential equations only. 

![Figure 15 of NACA-TN-2904. Water-drop-trajectory analog.
Two investigators operate a large mechanical computer. 
One is seated turning a crank attached to a large cylinder labeled "Input Chart". 
The second operator turns another input chart crank. 
Another cylinder is labeled "Droplet Trajectories". 
There are many shafts and gears visible in the machine. 
Some machine parts are labeled with the differential equations of motion being solved. 
](images/naca-tn-2904/Figure15.png)  
_Figure 15 of NACA-TN-2904. 
Yes, I have used this figure a lot, as it is one of the best of the hundreds I have viewed from the NACA-era.
There will be a tentative identification of these investigators later in this thread._  

With enough clever physics, math, and algebra, some geometries yield a closed-form solution for drop trajectories, 
at least in potential flow conditions. 
NACA-TR-1159 has examples for a wedge in supersonic flow with an attached shock wave. 

We saw the dye-tracer test technique in the [Icing on Cylinders thread]({filename}Icing%20on%20Cylinders.md). 
This more or less directly measured the rate of water impingement on a surface. 
It did not and could not measure individual water drop trajectories. 

![Figure 20. Experimental local water impingement rates for three cylinder sizes. 
Airspeed, 175 miles per hour.](images/naca-tn-3338/Figure20.png)  
_Figure 20 from NACA-TN-3338._  

A limitation was that the drop size distribution produced by the icing tunnel spray nozzles was not well known at the time, 
and the dye tracer method itself was used to better estimate the distribution, 
so that dye tracer test results could be more accurately assessed ([NACA-TN-3338]({filename}NACA-TN-3338.md)). 
See the [Calibration of the NACA Icing Tunnels thread]({filename}calibration_of_naca_icing_tunnels.md) for how drop size measurement techniques progressed.

![Figure 17. Typical experimental impingement rate for 
cylinder showing arbitrary increments of central 
angle theta and including contributions of several 
droplet size groups.](images/naca-tn-3338/Figure17.png)  
_Figure 17 from NACA-TN-3338._  

### Techniques

### Joukowski transformation  

- Bergrun, Norman R.: A Method for Numerically Calculating the Area and Distribution of Water Impingement on the Leading Edge of an Airfoil in a Cloud. NACA-TN-1397, 1947.  

### Differential Analyzer  

- Guibert, A. G., Janssen, E., and Robbins, W. M.: Determination of Rate, Area, and Distribution of Impingement of Waterdrops on Various Airfoils from Trajectories Obtained on the Differential Analyzer. NACA-RM-9A05, 1949.  
- Brun, Rinaldo J., Gallagher, Helen M., and Vogt, Dorothea E.: Impingement of Water Droplets on NACA 65A004 Airfoil and Effect of Change in Airfoil Thickness from 12 to 4 Percent at 4° Angle of Attack. NACA-TN-3047, 1953.  
- Brun, Rinaldo J., Gallagher, Helen M., and Vogt, Dorothea E.: Impingement of Water Droplets on NACA 651-208 and 651-212 Airfoils at 4° Angle of Attack. NACA-TN-2952, 1953.  
- Brun, Rinaldo J., and Mergler, Harry W.: Impingement of Water Droplets on a Cylinder in an Incompressible Flow Field and Evaluation of Rotating Multicylinder Method for Measurement of Droplet-Size Distribution, Volume-Median Droplet Size, and Liquid-Water Content in Clouds. NACA-TN-2904, 1953.  
    > review: [NACA-TN-2904]({filename}NACA-TN-2904.md)  
- Brun, Rinaldo J., Serafini, John S., and Gallagher, Helen M.: Impingement of Cloud Droplets on Aerodynamic Bodies as Affected by Compressibility of Air Flow Around the Body. NACA-TN-2903, 1953.  
    > review: [NACA-TN-2903]({filename}NACA-TN-2903.md)  
- Brun, Rinaldo J., and Vogt, Dorothea E.: Impingement of Water Droplets on NACA 65A004 Airfoil at 0° Angle of Attack. NACA-TN-3586, 1955.  
- Brun, Rinaldo J., and Vogt, Dorothea E.: Impingement of Water Droplets on NACA 65A004 Airfoil at 0° Angle of Attack. NACA-TN-3586, 1955.
- Hacker, Paul T., Brun, Rinaldo J., and Boyd, Bemrose: Impingement of Droplets in 90° Elbows with Potential Flow. NACA-TN-2999, 1953.
- Brun, Rinaldo J., and Dorsch, Robert G.: Impingement of Water Droplets on an Ellipsoid with Fineness Ratio 10 in Axisymmetric Flow. NACA-TN-3147, 1954.  
- Dorsch, Robert G., and Brun, Rinaldo J.: A Method for Determining Cloud-Droplet Impingement on Swept Wings. NACA-TN-2931, 1953.  
- Dorsch, Robert G., Brun, Rinaldo J., and Gregg, John L.: Impingement of Water Droplets on an Ellipsoid with Fineness Ratio 5 in Axisymmetric Flow. NACA-TN-3099, 1954.  
- Brun, Rinaldo J., and Dorsch, Robert G.: Impingement of Water Droplets on an Ellipsoid with Fineness Ratio 10 in Axisymmetric Flow. NACA-TN-3147, 1954.  
- Dorsch, Robert G., and Brun, Rinaldo J.: Variation of Local Liquid-Water Concentration about an Ellipsoid of Fineness Ratio 5 Moving in a Droplet Field. NACA-TN-3153, 1954.  
- Brun, Rinaldo J., and Dorsch, Robert G.: Variation of Local Liquid-Water Concentration about an Ellipsoid of Fineness Ratio 10 Moving in a Droplet Field. NACA-TN-3410, 1955.  
- Lewis, William, and Brun, Rinaldo J.: Impingement of Water Droplets on a Rectangular Half Body in a Two-Dimensional Incompressible Flow Field. NACA-TN-3658, 1956.  
- Dorsch, Robert G., Saper, Paul G., and Kadow, Charles F.: Impingement of Water Droplets on a Sphere. NACA-TN-3587, 1955.  
- Lewis, William, and Brun, Rinaldo J.: Impingement of Water Droplets on a Rectangular Half Body in a Two-Dimensional Incompressible Flow Field. NACA-TN-3658, 1956.  
- Brun, Rinaldo J., Lewis, William, Perkins, Porter J., and Serafini, John S.: Impingement of Cloud Droplets and Procedure for Measuring Liquid-Water Content and Droplet Sizes in Supercooled Clouds by Rotating Multicylinder Method. NACA-TR-1215, 1955. (Supersedes NACA TN’s 2903, 2904, and NACA-RM-E53D23)  
    > review: [NACA-TR-1215]({filename}NACA-TR-1215.md), [NACA-TR-1215 Thermodynamics]({filename}NACA-TR-1215-Thermodynamics.md)  
- Hacker, Paul T., Saper, Paul G., and Kadow, Charles F.: Impingement of Droplets in 60° Elbows with Potential Flow. NACA-TN-3770, 1956.  

### Closed-form solution  

- Serafini, John S.: Impingement of Water Droplets on Wedges and Double-Wedge Airfoils at Supersonic Speeds. NACA-TR-1159, 1954. (Supersedes NACA-TN-2971.)  

### Dye Tracer  

- von Glahn, Uwe H., Gelder, Thomas F., and Smyers, William H., Jr.: A Dye-Tracer Technique for Experimentally Obtaining Impingement Characteristics of Arbitrary Bodies and a Method for Determining Droplet Size Distribution. NACA-TN-3338, 1955.  
    > review: [NACA-TN-3338]({filename}NACA-TN-3338.md)  
- von Glahn, Uwe H.: Use of Truncated Flapped Airfoils for Impingement and Icing Tests of Full-Scale Leading-Edge Sections. NACA-RM-E56E11, 1956.  
    > review: [Scaling in NACA tests]({filename}scaling_in_naca_tests.md)  
- Gelder, Thomas F., Smyers, William H., Jr., and von Glahn, Uwe H.: Experimental Droplet Impingement on Several Two-Dimensional Airfoils with Thickness Ratios of 6 to 16 Percent. NACA-TN-3839, 1956.  
- Brun, Rinaldo J., and Vogt, Dorothea E.: Impingement of Cloud Droplets on 36_5-Percent-Thick Joukowski Airfoil at Zero Angle of Attack and Discussion of Use as Cloud Measuring Instrument in Dye-Tracer Technique. NACA-TN-4035, 1957.  
- Lewis, James P., and Ruggeri, Robert S.: Experimental Droplet Impingement on Four Bodies of Revolution. NACA-TN-4092, 1957.  
- Gelder, Thomas F.: Droplet Impingement and Ingestion by Supersonic Nose Inlet in Subsonic Tunnel Conditions. NACA-TN-4268, 1958.  
