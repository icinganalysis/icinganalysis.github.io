# icinganalysis.github.io
Information about aircraft icing analysis, particularly in the era of the National Advisory Committee for Aeronautics 
(NACA), 1915 to 1958.

website [https://icinganalysis.github.io/](https://icinganalysis.github.io)

## How to install the software as a python package from github  

__DRAFT__  

Ensure that you have python 3.7 or greater installed.
>python3 --version  

Ensure that you have Anaconda version 2021-11 or greater.  
Otherwise, you will need to have several packages installed (matplotlib, scipy)

python3 -m pip install git+https://github.com/icinganalysis/icinganalysis.github.io.git  

You should now be able to verify that the icinganalysis package is installed for you python installation.
> python3
> import icinganalysis
> print(icinganalysis.__dict__)
