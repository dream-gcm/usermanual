![chapter4](./img/chapter_4.png)
# Chapter 4: Total Recall - The Many Different Ways of Using DREAM

---
## 4.1 Running DREAM

### a. A tour of the job script
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


### b. Running DREAM as a simple GCM with an annual cycle
This is again a GCM-style experiment so again we’re talking control and perturbation. But now you have an annual cycle, you’ll have to do a bit more work on the diagnostics, extracting seasonal means etc. And inevitably you’ll have four seasons to consider. 

Technically all you have to do is set `RUNTYPE=“CYCLE”` and choose your initial condition, forcing and reference states accordingly. The model will normally start at the beginning of the calendar year so your initial condition should be a first of January or at least some sort of boreal winter state, and you should consider a spinup. The forcing will be `ERAi_cyc4x_1979-2016_fcm_RM41.b` and the basic state will now also be an annual cycle sequence file `ERAi_cyc4x_1979-2016_RM41.b`. Both these files will step forward once every 6 hours, or 16 timesteps and will return at the end of a 365.25-day model year. 

It is possible to start the annual cycle at the beginning of any month by setting KBEGMNSST to the desired month between 1 and 12. The model will skip through the forcing and reference data until it gets to the right part of the annual cycle and start from there. And you don’t need to actually read SSTs or enable SST forcing in order to play this trick. If you do this the history records will have the correct time signature and your ensuing netCDFs will flag the correct calendar date. 

### Running DREAM as an ensemble forecast model
Ensemble forecast runs can be made in any configuration: perpetual, cycle or even idealised stationary wave runs with a fixed basic state. All that is required is to use a script that runs the model multiple times and then takes an average of the output. Such a scrip is available and it is called `run_ensemble.ksh`. 

The comments section at the beginning of this script is extremely comprehensive so just follow it. Basically you have to decide how many members your ensemble has, and how to initialise each member. The script assumes that all your initial conditions are gathered in a single file, one per record. It can read the initial conditions sequentially, or it can skip records at a fixed interval. This is useful if you’re using a previous long run to supply initial conditions. Some options for the initial condition file are already provided in /seq directory but you can also make your own. The script will copy each initial condition to a file called initial_condition which is overwritten as you run each member of the ensemble. 

A subdirectory is created in your experimental directory for the history records from each ensemble member. Each will have a run number appended to the file name: `history_n`. When all the members have run, the ensemble mean history is calculated and deposited up in your experimental directory. So note that the file in your experimental directory at the end that is called “history” is not a direct product of the model, it is the ensemble mean. This can also all be done for `grid2d` files if you have rainfall but you may need to uncomment those lines from the script. 

### c. Running DREAM as a perturbation model with a fixed basic state
This is the story of a dynamical model with a climatological initial condition, and of the one forcing that will cancel all its tendencies. It’s Arrested Development. 

You should try this first: set  `RUNTYPE=“PERPETUAL”` and  `THERMTYPE=“DRY”`
and then initialise with the climatology `ERAi_ave4x_1979-2016_DJF.b` in channel 10 and also as a reference state in channel 16. 

Then use:
`$DATADIRSP/fbs/ERAi_ave4x_1979-2016_DJF_fbs.b` as the forcing in channel 13. 

Make sure `LSST` and `LFAN` are both set to `.F.` Run for about 10 days and you’ll get the idea. There should be no development. The model reports its 100th spectral coefficient of vorticity every time it outputs history, and you’ll see that number scroll down the screen, unchanging, except on the last couple of decimal places at machine precision. This tiny development is due to rounding errors and if your basic state is unstable, which it will be if it’s a mean winter state, then this will grow like Lorenz' butterflies until it reaches finite amplitude, usually a few hundred days into the run. 

In the meantime you’ve got plenty of time to do perturbation experiments. There are two ways to perturb the run so that it develops an anomaly. You can change the initial condition (more on that in section 4i), or you can add a perturbation to the forcing. Here we will concentrate on the latter. 

Forcing perturbations can be introduced either through a direct perturbation in spectral space, setting `LFAN=.T.` and reading a `_fan` file into channel 15, or through an SST anomaly, reading SST data into channels 17 and 18. 

Try repeating the run you just did, and adding one of the forcing anomalies in `dream_data/T31/fan`. A deep heating in the tropics will set off a classical chain of events: tropical Kelvin and Rossby waves going east and west, then a Rossby wave propagating out into the extratropics and finally baroclinic waves on the extratropical jets that propagate eastwards and grow exponentially. You can diagnose all these effects by looking at the difference between the solution and the initial condition / basic state. 

