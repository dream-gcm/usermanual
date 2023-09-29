# Appendix C: Do Androids Dream of Electric Sheep ? - Default values in namelist.
![appendixC](./img/appendix_C.png)


All the namelist variables are listed here with their default values and a brief explanation.

---
## C1. Setup
* `KRUN = 0` - The timestep on which the run will end (eg set to 320 for a 5-day run).
* `KTFIN = 1` - Number of times the model is run when `LTRAIN=.T.` - should be set equal to number of records in initial condition sequence.

The following three string variables engage packages of namelist parameters - there is no default. 

* `RUNTYPE` - Specifies the type of run in terms of forcing or symmetry: `CYCLE`, `PERPETUAL`, `UNFORCED`, or `CHANNEL`.
* `THERMTYPE` - Specifies the type of moist thermodynamics: `DRY`, `WET` or `INTER`. 
* `SSTZONE` - Specifies the region in which SSTs are read: `TROPICS`, `PACIFIC`, `ATLANTIC` or `INDIAN`.

---
## C2. Initial

### Physical constants
* `GA = 9.81` - Acceleration due to gravity - m/s$^2$
* `GASCON = 287.` - The gas constant R - J/kg K or m$^2$/s$^2$ K
* `RADEA = 6371000.` - Radius of the earth - m
* `AKAP = 0.286` - Kappa, the ratio gas constant to specific heat capacity: R/Cp
* `WW = 7.292E-5` - Angular velocity of the earth - rad/s

### Numerical and run control
* `BEGDAY = 0.` - The day on which the run starts.
* `TSPD =  64.` - Number of timesteps per day.
* `PNU =  0.015` - Time filter coefficient for the leapfrog scheme. 
* `TDISS = 0.5` - Dissipation timescale (days) for spectral hyperdiffusion. 
* `NDEL = 6` - Exponent of the gradient operator for spectral hyperdiffusion.
* `T0 = 15*250.` - Reference temperature (K) for the fifteen layers. 
* `NCOEFF = 0` - Maximum wavenumber of printed coefficients (only relevant for output text in `channel 2`). 
* `NLAT = 16` - Number of latitudes in printed gridpoint fields (only relevant for output text in `channel 2`).
* `LSTRETCH = .F.` - Legacy. Engages the original sigma level spacing from HS75. 
* `LLSD = .F.` for T31 otherwise `.T.` - Activates “Lucy in the Sky with Diamonds” mode, in case you are hallucinating enough to believe that adding Land-Sea Drag will improve model performance. Doubles the drag over land in the lowest layer.

### Forcing type
* `LTRAIN = .F.` - Switch to put the model run into training mode, to make successive forecasts from a sequence of initial conditions. Only used when generating a new forcing file. 
* `LFCE = .T.` - Switch to apply spectral forcing from channel 13.
* `LCYC = .F.` - Switch to enable annual cycle and sequentially update forcing and reference fields.

### Grid output for thermodynamic diagnostic variables
* `LGRIDOUT2D = .T.` - Controls output of 2-d grid diagnostics related to precipitation.
* `LGRIDOUT3D = .F.` - Controls output of 3-d grid condensation heating.

### Counters
* `RNTAPE =  100.` - Variable for checking correct read/write of spectral history and restart files and also identifying type file: 100 for model output (restart); 200 for ERAi data; 300 for forcing files `_fcm` and `_fbs` and 400 for forcing anomaly files _fan. 
* `KOUNTH = 16` - Interval in timesteps at which history records are written.
* `KOUNTR = 64000` - Interval in timesteps at which restart records are written.
* `KOUNTREF = 16` - Interval in timesteps at which reference fields are updated from `channel 16.`
* `KOUNTNUDGE = 16` - Interval in timesteps at which nudging fields are updated from `channel 20.`
* `KOUNTFAN = 16` - Interval in timesteps at which forcing anomaly fields are updated from `channel 15`.
* `KOUNTSSTC = 1948` - Interval in timesteps at which Climatological SST fields are updated from `channel 18` (1948 corresponds to one average calendar month).
* `KOUNTSST = 448` - Interval in timesteps at which SST fields are updated from `channel 17` (448 corresponds to one week). 
* `KBEGYRSST = 0` - Start year for reading SST YYYY. Works with SST metadata. 
* `KBEGMNSST = 0` - Start month for reading climatological SST MM. Can also be used to force the model to start its annual cycle at the beginning of any month. 
* `KSTOPSST = 0` - Value of KOUNT at which to stop updating the SST and the SSTC and fix it at its current value. If set to zero this is inactive and SST and SSTC will update as normal.  See also `LPERSIST`. 

