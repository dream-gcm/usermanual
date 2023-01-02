![nomenclature tab](./img/chapter_3.png)
# Chapter 3: The Matrix - Description of the DREAM File Structure



The sub-headings in this chapter refer to directory names under the DREAM root directory. As well as giving you a guide to the file structure, we’ll also have a look inside and see what data there is, and what code is available for pre-processing and manipulating the data, running the model and post processing the output. This chapter is mainly a guide to the files available with a few details where appropriate, especially for the data files. A more comprehensive guide to running the model and diagnosing the output follows in Chapter 4. 

---
## 3.1 `dream_data`directory
The first of three main branches from DREAM is `dream_data`. There are four sub-directories as the data is split into two resolutions, and into spectral and grid data. So T31 spectral data goes with G96 grid data, and T42 spectral data goes with G128 grid data. 


### a. Spectral files
Let's look at spectral data first. These files are all in the same format and contain the base variables of the model: vorticity, divergence, temperature, log surface pressure and specific humidity. Details of the file structure are given in Appendix A, but for now let’s look at the files in the different subdirectories. Note that the file names can be the same for T31 or T42 so it is important to keep them in their correct directories. 

_i) ave: Average_ 

Contains fortran binary files (extension .b) for time-mean climatologies. The annual mean of the analysis period 1979-2016 is given (ANN) and the four seasons DJF, MAM, JJA and SON. For example  `ERAi_ave4x_1979-2016_DJF.b`
 is ERA-interim, average of 4x-daily data, from 1979 to 2016, for the December, January February season. 
These files are a single record. They are often used as reference states for the model (`channel 16`) and sometimes for the initial condition (`channel 10`), especially for perturbation stationary wave experiments (see chapter 4 section 1v). 

As well as these mean climatologies, there are some idealised fields, which are derived from the mean fields, for example the global mean resting basic state
`ERAi_ave4x_1979-2016_ANN_GM_REST.b`
which is derived from the annual mean, but with globally uniform fields of temperature and humidity and no winds. There are thus no horizontal gradients, but the stratification is retained. 

Another example `ERAi_ave4x_1979-2016_DJF_ZM.b` is the time-mean zonal mean from DJF and `ERAi_ave4x_1979-2016_DJF_ZM_SYM.b`
is the same but symmetrical about the equator. The code to create these files is outlined in the next section. 

_ii) cyc: Cycle_

`ERAi_cyc4x_1979-2016_RM41.b` contains the mean annual cycle over the analysis period. 
This file is 4x daily data over one model year of 365.25 days. So it has 1461 records. It is based on a simple mean by calendar date which has then been smoothed with a 10-day running mean (RM41 for 41-point running mean). 

_iii) fan: Forcing Anomaly_

Still in the same data format, but these files are actually tendencies rather than states. They are mostly idealised heating fields but can be used to add a perturbation forcing to any model variable, read into `channel 15`. They are usually just one record for a time independent perturbation but they can also be a sequence. So for example `CPac_EQ180E_40x15_Deep_2dpd_fan.b`.

Is a Central Pacific heating anomaly centred at the equator and 180 degrees longitude. It is elliptical in shape with semi-major and minor axes of 40 degrees in longitude and 15 degrees in latitude. The horizontal distribution is a cosine squared bell shape. The heating is injected into a deep convective profile (peaking at sigma=0.35) with a vertical average heating rate of 2 degrees per day. 

`_fan` files can be more sophisticated, with for example a canonical MJO sequence. The model can be set to read sequential records at a user-defined rate. When the model reaches the end of the file it will return to the beginning for a cyclic perturbation. 

_iv) fbs: Forcing the Basic State_

These are single-record files that contain tendency information in the standard spectral format. They are read into the `channel 13` to provide the basic forcing for the model. If an _fbs file is chosen to force the model it should be used in conjunction with the correct initial condition, which corresponds to the desired basic state.  This is because an _fbs file contains exactly the value required to cancel the tendency that the unforced model would have if it were integrated one timestep forward from that basic state. So if the basic state is used as an initial condition in conjunction with its _fbs file, there will be no development in the model. It will step forward in time and its state will remain the same as its initial condition. So if you read  `fbs/ERAi_ave4x_1979-2016_DJF_fbs.b` into `channel 13`, and use  `ave/ERAi_ave4x_1979-2016_DJF.b` in `channel 10` and `channel 16`, the model will just sit on that state until rounding errors grow to finite amplitude through instability (this usually takes a few hundred days). 

Of course this configuration is intended for use in experiments where there is a perturbation either to the forcing ( a `_fan` file) or to the initial condition. More on this in Chapter 4 section 4i. 

