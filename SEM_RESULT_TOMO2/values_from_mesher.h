 
 !
 ! purely informative use
 !
 ! mesh statistics:
 ! ---------------
 !
 ! note: 
 !    the values are only approximate and differ for different processes
 !    because the CUBIT + SCOTCH mesh has
 !    a different number of mesh elements and points in each slice
 !
 ! number of processors =          144
 !
 ! number of ES nodes =    18.00000    
 ! percentage of total 640 ES nodes =    2.812500      %
 ! total memory available on these ES nodes (Gb) =    288.0000    
 !
 ! min vector length =           25
 ! min critical vector length =           75
 !
 ! master process: total points per AB slice =       127821
 ! total elements per AB slice = (will be read in external file)
 ! total points per AB slice = (will be read in external file)
 !
 ! total for full mesh:
 ! -------------------
 !
 !
 ! number of time steps =       150000
 !
 ! time step =   5.000000000000000E-004
 !
 ! attenuation uses:
 !  NSPEC_ATTENUATION =         1848
 ! 
 ! anisotropy uses:
 !  NSPEC_ANISO =            1
 ! 
 ! adjoint uses:
 !  NSPEC_ADJOINT =            1
 !  NGLOB_ADJOINT =            1
 ! 
 ! approximate least memory needed by the solver:
 ! ----------------------------------------------
 !
 ! size of arrays for the largest slice =    22.2807159423828       MB
 !                                      =   2.175851166248322E-002  GB
 !
 !   (should be below 90% or so of the amount of memory available per processor 
 core
 !   (if significantly more, the job will not run by lack of memory)
 !   (if significantly less, you waste a significant amount of memory)
 !
 ! check parameter to ensure the code has been compiled with the right values:
 &MESHER
 ABSORB_FREE_SURFACE_VAL = F
 /
 
