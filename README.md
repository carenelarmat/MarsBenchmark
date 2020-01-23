# MarsBenchmark
Finite difference/spectral element method codes benchmark for 1D Mars model with steps

Notes:

-Source is an explosion of Mo = 3.5e6 N.m for the three codes: checked. 

-STF has important effect on the waveforms: checked. SEM results have results for both Kupper and derivative of the Error function as seismic moment rate history. 

-Velocity models format:
    python scripts trying to mimick the *parameterization* of the codes are provided. 

    .AxiSEM: format 'bm' ; It interpolates in a stepwise model. (1) find the layer; (2) interpolate between the bottom and top of the layer. 
    .OpenSWPC: format 'lhm'; It is a model by STEPS (constant per layer). 
    .SPECFEM3D: format 'xyz'; It is a smooth tomography model with even sampling and linear interpolation. *This is the choice for the moment to facilitate the issue of parameterization.*
    
    
**Benchmarking failed because:
(1) Velocity models differ
(2) STF matter 
(3) code parameterization (bm is a versatile format but so requires quality control) 
**

    
