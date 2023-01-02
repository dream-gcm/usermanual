![chapter4](./img/chapter_4.png)
# Chapter 4: Total Recall - The Many Different Ways of Using DREAM

---
## 4.1 Running DREAM

### A tour of the job script
Let’s look in more detail now at `runmodel_v8.1.ksh`.

First you choose your resolution with `RESSP` and `RESGR`. They should match, i.e. T31G96 or T42G128. In fact if you choose a different combination the model will still run, so if for example you want to degrade the resolution of the grid-point calculations compared to the spectral resolution, or vice versa, it is possible but an unlikely use case. 

The next block of commands sets up the working directories and the fortran compiler and then we're into the namelists. A complete specification of namelist variables is given in Appendix C, and any one of them can be included here but the standard job script only contains the most commonly used.

* First we have `SETUP`, in which we specify the use cases `RUNTYPE`,`THERMTYPE` and `SSTZONE`. These are controlled in the include file `setup.f` mentioned above. 

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

That’s the basic overview - let’s look at some specific examples.


### Running DREAM as a simple GCM in perpetual mode
This is pretty straightforward. You want to simulate an equilibrium climate. You’ll need to decide how long you want to run it. Bear in mind that the model can clear about 50-days per minute at T31 and about half that at T42 - your mileage may vary !  I suggest doing a few short test runs before you plunge into your long reference runs. Run it for a few hundred days and do some diagnostics. You probably want to have a control simulation, and the some sort of experiment in which you perturb something. You’ll need to decide what perpetual season you want to simulate. 

So first set your resolution and set `RUNTYPE=“PERPETUAL”`. 
For a 100-day run you’ll set `KRUN=6400`. 
Is this a dry run or do you want explicit condensation processes ? Do you want them to affect the dynamics ? Set `THERMTYPE` accordingly. If you choose a `WET` or `INTER` run the model will automatically write `history_grid2d` files for the precipitation. 

The rest is just a matter of choosing files. Your initial condition would normally be an instantaneous field. Your forcing and reference files must agree: for example `ERAi_ave4x_1979-2016_DJF_fcm.b` and `ERAi_ave4x_1979-2016_DJF.b` in channels 13 and 16. 

When you come to do diagnostics you should skip a set number of spinup days and look at the mean (and maybe fluxes) over the remainder of the run. A spinup of about a month is usually sufficient. For statistically significant results for a climate signal you’ll have to experiment. The model can display some very low frequency variability so be prepared to do long runs. The length of the runs you’ll need to do depends entirely on how strong the perturbation you are testing is, and how strongly the model dynamics responds to it. 


### Running DREAM as a simple GCM with an annual cycle
This is again a GCM-style experiment so again we’re talking control and perturbation. But now you have an annual cycle, you’ll have to do a bit more work on the diagnostics, extracting seasonal means etc. And inevitably you’ll have four seasons to consider. 

Technically all you have to do is set `RUNTYPE=“CYCLE”` and choose your initial condition, forcing and reference states accordingly. The model will normally start at the beginning of the calendar year so your initial condition should be a first of January or at least some sort of boreal winter state, and you should consider a spinup. The forcing will be `ERAi_cyc4x_1979-2016_fcm_RM41.b` and the basic state will now also be an annual cycle sequence file `ERAi_cyc4x_1979-2016_RM41.b`. Both these files will step forward once every 6 hours, or 16 timesteps and will return at the end of a 365.25-day model year. 

It is possible to start the annual cycle at the beginning of any month by setting KBEGMNSST to the desired month between 1 and 12. The model will skip through the forcing and reference data until it gets to the right part of the annual cycle and start from there. And you don’t need to actually read SSTs or enable SST forcing in order to play this trick. If you do this the history records will have the correct time signature and your ensuing netCDFs will flag the correct calendar date. 

### Running DREAM as an ensemble forecast model
Ensemble forecast runs can be made in any configuration: perpetual, cycle or even idealised stationary wave runs with a fixed basic state. All that is required is to use a script that runs the model multiple times and then takes an average of the output. Such a scrip is available and it is called `run_ensemble.ksh`. 

The comments section at the beginning of this script is extremely comprehensive so just follow it. Basically you have to decide how many members your ensemble has, and how to initialise each member. The script assumes that all your initial conditions are gathered in a single file, one per record. It can read the initial conditions sequentially, or it can skip records at a fixed interval. This is useful if you’re using a previous long run to supply initial conditions. Some options for the initial condition file are already provided in /seq directory but you can also make your own. The script will copy each initial condition to a file called initial_condition which is overwritten as you run each member of the ensemble. 

A subdirectory is created in your experimental directory for the history records from each ensemble member. Each will have a run number appended to the file name: `history_n`. When all the members have run, the ensemble mean history is calculated and deposited up in your experimental directory. So note that the file in your experimental directory at the end that is called “history” is not a direct product of the model, it is the ensemble mean. This can also all be done for grid2d files if you have rainfall but you may need to uncomment those lines from the script. 