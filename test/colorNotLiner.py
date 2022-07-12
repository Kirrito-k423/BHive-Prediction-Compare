import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from icecream import ic
N = 100
X, Y = np.mgrid[-3:3:complex(0, N), -2:2:complex(0, N)]

ic(X)
ic(Y)

# A low hump with a spike coming out of the top.  Needs to have
# z/colour axis on a log scale so we see both hump and spike.  linear
# scale only shows the spike.

Z1 = np.exp(-(X)**2 - (Y)**2)
Z2 = np.exp(-(X * 10)**2 - (Y * 10)**2)
Z = Z1 + 50 * Z2

ic(Z)

num=6
fig, ax = plt.subplots(num, 1,figsize=(8, 8*num))

ax[0].set_title('FFTW')
ax[0].set_xlabel('Measured Throughput(Bhive)')
ax[0].set_ylabel('Predicted Throughput(llvm-mca)')
pcm = ax[0].pcolor(X, Y, Z,
                   norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
                   cmap='hot_r')
fig.colorbar(pcm, ax=ax[0])

pcm = ax[1].pcolor(X, Y, Z, cmap='hot_r')
fig.colorbar(pcm, ax=ax[1], extend='max')

pcm = ax[2].pcolormesh(X, Y, Z, norm=colors.PowerNorm(gamma=1. / 1.),
                       cmap='hot_r')
fig.colorbar(pcm, ax=ax[2], extend='max')

pcm = ax[3].pcolormesh(X, Y, Z, norm=colors.PowerNorm(gamma=1. / 2.),
                       cmap='hot_r')
fig.colorbar(pcm, ax=ax[3], extend='max')

pcm = ax[4].pcolormesh(X, Y, Z, norm=colors.PowerNorm(gamma=1. / 10.),
                       cmap='hot_r')
fig.colorbar(pcm, ax=ax[4], extend='max')

pcm = ax[5].pcolormesh(X, Y, Z, norm=colors.PowerNorm(gamma=1. / 30.),
                       cmap='hot_r')
fig.colorbar(pcm, ax=ax[5], extend='max')
fig.suptitle('This is a somewhat long figure title', fontsize=16)
plt.savefig('plot_test.png')