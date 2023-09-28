![appendixD](./img/appendix_D.png)
# Appendix D: Nightmare on Elm Street - The model subroutines.

The scope of this user guide is to give an indication of how things work without explaining every line of the code. The main body of the program has already been presented in Appendix A. Here the subroutines get a similar treatment, in the order they currently appear in the source code. 

---
* `INISET`: Called just once at the beginning of the run to set up basic constants and default values of namelist variables. It then reads the `SETUP` namelist to override the defaults. `SETUP` has just five variables which are used for basic run types. The user modifiable code setup.f is then included. It uses the namelist `SETUP`, and overrides the defaults in the namelist INITIAL. Then `INITIAL` is read and this overrides both defaults and whatever has been set in the setup file. This way, what you see is what you get in the job script. The subroutine goes on to calculate basic indices, horizontal diffusion coefficients and non-dimensionalising factors and coefficients for calculating derivatives in from spectral coefficients. Finally it sets up all the non-dimensional time scales and associated rates for model parameterised processes. 
---
* `INIGAU`: Called just once at the beginning of the run. Calculates Gaussian weights and latitudes. 
---
* `INISI`: Called just once at the beginning of the run. Sets up the sigma levels from specified sigma half levels. Then sets up alpha weights used for calculating the geopotential in the gravity wave source term, see fig. A2.  
---
* `INIRES`: Called just once at the beginning of the run (the name is historical, this routine is no longer used for restoration forcing). Contains some setup for the vertical profile of vertical diffusion coefficients. These are calculated according to the specified timescales and introduced into the profile `PRDAMP`. Also sets up the vertical profile for convective heating using input parameter `PRHEATMAX`. This profile is written into `PRHEAT`. 
---
* `INIVAR`: Called just once at the beginning of the run. Initialises model variables. First single-level grid variables: masks, precipitation diagnostics and SSTs. Then multi-level grid variables. Then reads in the land-sea mask. Sets up a latitude-dependent function `CD` for the boundary layer vertical diffusion. Then defines regional masks for SSTs and nudging. Finally (and redundantly) initialises all spectral variables to zero, including tendencies. 
---
* `INIIC`: Called at the start of each run, which is once per initial condition if we are in a training loop, but only once for a normal run. Initialises all spectral variables to zero, including tendencies. Initialises gridpoint output diagnostics to zero. Reads the initial condition from `channel 10` and sets up the model year `RMYR`. Initialises previous timestep spectral variables to be the same as the initial condition. 
---
* `INITEND`: Called at the beginning of the adiabatic part of the timestep and again at the beginning of the diabatic part. Initialises all spectral tendencies to zero. 
---
* `INIQCON`: Called each time the forcing and reference state is updated and also at the beginning of the adiabatic part of the timestep. Initialises the spectral moisture flux convergence to zero. 
---
* `READFCE`: Called at the start of each run and each time the forcing and reference state is updated. Reads forcing (`channel 13`) and reference states (`channel 16`). Takes their zonal mean if `LZMFC` enabled. Performs calculations to modify the forcing of humidity and temperature if `LCHX` is enabled (wet run). This entails wave to grid transformations using spectral workspace variables and gridpoint moisture and temperature variables `QG` and `TG` temporarily. The modified forcing is defined in grid space as the positive only source of `Q` and an adjusted heating for T. Wave to grid transformations are also made to store gridpoint values of the reference state. Moisture flux convergence is truncated to smooth it before finally going back to grid space to store a gridpoint reference value of the moisture flux convergence. 
---
* `READNUDGE`: Called at the start of each run and each time the nudging state is updated. Reads the spectral nudging state from `channel 20`. 
---
* `READFAN `: Called at the start of each run and each time the forcing anomaly is updated. Reads the spectral forcing anomaly from `channel 15`. Rewinds if at end of file. 
---
* `INISSTC`: Called at the start of each run. Initialises grid climatological SST by reading from channel 18. Scrolls through the data until it picks up the correct record for the month `KBEMNSST`. 
---
* `READSSTC`:  Reads grid climatological SST from `channel 18` each time it is updated. Will stick on the last record unless `LOOPSST` is enabled in which case it will rewind at the end of the file. 
---
* `INISST` (`MREMAIN`): Called at the start of each run. Reads grid SST data from `channel 17`. If the SST data contains metadata the it initialises SST at correct year and month specified by `KBEGYRSST` and `KBEGMNSST`. Otherwise it just reads the first record of SST data. Calculates the right value of `RMYR` to pass the correct calendar date to the diagnostics. Passes back `MREMAIN`, the number of days to wait before reading again, to the main program to offset the counter for reading SST data. 
---
* `READSST` Reads grid SST from `channel 17` each time it is updated. Will stick on the last record unless `LOOPSST` is enabled in which case it will rewind at the end of the file. Handles SST data with or without metadata. 
---
* `SPECPREP`:  Called just before the diabatic tendencies are calculated. Calculates smoothed values of Q and Q flux convergence by spectral truncation. 
---
* `SPECPOST`: Called immediately after the diabatic tendencies are calculated. Sets global mean spectral coefficients of diabatic tendencies of vorticity, divergence and surface pressure to zero. 
---
* `FANDAMP`: Called before the diabatic timestep. Adds in spectral tendencies from the forcing anomaly. If `LPULSE` is enabled a sin-squared temporal pulse is imposed on the anomaly amplitude at the beginning of the run, otherwise it is time-independent. If `LSTAB` is enabled an additional damping is applied equally to all spectral tendency coefficients. 
---
* `DIFUSE`: Called before the diabatic timestep. Adds spectral tendency due to scale-selective hyperdiffusion. 
---
* `DSTEP`: The diabatic timestep. Updates spectral variables with accumulated diabatic tendencies. 
---
* `FSTEP`: Called immediately after the diabatic timestep. Updates spectral variables with basic empirical forcing tendencies. 
---
* `TFILT`: Called at the end of the model timestep. Completes the time filter by modifying the previous values of the spectral variables, `ZMI` etc. 
---
* `HANAL`: Called from numerous places during grid to wave transformations, notably the subroutine `LTD` and its derivatives. Used in direct Legendre transforms in to calculate Legendre coefficients for the latitudinal structure from variables in latitude-Fourier space. Different types of transform are used to obtain the fields or their derivatives for variables with differing symmetries. 
---
* `HANAL1`:  As `HANAL` but for single-level fields. 
---
* `HEXP`:  Called from numerous places during wave to grid transformations, notably the subroutine `LTI` and its derivatives. Used in inverse Legendre transforms in to calculate variables on Gaussian latitudes  / Fourier space from spectral space. Different types of transform are used to obtain the fields or their derivatives for variables with differing symmetries. 
---
* `HEXP1`: As `HEXP` but for single-level fields.
---
* `LGNDRE`: Called from `INIGAU`. Calculates Legendre polynomials and their derivatives as a function of latitude. 
---
* `LTD`: Called from `G2WA`. Similar routines are called elsewhere during grid to wave transformations. Stands for Legendre Transform Direct. Transforms from latitude-Fourier space to grid space for a number of variables in order to calculate spectral tendencies for the first part of the time step. Includes multiple calls to `HANAL` to achieve this, with various requirements to take meridional derivatives as part of the transformation. 
---
* `LTI`: Called from `W2GA`. Similar routines are called elsewhere during wave to grid transformations. Stands for Legendre Transform Indirect. Transforms from grid space to latitude-Fourier space for a number of variables in order to provide basic gridpoint fields for the calculation of tendencies in grid space. Includes multiple calls to `HEXP` to achieve this, with various requirements to take meridional derivatives as part of the transformation.
---
* `MATINV`: Called from `INISI` when setting up arrays for the semi-implicit scheme. Inverts a matrix. 
---
* `W2GA`: Called from the adiabatic part of the timestep. Collects together the wave to grid operations in the adiabatic part of the time step, calling `LTI` for meridional (spectral to latitude-Fourier) and `FFT991` for the zonal (latiude-Fourier to grid) part of the transformation. Returns grid point model variables. 
---
* `G2WA`: Called from the adiabatic part of the timestep. Collects together the grid to wave operations in the adiabatic part of the time step, calling `FFT991` for the zonal (grid to latiude-Fourier) and `LTD` for meridional (latitude-Fourier to spectral) part of the transformation. Returns spectral fields that will be further manipulated to find the spectral tendencies. 
---
* `W2GD`: Called from the diabatic part of the timestep. As `W2GA` but for grid point variables needed in diabatic calculations, including instantaneous and reference moisture flux convergence. 
---
* `G2WD`: Called from the diabatic part of the timestep. As `G2WA` but for grid point tendencies derived from diabatic calculations. 
---
* `ADVECTION`: Called from the main program after wave-to grid transforms in the adiabatic part of the timestep. Calculates all the advective tendencies with variable names marked in red on fig. A1. 
---
* `SPDEL2`: Called from `LTD` to find the `EKE` term in the divergence equation. Calculates the Laplacian (or inverse Laplacian) of a spectral variable. 
---
* `TSTEP`: Called just after the first set of spectral transforms that evaluate the advective tendencies in the main program. This subroutine basically implements the equations in HS75 in spectral space. It has nested loops for hemisphere, zonal wavenumber m and meridional wavenumber n. 

