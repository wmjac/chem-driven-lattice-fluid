import numpy as np
from numba import njit
import sys
import os
from numba.typed import List

BONDING = 1
SOLVENT = 0
INERT = -1

@njit
def set_rate(e,df,µdr,eta):
    kIB = np.full(5,eta).astype(np.float64)
    kBI = np.full(5,eta).astype(np.float64)

    # Driven reaction pathway
    for nB in range(5):
        t = np.exp(e*nB+df+µdr)
        if t < 1:
            kBI[nB] *= t
        else:
            kIB[nB] /= t

    # Undriven reaction pathway
    for nB in range(5):
        kBI[nB] += np.exp(e*nB+df)
        kIB[nB] += 1.0

    return kIB, kBI

# Setting matrices for kMC event rates
# matrix for nearest-neighboring B-molecules (matrix_nB)
# matrix for nearest-neighboring B and I-molecules (matrix_nBI)
# matrix for kMC rates (matrix_rate)
@njit
def set_rate_matrix(kIB,kBI,lattice,Ly,Lx,e,df,µdr,D,eta):
    matrix_nB = np.full((Ly,Lx),0,dtype=np.int8) # nearest-neighboring B molecules
    matrix_nBI = np.full((Ly,Lx),0,dtype=np.int8) # nearest-neighboring B and I molecules
    matrix_rate = np.full((Ly,Lx),0,dtype=np.float64)
    for y in range(Ly):
        for x in range(Lx):
            nB = 0
            nBI = 0
            for i,j in ((1,0),(-1,0),(0,1),(0,-1)):
                if lattice[(y+j)%Ly,(x+i)%Lx] == BONDING:
                    nB += 1
                    nBI += 1
                elif lattice[(y+j)%Ly,(x+i)%Lx] == INERT:
                    nBI += 1
            matrix_nB[y,x] = nB
            matrix_nBI[y,x] = nBI
            if lattice[y,x] == 1:
                matrix_rate[y,x] = kBI[nB] + D*np.exp(e*nB)*(4-nBI)/4
            elif lattice[y,x] == -1:
                matrix_rate[y,x] = kIB[nB] + D*(4-nBI)/4

    return matrix_nB, matrix_nBI, matrix_rate

@njit
def update_matrix_rate_rxn(kIB,kBI,e,D,lattice,matrix_nB,matrix_nBI,matrix_rate,update,Ly,Lx,y,x):
    for i,j in ((1,0),(-1,0),(0,1),(0,-1)):
        y1, x1 = (y+j)%Ly, (x+i)%Lx
        nB = matrix_nB[y1,x1]
        nB_new = nB + update
        matrix_nB[y1,x1] = nB_new

        nBI = matrix_nBI[y1,x1]

        if lattice[y1,x1] == INERT:
            matrix_rate[y1,x1] = kIB[nB_new] + D*(4-nBI)/4
        elif lattice[y1,x1] == BONDING:
            matrix_rate[y1,x1] = kBI[nB_new] + D*np.exp(e*nB_new)*(4-nBI)/4

@njit
def update_matrix_rate_displace(kIB,kBI,e,D,lattice,matrix_nB,matrix_nBI,matrix_rate,molecule_type,\
        update_y,update_x,Ly,Lx,y,x):
    # Around the original site
    for i,j in ((1,0),(-1,0),(0,1),(0,-1)):
        y1, x1 = (y+j)%Ly, (x+i)%Lx
        nB = matrix_nB[y1,x1]
        if molecule_typee == BONDING:
            nB_new = nB-1
        else:
            nB_new = nB
        matrix_nB[y1,x1] = nB_new

        nBI_new = matrix_nBI[y1,x1]-1
        matrix_nBI[y1,x1] = nBI_new

        molecule_type_new = lattice[y1,x1]
        if molecule_type_new == 1:
            matrix_rate[y1,x1] = kBI[nB_new] + D*np.exp(e*nB_new)*(4-nBI_new)/4
        elif molecule_type_new == -1:
            matrix_rate[y1,x1] = kIB[nB_new] + D*(4-nBI_new)/4
    # Around the new site
    for i,j in ((1,0),(-1,0),(0,1),(0,-1)):
        y1,x1 = (y+update_y+j)%Ly, (x+update_x+i)%Lx
        nB = matrix_nB[y1,x1]
        if molecule_type == 1:
            nB_new = nB+1
        else:
            nB_new = nB
        matrix_nB[y1,x1] = nB_new

        nBI_new = matrix_nBI[y1,x1]+1
        matrix_nBI[y1,x1] = nBI_new

        molecule_type_new = lattice[y1,x1]
        if molecule_type_new == 1:
            matrix_rate[y1,x1] = kBI[nB_new] + D*np.exp(e*nB_new)*(4-nBI_new)/4
        elif molecule_type_new == -1:
            matrix_rate[y1,x1] = kIB[nB_new] + D*(4-nBI_new)/4

