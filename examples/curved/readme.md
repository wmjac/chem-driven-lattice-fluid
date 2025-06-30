This directory contains the output data from the following example case:
```
Example: Simulation with ~547 molecules in the dilute phase and ~225 molecules in the condensed phase

                   L     ε      ∆f     ∆µ     Λ     η    N_vap   far-field threshold   start  batch_size       R
python curved.py  101  -2.95  1.7337  2.00   100   1.0    547             36             0        1         8.462843
```

lattice => The instantaneous configuration of the system at the end of simulation.<br />
list_sz => The number of B-molecules belong to the droplet measured every 100 sweeps of kMC events.<br />
           Sometimes useful for determining whether the system has reached the steady-state.<br />
rhoB => Average B-molecule density profile along the x and y-axes passing through the CoM of the droplet<br />
rhoI => The same but for I-molecules.<br />

The following data contain 3 heatmaps for which the index 0 = condensed droplet; 1 = interface; 2 = dilute phase.<br />
entropy => Steady-state entropy production rate density<br />
jB  => B-molecule diffusive flux along the x and y-axes passing through the CoM of the droplet<br />
jI  => The same but for I-molecules.<br />
NBI => B=>I chemical reactive flux density. Reaction along both passive and driven pathways are counted together.<br />
NIB => I=>B chemcial reactive flux density. Reaction along both passive and driven pathways are counted together.<br />