Briefly:

After setting up a few local variables, such as `RCN=1/n(n+1)` there are several calls to the matrix multiplier `SGEMM`. These evaluate variables like `RMPA=TTR*G`(the first part of the  term in HS75 eq 17) and `TMPG=TMI*G` (the geopotential in HS75 eq 11). 

Then a vertical integral to find :

```
D1 = 1/Cn DMI + DELT*[ PHI + (250/CT)*SPMI + 1/Cn DT(from advection) ]
              + DELT^2*[ TT(from advection)*G + (250/CT)*curlyP ]
```
where `curlyP = V.grad log p*` and is equal to `-VP`.

Then another matrix multiplication to get the left hand side of HS75 eq (17): 

```
DT = D1 * BM1(IBM1+1) 
```
Note that `DT` is used here to store the mean divergence, not the tendency !

Then a vertical sum to get the tendency of `log p*` (HS75 eq 4): `VP(I1)=VP(I1)+DT(K)*DSIGMA(L)`

Then another matrix multiplication to get `TMPA=DT*TAU`: to build the semi-implicit temperature tendency from HS75 eq (14). 

This is added to `TT`, and then the rest of the subroutine basically adds in the advection, integrating  with the time filter in triplets of lines like :

```
ZPAV=ZMI(I)
ZMI(I)=PNU21*Z(I)+PNU*ZPAV
Z(I)=ZPAV+DELT2*ZT(I)
```
And thus the model variables have been updated, and so have the pervious timestep versions, with just a time filter to close, which is done in the subroutine `TFILT`.

