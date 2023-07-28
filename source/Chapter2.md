![chapter 2 fig](./img/chapter_2.png)
# Chapter 2: Eyes Wide Shut - A Quick Start Guide to Running DREAM


## 2.1 Accessing the model
The DREAM code and a selection of data is currently hosted on GitHub:
[https://github.com/dream-gcm/DREAM](https://github.com/dream-gcm/DREAM)

You need to join the private DREAM project on github, so if you don’t already have a github account, the first step is to create one. Then contact us through the link on our web site to be invited to the DREAM private github page. Once you have been invited to the page, you’ll be able to download the model. Go to the model page, click on the green Code button to Download ZIP. Unzip it and you’re done. 

---
## 2.2 Compilation on your system
Now you’re on your computer and you have unzipped the directory named “DREAM-master”. Reaname this folder as DREAM, put it wherever you want, and go into this directory. 

First you’ll need to recompile the model libraries. Go into the “dream_model/source” directory to compile the model libraries on your computer (you should only have to do this once):

```
cd ./lib
./makelib.csh
cd ../..
````

and now you should be back in the dream_model directory.

---
## 2.3 Your first test simulation
Go into the `DREAM/dream_model/jobs` directory and open the script `runmodel_v8.1.ksh` (at time of writing).

Modify the root path `$KD` so it points to the DREAM directory:
`KD=/Users/yourname/DREAM` - for example

We recommend you compile the model with gfortran (so gfortran must be installed on your computer at this stage, along with its netCDF dependencies). Make sure that $FC is set to the name with which to call the fortran compiler on your machine.

The script writes a file that contains two namelists: SETUP and INITIAL. They contain the basic run parameters and a vast array of model parameters. For a first test run set:

* `KRUN=320` (your test experiment will be run for 320 timesteps, i.e. 320/64 = 5 days),
* `RUNTYPE="PERPETUAL"` (the model will run with fixed time independent forcing),
* `THERMTYPE="DRY"` (no moist thermodynamics).

Everything else should just behave itself and you will discover all the other options as you gain experience. 

The model also reads a number of files as input data and these can be seen in the last part of the script, assigned to the following fortran channels:

__Essential:__ 
* `10` - the initial condition - this can be anything you want - spectral
* `13` - the basic forcing - this will drive the model to simulate the season you choose - spectral
* `16` - the reference state - this must match the season chosen for the forcing - spectral
* `19` - the land-sea mask - grid

__Optional:__
* `20` - a nudging state - spectral,
* `15` - a forcing perturbation - spectral,
* `17` - either the full SST or a perturbation (SSTA) - grid,
* `18` - the climatological mean or reference SST - grid.

These data files all reside in `DREAM/dream_data` and its subdirectories. If there is a problem and the run doesn’t complete it will probably be because one of these files is specified incorrectly. 

To run the model execute the script in a terminal:

`./runmodel_v8.1.ksh`

The model will run, developing over five days from its initial condition, subject to the forcing you have specified.

---
## 2.4 Postprocess the model output
If the model has run without errors, some output files have now been produced and stored in `DREAM/dream_results/$EXPDIR`  (the default name for `$EXPDIR` is test_run).

The post processing code resides in `DREAM/dream_model/diagnostics`. There are many scripts here that produce a large variety of diagnostics, including sequences, time means and fluxes with output options for netCDF and binary grid. 

The simplest operation is to write a time sequence of netCDFs on model levels, using defaults for the choice of variables and levels. Edit the script run_output.ksh so it contains your path (set `KD`) and choose the values of logical switches lmean - if you want to calculate the time mean of your output and lseq if you want a sequence. 

Execute this script from within its directory

`./run_output.ksh`

and if all goes well, you will find some netCDFs in your experiment directory `DREAM/dream_results/test_run/netcdfs`

The probability of all going well is less than unity !  Typically there is some work to do to make sure your version of netCDF is compatible with your fortran compiler. 

The netCDFs are labelled with reference to resolution, variable name and level. So for example `dreamT31L15_u_250.nc` is output from the model run at T31 with 15 levels, zonal wind at 250 mb  
( but it’s not really millibars - in fact it’s output on the sigma=0.25 level, but it is close to data on a pressure surface because DREAM runs without orography and the surface pressure in the data is actually mean sea level pressure - see [Appendix A](https://dreamusermanual.readthedocs.io/en/latest/AppendixA.html)).

Now you can plot these variables and compute any diagnostics you want with your favourite tools and programs for dealing with netCDF datasets.

---
## 2.5  Further notes on installation
gfortran is strongly recommended, with netCDF libraries and big endian option. 

Example of the compilation line for the model code: 

```
gfortran -fdefault-real-8 -fconvert=big-endian -fno-align-commons -w -O3 -I/opt/local/include/ -L/opt/local/lib -lnetCDF -lnetCDFf
```

With gfortran version > 10.1.0 you need to add the option `-fallow-argument-mismatch` to the compiler when you compile the diagnostics code calling for the netCDF libraries. 

Example of the compilation line : 

```
gfortran -fdefault-real-8 -fconvert=big-endian -O3 -frecord-marker=4 -w -fallow-argument-mismatch -fno-align-commons specan_W2G.f -o a.out -I/usr/local/include/ -I./include -L/usr/local/lib -lnetCDF -lnetCDFf -L/yourpath/DREAM/lib -lfft -lblas -lutil -laux
```
---
## 2.6 So what else do you need to know ?
* I want to know where are all the files are stored and what are they’re all for - see [Chapter 3](https://dreamusermanual.readthedocs.io/en/latest/Chapter3.html).
* I want to go further with diagnostics and understand the data structure and timing - see [Chapter 3](https://dreamusermanual.readthedocs.io/en/latest/Chapter3.html) and [Appendix A](https://dreamusermanual.readthedocs.io/en/latest/AppendixA.html).
* What is the physical and numerical specification of this model ? - see [Appendix A](https://dreamusermanual.readthedocs.io/en/latest/AppendixA.html).
* What’s the difference between a GCM run and a perturbation experiment ? - see [Chapter 4](https://dreamusermanual.readthedocs.io/en/latest/Chapter4.html) and [Appendix B](https://dreamusermanual.readthedocs.io/en/latest/AppendixB.html).
* How is the basic forcing calculated ? - see [Chapter 4](https://dreamusermanual.readthedocs.io/en/latest/Chapter4.html).
* How do I make an anomaly forcing file ? - see [Chapter 4](https://dreamusermanual.readthedocs.io/en/latest/Chapter4.html).
* What are all those parameters in the namelist for ? - see Appendix C.
* I want to run ensemble forecasts, with an annual cycle, and nudging, and SST anomalies, and deep convection - whoah, calm down, one step at a time, it’s all in [Chapter 4](https://dreamusermanual.readthedocs.io/en/latest/Chapter4.html). 
* I want to know everything about how the model works - I’m afraid you have no choice but to look at [Appendix D](https://dreamusermanual.readthedocs.io/en/latest/AppendixD.html), good luck.

and finally…

* I’ve successfully used DREAM and my results are astonishing ! I think this is a major contribution to atmospheric science which will launch my career. My first draft is ready - Congratulations ! Now don’t forget about the rest of us - see [Chapter 5](https://dreamusermanual.readthedocs.io/en/latest/Chapter5.html).



