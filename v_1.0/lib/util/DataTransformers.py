#Matrix_transformations_and_capacitance_obtaining
#Description: Calculation of the 'X,Y' matrixs since 'S' matrix
from __future__ import division
from numpy.linalg import inv
import math
def single_z_from_s(data):
# function single_z_from_s(data) from module DataTransformers.py
# Arguments: data
##Returns a 4 elements list with the z-matrix parameters got from the s-parameters listed in "data" 
#with a characteristic impedance value of 50 ohms

    s11 = data[0]
    s12 = data[1]
    s21 = data[2]
    s22 = data[3]

    delta_s = (1-s11)*(1-s22) - s12*s21
    #print delta_s
    z0 = 50 # characteristing impendance of 50 ohms

    #Elements of the 'Z' matrix
    z11 = (((1+s11)*(1-s22)+s12*s21)/delta_s)*z0
    z12 = (2*s12*z0)/delta_s
    z21 = (2*s21*z0)/delta_s
    z22 = (((1-s11)*(1+s22)+s12*s21)/delta_s)*z0

    return [z11, z12, z21, z22]

def single_y_from_s(data):
# function single_y_from_s(data) from module DataTransformers.py
# Arguments: data
# #Returns a 4 elements list with the y-matrix parameters got from the s-parameters listed in "data" with a 
# characteristic impedance value of 50 ohms

    # Put data in matrix form for inversion
    s = [data[0], data[1], data[2], data[3]]
    z = single_z_from_s(s)
    matrix_z = [[z[0], z[1]],[z[2], z[3]]]
    matrix_y = inv(matrix_z).tolist()
    # Other parts of the program expect a flat list, not a matrix
    y = [item for sublist in matrix_y for item in sublist] # list flattening magic
    return y

def y_from_s(sdata):
# function y_from_s(sdata) from module DataTransformers.py
# Arguments: sdata
# #Returns a list with the form "ydata = [y11_list, y12_list, y21_list, y22_list]" with the y-matrix parameters got from the sdata matrix(list of lists)

    y11_list = []
    y12_list = []
    y21_list = []
    y22_list = []


    for idx, d in enumerate(sdata[0]):
        s11 = sdata[0][idx]
        s12 = sdata[1][idx]
        s21 = sdata[2][idx]
        s22 = sdata[3][idx]

        Y = single_y_from_s([s11, s12, s21, s22])
        y11_list.append(Y[0])
        y12_list.append(Y[1])
        y21_list.append(Y[2])
        y22_list.append(Y[3])

    ydata = [y11_list, y12_list, y21_list, y22_list]
    return ydata

def z_from_s(sdata):
# function z_from_s(sdata) from module DataTransformers.py
# Arguments: sdata
# #Returns a list with the form "zdata = [z11_list, z12_list, z21_list, z22_list]" with the y-matrix parameters got from the sdata matrix(list of lists)

    z11_list = []
    z12_list = []
    z21_list = []
    z22_list = []


    for idx, d in enumerate(sdata[0]):
        s11 = sdata[0][idx]
        s12 = sdata[1][idx]
        s21 = sdata[2][idx]
        s22 = sdata[3][idx]

        Z = single_z_from_s([s11, s12, s21, s22])
        z11_list.append(Z[0])
        z12_list.append(Z[1])
        z21_list.append(Z[2])
        z22_list.append(Z[3])

    zdata = [z11_list, z12_list, z21_list, z22_list]
    return zdata

def cga_from_s(freq_data, sdata):
# function cga_from_s(freq_data, sdata) from module DataTransformers.py
# Arguments: freq_data, sdata
# #Returns the list of Cga (gate-all) values got from the sdata matrix for a frecuencya freq

    ydata = y_from_s(sdata)
    cga = []
    for freq, ydatum in zip(freq_data, ydata[0]):
        cga.append(ydatum.imag/(freq*2*math.pi))
    return cga

def cgs_from_s(freq_data, sdata):
# function cgs_from_s(freq_data, sdata) from module DataTransformers.py
# Arguments: freq_data, sdata
# #Returns the list of Cgs (gate-source) values got from the sdata matrix for a frecuencya freq

    ydata = y_from_s(sdata)
    cgs = []
    for freq, ydatum in zip(freq_data, ydata[2]):
        cgs.append(-ydatum.imag/(freq*2*math.pi))

    return cgs

def cga_from_y(freq_data, ydata):
# function cga_from_s(freq_data, sdata) from module DataTransformers.py
# Arguments: freq_data, sdata
# #Returns the list of Cga (gate-all) values got from the sdata matrix for a frecuencya freq

    
    cga = []
    for freq, ydatum in zip(freq_data, ydata[0]):
        cga.append(ydatum.imag/(freq*2*math.pi))
    return cga

def cgs_from_y(freq_data, ydata):
# function cgs_from_s(freq_data, sdata) from module DataTransformers.py
# Arguments: freq_data, sdata
# #Returns the list of Cgs (gate-source) values got from the sdata matrix for a frecuencya freq

    
    cgs = []
    for freq, ydatum in zip(freq_data, ydata[2]):
        cgs.append(-ydatum.imag/(freq*2*math.pi))

    return cgs