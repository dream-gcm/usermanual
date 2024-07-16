# Chapter 1: Inception - Introduction to DREAM
![chapter 2 fig](./img/chapter_1.png)

## Preamble
In 1983,  Sir Brian Hoskins published a lecture in the QJ under the title “Dynamical processes in the atmosphere and the use of models” in which he commented on the interplay between observations, sophisticated numerical models and our understanding of dynamical processes. He advocated a hierarchical approach in which dynamical models of intermediate complexity play a role (I made a contribution to this vision in Hall 2004, but I don’t think anyone read it). There is always a tradeoff between physical realism and conceptual understanding. Models of varying complexity can bridge the gap. 

Four decades later, numerical modelling of the atmosphere and climate is more complex than ever. It has become a truly interdisciplinary endeavour shared by communities and worked on in teams, with a wide range of applications. At the same time, at a much more modest scale, a few simple models of the atmosphere have emerged to tackle various questions in a more restricted and often more economical way. DREAM is one of these models. 

The real world is complicated but our brains are limited, and indeed we are in the process of replacing them altogether with something more efficient. For those who still seek understanding, some sort of model hierarchy is needed. A model whose results are realistic enough to be useful, but whose physical specification is simple enough to offer some insight. One way to achieve this is to allow some of the solution to be constrained by data. There are several ways in which DREAM can interact with data that will be explained in this guide. This class of model is sometimes referred to as a “diagnostic model”. 

DREAM can produce realistic simulations of the atmosphere based on dynamics alone. It can also be used in highly idealised configurations. Because of the way its forcing can be manipulated, DREAM is not just a model. It is a hierarchy of models. DREAM stands for Dynamical Research Empirical Atmospheric Model. It is a dynamical model intended mainly for research. It is not a statistical model, but since some elements are taken from data, the word Empirical appears in the acronym. This guide is an overview of how to use the model. It is part technical manual, part research manual as I will try to explain not only the scripts and the code, but also some diagnostic techniques that arise naturally from using DREAM. 

---
## Empirical forcing and data integration
The problem of how to force a simple dynamical model to produce an equilibrium climate solution has often been approached by using relaxation forcing. An idealised radiative convective equilibrium temperature field is specified, and the model temperature field is relaxed linearly towards it on a chosen timescale. Since the radiative convective equilibrium is hydrodynamically unstable, the atmosphere never attains this state, nor even approaches it closely (unless a very short relaxation timescale is imposed). So it is difficult to appeal to data to deduce directly what this state should be.

DREAM is based on an alternative approach first used by Roads (1987) to make a cheap forecast model. A sequence of observed initial conditions is used and the unforced model is integrated for just one timestep. The negative average of the one-timestep tendencies thus produced is then adopted as the forcing on the right hand side of the model equations. We assume that the set of initial conditions represents a stationary climate state, and that the forcing of the atmosphere can be viewed as time independent. Under these assumptions, this forcing represents the missing term that corrects the systematic errors of an unforced model.

Some form of dissipation is also included, and the combination of forcing and dissipation is mathematically equivalent to the relaxation forcing approach discussed above. But instead of specifying an unknown equilibrium state and a dissipation timescale, we just specify the dissipation and appeal to data to furnish the forcing.

The result is a GCM that is simple in conception, based entirely on dynamics, but gives realistic enough simulations to be used for a variety of climate studies. DREAM can also be used in perturbation mode. The only thing that changes is that the forcing is designed to hold a fixed basic state in place, a technique first employed by Jin and Hoskins (1995). A perturbation is then added either to the forcing, as was the case with Jin and Hoskins, or to the initial condition (see for example Hall and Sardeshmukh, 1998). The model solution arising from the perturbation can be analysed. If the perturbation is constrained to be small, the solution will be linear. 

The data used with DREAM comes from four-times daily ERA-interim reanalysis from 1979-2016 (Dee et al, 2011). DREAM interacts with a version of this dataset that is written in the same spectral basis as the model output. The data can also be used to nudge selected regions of the model throughout the integration. A version of the empirical forcing with an annual cycle is also available. 

---
## How is DREAM different from other simple GCMs ?
DREAM is based on the spectral primitive equation model code first introduced by Hoskins and Simmons (1975, HS75). This code was initially used to study baroclinic wave lifecycles and quickly became one of the staple tools for dynamical studies at the Reading University Meteorology department, pressed into service for a diverse range of topics in synoptic meteorology and global climate dynamics. As a purely dynamical model, it lacks the physical source terms that maintain the climate, so for longer integrations, or for studies of perturbations on a specified basic state, a prescription is needed for the right hand side of the equations. Various solutions have been implemented, and as the model was used for more sophisticated applications, further representations of physical processes were added. At the same time a sequence of technical modifications were also made to simplify the code and make it more portable. That model is now known as the “IGCM” and the current version (Joshi et al, 2015) is shared by a consortium of users at UK universities. 