---
* `WRSPS`: Legacy routine to print out spectral coefficients
---
* `SCALEDOWN`: Called from the main program after the timestep has been completed. Activates the modefinder, which compares a quadratic norm in vorticity with its reference value. If this ratio exceeds 10, the difference between the model state and the reference state is scaled down by this ratio so the anomaly returns to its standard magnitude. This scaling is applied to both current and previous model state. If the ratio is less than 0.1 the anomaly is scaled up. 
---
* `LTIUVTPQ`: Called during wave to grid transformations in the diabatic part of the time step. See `LTI`. 
---
* `LTDUVTPQ`: Called during grid to wave transformations in the diabatic part of the time step. See `LTD`. 
---
* `DIABATIC`: Called from the main program after wave-to grid transforms in the diabatic part of the timestep. This is the master subroutine for calculating diabatic tendencies in grid space. Each call to `DIABATIC` is for a vertical slice of grid data at north and south latitude pair JH (see Appendix A section 2). First all the grid point tendencies are initialised to zero. Then in sequence: 

    - The nudging tendencies are evaluated directly.  
    - The moisture flux convergence is calculated in `PWATER` and the deep convective tendencies are calculated in `DEEPTEND`. 
    - The influence of SST is calculated  with first another call to `PWATER` and then `SSTTEND`.
    - The vertical diffusion is evaluated in `VDIFFTEND`.
    - Land-sea drag is added directly. 
    - Large scale rain tendencies are calculated in `LSRTEND`.