_v) fcm: Forcing a Circulation Model_

This is technically the same as the _fbs file described above, but it will not maintain any basic state. If you read an `_fcm` file into `channel 13`, the model will develop regardless of the initial condition you choose in `channel 10`. But note that it is still important to use the correct associated reference state in channel 16. 

This is the simple GCM forcing, which can be used for long runs or forecasts to get the model to behave like a GCM. The model will develop a fully turbulent eddy field with a mean state and transient fluxes that resemble those of a real GCM (or even the real atmosphere). Often used in experiments where there is a long perturbed equilibrium simulation, to be compared with a long control run. Forcing for perpetual runs simulating each of the four seasons is provided. 

Most of the files in this directory are single record files, designated ave4x, but there is one that is designated `cyc4x`, which has 1461 records. This is the annual cycle forcing described in Chapter 4 section 1iii. If the annual forcing cycle is chosen, then the reference state must be the mean annual cycle. The model will read forcing and reference data sequentially every six hours and return to the beginning of the year at the end of the files. 

_vi) inst: Instantaneous data snapshots_

Useful as initial conditions to get the model started in a realistic way, or to throw some multi-scale noise at an idealised simulation to break symmetry. These are single record data files where the date is specified. 

_vii) seq: Sequence_

These are multiple record data files that can be used directly for pre-processing, for calculating model forcing functions, for nudging, or for ensemble initial conditions. For example `ERAi_seq4x_1979-2016_ANN.b` contains the entire dataset from 01/01/1979 to 31/12/2016: 55520 records. 
This has been split into datasets with sequential discontinuous chunks for the four seasons: `ERAi_seq4x_1979-2016_DJF.b`, etc. 

There are also sequences for a given date: `ERAi_seq_1979-2016_01_01.b` contains 38 records with every first of January, useful for ensemble forecasts. And  `DREAM_dry_seq_120_28d_interval.b`
is actually output from a long perpetual DJF integration of DREAM, sampled once every 28 days. So there are 120 records of independent data sampled from the model’s own climate: useful for drift-free idealised ensemble work. 


### b. Grid files
The only essential grid file the model needs is the land-sea mask, `LSmask_G96.b` for T31 and `LSmask_G128.b` for T42. Apart from that the most important grid-based input to the model is the SST data. Single record climatologies are given for the four seasons, and a monthly climatology is also provided in a 12-record file. These climatologies are used in conjunction with either realistic or idealised SST anomalies to calculate the associated atmospheric heating anomaly. This is still  subject of research. 

---
## 3.2 `data_process` directory
In the second main directory, dream_model, we have a set of routines to manipulate the data and prepare data files and forcing for the model. 

### a. In `/data_manip/`:
Here we have a selection of fortran programs for a wide variety of tasks. They are stand-alone without scripts to run them, so it’s up to you to compile them:

```
gfortran -fdefault-real-8 -fconvert=big-endian
```

and link the right input files to the appropriate channels and to rename the output as required. This means you’ll have to understand how the programs work, and possibly edit them to your needs. None of them are very long. They all have very specific purposes. Most of them work on spectral “history” files which may be reanalysis data or model output. Some work on grid data which is from model output of fields that are not spectrally analysed in the model, such as rainfall. 

