Title: LEWICE Quick Start      
header: The Basics: Intermediate Topics  
Date: 2024-04-15 14:00  
tags: intermediate topics, ice shape, LEWICE   
status: draft  
rights: CC-BY-NC-SA 4.0  

![LEWICE Ice Shape for Example Case 1. A 2D profile of an airfoil with a calculated ice shape 
and an ice shape measured in an icing  wind tunnel test.](/images%2Fbasics%2FLEWICE%20manual%20example%201.png)  
_from User's Manual for LEWICE Version 3.2 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20080048307)_  

## Summary  

The "least that you need to know" to start using LEWICE, 
the NASA-provided icing simulation tool.  

## Prerequisites  

See [Analysis Toolset]({filename}intermediate_toolset.md) 
for how to obtain LEWICE.  

## Introduction  

Decades ago there was training available for using LEWICE. 
I do not know of recent training. 
You are largely on your own, with the manual and supporting material. 

This certainly does not contain complete information,
but it will help you get started in the basics of running LEWICE.  

## Discussion  

The LEWICE manual provides these instructions:  

>3.1.  
LEWICE Quick Start Guide  
This section is intended for users unfamiliar with LEWICE and/or DOS Shell commands.
The commands below (indented bold lines) should be typed at the C:\ prompt in a DOS Shell
window on a Windows machine. Alternatively, the user can use the Windows interface for any
of the commands shown. Windows XP refers to a DOS Shell window as a “Command Prompt”
and can be accessed from the Program menu under the “Accessories” submenu.  
>1) Create a directory on the hard drive to store output  
md lewice  
>2) Insert the LEWICE CD-ROM and copy all files from this disk to the lewice directory as
described in the Installation Procedure.  
>3) Inside the lewice directory, make additional directories for each run  
md case1  
>4) Run LEWICE  
>lewice <return>  
>>- program will prompt for input file name. Enter the following:  
case1.inp <return>  
>>- after printing a copyright notice, the program will prompt for a geometry file name. Enter
the following:  
case1.xyd <return>  
>>- if any warning messages appear, type  
Y <return>  
to continue the simulation.  
>5) copy output data files to the proper directory  
copy *.dat case1  

You are not likely to have the "CD-ROM" source of LEWICE. 
You are more likely to have received a zipped file. 

The output file "final1.dat" is the final ice shape, 
which is what many users are interested in. 

## Usage tips  

Pay attention to warnings. 
They usually indicate something that you can and should fix, 
rather than just typing 'Y' and continuing. 

It is convenient to create a link to the LEWICE executable, 
so that it can be run from any directory without typing a long path name. 

>linux: ln -s {full path to LEWICE executable} /LEWICE  

### Input files  

Use the default settings, unless you have a good reason to use another value. 
Running with the defaults will result in the output file "final1.dat", 
the final ice shape, 
which is what many users are interested in. 
You can conveniently use the default by omitting the term from the case.inp file, 
but I often include the explicit value, so that it is obvious what was used. 
The particularly applies for ITIMFL 
(use ITMIFL = 1, unless you have a good reason not to).  

>8.3.1. ITIMFL  
Default Value: ITIMFL = 1  
ITIMFL is a flag indicating whether LEWICE will use automatic time stepping or will use a
user-defined number of time steps. If ITIMFL = 0 then the number of time steps will remain as
input by the user in the IFLO variable. If ITIMFL = 1 then the time step will be calculated based
on the accumulation parameter. In either case, the time steps are of equal length throughout the
run. When ITIMFL = 1, the minimum number of time steps is calculated internally in the
program by the following procedure...  

However, it is possible to over-do the defaults. 
The minimum input file that will run:

```text
&LEW20
&END
&DIST
&END
&ICE1
&END
&LPRNT
&END
&RDATA
&END
&BOOT
&END
```

The output from running this may not mean much, as all default values are used. 

You should have explicit values in the &LEW20 block, 
the &DIST block, and the &ICE1 block.

