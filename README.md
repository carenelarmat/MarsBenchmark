# MarsBenchmark
Finite difference/spectral element method codes benchmark for 1D Mars model with steps

**Important parameters for a successful benchmarking:**

**(1) Velocity models and their parameterization** very subtle variations can have important effect on the waveforms specially for this case where the source is at the surface which happens to be a region of rapid change of the seismic velocities. The bm format of AxiSEM is a very versatile format but it requires quality control from the user. 

**(2) STF matters** STF have a specific frequency content which can have big effect on the appareant group velocity of surfac waves. 


**Modelings in this directory:**

**OpenSWPC:** 

    Benchmark_KO_20191030. Velocity model entered as a 'lhm' model. 
    
**AxiSEM:** 

    AxiSEM_SEISShallow_2H_erf: Fist velocity model
    
    AxisSEM_SEIS_BM_v2: model for the benchmark
    
**AxiSEM3D:**

    AsiSEM3D_Ben010820: matches with first AxiSEM model
    
**SPECFEM3D:**

    SEM_RESULT_TOMOBM_ERF: Another velocity model, STF is an error function (like AxiSEM)
    
    SEM_RESULT_TOMOBM_KUPP: Another velocity model. STF is a Kupper wavelet
    
    SEM_RESULT_TOMO_FAT: model for the benchmkark

## Notes:


-Source is an explosion of Mo = 3.5e6 N.m for the three codes: checked. 

-STF has important effect on the waveforms: checked. SEM results have results for both Kupper and derivative of the Error function as seismic moment rate history. 

-Velocity models format:
    python scripts trying to mimick the *parameterization* of the codes are provided. 
    
    .AxiSEM: format 'bm' ; It interpolates in a stepwise model. (1) find the layer; (2) interpolate between the bottom and top of the layer. 
    .OpenSWPC: format 'lhm'; It is a model by STEPS (constant per layer). 
    .SPECFEM3D: format 'xyz'; It is a smooth tomography model with even sampling and linear interpolation. *This is the choice for the moment to facilitate the issue of parameterization.*




    
