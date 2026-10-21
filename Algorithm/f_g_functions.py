import numpy as np
from odlib_LeeDiPaolo import *
from baby_od import get_semi_major_axis, get_eccentricity

def get_delta_E(tau,r2,r2dot): #calculates the change in E using the newton-raphson method
    a=get_semi_major_axis(r2,r2dot)
    e=get_eccentricity(r2, r2dot, a)
    n=1/np.sqrt(a**3)
    
    r_r_dot=np.dot(r2,r2dot)
    sign_exp= r_r_dot/(n*a**2)*np.cos(n*tau-r_r_dot/(n*a**2)) + (1-np.linalg.norm(r2)/a)*np.sin(n*tau-r_r_dot/(n*a**2))

    if e<=0.1: #setting up initial conditions
        x=n*tau
    elif sign_exp>=0:
        x=n*tau+0.85*e-r_r_dot/(n*a**2)
    else:
        x=n*tau-0.85*e-r_r_dot/(n*a**2)

    f_x=x-(1-np.linalg.norm(r2)/a)*np.sin(x)+r_r_dot/(n*a**2)*(1-np.cos(x))-n*tau #first iteration of newton raphson
    f_prime_x=1-(1-np.linalg.norm(r2)/a)*np.cos(x)+r_r_dot/(n*a**2)*np.sin(x) 
    x_place=float(0)

    while np.abs(x-x_place)>1e-12: #subsequent iterations of newton raphson
        x_place=x
        x=x-f_x/f_prime_x

        f_x=x-(1-np.linalg.norm(r2)/a)*np.sin(x)+r_r_dot/(n*a**2)*(1-np.cos(x))-n*tau

        f_prime_x=1-(1-np.linalg.norm(r2)/a)*np.cos(x)+r_r_dot/(n*a**2)*np.sin(x)

    return x #delta E in radians

def f_function(tau,r2,r2dot,flag): #calculates f1 or f3 depending on the tau input. Has an option to run either the 3 term or 4 term series or the function depending on what the flag is set to
    #flag=int(input('3rd term f series; (0), 4th term; (1), f function; (2): '))
    u,z=1/np.linalg.norm(r2)**3, np.dot(r2, r2dot)/np.linalg.norm(r2)**2, 
    q=np.dot(r2dot, r2dot)/np.linalg.norm(r2)**2-u
    
    a=get_semi_major_axis(r2,r2dot)
    delta_E=get_delta_E(tau, r2, r2dot)

    if flag==0:
        f=1-1/2*u*tau**2+1/2*u*z*tau**3
    if flag==1:
        f=1-1/2*u*tau**2+1/2*u*z*tau**3+1/24*(3*u*q-15*u*z**2+u**2)*tau**4
    if flag==2:
        f=1-a/np.linalg.norm(r2)*(1-np.cos(delta_E))

    # f_3=float(1-1/2*u*tau**2+1/2*u*z*tau**3)
    # f_4=float(1-1/2*u*tau**2+1/2*u*z*tau**3+1/24*(3*u*q-15*u*z**2+u**2)*tau**4)
    # f_function=float(1-a/np.linalg.norm(r2)*(1-np.cos(delta_E)))

    return f
    # return f_3, f_4, f_function

def g_function(tau,r2,r2dot,flag): # same as the above f function but for g1 and g3. Still has the same options between series and function
    #flag=int(input('3rd term g series; (0), 4th term; (1), g series; (2): '))
    u,z=1/np.linalg.norm(r2)**3, np.dot(r2, r2dot)/np.linalg.norm(r2)**2

    a=get_semi_major_axis(r2,r2dot)
    n=1/np.sqrt(a**3)
    delta_E=get_delta_E(tau, r2, r2dot)

    if flag==0:
        g=tau-1/6*u*tau**3
    if flag==1:
        g=(tau-1/6*u*tau**3+1/4*u*z*tau**4)
    if flag==2: 
        g=tau+1/n*(np.sin(delta_E)-delta_E)
    
    # g_3=float(tau-1/6*u*tau**3)
    # g_4=float(tau-1/6*u*tau**3+1/4*u*z*tau**4)
    # g_function=float(tau+1/n*(np.sin(delta_E)-delta_E))

    return g
    # return g_3, g_4, g_function
    
#print(g_function(-0.17202648521795452, np.array([ 0.21321156187475016, -1.126743453662787, -0.4332117437394853 ]), np.array([ 0.9292542014317857, 0.5610640031517184, 0.0390010162885388 ]), 2 ) )