Here’s the complete list: 
* `add2_hst.f` - adds two model spectral history files together
* `checkhst.f` - simply reads a spectral history file to check the data
* `checkhst_modenorm.f` - reads a history file and calculates the norm used in “modefinder” (see Chapter 4 section 4i) 
* `compare_hst.f` - compares two history files
* `concat.f` - concatenates two history files into one
* `daily_means.f` - calculates daily means from 4x-daily spectral data
* `extract_10yr.f` - extracts a chosen decade from the data sequence
* `extract_38x1Jan.f` - extracts a sequence of 1st of Januarys from the data sequence
* `extract_38x1st_of_Month.f` - same but for the first of any chosen month
* `extract_DJF.f` - to create a sequence of DJF 4x-daily data from the full sequence
* `extract_IC_for_ensemble.f` - to create a sequence of states by reading a long model run at fixed intervals to provide ensemble initial conditions
* `extract_last_40_days_same_IC.f` - from model output of any length, extracts the last 40 days of 4x-daily data and writes it out with the original initial condition - useful for analysing modes
* `extract_season_means_cyc.f` - to make four seasonal means from a mean annual cycle 
* `extract_seasons_spec.f` - extracts the four seasons from the full sequential dataset - spectral
* `extract_seasons_grid2d.f` - same but for 2d grid fields (variables related to precipitation)
* `extract-label_years.f` - relabel spectral data with information about the year and daynumber
* `global_mean.f` - creates spectral data with the global mean of the input file but no horizontal variations
* `global_mean_resting.f` - same but with no wind at all
* `growth.f` - calculates growth rates in a quadratic vorticity norm (for analysis from the modefinder, see Chapter 4 section 4i)
* `make_inst2.f` - extracts a single record from a sequence to furnish a singe initial condition
* `make_inst.f` - same with KOUNT and DAY set to zero
* `modify_metadata.f` - to update timing information on history files
* `pack_history_grid.f` - deals with a bug in writing out grid data where some of the data were not output from the model
* `rephase_MJO_fan48d.f` - shuffles MJO forcing anomaly sequence to change initial phase
* `subtract2_hst.f` - subtracts one history file from another
* `subtract_BS.f` - subtracts a basic state from a history file and adds a resting state in its place, useful for looking at anomalies on a fixed basic state.  
* `subtract_CTL.f` - subtracts a time-dependent control experiment and adds a resting state, useful for tangent anomaly development. 
* `subtract_IC.f` - subtracts the initial condition from a history file and adds a resting state, useful for anomaly forecasts. 
* `TILS.f` - Time Independent Linear Solution. Complicated routine for extrapolating a set of three solutions found at different additional damping rates back to zero additional damping (see Appendix B section 3). 
* `time_filter_history.f` - creates a block mean history file for crude low-pass filtering.
* `time_mean.f` - creates a custom time-mean from the sequence data after skipping an initial period.
* `truncate_T42toT31.f` - creates T31 history record from T42 input
* `visualise_forcing_T42.f` - creates a history file that differs from the initial condition by an input forcing rate (from a _fan, _fcm or _fbs file) multiplied by one day to allow visualisation of tendency fields in units per day
* `W2G2W_sector_mean.f` - uses the model’s spectral analysis code to do geographical  manipulations on spectral data in grid space, notably the sector mean. 
* `zonal_mean+WN123.f` - takes the zonal mean of the input data, with options to also make it symmetric about the equator, and to retain wavenumbers 1, 1 and 2 or 1,2 and 3. 

### b. In `/prep_cyc/`:
A small number of fortran programs specifically focussed on computing cycles. The names of these programs are quite self explanatory (except the ones that refer to components of the annual cycle CT, TT, MC and CC which are highly specialised): 
* `annual_cycle_spec/grid` - calculates the mean annual cycle from a sequence - note that there is no smoothing filter applied in this code, that is done separately afterwards using cyclic_running_mean_spec/grid. 
* `composite_n_day_cycle_spec/grid` - used for diagnosing aggregate cyclic responses to cyclic forcing (like the MJO) in long model runs. 

### c. In `/prep_fan/`:
Scripts and programs for preparing idealised forcing anomalies. First look at makefan.ksh. It compiles and runs makefan.f to produce a gridpoint forcing anomaly for either temperature or vorticity. This is then spectrally analysed at T42 using `specanANOMT42.f` and written to a file called temp_fan.b (to be renamed as needed). T31 anomalies can be made by changing the parameters and using `specanANOMT31.f` (or by downscaling the T42 result using `truncate_T42toT31.f`). 

The program `makefan.f` starts from scratch and can be edited for the desired properties of the forcing anomaly. It will take the form of an ellipse with a cosine squared bell shaped horizontal distribution. You can specify its location and radius in x and y directions, its heating rate and its vertical profile. Examples are given in the file `Notes_for_forcing_anomalies.rtf`. 

More complex shapes can be defined from gridpoint input using makefan_ReadGrid.f and sequences of forcing can be produced using `makefan_seq.f`. The model will read through a forcing anomaly sequence at a user-defined rate until it reaches the end and then it will repeat to give a cyclic forcing anomaly. 

### d. In `/prep_lsm/`:
Code for creating the land-sea mask in model format from gridpoint data

### e. In `/prep_seq/`:
Basic code for creating the ERA-interim dataset as a sequential binary file in the model format. 

### f. In  `/prep_sst/`:
Code for manipulating and visualising SST data and idealised SST anomalies:
* `check_grid_SST.f` reads binary SST data in model format and prints it on the screen to check it’s OK. 
* `makessta.f` creates an elliptical SST anomaly in model grid format in a similar way to makefan.f

