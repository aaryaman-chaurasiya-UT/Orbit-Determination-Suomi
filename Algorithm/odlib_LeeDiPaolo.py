'''
Aaryaman Chaurasiya & Gabriele Lee Di Paolo
Library File
'''




import numpy as np
from copy import deepcopy
def approx_equals(expected: float, actual: float, rel_tol: float = 1e-10, abs_tol: float = 1e-10)->bool:
    '''Tests whether the fractional difference between `expected` and `actual` is less than
    `rel_tol`. Fractional difference formula: |actual - expected| over expected.

    Notes:
    - (Hint: Consider using the function np.abs)
    - This is a very thorough test suite for such a short function! However, it's here to show you
    what sorts of tests are helpful in general.
    '''
    # YOUR CODE 
    if np.abs(expected-actual)<abs_tol:#checks whether the absolute value of the difference between the actual and the expected is within the relative tolerance
        return True
    elif expected==0:#checks whether expected is equal to 0. 
        return False
    elif np.abs((actual-expected)/expected)<rel_tol:#checks whether the fractional difference is less than the relevant tolerance
        return True
    else:
        return False
    
def convert_hms_to_deg(hours: float, minutes: float, seconds: float) -> float:
    '''Converts an angle in degrees, minutes, seconds to decimal degrees
    '''
    # perform angle conversion
    dec_degrees_hms=15*hours+ minutes/4+seconds/240
    
    # return result
    return dec_degrees_hms

def convert_dms_to_deg(degrees: int, minutes: int, seconds: float, is_neg: bool) -> float:
    '''Converts an angle in degrees, minutes, seconds to decimal degrees
    '''
    # perform angle conversion
    dec_degrees=degrees+minutes/60+seconds/3600
    
    # handle angle sign
    if is_neg==True:
        dec_degrees=dec_degrees*(-1)
    # return result
    return dec_degrees

def parse_ra_string(ra_string: str) -> tuple[int, int, float]:
    '''Parses an RA string into hours, minutes and seconds.
    
    Note that RA strings have the form "HH MM SS.SS"
    '''
    sexigesimal_tuple_hms=(
                           int(ra_string[:2]), 
                           int(ra_string[3:5]), 
                           float(ra_string[6:])
                           )
    
    #slices the string and then puts the respective parts into a tuple
    
    return sexigesimal_tuple_hms

def parse_dec_string(dec_string: str) -> tuple[int, int, float, bool]:
    '''Parses a dec string into degrees, minutes and seconds. Also returns a boolean flag that
    signals whether 
    
    Note that dec strings have the form "?DD MM SS.S" (where ? is either + or -)
    '''
    if dec_string[0]=='-':#assigns a boolean value depending on whether the dec is negative or not
        negative=True
    else:
        negative=False
    sexigesimal_tuple=(
                       int(dec_string[1:3]),
                       int(dec_string[4:6]),
                       float(dec_string[7:]),
                       negative
                       )
    #turns the string into a tuple and displays whether the dec is negative or not

    return sexigesimal_tuple

def convert_radec_str_to_deg(radec_str: str) -> tuple[float, float]:
    '''Takes an RA & Dec string in sexigesimal coordinates, parses it, and returns the RA & Dec
    values in decimal degrees.

    RA & Dec string: “HH MM SS.SS ?DD MM SS.SS”
    '''
    parsed_ra=parse_ra_string(radec_str[:11]) #parses the first part of the radec string containg the ra and turns it into a tuple
    parsed_dec=parse_dec_string(radec_str[12:])#does the same thing as the above line, except with the dec part of the str. 
    if radec_str[12]=="-": #This part handles whether the dec is negative or not. 
        negative=True
    else:
        negative=False
    radec_tuple=(convert_hms_to_deg(
                                    (parsed_ra[0]),
                                    (parsed_ra[1]),
                                    (parsed_ra[2])
                                    ),
                convert_dms_to_deg(
                                    (parsed_dec[0]),
                                    (parsed_dec[1]),
                                    (parsed_dec[2]),
                                    negative
                                    )
                )
    #this part converts the tuples containing the ra and dec into a single tuple conatining the coordinates (ra, dec)
    
    return radec_tuple

def sum_list(numbers: list[float]) -> float:
    ''' Takes in a list of numbers and returns their sum
    '''
    sum=0
    for element in numbers: #traverses the list and takes each element and adds it to a running sum
        sum+=element
    return sum

def get_min(numbers: list[float]) -> float:
    ''' Takes in a non-empty list of numbers (length > 0) and returns the minimum value
    '''
    min=numbers[0] #initializes the variable min to the first item in the list
    for element in numbers: #traverses the list to find values less than the current minimum
        if element<min:
            min=element
    return min

def remove_min(numbers: list[float]) -> list[float]:
    ''' Takes in a non-empty list of numbers (length > 0) and returns a new list with the smallest
    value removed. If there are multiple smallest values, only one is removed.
    '''
    ind=0
    for i in range(len(numbers)): #traverses the list and finds the index at which the minimum value in the list is located
        if numbers[i]<numbers[ind]:
            ind=i
    for element in numbers: #once the index is found, the code removes the value at the index; it removes the minimum value
        if element==numbers[ind]:
            numbers.remove(element)
    return numbers