For each process, the gridpoint values of the model variables are updated as we go, so tendencies calculated for each process are influenced by the previous processes. 

Finally the radiative cooling is applied directly and all the tendencies are added up to be passed back through to spectral space. 

---
* `SHUFFLE`: Called from the main program for grid variables just after the diabatic tendencies have been evaluated in `DIABATIC`. Places the two-latitude slice data in a global gridpoint array. 
---
* `SHUFFLE1`: As shuffle but for single level data.
---
* `LTIUVTPQREF`: As `LTDUVTPQ` for reference data.
---
* `LTIUVTPQNDG`: As `LTIUVTPQ` for nudging data.
---
* `LTDQCONREF`: As `LTD` for Q flux convergence reference data.
---
* `LTDQTFCE`: As `LTD` for forcing data.
---
* `LTIQCONREF`: As `LTI` for Q flux convergence reference data.
---
* `LTIQTFC`: As `LTI` for temperature and humidity forcing data.
---
* `TRUNCATE(XTRUNC)`: Called from `READFCE` and `SPECPREP` an applied to specific humidity Q and its convergence. Truncates spectral variable `XRUNC` from `NN` to `NNTRUNC` by packing with zeros.
---
* `TRUNCATE1(XTRUNC)`: As `TRUNCATE` for single level data - by default not used. 
---
* `ZMEAN(ZWK,DWK,TWK,SPWK,QWK)`: Called from `INIIC` and `READFCE`. Takes the zonal mean of the entire model state passed to the work arrays. Can also be used for forcing data. Global namelist options control symmetry: ISYM=1 for the full zonal mean and `ISYM=0` for a zonal mean that is symmetric about the equator. `IWAVE` adds wavenumbers 1, 2 and 3 (see Appendix C). 
---
* `PWATER`: Called from `DIABATIC`. Calculates column total moisture flux convergence and water content. Works on one latitude pair at a time. Evaluates: 
  `VIMCON`: the vertically integrated moisture flux convergence, by summing the flux convergence `QCONG` over sigma layers and dimensionalising to mm/day. 
  `VIMCONTR`: as `VIMCON` but with truncated moisture flux convergence. 
  `VIMCONREF`: as `VIMCON` for the reference state. 
  `COLWATER`: the total column water, by summing over sigma layers and dimensionalising to mm. 
  `COLSAT`: for diagnostic purposes only, this is the value `COLWATER` would take if the column was at saturation at every level. 

Some values are accumulated into 2-d grid arrays for diagnostic output:
  `VIMC=VIMCON`, the vertically integrated moisture convergence (mm/day)
  `VICW=COLWATER`, the column total water (mm)
  `VISF=COLWATER/COLSAT`, the saturated fraction. 
(note that 2-d values in mm could also be expressed in kg/m2 ).

