import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import global_variable as glv

def generateHeatmapPic(taskName,dataDict):
    fineness = 100 # xy轴的粒度
    XYMax=10
    scale = fineness/XYMax
    X, Y = np.mgrid[0:XYMax:complex(0, fineness), 0:XYMax:complex(0, fineness)]
    Z=X*0+1.0

    for key, value in dataDict.dataDict.items():
        globals()[key]=value 

    for tmp_block_binary_reverse in unique_revBiblock:
        if BhiveCyclesRevBiBlock[tmp_block_binary_reverse]==-1:
            continue
        if accuracyLLVM[tmp_block_binary_reverse] != 0:
            tmpZ=frequencyRevBiBlock[tmp_block_binary_reverse]
            tmpYPosition=int(scale*(int(llvmmcaCyclesRevBiBlock[tmp_block_binary_reverse])*1.0/glv._get("BHiveCount")))
            tmpXPosition=int(scale*(int(BhiveCyclesRevBiBlock[tmp_block_binary_reverse])*1.0/glv._get("BHiveCount")))
            ic(tmpXPosition,tmpYPosition)
            if tmpXPosition > 0 and tmpXPosition < fineness and tmpYPosition > 0 and tmpYPosition < fineness:
                Z[tmpXPosition][tmpYPosition]+=tmpZ

    ic(Z.min(),Z.max())
    fig, ax = plt.subplots(figsize=(8, 7))

    ax.set_title(taskName)
    ax.set_xlabel('Measured Throughput(Bhive)')
    ax.set_ylabel('Predicted Throughput(llvm-mca)')
    pcm = ax.pcolor(X, Y, Z-1.0,
                    norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
                    cmap='Reds')
    fig.colorbar(pcm, ax=ax)
    fig.suptitle('Heatmaps for BHiveU for basic blocks with a measured throughput of less than 10 cycles/iteration on Kunpeng', fontsize=16)
    plt.savefig("./pictures/"+taskName+'.png')