def sort_list(numbers: list[float]) -> list[float]:
    ''' Takes in a list of numbers and returns a new list with the same values sorted from smallest
    to largest.
    '''
    sorted_numbers=[]
    for i in range(len(numbers)): #traverses the list and adds the minimum of the list each time to a new list. 
        sorted_numbers.append(get_min(numbers))
        remove_min(numbers) #Once the current minimum is added, it removes it from the list so that a new minimum can be added.
    return sorted_numbers

def get_vector_magnitude(vectors: list)->float:
    sum=0
    if vectors==[]: #if the vector is empty, its magnitude is 0
        return 0
    for element in vectors: #traverses the list and squares each component in the vector
        sum+=element**2
    return sum**(1/len(vectors)) #returns the sum of all the squares, to a fractional power that is based on how many components there are

def get_dot_product(vector1:list, vector2:list)->float:
    dot_prod=0
    if vector1==[] or vector2==[]: #if either vector is completely empty, the dot product is 0
        return dot_prod
    for i in range(len(vector1)): #traverses the list and multiplies each respective component of each vector together and adds them
        dot_prod+=vector1[i]*vector2[i]
    return dot_prod

def get_cross_product(vector1:list, vector2:list)->list:
     cross_prod=[(vector1[1]*vector2[2])-(vector1[2]*vector2[1]), (vector1[2]*vector2[0])-(vector1[0]*vector2[2]), (vector1[0]*vector2[1])-(vector1[1]*vector2[0])]
     #using the cross product formula for two vectors with 3 componenents, the code multiplies the componenets together
     return cross_prod

def conv_deg_to_rad(deg:float)->float:
    rad=(np.pi/180)*deg
    return rad

def conv_rad_to_deg(rad:float)->float:
    deg=(180*rad)/np.pi
    return deg

def array_approx_equals(arr_expected, arr_actual, rel_tol=1e-10, abs_tol=1e-10):
    if arr_actual.shape[:]==arr_expected.shape[:]: #compares the shapes of the arrays first to see if they are equal
        arr_expected=arr_expected.flatten() #flattens the arrays so that you can iterate over them
        arr_actual=arr_actual.flatten()
        length=arr_actual.shape[0]
        if arr_actual.shape[0]==0 and arr_expected.shape[0]==0: #if both arrays are empty, then they are equal to each other
            return True
        for i in range(length): #looks through every value in the arrays and compares them
            if approx_equals(arr_expected[i], arr_actual[i], rel_tol, abs_tol)==False: return False
            else: return True
    else: return False

def conv_spherical_to_rectangular_coords(spher_coords):
    arr_shape=spher_coords.shape #finding the shape of the array so that the fucntion know how many times to loop
    rect_coords=np.ones([arr_shape[0],arr_shape[1]])
    for i in range(arr_shape[0]): #loops and converts the coordinates by using the equations
        rect_coords[i,0]=spher_coords[i,0]*np.sin(conv_deg_to_rad(spher_coords[i,2]))*np.cos(conv_deg_to_rad(spher_coords[i,1]))
        rect_coords[i,1]=spher_coords[i,0]*np.sin(conv_deg_to_rad(spher_coords[i,1]))*np.sin(conv_deg_to_rad(spher_coords[i,2]))
        rect_coords[i,2]=spher_coords[i,0]*np.cos(conv_deg_to_rad(spher_coords[i,2]))
    return rect_coords

def conv_rectangular_to_spherical_coords(rect_coords):
    arr_shape=rect_coords.shape
    spher_coords=np.ones([arr_shape[0],arr_shape[1]])
    for i in range(arr_shape[0]):
        spher_coords[i,0]=(rect_coords[i,0]**2+rect_coords[i,1]**2+rect_coords[i,2]**2)**(1/2)
        spher_coords[i,1]=conv_rad_to_deg(np.arctan2(rect_coords[i,1], rect_coords[i,0]))%360
        spher_coords[i,2]=conv_rad_to_deg(np.arccos(rect_coords[i,2]/spher_coords[i,0]))%360 #literally the exact same as the above function but with different conversion equations since you are converting back
    return spher_coords

def calc_lst_from_jd(jd:float,lat:float)->float: #calculates lst from jd
    j100=(jd-2451545)/36525
    theta0=100.46061837+36000.77053608*j100+3.87933e-4*j100**2-j100**3/3.871e7
    thetag=theta0+360.985647366*(jd-(int(jd-0.5))+0.5)
    lst=(thetag+lat)%360
    return lst

def conv_ra_to_hms(ra):
    ra_h=np.floor(ra/15) #converts the ra from decimal degrees to hms
    ra_m=np.floor((ra/15-ra_h)*60)
    ra_s=((ra/15-ra_h)*60-ra_m)*60
    ra_conv=f'{int(ra_h)}:{int(ra_m)}:{round(ra_s,2)}'
    return ra_conv

def conv_dec_to_dms(dec):
    if dec<0: #converts declination to dms
        sign='-'
    if dec>0:
        sign='+'
    dec=np.abs(dec)
    dec_d=int(dec)
    dec_m=int((dec-dec_d)*60)
    dec_s=((dec-dec_d)*60-dec_m)*60
    dec_conv=f'{sign}{dec_d}:{dec_m}:{round(dec_s,2)}'
    return dec_conv