
import numpy
import cmath
import matplotlib.pyplot as plt
def Obtain_R(Z11):  #Para un voltaje especifico, varias frecuencias
    Z11.sort(key=lambda x: x.real)
    print Z11
    Zreal=numpy.real(Z11)
    print Zreal
    Zimag=numpy.imag(Z11)
    print Zimag
    Mitad1=Zimag[0:len(Zimag)/2]
    print Mitad1
    Mitad2=Zimag[len(Zimag)/2:len(Zimag)]
    print Mitad2
    Zeros=[]
    for i in range(len(Mitad1)):
        if numpy.abs(Mitad1[i])==numpy.min(numpy.abs(Mitad1)):
            Zeros.append(Zreal[i])
            break
    for i in range(len(Mitad2)):
        if numpy.abs(Mitad2[i])==numpy.min(numpy.abs(Mitad2)):
            Zeros.append(Zreal[i+len(Zimag)/2])
            break
    print Zeros
    Zeros=numpy.sort(Zeros)
    print Zeros
    Rseries=Zeros[0]
    RDT=Zeros[1]-Rseries
    return [Rseries, RDT]
def Obtain_Cgate(Z11,F, RDT, Rseries): #Para un voltaje y una fecuencia especificos
    Real=numpy.real(Z11)
    w=2*cmath.pi*F
    Cgate=cmath.sqrt((((Rseries+RDT)/Real)-1)/((w^2)*(RDT^2)*(1-(Rseries/Real))))
    return Cgate
def Frecuency_Graphics(Z11,F): #Para un voltaje especifico, varias frecuencias
    Zreal=numpy.real(Z11)
    Zimag=numpy.real(Z11)
    plt.plot(Zreal,Zimag)
    plt.figure()
    plt.plot(F,Zreal)
    plt.plot(F,Zimag)
    plt.show
def Voltage_Graphics(Z11,Voltajes,Frecuencias):
    Resistencias=[]
    for i in range(len(Frecuencias)):
        Resistencias.append(Obtain_R([item[i] for item in Z11]))
    Cgates=[]
    for i in range(len(Frecuencias)): #Para cada frecuencia tengo un arreglo Cgate
        F=Frecuencias[i]
        Zin=Z11[i]
        Cgate=[]
        for j in range(len(Zin)):
            Rseries=Resistencias[j][0]
            RDT=Resistencias[j][1]
            C=Obtain_Cgate(Zin,F, RDT, Rseries)
            Cgate.append(C)
        Cgates.append(Cgate)
    for k in Cgates:
        plt.plot(Voltajes,k)
    plt.figure()
    RDT=[R[1] for R in Resistencias]
    plt.plot(Voltajes,RDT)
    plt.show()
'''
Z11=[1+4j,15+5j,7+3j,4+5j,13+-4j,2+5j,7+-1j]
[Rseries, RDT]=Obtain_R(Z11)
print [Rseries, RDT]
'''