You can also control the amplitude of the perturbation directly from the job script using `SCALEFAN`. Double the forcing anomaly by setting `SCALEFAN=2`. Change its sign of by setting `SCALEFAN=-1`. If you set `SCALEFAN` to a very small number, say 0.0001, the model response will be correspondingly small and will develop as a linear perturbation around the basic state. You can scale it back up for presentation in the diagnostics. 

By default the forcing anomaly is fixed and persistent. As already discussed you can make it time-dependent by using a sequential file, leading to a cyclic forcing perturbation. More simply, you can also create a short-lived initial pulse of forcing anomaly with LPULSE, using `KPULSE` to determine the length of time in timesteps over which the initial pulse grows and decays symmetrically in time following a sin-squared curve. The integrated amplitude is normalised so that it is equivalent to having a fixed amplitude pulse over the same time interval. 

If you wish to perturb a fixed basic state with an SST anomaly instead there are various considerations about how the model responds to SST data that are covered in section 4iv, but the basic principles are the same, and there are also options for scaling the perturbation in this case. 

To diagnose perturbation runs it’s best to subtract the climatology from the model state, and this can be done in the diagnostics package, furnishing netCDFs that look like anomalies on a resting state. Of course you can also do this independently of the code presented here by using your own software to compare netCDFs generated by the perturbation run with a netCDF of the basic state. As always, it's up to you.

---
## 4.2 Calculating the forcing
The theory of how a set of one-timestep tendencies can represent either diabatic and transient eddy forcing is laid out in Appendix B. Simply put, the _fcm forcing represents just the diabatic terms that are normally parameterised in a GCM. The _fbs forcing represents the sum of this diabatic forcing and the systematic effect of transient flux convergence, often termed “transient eddy forcing”.  The latter is simpler to calculate so we’ll start with that. 

### a. Forcing a perturbation model with a fixed basic state
Suppose you have a basic state that you want to use for perturbation experiments. You want the model to develop as a response to your perturbation, in conjunction with this basic state. The first thing you need is a forcing that will stop the basic state from evolving. 

To find this forcing, you take your basic state, use it as an initial condition (channel 10) and also as a reference (channel 16) and run the model with no forcing at all, for just one timestep. To achieve this, all you have to do is set `RUNTYPE=“TRAIN”` and `KTFIN=1`, and make sure all your perturbations are switched off (`LFAN=.F.` and `LSST=.F.`). This setup will impose dry dynamics, switch off the basic forcing and run the model for one timestep. 

When your run is complete (it happens very quickly) you need to use the information from the initial condition and the result after one timestep. These are both in your experimental directory as history and restart.12. In the job directory the script makefrc.ksh consults these two files to find the tendency and thence the forcing. Remember to set `KTFIN=1` in this script in the namelist `ktfin_input_data`  and set the call to the `calcfrc.f` fortran program to the correct resolution. Then all you have to do is make sure your output is renamed to the appropriate file, which should finish with `_fbs.b`. This can be in your experimental directory for specific applications or if you want to keep it across multiple experiments put it in dream_data in the appropriate `/fbs` directory. 

To check that it worked, try running the model in `PERPETUAL` mode (forcing will be switched back on and the model will run to whatever you have set as `KRUN`). You should get zero development as described above (be careful interpreting the `Z(100)` output on the screen for very simple basic states - it is likely to be zero so you’ll get some very small numbers that dance around at machine precision). 

Remember - every time you change anything in the model, damping parameters for example, you will need to recalculate the forcing. 

### b. Forcing a simple GCM in perpetual mode
The forcing for a simple GCM is fundamentally different because it represents only the diabatic forcing and not the transient eddy part. In a fully turbulent GCM simulation the transient eddies are explicit and so their mean fluxes are represented explicitly in the simulation, they are not present in the forcing. But to calculate this _fcm forcing we follow exactly the same procedure as for the _fbs forcing, and use the same code. 

The only thing that differs is the value of `KTFIN`. Now we have to scroll through a long list of initial conditions, running for one timestep from each of them. In principle it doesn’t matter what order the initial conditions come in, but in practice it is usually a time sequence. 

