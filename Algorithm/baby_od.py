#baby_od

from odlib_LeeDiPaolo import *
from ephem_gen import *
import numpy as np

def get_jd_from_ut(date:str): # converts a ut date/time string into a jd
    t_dec=float(date[11:13])+float(date[14:16])/60+float(date[17:19])/3600
    yr=float(date[:4])
    month=float(date[5:7])
    day=float(date[8:10])
    
    j0=367*yr-np.floor(7/4*(yr+np.floor((month+9)/12))) + np.floor(275/9*month)+day+1721013.5
    jd=j0+t_dec/24

    return jd

def conv_vectors_to_ecliptic(vector): # converts the vectors in equatorial to ecliptic
    obliq=np.deg2rad(23.4383661095)
    vy=vector[1]*np.cos(obliq)+vector[2]*np.sin(obliq)
    vz=-vector[1]*np.sin(obliq)+vector[2]*np.cos(obliq)

    vector_conv=np.array([vector[0], vy, vz])

    return vector_conv

def get_semi_major_axis(r, r_dot): # gets the semi major axis
    a=((2/np.linalg.norm(r)) - np.dot(r_dot, r_dot))**-1
    
    return a #au

def get_eccentricity(r, r_dot, a): #calculates the eccentricity
    e=np.sqrt(1-(np.linalg.norm(np.cross(r,r_dot)))**2/a)
    
    return e #unitless float

def get_I(r, r_dot): #calculates the inclination
    I=np.rad2deg(np.acos((np.cross(r, r_dot)[2])/np.linalg.norm(np.cross(r, r_dot))))
    
    return I #degrees 

def get_omega(r,r_dot,I): #calculates capital omega, the longitude of the ascending node
    incl=np.deg2rad(I)
    
    h=np.linalg.norm(np.cross(r,r_dot))
    
    hx=r[1]*r_dot[2]-r[2]*r_dot[1]

    hy=r[2]*r_dot[0]-r[0]*r_dot[2]
    
    y=hx/(h*np.sin(incl))
    x=-hy/(h*np.sin(incl))

    omega=np.rad2deg(np.arctan2(y,x))
    if omega<0:
        omega+=360

    return omega #degrees

def get_f(a,e,r,r_dot): #calculates f, the true anomaly
    y=np.dot(r, r_dot)/(e*np.linalg.norm(r))*np.sqrt(a*(1-e**2))
    x=1/e*((a*(1-e**2))/np.linalg.norm(r)-1)

    f=np.arctan2(y,x)

    return f #radians

def get_womega(r, I, f, omega): #calculates lowercase omega, the longitude of the perihelion
    y= r[2]/(np.linalg.norm(r)*np.sin(np.deg2rad(I)))
    
    x=(r[0]/np.linalg.norm(r)+np.cos(np.deg2rad(I))*y*np.sin(np.deg2rad(omega)))/np.cos(np.deg2rad(omega))
    
    womega=np.rad2deg(np.arctan2(y, x)-f)
    if womega<1:
        womega+=360
    return womega #degrees

def get_mean_anomaly_at_epoch(eccentricity,r,a,f): #calculates the mean anomaly at the observation time
    E=np.acos(1/eccentricity*(1-np.linalg.norm(r)/a))
    true_anom=np.deg2rad(f)

    # sinf=np.sin(f)
    # if sinf>=0:
    #     m_m=np.rad2deg(E-eccentricity*np.sin(E))
    #     return m_m
    # else: 
    #     m_m=np.rad2deg(E-eccentricity*np.sin(E))
    #     return 360-m_m
    
    if np.pi<=true_anom<=2*np.pi:
        E=360-E
        m_m=np.rad2deg(E-eccentricity*np.sin(E))
        return m_m
    
    m_m=np.rad2deg(E-eccentricity*np.sin(E))
    
    return 360-m_m #degrees

def get_baby_od(r, r_dot, tm): #calculates all the orbital elements with an input of r and r dot

    #r=np.array([[float(input('Input the x of r: ')), float(input('Input the y of r: ')), float(input('Input the z of r: '))]]) # au 
    # np.array([[0.1484643559932487,-1.352307084329128,-0.4420279417598032 ]]) 
    #r_dot= np.array([[float(input('Input the x of vel: ')), float(input('Input the y of vel: ')), float(input('Input the z of vel: '))]]) # au/d
    #np.array([[0.01627996652684147,0.0026131934983923315,0.0014336794520893512 ]])
    t0= 2460874.75   #input('Input the epoch time: ') # JD
    
    #2460858.747470817 

    #r=conv_vectors_to_ecliptic(r)
    #r_dot=conv_vectors_to_ecliptic(r_dot)/ 0.0172020989484
    r_dot=r_dot/0.0172020989484
    a=get_semi_major_axis(r,r_dot)
    e=get_eccentricity(r,r_dot,a)
    incl=get_I(r,r_dot)
    omega=get_omega(r,r_dot,incl)
    f=get_f(a,e,r,r_dot)
    womega=get_womega(r, incl, f, omega)

    mean_motion=get_orbit_mean_motion(a)

    M_m=get_mean_anomaly_at_epoch(e, r, a, f)
    M0=np.rad2deg(np.deg2rad(M_m)+mean_motion*(t0-tm))


    print(f'a: {a} \ne: {e} \nI: {incl} \nOmega: {omega} \nWomega: {womega} \nM-m: {M_m}\nM0: {M0}')
    return (a, e, incl, omega, womega, M_m, M0)

#print(get_baby_od())