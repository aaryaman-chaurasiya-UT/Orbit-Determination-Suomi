import numpy as np
from odlib_LeeDiPaolo import *
from f_g_functions import *
from baby_od import *

def get_jd_from_ut(date:str): # converts a ut date/time string into a jd
    t_dec=float(date[11:13])+float(date[14:16])/60+float(date[17:19])/3600
    yr=float(date[:4])
    month=float(date[5:7])
    day=float(date[8:10])
    
    j0=367*yr-np.floor(7/4*(yr+np.floor((month+9)/12))) + np.floor(275/9*month)+day+1721013.5
    jd=j0+t_dec/24

    return jd

def adjust_obs_time(time, distance): # calculates the adjusted observation time 
    c=173.145
    adj_time=time-distance/c
    return adj_time

def calc_gaussian_time(time1, time2): #calculates all the gaussian times, taus
    k=0.0172020989484
    tau=k*(time1-time2)
    return tau

def calc_c1s(f1, f3, g1, g3): #calculates the c1
    c1=g3/(f1*g3-g1*f3)
    return c1

def calc_c3s(f1, f3, g1, g3): #calculates the c3
    c3=-g1/(f1*g3-g1*f3)
    return c3

def calc_d1s(f1, f3, g1, g3): #calculates the d1
    d1=-f3/(f1*g3-g1*f3)
    return d1

def calc_d3s(f1, f3, g1, g3): #calculates the d3
    d3=f1/(f1*g3-g1*f3)
    return d3

