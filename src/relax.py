import numpy as np
from numba import njit
import sys
import os
from numba.typed import List
from search import condensed_search, dilute_search
from set_rate import set_rate_matrix, update_matrix_rate_rxn, update_matrix_rate_displace

BONDING = 1
SOLVENT = 0
INERT = -1

DILUTE = 2
INTERFACE = 1
CONDENSED = 0

# Run simulation without collecting fluxes
@njit
def relax(kIB,kBI,lattice,Ly,Lx,e,df,µdr,D,eta,rng):
    # matrix for nearest-neighboring B-molecules (matrix_nB)
    # matrix for nearest-neighboring B and I-molecules (matrix_nBI)
    # matrix for kMC rates (matrix_rate)
    matrix_nB, matrix_nBI, matrix_rate = set_rate_matrix(kIB,kBI,lattice,Ly,Lx,e,df,µdr,D,eta)

    for count in range(100*(lattice != 0).sum()):
        cumul = matrix_rate.sum()
        rn = rng.random()*cumul
        v = np.searchsorted(matrix_rate.cumsum(),rn,side="right")
        y = v // Lx
        x = v % Lx

        update_rxn = 0
        update_x = 0
        update_y = 0
        molecule_type = lattice[y,x] # 1 = BONDING; 0 = SOLVENT; -1 = INERT
        nB = matrix_nB[y,x]
        nBI = matrix_nBI[y,x]

        rn = rng.random() * matrix_rate[y,x]
        # Diffusion
        if (molecule_type == 1 and rn < D*np.exp(e*nB)*(4-nBI)/4) or\
                (molecule_type == -1 and rn < D*(4-nBI)/4):
            while True:
                rn = rng.random()
                if rn < 0.25:
                    if lattice[(y+1)%Ly,x] == SOLVENT:
                        update_y = 1
                        break
                elif rn < 0.5:
                    if lattice[y,(x+1)%Lx] == SOLVENT:
                        update_x = 1
                        break
                elif rn < 0.75:
                    if lattice[(y-1)%Ly,x] == SOLVENT:
                        update_y = -1
                        break
                else:
                    if lattice[y,(x-1)%Lx] == SOLVENT:
                        update_x = -1
                        break
            lattice[(y+update_y)%Ly,(x+update_x)%Lx] = molecule_type
            lattice[y,x] = 0
            matrix_rate[y,x] = 0
        # B->I
        elif molecule_type == 1:
            lattice[y,x] = INERT
            update_rxn = -1
            matrix_rate[y,x] = kIB[nB] + D*(4-nBI)/4

        # I->B
        elif molecule_type == -1:
            lattice[y,x] = BONDING
            update_rxn = 1
            matrix_rate[y,x] = kBI[nB] + D*np.exp(e*nB)*(4-nBI)/4

        # Update rate matrices after reaction
        if update_rxn:
            update_matrix_rate_rxn(kIB,kBI,e,D,lattice,matrix_nB,matrix_nBI,matrix_rate,update_rxn,Ly,Lx,y,x)

        # Update rate matrices after molecule displacement
        elif update_x != 0 or update_y != 0:
            update_matrix_rate_displace(kIB,kBI,e,D,lattice,matrix_nB,matrix_nBI,matrix_rate,molecule_type,\
                    update_y,update_x,Ly,Lx,y,x)

    return lattice