---
* `DEEPTEND(J,TGTDEEP,QGTDEEP)`: Called from `DIABATIC`. Returns deep convective tendencies for temperature and specific humidity. Works on one latitude pair at a time. See [Chapter 4, section 4](https://dreamusermanual.readthedocs.io/en/latest/Chapter4.html#c-moisture-condensation-and-convection) for a description of the convection scheme. 

This subroutine first sets the decision to trigger convection `LTRIG` as true, and then looks for reasons to set it to false. The first criterion depends on the difference `VIMCONA` between the smoothed vertically integrated moisture convergence `VIMCONTR` minus its reference value `VIMCONREF`. This difference must be positive and exceed a threshold for convection to be triggered. 

The other optional criterion depends on vertical temperature differences in the lowest four layers of the model: specifically the mean of the bottom two layers minus the mean of the next two layers up.  The “instability anomaly” `BLSIA` is the departure of this difference from its reference value. It must exceed a threshold for convection to be triggered. 

If convection is triggered the column total rain falling in next `TAUCOND` period `PPTTAU` is calculated in mm as the convergence in mm/day times the period `TACOND`. `PPTTAU` is constrained not to exceed the total column water COLWATER and to be positive. It is also subject to a maximum value `PPTTAUCAP`, which is is constrained to approach asymptotically. 

The value of `PPTTAU` is passed to `PROFILEHEAT` to evaluate the tendencies of specific humidity and temperature. The convective precipitation rate in mm/day associated with `PPTTAU` is stored for the current latitude pair for diagnostic 2-d output in `PPTRATEDEEP`. 

---
* `PROFILEHEAT(J,FR,PPTTAU,QGT,TGT)`: Called from `DEEPTEND` and `SSTTEND`. Uses the precipitation `PPTTAU`(mm) that is passed to it and the associated rate FR, and returns tendencies for temperature and specific humidity for deep convective heating. Works on one latitude pair at a time. 

For a given column total rain `PPTTAU`(mm) falling in next tau period associated with rate FR, this subroutine calculates the tendency QGT of gridpoint specific humidity based on pro-rata reduction of specific humidity at rate `FR` at each level. This operation is carried out on smoothed humidity if the option `LTRUNCQ` is enabled. 

It also sets the tendency `TGT` of temperature by spreading the total latent heating over the predetermined profile `PRHEAT(L)`. Along the way it accumulates the 3-d diabatic heating rate `CONDHEAT` (deg/day) for diagnostic output. 

These calculations are done level by level and the grid point values of temperature TG and specific humidity `QG` are updated as we go. This subroutine also updates the total precipitation rate for diagnostics `PPTRATE` (mm/day). 

---
* `SSTTEND`: Called from DIABATIC. Returns tendencies for temperature and specific humidity associated with the response to an SST anomaly. Works on one latitude pair at a time. See [Chapter 4, section 4c](https://dreamusermanual.readthedocs.io/en/latest/Chapter4.html#adding-sea-surface-temperature-effects) for a description of the way SST anomalies are implemented. 




The purpose of this subroutine is to read SST data and, depending on the options set for `ISSTRAN`, calculate a precipitation rate anomaly associated with an anomaly in SST. 

The subroutine starts by calculating the SSTA based on the nature of the variable SST. In the case `ISSTREAD=1` the SSTA is calculated by subtracting SSTC from SST. Otherwise (`ISSTREAD=0`) SST is just used directly as the SSTA. At this point the SSTA can also be scaled by the factor `SCALESSTA`. 

There different methods of for deducing a precipitation rate anomaly from the `SSTA` are set by `ISSTRAN`. The first three options  translate the SST anomaly directly into a precipitation rates in mm/day (`ISSTTRAN=1,2,3`). The fourth passes the problem to the vertical diffusion scheme (`ISSTTRAN=4`). This is described in [Chapter 4, section 4c](https://dreamusermanual.readthedocs.io/en/latest/Chapter4.html#adding-sea-surface-temperature-effects). 

For the first three cases the code actually uses the variable `PPTTAU` for rainfall in mm. And then it assumes that this amount of rain falls in one day by setting the rate `FRSST` appropriately. This is quite artificial and it is only done like this so that the subroutine `PROFILEHEAT` can be used to get the tendencies. For the fourth case (`ISSTTRAN=4`), this step is bypassed by setting `PPTTAU=0.` and the effect of the SSTA is calculated in the subroutine `VDIFFTEND`. 

For the nonlinear transfer function, SSTC and the model divergence at $\sigma$=0.2, together with its reference value are used, along with a number of tuneable parameters. These parameters have not yet made their way into a namelist and this part of the code is work in progress. Once `PPTTAU` has been calculated, it is constrained by the land-sea mask to be only over the sea, and by the selective mask to either pick an ocean basin or cover the whole of the tropics. A constraint is added in the case that the convection scheme is being used, that the daily rainfall cannot exceed the column water total. 

Finally `PROFILEHEAT` is called to set the tendencies of specific humidity and temperature associated with the SSTA: `QGTSST` and `TGTSST` as it does for the convection scheme, by spreading the heating into the deep profile and removing humidity pro-rata. But unlike the convection scheme call to `PROFILEHEAT`, the rate `FRSST` is now one day. 

---
* `VDIFFTEND(J,UGTVDIFF,VGTVDIFF,TGTVDIFF,QGTVDIFF)`:  Called by `DIABATIC`. Returns tendencies for zonal and meridional wind, temperature and specific humidity due to vertical diffusion. Works on one latitude pair at a time. For a description of the vertical diffusion see Appendix A section 5 and fig. A4. 

This subroutine sets up damping rates due to vertical diffusion according to the damping rate profile `PRDAMP`, which is defined on sigma layer boundaries. `DM` and `DP` refer to the layer boundaries above and blow a given sigma level. Variables such as `UGM` and `UGP` are assigned to represent the values in fictitious layers above and below the vertical domain so that different boundary conditions can be imposed. We choose damped boundary conditions with these variables fixed at the reference values at the adjacent (top and bottom) levels. 

It is at this point that the anomalous boundary flux due to SSTAs is added in the case that this is selected by setting `ISSTTRAN=4`. The SSTA is defined again as a local variable like in `SSTTEND`. Anomalies in temperature and humidity (the difference in saturation value) are calculated and added to the bottom boundary condition. The optional boost in land-surface humidity flux by the factor `QGPFAC` is also implemented here. 

A simple centred difference is applied to find diffusive flux convergence and this is assigned to the  tendencies of momentum, temperature and specific humidity. Only temperature and specific humidity grid variables are updated as there is no need to keep the momentum up to date. 

---
* `LSRTEND(J,TGTLSR,QGTLSR)`: Called by `DIABATIC`. Returns height dependent tendencies for temperature and specific humidity associated with resolved condensation (large scale rain). Works on one latitude pair at a time. See [Chapter 4, section 4c](https://dreamusermanual.readthedocs.io/en/latest/Chapter4.html#large-scale-rain) for a description of the large scale rain scheme. 

This subroutine calculates saturated specific humidity QSAT at every level at a given grid point and compares it with the local specific humidity (or its smoothed value `QGTR` if `LTRUNCQ` is enabled). The supersaturation `QDIFF` is the difference between the two, and it is used directly to calculate the local specific humidity tendency `QGTLSR` using the rate `FRCOND` derived from the timescale `TAUCOND`. The associated latent heating rate is applied to the local temperature tendency `TGTLSR`. A limit is set to the maximum value of supersaturation that can be rained out at any given level. It is current;y set in the code as `QDIFFCAP=50./16. * 1.e-4`. For a standard value of `TAUCOND=0.0625` (i.e. 1.5 hours) this means that the maximum precipitation rate possible (provided the limit is hit at every level) is 50 mm/day. 

For diagnostic output, the rain rate `PPTRATE` (mm/day) is updated level by level. Note that this 2-d grid variable is the sum of all precipitation in the model. It is updated directly from this `LSR` scheme and also from the deep convection and SSTA schemes in `PROFILEHEAT`. Likewise the 3-d grid diagnostic variable for condensation heating `CONDHEAT` (deg/day) is updated level by level. 

Finally the grid values of temperature `TG` and specific humidity `QG` are updated with the `LSR` tendencies. 

---
* `CUSTOMMASK(JN,JS,IW,IE,WRKMASK)`: Called by `INIVAR`. Returns a 2-d mask for a region defined by latitude and longitude boundaries `JN`,`JS`,`IW`,`IE`. 

A box is bounded by `JN` to the north, `JS` to the south, `IW` to the west and `IE` to the east. These are Gaussian latitudes and equally spaced longitudes with the first point on Greenwich. The box is filled with the value 1, so information is retained inside the box when the mask is applied. Outside this box the values are zero so this area is masked out. On the boundaries the value is 0.5 for a smooth transition from unmasked to masked areas. 

This subroutine is called to define the SST mask `RMASKSST`: currently four options, the full tropics, and the Pacific, Atlantic and Indian tropical oceans (these three masks are contiguous). The boundaries of these masks for T42 and T31 are given in the include file setup.f. 

This subroutine is also called to define the nudging mask `RMASKNDG`: the default values included in `setup.f `are for the full tropics. 