def mog(ra, dec): #runs the mog code using an input file
    k=0.0172020989484

    ut_date_time1='2025 06 23 07:34:00'
    ut_date_time2='2025 07 08 03:08:05'
    ut_date_time3='2025 07 09 06:00:00'

    ra1=ra[0]
    dec1=dec[0]
    ra2=ra[1]
    dec2=dec[1]
    ra3=ra[2]
    dec3=dec[2] #taking all the values from the files and initializing the proper variables

    jd1=get_jd_from_ut(ut_date_time1) #converts the ut date/times to jd
    jd2=get_jd_from_ut(ut_date_time2)
    jd3=get_jd_from_ut(ut_date_time3)

    R1_components=[-3.097091501145251E-02, 9.321078564668941E-01, 4.040169797051142E-01]
    R2_components=[-2.781261138754456E-01, 8.971888181261354E-01, 3.888824371765016E-01]
    R3_components=[-3.609839915836430E-01, 8.718534148353698E-01, 3.779459286625187E-01]

    R1=np.array( [float(R1_components[0]), float(R1_components[1]), float(R1_components[2])] ) #gets the earth-sun vectors from the file
    R2=np.array( [float(R2_components[0]), float(R2_components[1]), float(R2_components[2])] )
    R3=np.array( [float(R3_components[0]), float(R3_components[1]), float(R3_components[2])] )

    tau1=calc_gaussian_time(jd1, jd2) #calculates all the initial taus based on the observation times
    tau3=calc_gaussian_time(jd3, jd2)
    tau0=calc_gaussian_time(jd3, jd1)

    c1=tau3/tau0 #using Kepler's method get initial values for c1, c3
    c2=-1
    c3=-tau1/tau0

    rho1_hat=np.array([np.cos(ra1)*np.cos(dec1), np.sin(ra1)*np.cos(dec1), np.sin(dec1)]) #calculate the rho hats
    rho2_hat=np.array([np.cos(ra2)*np.cos(dec2), np.sin(ra2)*np.cos(dec2), np.sin(dec2)])
    rho3_hat=np.array([np.cos(ra3)*np.cos(dec3), np.sin(ra3)*np.cos(dec3), np.sin(dec3)])

    D0= np.dot(rho1_hat, np.cross(rho2_hat, rho3_hat)) 

    D_mat=np.array( [[ np.dot(np.cross(R1,rho2_hat),rho3_hat), np.dot(np.cross(R2,rho2_hat),rho3_hat), np.dot(np.cross(R3,rho2_hat),rho3_hat) ],
                     [ np.dot(np.cross(rho1_hat,R1),rho3_hat), np.dot(np.cross(rho1_hat,R2),rho3_hat), np.dot(np.cross(rho1_hat,R3),rho3_hat) ],
                     [ np.dot(rho1_hat, np.cross(rho2_hat, R1)), np.dot(rho1_hat, np.cross(rho2_hat, R2)), np.dot(rho1_hat, np.cross(rho2_hat, R3)) ]])

    #sets up all the formulas for the D values in order to later calculate the rhos

    rho1=(c1*D_mat[0,0]+c2*D_mat[0,1]+c3*D_mat[0,2])/(c1*D0)
    rho2=(c1*D_mat[1,0]+c2*D_mat[1,1]+c3*D_mat[1,2])/(c2*D0)
    rho3=(c1*D_mat[2,0]+c2*D_mat[2,1]+c3*D_mat[2,2])/(c3*D0) #calculating the initial rhos using the D and c values

    r1=rho1*rho1_hat-R1 #calculating the initial position of the asteroid using the fundamental triangle
    r2=rho2*rho2_hat-R2
    r3=rho3*rho3_hat-R3
    
    r12_dot=(r2-r1)/-tau1
    r23_dot=(r3-r2)/tau3

    r2_dot=tau3/tau0*r12_dot-tau1/tau0*r23_dot #calculating r2 dot using the weighted sum method

    t1=adjust_obs_time(jd1,rho1) #adjusting for the light travel time
    t2=adjust_obs_time(jd2,rho2)
    t3=adjust_obs_time(jd3,rho3)
    
    rho2_place=0
    i=0
    rho_difference=0

    flag=int(input('For 3rd term-> 0, 4th term-> 1, function-> 2: ')) #asks the user which method they want for f&g functions (3 term, 4 term, function)

    while np.abs(rho2-rho2_place)>1e-12 and i<1000 and np.abs(rho2-rho2_place)>rho_difference:
        rho2_place=rho2
        rho_difference=np.abs(rho2-rho2_place)

        tau1=calc_gaussian_time(t1, t2) #recalculates the taus since the observation times have been adjusted
        tau3=calc_gaussian_time(t3, t2)
        tau0=calc_gaussian_time(t3,t1)

        f1=f_function(tau1, r2, r2_dot, flag) #calculates f1, f3 using the f functions
        f3=f_function(tau3, r2, r2_dot, flag)

        g1=g_function(tau1, r2, r2_dot, flag) #calculates g1, g3 using the g functions
        g3=g_function(tau3, r2, r2_dot, flag)

        c1=calc_c1s(f1, f3, g1, g3) #recalculates the c values to be more accurate
        c3=calc_c3s(f1, f3, g1, g3)

        d1=calc_d1s(f1, f3, g1, g3) #calculates the d values 
        d3=calc_d3s(f1, f3, g1, g3)

        rho1=(c1*D_mat[0,0]+c2*D_mat[0,1]+c3*D_mat[0,2])/(c1*D0) #recalculates the rhos using the new c values and D values
        rho2=(c1*D_mat[1,0]+c2*D_mat[1,1]+c3*D_mat[1,2])/(c2*D0)
        rho3=(c1*D_mat[2,0]+c2*D_mat[2,1]+c3*D_mat[2,2])/(c3*D0)

        r1=rho1*rho1_hat-R1 #recalculating the position vectors using the fundamental triangle
        r2=rho2*rho2_hat-R2
        r3=rho3*rho3_hat-R3

        r2_dot=d1*r1+d3*r3 #recalculating r2 dot using the d values we calculated earlier

        t1=adjust_obs_time(jd1,rho1) #adjusting for time again now that we have more accurate distances
        t2=adjust_obs_time(jd2,rho2)
        t3=adjust_obs_time(jd3,rho3)

        i+=1
    r2_dot=r2_dot*k #converting r2 dot vector to gaussian time

    r2_ecliptic=conv_vectors_to_ecliptic(r2) #converting the vectors to the ecliptic plane
    r2_dot_ecliptic=conv_vectors_to_ecliptic(r2_dot)

    return (r2_ecliptic, r2_dot_ecliptic, t2)

ra=[]
dec=[]

mog_output=mog(ra,dec)

orbital_elements=get_baby_od(mog_output[0], mog_output[1],mog_output[2])




