#Python_plotter
import matplotlib.pyplot as plt

def plot(x, y, fname):
    plt.plot(x, y)
    plt.xlabel("Polarizacion")
    plt.ylabel("Capacitancia")
    plt.savefig(fname + '.png', bbox_inches='tight')