Here is a more meaningful input file, that runs Example 2-4 from the Aircraft Icing Handbook 
with a Langmuir D drop size distribution, with the geometry file 
/lewice/version3.2.3/BATCH/inputs/shapes/NACA0012.XYD:  

```text
AIHB Example 2-4
&LEW20
TSTOP  =  300.0
&END
&DIST
FLWC   =  0.05, 0.10, 0.20, 0.30, 0.20, 0.10, 0.05
DPD    =  6.2, 10.4, 14.2, 20.0, 27.4, 34.8, 44.4
&END
&ICE1
CHORD  =  0.9449
AOA    =  0.
VINF   =  102.89
LWC    =  0.5
TINF   =  253.15
PINF   =  69681.6
&END
&LPRNT
&END
&RDATA
&END
&BOOT
&END
```

LEWICE can optionally produce several large, detailed output files 
(45 MB may or may not count as "very large" on your computing system, 
it was in the Windows XP era). 
You may not need all of them, so choose carefully before setting values 
in the $LRPT namelist, 
particularly TPRT, which controls the water drop trajectory reporting.  

>6.11. Printer Flags  
Output files from LEWICE can be very large. If all of this information is not needed, the user
can save a great deal of disk space by not generating individual files or by reducing the amount
of information which is sent to those files. Example Case 2 illustrates this effect. As listed in this
example, the case produces 3.3 MB of output. If all of the printer flags are activated, the output
will exceed 45 MB...

## Next steps  

### Read the material that comes with the software  

The distribution comes with a "TRAINING" folder, 
the contents of which you are encouraged to read. 

The distribution comes with a "REPORTS" folder. 
You are encouraged to read them, particularly "datarpt.pdf",
which has Validation Results for LEWICE 2.0 
(also available at [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19990021235)). 
This quantifies the differences between LEWICE ice shape analysis and test results, 
for over 100 test cases 
(there are some repeated results of the tests, so there are hundreds of ice tracings.) 

(The current version of LEWICE is 3.2.3. 
However, the validation is re-run for each release, 
and the report for version 2.0 is still applicable.)

### Consider automation  

You are encouraged to run you first several analyses using the manual methods described. 
However, you may soon discover that some parts of this are repetitious, 
and are good candidates for automation. 

I have written a script that automate steps such as converting 
domain units (KTAS or MPH, altitude in feet, etc.) to the units used in the LEWICE
and to make the input file, 
as has almost every analyst that I know that has run LEWICE for more than a few cases. 

Processing the output files is also another candidate for automation. 
The file formats are often unique, and may require processing for subsequent use
(such as plotting dimensional quantities, not just s/c).  

The LEWICE manual describes a LewCon or LEWICE Console program, 
but it is only available for Windows (I have not used it).   

>Our goal was to improve LEWICE’s usability by creating a user interface that would
automatically generate LEWICE input from a spreadsheet and automatically put LEWICE output
into spreadsheets with charts. Additionally, this user interface would automatically convert units
(as LEWICE only accepts input in certain units) and offer several output options. This program
will be called the “LEWICE Console”...
> 
> These capabilities are just the beginning for the LEWICE Console...

Also see the commercially available [LewInt]({filename}intermediate_toolset.md#LewInt).    

## Resources  

User's Manual for LEWICE Version 3.2, NASA/CR-2008-214255 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20080048307)  
Note that a "manual.pdf" file comes with the LEWICE software distribution (apparently for version 3.0), 
and a file "Lew32manual_changes.doc". 
I find it easier to just use the Version 3.2 manual.  

Validation Results for LEWICE 2.0, NASA/CR-1999-208690 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19990021235)  
The current version of LEWICE is 3.2.3. 
However, the validation is re-run for each release, 
and the report for version 2.0 is still applicable.

Validation Results for LEWICE 3.0, NASA/CR-2005-213561 [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20050160961)  
Includes data for large drop size icing conditions.  

## Related  

Back to [Intermediate Topics]({filename}intermediate.md#intermediate-topics)  
