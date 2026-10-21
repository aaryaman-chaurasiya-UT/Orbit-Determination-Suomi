import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import odlib_chaurasiya as od
import mog_mcmc as mg
import baby_od as bo

n_iterations = 10



raList = [5.245994310361089, 5.187812305304815, 5.163737669935118]
decList = [0.33809112309958933, 0.3395882277468556, 0.3328216831996098]



raSD = [np.radians(0.3788657604218315/3600 * 15), np.radians(0.07519353009683982/3600 * 15), np.radians(0.019875680186487443/3600 * 15)]
decSD = [np.radians(0.3336519673283078/3600), np.radians(0.07916573787554171/3600), np.radians(0.08989177283496019/3600)]


a = []
e = []
I = []
omega = []
Omega = []
Mm = []

mog_output = []

for i in range(n_iterations):
    ras = np.random.normal(raList, raSD)
    decs = np.random.normal(decList, decSD)
    mog_output = mg.mog(ras, decs)
    if mog_output[0] < 0:
        continue
    # a.append(orbital_elements[0])
    # e.append(orbital_elements[1])
    # I.append(orbital_elements[2])
    # omega.append(orbital_elements[3])
    # Omega.append(orbital_elements[4])
    # Mm.append(orbital_elements[5])
    print(mog_output)

