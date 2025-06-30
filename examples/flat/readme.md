```
Example: 8 independent simulations (= batch_size) from index 0 (= start) to 7

               Ly    Lx     ε     ∆f      ∆µ     Λ    η   batch_size   start
python flat.py 50   200   -2.95  1.7337  2.00   100  1.0      8          0
```
lattice => The instantaneous configuration of the system at the end of simulation.<br />
left  => Snapshots of instantaneous interface on the left-hand side collected every 100 kMC events.<br />
right => The same but for the right-hand side interface.<br />
rhoB => Average B-molecule density profile along the direction perpendicular to the average direction of the interface.<br />
rhoI => The same but for I-molecules.<br />

The following data contain 3 heatmaps for which the index 0 = condensed phase; 1 = interface; 2 = dilute phase.<br />
entropy => Steady-state entropy production rate density<br />
jB  => B-molecule diffusive flux along the the direction perpendicular to the average direction of the interface.<br />
jI  => The same but for I-molecules.<br />
NBI => B=>I chemical reactive flux density. Reaction along both passive and driven pathways are counted together.<br />
NIB => I=>B chemcial reactive flux density. Reaction along both passive and driven pathways are counted together.<br />