There is a big loop in the model that scrolls through this sequence when training mode is activated. The initial condition should therefore be a `_seq` file for whatever season or composite you are interested in. The reference data should be set appropriately to the seasonal mean. And `KTFIN` should be set to the number of records in the sequence (some values are given in the job script for the data provided). Don’t forget to set `KTFIN` to the same value in the job script and in the makefrc script. After looping for a while, first to run the model and then to find the average tendency, you’ll get a `_fcm.b` file - make sure you put it in the right place, i.e. in a `/fcm` directory. 

There is no simple way to check that it worked this time. You’ll just have to use it as a forcing for a long run of the simple GCM, with whatever initial condition you want, and a suitable spinup period, and then validate. 

### c. An aside on reference data
Every time you do an operation like this you need to use the appropriate reference climatology in channel 16. This seems like a pain, and to be honest it is, and it’s not strictly necessary if all the dissipation in the model is linear. This is just the way it evolved. In principle, any reference file could be substituted in and give the same result, because the forcing that you calculate would simply redress the large tendency associated with whatever reference state you use. DREAM could therefore be configured to avoid this reference state altogether and have one less input file to worry about. But that’s not the way it has been done, and in fact the reference state does play a role in some very nonlinear bits of the model, especially concerning deep convection and the response to SSTs. 

### d. Forcing a simple GCM with an annual cycle
The procedure for finding the annual cycle forcing is not so straightforward, and the theory is outlined in Appendix B. The forcing consists of an advective part, calculated with the model, and a tendency part, calculated directly from the data. To calculate the advective part the procedure for running the model is the same as above with a very long sequence of consecutive years. But the time averaging is now cyclic in nature so the resulting forcing file is a sequence. The tendencies are calculated in the script makefrc_cyc.ksh but the cyclic averaging must be done manually using the code in data_process/prep_cyc (see Chapter 3, section 2). The full procedure to calculate the annual cycle forcing is: 

First step:
* Calculate the annual cycle of the data: `annual_cycle_spec.f`
* Smooth it: `cyclic_running_mean_spec.f`
* Use it to calculate the tendency part: `calcfrc_cycTEND.f`

Second step:
* Calculate the advective part using the model: `makefrc_cyc.ksh` and `calcfrc_cycADV.f`
* Calculate its annual cycle: `annual_cycle_spec.f`
* Smooth it: `cyclic_running_mean_spec.f`

Final step:
* Add the two cycles together (the tendency and advective parts): `add2_hst.f`
* Smooth it all again: `cyclic_running_mean_spec.f`

### e. How to calculate forcing perturbations
There are many ways to perturb the model. Let’s start with a simple idealised heating perturbation. In `data_process/prep_fan` open the script `makefan.ksh`. This script will help you to make a spectral forcing perturbation file `_fan.b` by specifying the shape and amplitude of your forcing in grid space. 

To do this you will need to edit the fortran program `makefan.f`. This program is set up to generate idealised perturbations either to temperature T or vorticity Z. The first thing it does is set up the amplitude. Then you decide on your vertical profile. There are many to choose from (see `notes_for_forcing_anomalies.rtf`) or you can invent your own. Make sure it integrates to unity between sigma=0,1. Then you specify four coordinates: the longitude and latitude of the centre of the anomaly, and its radius in longitude and latitude directions. The program will fill this ellipse with a cosine-squared bell function and put zeros outside it. Note that makefan.f works on a T42 Gaussian grid but the output can still be used to make T31 forcing anomalies.

Back to the script and the output from makefan.f is fed into a spectral analysis routine `specanANOMT42.f` (or T31 if you want). Use the resulting `temp_fan.b` file in the model (channel 15) and see what it does. You can have no end of fun. 

If you want a time-dependent forcing perturbation then you can create a time sequence with `makefan_seq.f`, which will allow your idealised source to move. It is set up to translate uniformly from a beginning position to an end position. It can also grow, shrink or change shape as it goes, but for the moment the vertical profile is fixed. 

Sequences of forcing anomaly data are read by the model at a frequency determined by the namelist variable `KOUNTFAN` until it reaches the end of the sequence, then it will rewind and repeat. If you want to be a bit less idealised, then you can read the forcing anomaly from grid data using `makefan_ReadGrid.f`. These programs should serve as an example of how it’s done and form this basis you can develop your forcing anomalies as you please. 

---
## 4.3 Diagnosing the output

### a. Time-mean diagnostics
So you’ve run the model and successfully produced a history file with all the model dynamics. And if you ran the wet version you might have `history_grid2d` and `3d` with rainfall and diabatic heating as well. Well done, you’re about half way there. It remains to convert this information into useable form and then visualise it. 

