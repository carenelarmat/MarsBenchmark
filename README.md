# MarsBenchmark
Finite difference/spectral element method codes benchmark for 1D Mars model with steps

Notes: 
-Source is an explosion of Mo = 3.5e6 N.m for the three codes: checked. 
-STF has important effect on the waveforms: checked. More SEM will be posted. 
-Velocity models format:
    .AxiSEM: format 'bm' ; It interpolates in a stepwise model. (1) find the layer; (2) interpolate between the bottom and top of the layer. 
    .OpenSWPC: format 'lhm'; It is a model by STEPS (constant per layer). 
    .SPECFEM3D: format 'xyz'; It is a smooth tomography model with even sampling and linear interpolation. **This is the choice for the moment.**
    
** ** Velocity models differ ** **

    