### Tuneable parameters for simple physics
* `TAUBL = 0.6667` - Average vertical diffusion timescale in the boundary layer in days.
* `TAUBLEQ = 0.6667` - Value of `TAUBL` at the equator for runs with modified vertical diffusion in the tropics. 
* `PHITROPIC =  45.` - Latitudinal extent over which `TAUBL` is modified by `TAUBLEQ`. 
* `TAUFT =  20.`  - Average vertical diffusion timescale above the boundary layer (free troposphere) in days.
* `TAURC =  10.` for T31 otherwise 12. - Timescale in days for Newtonian linear restoration of temperature throughout the atmosphere.
* `SIGMAB = 0.8` - Sigma level that defines the top of the boundary layer for vertical diffusion coefficients. 
* `TAUCOND =  0.0625` (i.e. 90 minutes) - Timescale used to convert amount of water to be precipitated into a rain rate for the tendencies of T and Q in convection and large scale condensation schemes.
* `TAUNUDGE = 0.25` - Timescale in days for linear nudging to nudge state read from channel 20.
* `TAUSTAB =  0.` - Timescale in days for uniform basic state stabilisation.
* `NNTRUNC =15` - Wavenumber for spectral truncation of moisture variables in moist thermodynamic calculations, see also `LTRUNC` and `LTRUNCQ`. 
* `VIMCONTHR =  0.` - Threshold for anomaly in vertically integrated moisture flux convergence compared to climatology required to trigger deep convection.
* `BLSITHR =  0.` - Threshold for anomaly in boundary layer static instability (bl vertical temperature gradient) compared to climatology required to trigger convection, see also `LBLSI`.
* `PPTCAP =  15.` - Maximum precipitation rate allowed for the deep convection scheme in mm/day. This limit is approached smoothly. 
* `PRHEATMAX = 0.35` - Sigma level at which normalised vertical profile for convective heating is maximum. This profile is used in the convection scheme and also in the response to SST anomalies.
* `QGPFAC = 1.0` - Multiplying factor to boost continental humidity flux from the bottom boundary condition of the vertical diffusion scheme. Only applied over land. The sub-layer climatological value of specific humidity is multiplied by QGPFAC when MASK=1. 

### Forcing anomaly
* `LFAN = .F.` - Switch to apply spectral forcing anomaly from channel 15 on temperature or other variables.
* `LPULSE = .F.` - Causes the model to read a spectral forcing anomaly as a temporary pulse at the beginning of a run, with a squared sinusoidal temporal amplitude signature (normalised). 
* `KPULSE = 64 `- Duration in timesteps of the anomaly forcing pulse. 
* `LSTAB = .F.` - Enables damping that is the same for all degrees of freedom - used to stabilise basic states.
* `LMODE = .F.` - Enables modefinder, which successively rescales anomalies, for use in diagnosing unstable structures and growth rates from a basic state.
* `LNUDGE = .F.` - Enables nudging which reads a sequence of nudging data from `channel 20`. 

### Condensation scheme options
* `LDEEP = .F.` - Switch on the deep convection scheme.
* `LLSR = .F.` - Switch on the large scale in-situ condensation scheme (large scale rain).
* `LCHX = .F.` - Switch to set any negative values of forcing on humidity to zero. Also modifies temperature forcing. To be used in conjunction with explicit condensation and diabatic heating schemes.
* `LTRUNC = .T.` - Enables truncation of vertically integrated moisture flux convergence (`VIMC`) when used as a criterion for triggering deep convection - see also `NNTRUNC`. 
* `LTRUNCQ = .F.` - Enables truncation of specific humidity when used for thermodynamic calculations - see also `NNTRUNC`
* `LBLSI = .F.` - Switch to enable a boundary layer static stability criterion in the decision to trigger deep convection.
* `LPPTCAP = .T.` - Enables limit to deep convective precipitation rate.

