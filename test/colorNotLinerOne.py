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

fig, ax = plt.subplots()
ax.set_aspect('equal') 
plt.axis("equal")
plt.xlim([X.min(), X.max()])
plt.ylim([Y.min(), Y.max()])
#设置坐标轴刻度
my_x_ticks = np.arange(0, 10.1, 1)
ic(my_x_ticks)
my_y_ticks = np.arange(0, 10.1, 1)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)

ax.set_title('FFTW')
ax.set_xlabel('Measured Throughput(Bhive)')
ax.set_ylabel('Predicted Throughput(llvm-mca)')

# Color: https://juejin.cn/post/6844904145032331272
dotDensity=75
dashLine = np.mgrid[0:10:complex(0, dotDensity)]
ax.plot( dashLine, dashLine, linewidth=0.25,linestyle=":",color='silver') 
ax.plot( dashLine, 0.9*dashLine, linewidth=0.25,linestyle=":",color='springgreen') 
ax.plot( dashLine, 0.8*dashLine, linewidth=0.25,linestyle=":",color='royalblue') 
dashLine = np.mgrid[0:10/1.1:complex(0, dotDensity)]
ax.plot( dashLine, 1.1*dashLine, linewidth=0.25,linestyle=":",color='springgreen') 
dashLine = np.mgrid[0:10/1.2:complex(0, dotDensity)]
ax.plot( dashLine, 1.2*dashLine, linewidth=0.25,linestyle=":",color='royalblue') 
pcm = ax.pcolor(X, Y, Z,
                   norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
                   cmap='Reds')
fig.colorbar(pcm, ax=ax)
# fig.suptitle('This is a somewhat long figure title', fontsize=16)
plt.savefig('plot_test.png')