DREAM has the same dynamical core as the Reading IGCM, but it has far fewer physical parameterisations available and has not been developed by a community like the Reading model. Instead the development has been more in the direction of working with data for diagnostic modelling. The paraemterizations in DREAM are home-grown, and semi-empirical. 

Here’s a list of some models that fit into the simple GCM niche: 

* IGCM - As mentioned above, based on code originally developed at Reading University back in the 1970s and identical to DREAM in its dynamical core. Runs as a physically based GCM with simple parameterisations. 

* SPEEDY - Developed at ICTP in Trieste. Based on the GFDL spectral dynamical core. Runs as a physically based GCM with simple parameterisations. 

* PUMA - Developed at the University of Hamburg. Based on the ECHAM spectral dynamical core (which in turn was derived from the ECMWF model, which originally evolved from the Reading model). Works with restoration forcing and relatively simple dissipation. 

* ISCA - Developed at the University of Exeter. Based on the GFDL spectral dynamical core. Can be forced at various levels of complexity from relaxation to full radiation. Applicable to Earth and other planets. 

---
## What can you do with DREAM ?
In its simplest form DREAM is a dynamical model that either simulates a perpetual season or can be used to study perturbations about a fixed basic state, in both cases with time-independent forcing. An extension to the forcing has been developed that includes an annual cycle. In this way DREAM can be used for climate studies in which a one-to-one correspondence with historical data is required. DREAM is designed to work with the reanalysis data that is used to calculate the empirical forcing. This dataset can be consulted during a run to constrain predefined regions of the world to a time sequence of observations by “nudging” on a specified timescale. Further extensions to DREAM have been developed, including interaction with moist thermodynamics associated with the model’s specific humidity variable, and the response to tropical SST anomalies.  DREAM has been used for a wide range of applications, including fundamental properties of the midlatitude jets and baroclinic waves, easterly waves over West Africa, teleconnections from tropical convection, the annual cycle and seasonal prediction of continental rainfall. A complete list of publications is given in [Appendix E](https://dreamusermanual.readthedocs.io/en/latest/AppendixE.html). 

---
## Some references
* Dee D.P., et al, 2011: The ERA INTERIM reanalysis: Configuration and performance of the data assimilation system. Quart. J. Roy. Meteor. Soc., 137, 553–597. 
* Hall, N.M.J., 2000: A simple GCM based on dry dynamics and constant forcing. J. Atmos. Sci., 57, 1557-1572.
* Hall, N.M.J., 2005: The atmospheric response to boundary forcing and the use of diagnostic models. ERCA6, EDP sciences, C. Boutron ed. J. Phys IV, France, 121, pp 125-137.
* Hall, N.M.J., S. Leroux and T. Ambrizzi, 2019: Transient contributions to the forcing of the atmospheric annual cycle: A diagnostic study with the DREAM model. Climate Dyn. [https://doi.org/10.1007/s00382-018-4539-y](https://doi.org/10.1007/s00382-018-4539-y)
* Hall, N.M.J. and P.D. Sardeshmukh, 1998: Is the time mean Northern Hemisphere flow baroclinically unstable ?  J. Atmos. Sci., 55, 41-56.
* Hoskins, B.J., 1983: Dynamical processes in the atmosphere and the use of models. Quart. J. Roy. Meteor. Soc., 109, 1-21. 
* Hoskins, B. J., and A. J. Simmons, 1975: A multi-layer spectral model and the semi-implicit method. Quart. J. Roy. Meteor. Soc., 101, 637–655.
* Jin, F., and B. J. Hoskins, 1995: The direct response to tropical heating in a baroclinic atmosphere. J. Atmos. Sci., 52, 307–319. 
* Joshi, M., M. Stringer, K. van der Wiel, A. O’Callaghan and S. Fueglistaler, 2015: IGCM4: a fast, parallel and flexible intermediate climate model. Geosci. Model Dev., 8, 1157–1167.
* Roads, J. O., 1987: Predictability in the extended range. J. Atmos. Sci., 44, 3495–3527. 
* Simmons, A. J., and D. M. Burridge, 1981: An energy and angular-momentum conserving vertical finite-difference scheme and hybrid vertical coordinates. Mon. Wea. Rev., 109, 758–766. 
* Simmons, A. J., and B. J. Hoskins, 1978: The lifecycles of some nonlinear baroclinic waves. J. Atmos. Sci., 35, 414–432.