### Sea surface temperature options
* `LSST = .F.` - Switch to read SST data from `channels 17` and `18`, which can be used to introduce heating anomalies.
* `ISSTREAD = 1` - Instruction for how to interpret the SST data: 1 for full SST and 2 for SST anomaly. 
* `ISSTTRAN = 1` - Instruction for how to convert the SST anomaly into a precipitation anomaly: 1 for linear (one degree per day heating per degree of SSTA); 2 for nonlinear transfer to precipitation; 3 for direct reading of precipitation data; 4 to introduce the SST anomaly as a boundary condition in the vertical diffusions scheme. 
* `LSSTMASK = .T.` - To apply the SST mask to the SST anomaly. 
* `LPERSIST = .F.` - Will read one record of SST as directed by `KBEGYRSST` and `KBEGMNSST` if using SST metadata, otherwise just the first record. But will not update the SST after this, so the run will have a persisted SSTA. 
* `LREADMETA = .T.` - Instructs the model to look for metadata in the SST file in `channel 17`. 
* `LOOPSST = .F.` - Tells the model whether to return to the beginning of the file when it comes to the end of the SST data (`channel 17`) or SSTC data (`channel 18`). If set to false the model will stick on the last values read of both SST and SSTC if it gets to the end of either file. 

### Anomaly scaling factors
* `SCALEFAN =  1.` - Factor that multiplies anomaly forcing from a _fan file (channel 15). It can be used to double, halve, or reverse the sign of a forcing anomaly. It can also be used to scale down an anomaly (normally use a factor of 0.0001) to provide linear perturbation solutions (the anomalies in the solution can then be scaled back up for presentation).
* `SCALESSTA =  1.` - Factor that multiplies the SST anomaly directly. 
* `SCALEPPTA =  1.` - Factor that multiplies the precipitation and thus the diabatic heating directly associated with an SST anomaly. If the transfer function is nonlinear this will have a different effect to `SCALESSTA`. 
* `SCALELHEAT =  1.` - Factor that multiplies the specific latent heat of condensation. Normally = 1. Set it to zero if you want to force dry dynamics whilst retaining condensation processes (as in `RUNTYPE=INTER`) or to something else if you want to play. 

### Zonal averaging options
* `LZMFC = .F.` - Takes the zonal mean of the forcing and reference data to provide zonally uniform forcing (but not for anomaly forcing). 
* `LZMIC = .F.` - Takes the zonal mean of the initial condition. 
* `ISYM = 1` - Set this to zero to make these zonal mean calculations symmetric about the equator. 
* `IWAVE = 0` - Set this to 1 to add wavenumber 1 to these zonal mean calculations. Set it to 2 to add wavenumbers 1 and 2. Set it to 3 to add wavenumbers 1,2 and 3, etc. 

### Definition of regions for reading SSTs and nudging
* `JNSST = 25` (reset to 19 for T31) - Sets northern latitude for the SST mask in a N-S Gaussian grid.  
* `JSSST = 40` (reset to 30 for T31) - Sets southern latitude for the SST mask in a N-S Gaussian grid.  
* `IWSST = 0` - Sets western longitude for the SST mask in a regular grid that starts on Greenwich. 
* `IESST = MG+1` (129 or 97) - Sets eastern longitude for the SST mask in a regular grid that starts on Greenwich. 
* `JNNDG = 25` (reset to 19 for T31) - Sets northern latitude for the nudging mask in a N-S Gaussian grid.
* `JSNDG = 40` (reset to 30 for T31) - Sets southern latitude for the nudging mask in a N-S Gaussian grid.
* `IWNDG = 0` - Sets western longitude for the nudging mask in a regular grid that starts on Greenwich.
* `IENDG = MG+1` (129 or 97) - Sets eastern longitude for the nudging mask in a regular grid that starts on Greenwich.
