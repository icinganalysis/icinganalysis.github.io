# icinganalysis.github.io
Information about aircraft icing analysis, particularly in the era of the National Advisory Committee for Aeronautics 
(NACA), 1915 to 1958.

website [https://icinganalysis.github.io/](https://icinganalysis.github.io)

## How to install the software as a python package from github  

Ensure that you have python 3.7 or greater installed.
>python3 --version  

Ensure that you have Anaconda version 2021-11 or greater.  
Otherwise, you will need to have several packages installed (scipy, matplotlib, pyqt5 [for interactive plots], and dependencies)

python3 -m pip install git+https://github.com/icinganalysis/icinganalysis.github.io.git  

You should now be able to verify that the icinganalysis package is installed for you python installation.  
Here is an example using the REPL:  
```
> python3  
> import icinganalysis  
> print(icinganalysis.__dict__)  
```
(Outputs a long list of attributes.)
(CTRL-C to exit the REPL.)

You can now navigate to the icinganalysis directory and run, for example, 
> python3 naca-tn-779.py  

