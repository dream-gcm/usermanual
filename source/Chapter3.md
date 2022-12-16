![nomenclature tab](./img/chapter_3.png)
# Chapter 3: The Matrix
_Description of the DREAM File Structure_


The sub-headings in this chapter refer to directory names under the DREAM root directory. As well as giving you a guide to the file structure, we’ll also have a look inside and see what data there is, and what code is available for pre-processing and manipulating the data, running the model and post processing the output. This chapter is mainly a guide to the files available with a few details where appropriate, especially for the data files. A more comprehensive guide to running the model and diagnosing the output follows in Chapter 4. 


## `dream_data` directory
The first of three main branches from DREAM is dream_data. There are four sub-directories as the data is split into two resolutions, and into spectral and grid data. So T31 spectral data goes with G96 grid data, and T42 spectral data goes with G128 grid data. 


## Spectral files
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


## Grid files
The only essential grid file the model needs is the land-sea mask, `LSmask_G96.b` for T31 and `LSmask_G128.b` for T42. Apart from that the most important grid-based input to the model is the SST data. Single record climatologies are given for the four seasons, and a monthly climatology is also provided in a 12-record file. These climatologies are used in conjunction with either realistic or idealised SST anomalies to calculate the associated atmospheric heating anomaly. This is still  subject of research. 

