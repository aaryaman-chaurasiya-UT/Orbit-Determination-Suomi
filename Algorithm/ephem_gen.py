# Ephemeris generation

import numpy as np
from odlib_LeeDiPaolo import *

def get_orbit_mean_motion(semi_major_axis:float)->float:
    mean_motion=float(0)
    mean_motion=0.0172020989484/np.sqrt(semi_major_axis**3)

    return mean_motion # returns the mean motion of the obj in rad/day

def get_mean_anomaly(m_naught:float, mean_motion:float, time:float, t_epoch:float)->float:
    mean_anomaly=float(0)
    mean_anomaly=np.deg2rad(m_naught)+mean_motion*(time-t_epoch)

    return mean_anomaly # radians

def get_ecc_anomaly(mean_anomaly:float, eccentricity:float )->float:
    ecc_anomaly_init=mean_anomaly
    ecc_anomaly_guess=mean_anomaly+eccentricity*np.sin(ecc_anomaly_init)
    place=float(0)
    while not(approx_equals(ecc_anomaly_init, ecc_anomaly_guess, 1e-15, 1e-15)):
        place=ecc_anomaly_guess
        ecc_anomaly_guess=mean_anomaly+eccentricity*np.sin(ecc_anomaly_guess)
        ecc_anomaly_init=place
    ecc_anomaly_guess=ecc_anomaly_guess

    return ecc_anomaly_guess # radians
    
def get_r_and_true_anomaly(semi_major_axis:float, ecc_anomaly:float, eccentricity:float)->tuple[float,float]:
    x=semi_major_axis*(np.cos(ecc_anomaly)-eccentricity)
    y=semi_major_axis*np.sqrt(1-eccentricity**2)*np.sin(ecc_anomaly)
    r=np.sqrt(x**2+y**2) 
    
    true_anomaly=np.arctan2(y,x)

    return (r, true_anomaly) # au, radians

def get_ecliptic_coords_of_r(r:float, true_anomaly:float, perihelion_long:float, ascending_long:float, inclination:float)->np.array:
    perihelion_long=np.deg2rad(perihelion_long)
    ascending_long=np.deg2rad(ascending_long)
    inclination=np.deg2rad(inclination)

    X=r*( np.cos(true_anomaly+perihelion_long)*np.cos(ascending_long) - np.cos(inclination)*np.sin(true_anomaly+perihelion_long)*np.sin(ascending_long) )
    Y=r*( np.cos(inclination)*np.cos(ascending_long)*np.sin(true_anomaly+perihelion_long) + np.cos(true_anomaly+perihelion_long)*np.sin(ascending_long) )
    Z=r*np.sin(inclination)*np.sin(true_anomaly+perihelion_long)
    r_components=np.array([[X,Y,Z]])

    return r_components # r is the sun to obj vector in au

# def get_earth_sun_vector(time:float, t_epoch)->np.array:
#     mean_motion=get_orbit_mean_motion(1)
#     mean_anomaly=get_mean_anomaly(204.230676, mean_motion, time, t_epoch)
#     ecc_anomaly=get_ecc_anomaly(mean_anomaly, 0.0167)
    
#     r_true_anomaly=get_r_and_true_anomaly(1, ecc_anomaly, 0.0167)
#     r=r_true_anomaly[0]
#     true_anomaly=r_true_anomaly[1]

#     sun_vector=-get_ecliptic_coords_of_r(r, true_anomaly, 102.94719, -11.26064, 0.00005)
#     earth_sun_vector=np.array([[-sun_vector[0,0], -sun_vector[0,1], -sun_vector[0,2]]])
#     return earth_sun_vector

def get_earth_obj_vector(earth_sun_vector, r)->np.array:
    earth_obj_vector=earth_sun_vector+r
    
    return earth_obj_vector # in au

def conv_earth_obj_vector_to_equ_coords(earth_obj_vector:np.array)->np.array:
    rho_x_eq=earth_obj_vector[0,0]
    rho_y_eq=earth_obj_vector[0,1]*np.cos(np.deg2rad(23.43596))-earth_obj_vector[0,2]*np.sin(np.deg2rad(23.43596))
    rho_z_eq=earth_obj_vector[0,1]*np.sin(np.deg2rad(23.43596))+earth_obj_vector[0,2]*np.cos(np.deg2rad(23.43596))
    rho_eq=np.array([[rho_x_eq, rho_y_eq, rho_z_eq]])
    
    return rho_eq

def calc_ra_and_dec(rho_eq:np.array)->tuple:
    rho_mag=np.sqrt(rho_eq[0,0]**2+rho_eq[0,1]**2+rho_eq[0,2]**2)
    dec=np.asin(rho_eq[0,2]/rho_mag)
    ra=np.rad2deg(np.arctan2(rho_eq[0,1]/(rho_mag*np.cos(np.deg2rad(dec))), rho_eq[0,0]/(rho_mag*np.cos(np.deg2rad(dec)))))
    if ra<0: 
        ra+=360
    dec=np.rad2deg(dec)
    
    return (ra, dec) # degrees

def generate_ephemeris()->str:
    t_epoch=2460800.5 #float(input('Input time epoch (t0): '))
    time= 2461226.0 #float(input('Input the time (t): '))
    semi_major_axis= 2.515867717273818 #float(input('Input the semi major axis (a): '))
    m_naught= 40.40257537134102 #float(input('Input the mean anomaly at epoch (m0): '))
    eccentricity= 0.6615482135209798 #float(input('Input the the eccentricity (e): '))
    inclination= 3.408173977587257 #float(input('Input the inclination (I): '))
    ascending_longitude= 271.3656150822561 #float(input('Input the longitude of the ascending node (Omega): '))
    perihelion_longitude= 134.3613660764138 #float(input('Input the longitude of the perihelion (womega): '))
    
    mean_motion=get_orbit_mean_motion(semi_major_axis)
    mean_anomaly=get_mean_anomaly(m_naught, mean_motion, time, t_epoch)
    ecc_anomaly=get_ecc_anomaly(mean_anomaly, eccentricity)

    r_and_true_anomaly=get_r_and_true_anomaly(semi_major_axis, ecc_anomaly, eccentricity)
    r=r_and_true_anomaly[0]
    true_anomaly=r_and_true_anomaly[1]

    r_ecliptic_coords=get_ecliptic_coords_of_r(r, true_anomaly, perihelion_longitude, ascending_longitude, inclination)
    
    earth_sun_vector_x= -2.143933664706825e-01 #float(input('X of Earth-Sun vector: '))
    earth_sun_vector_y= 9.937715392289074e-01 #float(input('Y of Earth-Sun vector: '))
    earth_sun_vector_z= -8.007904949494417e-05 #float(input('Z of Earth-Sun vector: '))
    earth_sun_vector=np.array([[earth_sun_vector_x, earth_sun_vector_y, earth_sun_vector_z]])

    earth_obj_vector=get_earth_obj_vector(earth_sun_vector, r_ecliptic_coords)

    rho_eq=conv_earth_obj_vector_to_equ_coords(earth_obj_vector)
    ra_dec=calc_ra_and_dec(rho_eq)

    ra_conv=conv_ra_to_hms(ra_dec[0])
    dec_conv=conv_dec_to_dms(ra_dec[1])

    return f'RA: {ra_conv} \nDEC: {dec_conv}'



#print(generate_ephemeris())



   