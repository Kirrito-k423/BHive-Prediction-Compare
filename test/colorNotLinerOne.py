import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from icecream import ic
N = 100
X, Y = np.mgrid[0:10:complex(0, N), 0:10:complex(0, N)]

ic(X)
ic(Y)

# A low hump with a spike coming out of the top.  Needs to have
# z/colour axis on a log scale so we see both hump and spike.  linear
# scale only shows the spike.

Z1 = np.exp(-(X)**2 - (Y)**2)
Z2 = np.exp(-(X * 10)**2 - (Y * 10)**2)
Z = Z1 + 50 * Z2
Z=X*0+1.0
Z[10][50]=100
ic(Z.min())
ic(Z)

fig, ax = plt.subplots(figsize=(8, 7))

ax.set_title('FFTW')
ax.set_xlabel('Measured Throughput(Bhive)')
ax.set_ylabel('Predicted Throughput(llvm-mca)')
pcm = ax.pcolor(X, Y, Z,
                   norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
                   cmap='Reds')
fig.colorbar(pcm, ax=ax)
# fig.suptitle('This is a somewhat long figure title', fontsize=16)
plt.savefig('plot_test.png')