import matplotlib.pyplot as plt
import numpy as np
from math import *

def f(t):
    if t>=-20 and t<-10:
        return np.exp(-(t+10)**2/4**2)
    elif t>=-10 and t<=10:
        return 1
    else:
        return np.exp(-(t-10)**2/4**2)

X=np.arange(-20,20,0.1)
plt.plot(X,list(map(f,X)),label='Observed')
plt.show()