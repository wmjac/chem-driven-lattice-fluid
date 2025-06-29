Needs "numba" python package for faster calculation.

# Coexistence simulation across a flat interface
src/flat.py => Concentration profiles, diffusive and reactive flux densities, entropy production rate density, and interfacial roughness
```
Example: 8 independent simulations (= batch_size) from index 0 (= start) to 7

               Ly    Lx     ε     ∆f      ∆µ     Λ    η   batch_size   start
python flat.py 50   200   -2.95  1.7337  2.00   100  1.0      8          0 
```

# Coexistence simulation across a curved interface
src/curved.py => The same but flux densities are measured along the principal axes passing through the CoM of the droplet only
```
Example: Simulation with ~547 molecules in the dilute phase and ~225 molecules in the condensed phase

                   L     ε      ∆f     ∆µ     Λ     η    N_vap   far-field threshold   start  batch_size       R
python curved.py  101  -2.95  1.7337  2.00   100   1.0    547             36             0        1         8.462843
```
Example output data for the corresponding case is available in examples/curved.

# First-principles phase diagram prediction
theory/FLEX_phase_diagram.py => Prediction on nonequilibrium phase coexistence with as in figure 3 of the main text.
                                NOTE: This prediction is for macroscopic phase coexistence with flat interface.
```
Example: Predictions at Λ = 10^1, 10^2, 10^3, and µdr = -2.0, 2.0 at specified parameters ε = -2.95 and \rhov = 0.05.

                                 ε     rhov
python FLEX_phase_diagram.py   -2.95   0.05
```
Example output data for the corresponding case is available in examples/flat.
