![chapter4](./img/chapter_4.png)
# Chapter 4: Total Recall - The Many Different Ways of Using DREAM

---
## 4.1 Running DREAM

### A tour of the job script
Let’s look in more detail now at `runmodel_v8.1.ksh`.

First you choose your resolution with `RESSP` and `RESGR`. They should match, i.e. T31G96 or T42G128. In fact if you choose a different combination the model will still run, so if for example you want to degrade the resolution of the grid-point calculations compared to the spectral resolution, or vice versa, it is possible but an unlikely use case. 

The next block of commands sets up the working directories and the fortran compiler and then we're into the namelists. A complete specification of namelist variables is given in Appendix C, and any one of them can be included here but the standard job script only contains the most commonly used.

First we have `SETUP`, in which we specify the use cases `RUNTYPE`,`THERMTYPE` and `SSTZONE`. These are controlled in the include file `setup.f` mentioned above. 

* `RUNTYPE` has five presents: `TRAIN`-to calculate forcing data, `CYCLE` and `PERPETUAL` for the type of forcing used, `UNFORCED` to run without forcing and `CHANNEL` which will execute a perpetual run with zonally uniform forcing (and optionally a zonally uniform initial condition, and there are further options for the type of symmetry or for adding long waves - but you’ll need either to edit the setup file or set the namelist manually). 

* `THERMTYPE` refers to moist thermodynamics. There are three options inspired by formula 1 racing: `DRY`, `WET` and `INTER`. `DRY` is just dry dynamics where the specific humidity variable is strictly a passive tracer with a source and sink in the forcing and so it has a reasonable climatology. `WET` has the model's large scale rain and deep convection schemes switched on. The model will produce rainfall and output it into grid files. And the heating from condensation will feed back onto the dynamics. `INTER` runs with dry dynamics but the rainfall schemes are switched on. So the model will produce rainfall and the humidity variable will not be just a passive tracer. But the feedback onto the heating is cut, so the dynamical development is the same is in a `DRY` run. 

* `SSTZONE` works with the SST forcing input and restricts it to a pre-defined zone, always in the tropics - either the entire tropical band or one of the three ocean basins. 

* Also in `SETUP` we have the basic run length `KRUN`. This is in timesteps and there are 64 timesteps per day. So if you want to run for 10 days, set `KRUN=640`. But what if you want to run for the entire month of January, with the initial condition at 00Z on 1st Jan and the final record at 18Z on 31st Jan ? That's 31 days right ? Well, no not really. If you set `KRUN=64x31=1984` and you  use the default value of `KOUNTH=16` (the output frequency in timesteps for 4x daily output) then your resulting history file will have 125 records, the first of which is your initial condition and the last one will be 00Z on 1st Feb. If you want to finish in Jan, you’ll need to set up the run to deliver 124 records, which means setting `KRUN=1984-16=1968`. It’s up to you of course, you do whatever you want. Are you more of an Orwellian bent, or more in the spirit of peace and love ?

* Finally in `SETUP` we have the important variable `KTFIN`. This is only needed when using the model to generate a forcing file (`RUNTYPE=TRAIN`). Set it to 1 to make a single-shot _fbs file. Set it to something else to scan through a longer set of initial conditions: values are given in the comments. 

* The other namelist is `INITIAL` and there are many choices here. Whatever you put here explicitly will override the defaults, and it will also override the use case scenarios provided in the setup file. So you can tinker here to your heart’s content. `KOUNTH` and `KOUNTFAN` are intervals for writing history records (channel 9) and reading spectral forcing anomaly data (channel 15) respectively. 
A multi-record forcing anomaly file will be read sequentially until the end and then rewound and read gain. 

* `KBEGYRSST` and `KBEGMNSST` are the year and month at which the model will start reading SST data when it is using SST data with metadata - for use in seasonal forecasts/hindcasts. This date will also be assigned to model output. 

* `LSST` controls whether the model reads SST data and the following switches determine what it does with it, including the type if transfer function to atmospheric heating and some timing options. Note that SSTs can heat the atmosphere even in `DRY` or `INTER` runs. 

* `LFAN` controls the reading and implementation of a spectral forcing anomaly, with scaling and timing options. 

* `LNUDGE` activates nudging. 

* `LSTAB` activates a uniform damping on all degrees of freedom, for use in stability calculations and derivation of time independent solutions when the basic state is unstable. 

* `LMODE` activates the modefinder, which turns the model into a crude eigensolver to get the fastest growing mode for a given basic state by timestepping. 

* `PRHEATMAX` sets the level at which the deep convective profile has its maximum amplitude. This applies to the deep convection scheme and also to the SST transfer function. 

After this we are into linking input and output files. We’ve already covered the input files in Chapter 2, and the rest is fairly self explanatory. The main file you will work with is the history file which is a binary output with sequential records describing the model state as spectral coefficients of the state variables. For diagnostic fields related to precipitation the model writes `history_grid2d` and `history_grid3d` as needed. These outputs are controlled by namelist options. Restart files are written periodically (`restart.11`) and at the end of the run (`restart.12`). These files contain two consecutive timesteps so in principle can be used to restart the model and continue the run. Some basic information about the run is written into the text file results. 

That’s the basic overview - let’s look at some specific examples