There are a few basic ways you’ll want to visualise the output. The diagnostics package is very focussed on horizontal maps on selected model levels. These can be written straight to netCDF, and there is a fairly comprehensive set of diagnosed variables. For vertical sections you’ll have to delve into the binary 3d output and do it yourself. And then there are a few basic arithmetic operations you’ll want to do: time sequences and time averages; anomalies from a reference state, and possibly time-mean second order transient fields, with various time-filters. This is all possible in the diagnostics package. Needless to say this is all in the `dream_model/diagnostics` directory. 

Let's start with the simplest option: a time sequence and/or time mean of the basic dynamical diagnostics on selected model levels. Have a look at `run_output.ksh`. After choosing your resolution you then select the records to be included in your time mean: you skip nspinup records and then average over nmean records. If nmean is greater than the number of remaining records the average will be just over the remainder of the sequence (note that these two parameters only affect the time mean, the sequence output will go through the whole history record regardless). If you want to take the mean of the whole sequence just set them to `nspinup=0` and `nmean = something big`.

After this we have the usual directory allocation as in the model job script. Then there are various choices on what kind of output you want and where to send it. 

`HISTID` and `FILTER` are strings appended to history files and output directories to distinguish them from one another. For example it might be useful to set `HISTID="_DJF"` and `FILTER="_mm"` or `"_hp"` if you’re dealing with data from various seasons in the same directory, and you want to treat monthly mean or high pass components. More on that later. 

`REFSP` and `REFGR` are reference states for spectral and 2d grid point data that you might want to subtract from your results to display an anomaly. To do so set lsubtractsp and lsubtractgr to true. 

You can choose to calculate a time mean and/or a sequence by setting lmean and lseq. If you have 2d or 3d grid data from the run and you want output from it set `lreadgrid2d` and `lreadgrid3d` accordingly. Remember the 2d grid comprises fields related to precipitation and the 3d grid data is just the associated diabatic heating. 

`run_output.ksh` is a high level script and most of the action takes place one level down in the script it calls: `model_output.ksh`, let's have a look. After a bit of file handling you see that this script is split into two sections: the time mean output and the sequential output. 

For the time mean output there are two namelists. The first passes information that we’ve already set up about the averaging period to the fortran code. The second namelist is used to for output options. The levels for output are chosen with `LEVOUT`. Set it to true for each level required: the list of levels is given in the comment. This namelist also picks what kind of binary grid output you want, if any. `LBINDYN` and `LBINPPT` will send basic dynamical fields and precipitation information respectively to binary output. If you want full 3d information rather than just level by level then activate `LBIN3D`. Note that it is assumed that netCDFs are always wanted on the levels chosen so there isn’t a way to switch that off !  

The script then calls the fortran program `time_mean_spec_grid.f` to do the averaging operation on the spectral and grid history files. This produces single-record average history files: `history_ave` and `history_grid2d_ave`, in your experimental directory. These history files are then fed to the main analysis programs: `specan_W2G.f`, and if needed `gridan2d.f` and `gridan3d.f` (details of the binary file structures are given in Appendix A). 

`specan_W2G.f` calls the spectral analysis routines from the model and then does some analysis in grid space to produce a number of diagnostics which it sends to netCDF and binary grid output. The fields it produces are labelled as follows: 

