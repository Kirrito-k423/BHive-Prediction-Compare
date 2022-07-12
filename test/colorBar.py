import matplotlib.pyplot as plt
import numpy as np
from icecream import ic

# Fixing random state for reproducibility
np.random.seed(19680801)

fig, axs = plt.subplots(2, 2)
cmaps = ['hot_r','RdBu_r', 'viridis'] # 代表两种颜色
ic(np.random.random((5, 5)))
for col in range(2):
    for row in range(2):
        ic(col,row)
        ax = axs[row, col]
        pcm = ax.pcolormesh([[0.5,0.25],[0,20]],
                            cmap=cmaps[col])
        fig.colorbar(pcm, ax=ax)


plt.show()
plt.savefig('plot_test.png')