---
## 3.3 `source` directory
In the `/source` directory you’ll find the model: at time of writing it’s `dream_v8.1.f`. Appendix A section 6 and Appendix D take you through the code in some detail. It is easy to edit the code but not recommended ! If you do want to hack it for some special reason, just make sure you keep a safe original copy. The model calls some library routines in /lib but once compiled these should not be touched. It also reads a lot of parameters and common block variable declarations from the `/include` directory. Note that this is set up to work at two resolutions, T31 and T42, with the associated grid resolutions of 96 and 128 points around a latitude circle (and 24 and 32 latitudes per hemisphere). Switching between resolutions is transparent for the code, and to a large extent also for the associated data files. It's all set up in the job script, as described in the next section. So you have very little reason to visit this source directory. 

Also in the include subdirectory is a `setup` file. This contains a few edits to the code to alter its behaviour depending on some choices made in the job script namelists. The idea is to have some standard use cases, but we haven’t gone very far down this road as in general everyone’s use case is different. 

Finally there is a `change-log` which contains notes on changes made between versions of DREAM. As such it is a nice chronological summary of the development history which complements this user guide. 


---
## 3.4 `jobs`directory
This is where you’ll spend a lot of your time. We’ve already had a look at the job script to run the model in chapter 2, and we’ll go into much more detail in chapter 4. Here’s just an overview of the files in this directory. 

* `runmodel_v8.1.ksh` - your basic script for running the model
multirun.ksh - a bog standard script to sequentially run several experiments - edit at will.

* `makefrc.ksh` - the script for making forcing files _fbs and _fcm. How to do this is explained in Chapter 4 section 2. It calls fortran routines: calcfrc_T31.f or calcfrc_T42.f. 

* `makefrc_cyc.ksh` - calculating a forcing function with an annual cycle is a protracted and elaborate business, see Chapter 4 section 2iv and Appendix B section 8 . This script is only part of the procedure, along with fortran routines: calcfrc_cycADV.f and calcfrc_cycTEND.f

* `makefed.ksh` - if you want to diagnose the transient eddy part of the forcing, it is the difference between a _fbs file and an `_fcm` file (see Appendix B). This script works it out using `calcfed.f`. 

* `run_ensemble.ksh` - a very useful script for organising an ensemble forecast and then calculating an ensemble mean history record. It calls the script make_ensemble_mean.ksh, and fortran routines: `ensemble_ic.f` and `ensemble_mean.f` or `ensemble_mean_dry.f`.

---
## 3.5 `results` directory
So the model has run without crashing and you have some history files. They will have been put into your experimental directory under DREAM/dream_results. Here you will find for reference a record of how you set up the experiment in the form of the following files: 
* `runmodel_v8.1.ksh` - a record of the script you used to run the model
* `namelist_data` - the changes you made to the model namelist defaults
* `results` - a text file with details of the run including namelist values etc. 
* `dream_v8.1.f` and `setup.f` - a clone of the model code you used
* `parameters.f` - a record of your parameter (i.e. the resolution)
* `prog` - the executable file for the model
* `history` - the dynamical output from the model
* `history_grid2d` and `history_grid2d` - precipitation-related gridpoint output if appropriate
`restart.11` and `restart.12` - restart files periodically during the run (11) and at the end (12). 

When you run the diagnostics you’ll also get:
* `run_output.ksh` and `model_output.ksh` - a record of the diagnostic scripts you used
`/netcdfs` - your netCDF output goes here
* `/binary_grid` and `/binary_grid3d` - binary diagnostic output if you selected it. 

---
## 3.6 `diagnostics` directory
Another directory where you’ll spend a lot of your time. Again, this is an overview of the files. A comprehensive guide to diagnostics is given in Chapter 4. 
* `specan_W2G.f` - the core fortran program that everything depends on, this routine uses the spectral analysis from the model to take a model history file and write grid diagnostic fields for dynamical variables into binary and netCDF formats.
* `gridan2d.f` and `gridan3d.f` do a similar job but for model grid output, i.e. fields that are related to model precipitation.

* `time_mean_spec_grid.f` - calculates a time mean from your sequential output, called by the script if requested. 

* `run_output.ksh` - this is your basic script for running the output, it calls `model_output.ksh` and `file_renamer.ksh` as well as the diagnostics programs cited above. 

* `run_output_flux.ksh` - an extended script that does the same job as `run_output.ksh` but will also provide quadratic quantities with time-filtering, such as heat, moisture and momentum fluxes, geopotential variance and eddy kinetic energy. To do this it calls `model_output.ksh`, `model_flux.ksh`, `hp_flux.ksh`, and the fortran programs cited above. For handling fluxes and time filtering it also calls: `time_filter_history.f`, `time_mean_flux2d.f`, `gridan_flux2d.f` and `hp_flux2d.f`. 

* `/include` - contains parameters and common blocks. Note that the common block files are not simply copies of the ones in the source directory. 

* `check_grid3d.f` - this is just a verification program to print 3d grid data on the screen.