* chi` - velocity potential - m2/s
* `div` - divergence - s-1
* `gph` - geopotential height - m
* `omega` - pressure vertical velocity - mb/hour
* `psi` - streamfunction - m2/s
* `q` - specific humidity - kg/kg
* `sp` - surface pressure - mb
* `T` - temperature - deg C
* `u` - zonal wind - m/s
* `v` - meridional wind - m/s
* `vort` - vorticity - s-1.

Apart from geopotential height and vertical velocity, which are calculated in the diagnostics program, these variables are all direct from the model’s state variables. 

The gridan programs are more limited in scope and only concern grid output from model runs with moist thermodynamics enabled. 

* `ppt` - precipitation rate - mm/day
* `vimc` - vertically integrated moisture convergence - mm/day
* `vicw` - vertically integrated column water - mm
* `visf` - vertically integrated saturated fraction - nondimensional
* `pptdeep` - precipitation rate from the deep convection scheme - mm/day
* `condheat` - condensation heating (3d variable) - degrees/day.

### b. Sequence diagnostics
The second half of model_output.ksh repeats these operations for the sequential model output. So it will produce netCDFs with a time dimension. There is nothing new to say about this, it is just a repeat of the calls used for the time mean. The only thing worth mentioning is that the namelist input is written again here - so you have the opportunity to make different choices for time mean and sequential output. You could, for example use different levels for time mean and sequential data, or plot full fields for the time-mean and anomalies for the sequence, or request binary output only for the time-mean, or whatever combination you desire. All these choices are for the moment in this lower level script as I expect them to be fairly standardised, and thus choose not to clutter the top level scripts. 

### c. Time-filtered transient fluxes, variance and eddy kinetic energy
It remains to discuss time filtering and second order products. This is a fairly recent development and it is all dealt with from the script `run_output_flux.ksh`. This starts off the same way as run_output.ksh to do the basic mean and sequence diagnostics. Then the script deals with filtering and fluxes. The sequence of operations is as follows:

1. Run model output on history file, skipping spinup, with sequence and mean output. A copy of run_output.ksh so you only need to run this one script. Note that lbinflux is set to true, so further sequence and mean diagnostics are output to binary grid. These extra files include eddy kinetic energy, momentum flux and zonal and meridional fluxes of temperature and specific humidity, as well as geopotential height and vertical velocity. 

2. Create low pass and monthly mean history records. Calls `time_filter_history.f` to produce sequential history files with block mean values. So each record of the resulting history files is a contiguous mean of `NBLEN` records from the original history file. If this block length `NBLEN=12` for a low pass filter, this corresponds to consecutive 3-day means. Diagnostics from this sequence will be like from the original sequence with a crude 6-day low pass filter applied. If `NBLEN=120` then the sequence will contain consecutive monthly means. These reduced block-mean history sequences are labelled `_lp` and `_mm` respectively. 

3. Run model output for low pass and monthly mean, for sequence output only. Low pass and monthly mean sequence diagnostics are produced for further calculations.  

4. Run model flux level by level for total flux, low pass and monthly mean. The script `model_flux.ksh` takes the time mean of the sequences just produced, squaring the geopotential height and vertical velocity as it goes to output mean standard deviations of these quantities. These mean quantities are written to netCDF providing the following diagnostics: 

* `gph` - standard deviation of geopotential height - m
* `omega` - standard deviation of vertical velocity - mb/hour
* `eke` - eddy kinetic energy - m2/s2
* `uv` - momentum flux - m2/s2
* `uT` - zonal temperature flux - deg C m/s
* `vT` - meridional temperature flux - deg C m/s
* `uQ` - zonal specific humidity flux - kg/kg m/s
* `vQ` - meridional specific humidity flux - kg/kg m/s.

This is done level by level for the total unfiltered quantities, low pass and monthly means. The three levels chosen are 250, 500 and 850. 

5. Calculate high pass fluxes level by level. It remains to subtract the low pass quantities from the total to give the high pass component. 

6. Run model flux level by level for high pass netCDF output. And output netCDFs of that. 

Finally, if you do decide to use the filtered-transient package, bear in mind that it is relatively untested so pay attention to all the switches and directory names along the way. You’ll probably have to be quite hands-on and it would be best if you had a good look at the code rather than using it as a black box. 

---
## 4.4 Going further

### a. Diagnosis of normal modes and time-independent solutions
Linear analysis around a fixed basic state is one of the things that DREAM has been used for quite a bit. For mathematical details see Appendix B section 3. The trick of fixing the basic state in a time-stepping model allows you to track the response to a perturbation in the forcing for a limited time, usually about 20 days. After this, the instability of the basic sate starts to manifest, in the form of exponentially growing modes that usually look like midlatitude wavetrains. They can be a nuisance, because they are pretty independent of whatever carefully designed perturbation you are trying to study. On the other hand they can be interesting in their own right as a fundamental property of the basic state. 

DREAM has provisions for addressing both these concerns. So if you want to study the structure and growth rate of the fastest growing normal mode on a given basic state, you can enable the modefinder. Choose your basic state. Set the forcing to maintain it as explained above. Then set `LMODE=.T.` in the namelist. Oh and make sure you initialise with a state that has enough multi-scale information to break the symmetry of whatever basic state you’re using, especially if it is zonally uniform, because the modes you’re looking for won’t be zonally uniform and they have to grow from something. 

The model will call the subroutine `SCALEDOWN`, which compares a mid-level mean mean-squared vorticity norm with a standard value. For a growing perturbation on an unstable basic state, every time the ratio creeps up above 10, the difference between the model state and the basic state will be scaled back down. This is also done to the tendency so the model will continue seamlessly. To start with, this perturbation will be a mess, because it will contain many different modes. But you’ll need to run it for a good long time, and as the run progresses, the fastest growing normal mode will eventually dominate, and the signal will be a pure shape-preserving mode that cycles sinusoidally between phases and grows exponentially. You can analyse it using the simple program `data_process/data_main/growth.f` (remember the norm is quadratic). 

If your basic state is stable, then you’ll have no long term growing modes but don’t worry. Instead of scaling down, the model will scale up, and you’ll find the slowest decaying mode. 

The stability or otherwise of the basic state depends on both its three-dimensional structure and on the dissipation parameters chosen in the model run. If instability is an undesirable property, then we can do our best to eliminate it but adding extra damping to the model. If you set `LSTAB=.T.` some extra linear damping will be added equally to every degree of freedom of the model, thus preserving the modal structure of the basic state. The damping rate is set in days with `TAUSTAB`. If you’ve already diagnosed the growth rate of the fastest growing mode of your basic state with the modefinder, then you know what value of `TAUSTAB` you need to use to kill it. But remember, every time you mess with the model, in this case by altering its dissipation, you will need to recalculate the `_fbs` file that maintains the basic state. 

What if you’re interested in the time-independent response to a given forcing anomaly but your basic state is unstable ? Time stepping the model will not converge to a fixed anomaly solution, but rather degenerate into instability and chaos. But if you stabilise your basic state you’ll find that you can then repeat your perturbation experiment and a long run will converge to a time independent state. You don’t get something for nothing though, because the extra damping will considerably weaken the response so it won’t be the same as the imagined time-independent response with standard damping parameters. A crude fix to this is to use various values of `TAUSTAB` and then extrapolate back to zero extra damping. The fortran program `data_process/data_main/TILS.f` will calculate the solution using a quadratic extrapolation with three values of `TAUSTAB` (note that the extrapolation is actually done in terms of damping rate, not timescale). `TILS` stands for Time Independent Linear Solution. It will only be linear if by construction your perturbation is small. Otherwise it’s nonlinear but it will still work. 

### b. Nudging
Set `LNUDGE=.T.` to activate the nudging option. This is a linear relaxation towards a prescribed state that takes place in grid space. This makes it possible to nudge specific regions whilst leaving the solution unconstrained over the rest of the globe. It’s useful to evaluate the remote impact of some observed sequence of events. 

The nudging state is separate from the rest of the input data and so can be different to the model’s reference state. It can be a single-record fixed state or a sequence. The model will read the next record from this file periodically, at a frequency that can be set to `KOUNTNUDGE` timesteps (default 16, i.e. 6 hours). If it reaches the end of the file it will rewind and start again. Each time the nudge state is read it is transformed to grid space and the variables `u`,`v`,`T`,`q` at all levels and sp are relaxed towards this state on a timescale specified by `TAUNUDGE` (default 6 hours). 

The region in which nudging occurs is defined by the grid coordinates `IWNDG`, `IENDG` for the western and eastern boundaries and `JNNDG`,`JSNDG` for the northern and southern boundaries which define the mask `RMASKNDG` (see Appendix A for details of the model grid). The strength of the nudging is halved on the grid boundaries for a smooth transition to un-nudged regions. 

### c. Moisture, condensation and convection
When you choose the setup option `THERMTYPE=“WET”` you are activating schemes that will condense water vapour to produce precipitation and heating. The conditions under which this happens, and the amount and distribution of precipitation and heat requires some explanation, as  the user has a great deal of control over these routines. The three essential switches that are thrown to positive are `LCHX`, `LLSR` and `LDEEP`. Let’s take them in reverse order. 

#### Deep Convection:
`LDEEP` activates the model’s deep convection scheme. This is a semi-empirical home-grown scheme that first decides for a given grid point whether deep convection takes place, then calculates the amount of precipitation produced, and accordingly modifies the tendencies of specific humidity and temperature. Before it calls the deep convection scheme the model does a quick check on how much water there is, by calling a routine called `PWATER`. For a given grid point this routine calculates the amount of water in the column in mm, and the amount of water there would be in the column if it were saturated. If the option `LTRUNGQ` is enabled (by default it is) these calculations are done with a smoothed humidity field. `PWATER` also calculates the vertically integrated moisture flux convergence (mm/day) at that instant in the model and also for the model reference state. 

Then the model calls its convection scheme `DEEPTEND`. The first task is to decide whether to do anything. Convection is triggered only if the following criteria are met: 

The column integrated moisture flux is convergent. 
The moisture flux convergence is stronger than the reference value by more than a certain threshold (the default for this threshold is zero so in fact it’s a simple comparison with the reference state). In fact this criterion is evaluated with a smoothed version of the moisture flux convergence, spectrally truncated to an equivalent wavenumber T15 (this can be modified by setting `NNTRUNC`). So the model convection scheme sees the large scale moisture flux convergence, not the fine details. 
The low level temperature difference between the bottom two layers and the next two layers up exceeds the reference value (in the sense of the boundary layer being less statically stable than the reference state). 

The third criterion is optional and can be disactivated by setting `LBLSI=.F.`.

If deep convection is triggered then the amount by which the tendencies need to be adjusted is calculated with reference to a condensation time scale `TAUCOND` (default value 90 minutes). The amount of precipitation that will fall within this period is set equal to the moisture flux convergence multiplied by this time period. But there are a few modifications to this simple rule. First, it is the smoothed flux convergence that is used in this calculation. Second, we set limits to how much water can fall in the period `TAUCOND`. It can’t exceed the total column water. And it can’t exceed an imposed threshold rain rate `PPTCAP` (mm/day), but is only permitted to approach it asymptotically. The default value for `PPTCAP` is 15 mm/day but it is of course a user tuneable parameter. 

The reason for imposing all these controls on the amount of condensation associated with the divergent flow is that we need to tackle the beast known as CISK (Convective Instability o fthe Second Kind). CISK plagues simple models with condensation heating schemes that are linked to the divergent flow. It can lead to runaway grid-point instability and this has been observed in DREAM under certain parameter regimes. 

All that remains is to calculate the actual tendencies for the specific humidity and the temperature.  This is tackled in the subroutine `PROFILEHEAT`. Again if the option `LTRUNGQ` is enabled (by default it is) these calculations are done with a smoothed humidity field. The rate of loss of water in the column is distributed proportionally to the humidity content. The associated diabatic heating is distributed into a deep convective profile, meaning there is an implied unresolved moisture transport in the column. By default the heating profile peaks at sigma=0.35. But you guessed it, the peak level of the heating is a user definable parameter, set with `PRHEATMAX` in the namelist. 

#### Large Scale Rain:
Once the deep convection scheme as done its job, whatever super-saturation is left gets mopped up by the large scale rain scheme, activated by the option `LLSR`. The subroutine `LSRTEND` calculates the difference between the the specific humidity and its value at saturation. If the option `LTRUNGQ` is enabled (by default it is) these calculations are done with a smoothed humidity field. If the specific humidity exceeds the saturation value then this difference is condensed in-situ, for every grid location at every level. The timescale over which the condensation is to take place is again given by `TAUCOND`, and the appropriate negative tendency is applied to the specific humidity. The associated diabatic heating is also applied in-situ to the temperature tendency. 

#### Forcing Modification:
All these calculations for tendencies of humidity and temperature based on parameterisations of physical processes are bound to have a non-zero time-mean effect. There will be a net sink of moisture and a net source of heat. This is clearly in opposition to the DREAM philosophy of deriving climatological sources and sinks of state variables from data, using residual tendencies from the unforced dry model. We are effectively double counting, and so some correction must be made for this in the basic forcing. In fact it turns out to be crucial to obtaining realistic simulations. The rain schemes don’t have much work to do if realistic time-mean sources and sinks are already provided on the right hand sides of the equations. 

One objective way to proceed is to hand over all the condensation to the explicit schemes, while continuing to provide the evaporative sources. This is what happens when `LCHX` is enabled. The forcing for specific humidity is retained where it is positive, but set to zero wherever it is negative. When `LCHX` is enabled, the humidity variable quickly develops to supersaturation, and the explicit condensation processes kick in. 

There is also a modification to the temperature forcing to account for exactly the amount of condensation that has been removed from the humidity forcing. Note that this correction to the temperature forcing depends on the value of the latent heat of condensation. This can be modified by the user through the factor `SCALELHEAT`. In particular, if `THERMTYPE` is set to `INTER`, then `SCALELHEAT=0` and we recover dry dynamics with working rainfall schemes. The moist thermodynamics is present, but completely decoupled from the dynamical solution. In this case only the specific humidity forcing is altered, not the temperature forcing. But whatever the value chosen for `SCALELHEAT`, be it zero, unity something in between, or even greater, the model will incorporate it into the `LCHX` correction made to the temperature forcing.

This pragmatic forcing strategy has lead to some reasonably realistic rainfall climatologies, and so forms the basis of a hybrid dynamical-physical-empirical general circulation model. The ability to simulate rainfall opens up a lot of applications that were not possible for a simple dry GCM. 

#### Adding sea surface temperature effects
How the atmosphere reacts to an anomaly in the sea surface temperature is the subject of major importance and a vast literature. Because of the coupled nature of surface fluxes, convection and radiation it is difficult to derive empirical rules. But this doesn’t stop us from trying. We restrict ourselves to the tropics where we can more safely argue that the ocean forces the atmosphere, and to time scales long enough to hope we can apply empirical rules. The causal logic is that the SSTA leads to an anomaly in precipitation which in turn is translated into diabatic heating and fed into the model. Much of the architecture of the model’s convection scheme can be co-opted into this problem to take an anomalous precipitation rate and feed it into a deep convective heating profile. 

Set `LSST=.T.` and the model will expect to read two gridded SST datasets. Into channel 18 it will read a long term climatology, either fixed or developing. The default assumption is that it changes once per month but this can be modified with `KOUNTSSTC`. The SST data read into channel 17 can be either a realistic weekly value (this period can be modified with `KOUNTSST`) or an anomaly. Either way, the model is interested in the SST anomaly. How the model interprets channel 17 depends on the value of `ISSTREAD`. If `ISSTREAD=1`, then the model treats channel 17 as SST data and calculates the anomaly as the difference between this and the climatology (channel 18). If `ISSTREAD=2` the model will interpret channel 17 directly as an SST anomaly. 

Having obtained the SSTA, and with an SST climatology as well, the task is to translate this temperature anomaly in degrees C into a rain rate anomaly in mm/day. There are three options, depending on the value set for the transfer function switch `ISSTTRAN`. 

`ISSTTRAN=1` triggers a direct linear correspondence between SSTA and the precipitation rate anomaly. There is a dummy parameter DQDT, the rate of change of precipitation rate with SSTA, which is just set to 1. The translation thus follows geophysical constants to provide 1 mm/day for every degree of SSTA. 

`ISSTTRAN=2` activates the nonlinear transfer function. This is a highly tuned exponential function that depends not only on the SSTA but also on the climatological SST. The same SSTA has more impact in warm ocean than in cold. And the 200mb divergence also plays a role, attenuating the function in regions where you would not normally see upper level divergence. There are currently six tuneable parameters in this transfer function and it is still under development. Generally it does a better job than direct linear correspondence at mimicking observed interannual variations of precipitation in relation to interannual variations of SSTA.

Note that the precipitation anomaly thus calculated is passed into profileheat in the same way as it is from the convection scheme, and the diabatic heating will be placed into the same deep convective vertical profile. This anomaly is fixed, and it can be negative. So don’t be alarmed by negative values of mean precipitation in your long climate run. The SSTA-induced precipitation anomaly will impact the tendencies of moisture and temperature. So it interacts with the moisture budget of the model a well as the heat budget. Finally - be warned that the SSTA-induced heating will be affected by alternative specifications for the latent heat of condensation. So if you set `THERMTYPE` to `INTER`, don’t expect the model to respond to SSTAs !

`ISSTRTAN=3` is a short cut if you want to force the model directly with an observed precipitation anomaly. The values read from channel 17 are interpreted directly in mm/day and passed to `PROFILEHEAT`. 

There are some options for controlling your anomaly experiments. `SCALESSTA` can change the amplitude or sign of the SSTA in a similar way to `SCALEFAN`. `SCALEPPTA` does the same thing to the derived precipitation anomaly. If the transfer function is nonlinear it will not have the same effect. `LSSTMASK` can be switched on to limit the SSTA to the tropics, or to separate ocean basins in the tropics. These are controlled by `SSTZONE`, which can be set to `TROIPICS`, `PACIFIC`, `ATLANTIC` or `INDIAN`. It chooses useful values for the box boundaries of the mask, using the same code as for the nudging mask. 

Temporal behaviour can also be controlled from the job script. `LPERSIST` will force the model to stick on the first record of SST that it reads. `LOOPSST` controls looping behaviour for cyclic anomalies. `KSTOPSST` assigns a timestep `KOUNT` at which to stop progressing through the SST file: useful for honest hindcasts. Finally the metadata on the historical weekly SST data is very useful for allowing the model to scroll through the data and start a seasonal hindcast at a specific date. This metadata is not present on every file so if you want to read it you must set `LREADMETA=.T.` The structure of the metadata is described in Appendix A. 