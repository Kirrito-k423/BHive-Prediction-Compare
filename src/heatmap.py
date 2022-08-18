import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
import global_variable as glv
from tsjPython.tsjCommonFunc import *
from logPrint import *
import sys

def Zfromllvm(Z,dataDict,scale,fineness):
    for key, value in dataDict.dataDict.items():
        globals()[key]=value 

    for tmp_block_binary_reverse in unique_revBiblock:
        if BhiveCyclesRevBiBlock[tmp_block_binary_reverse]==-1:
            continue
        if accuracyLLVM[tmp_block_binary_reverse] >= 0 :
            tmpZ=frequencyRevBiBlock[tmp_block_binary_reverse]
            tmpYPosition=int(scale*(int(llvmmcaCyclesRevBiBlock[tmp_block_binary_reverse])*1.0/glv._get("BHiveCount")))
            tmpXPosition=int(scale*(int(BhiveCyclesRevBiBlock[tmp_block_binary_reverse])*1.0/glv._get("BHiveCount")))
            ic(tmpXPosition,tmpYPosition)
            if tmpXPosition > 0 and tmpXPosition < fineness and tmpYPosition > 0 and tmpYPosition < fineness:
                Z[tmpXPosition][tmpYPosition]+=tmpZ

    ic(Z.min(),Z.max())
    return Z

def ZfromBaseline(Z,dataDict,scale,fineness):
    for key, value in dataDict.dataDict.items():
        globals()[key]=value 

    for tmp_block_binary_reverse in unique_revBiblock:
        if BhiveCyclesRevBiBlock[tmp_block_binary_reverse]==-1:
            continue
        if accuracyLLVM[tmp_block_binary_reverse] >= 0 :
            tmpZ=frequencyRevBiBlock[tmp_block_binary_reverse]
            tmpYPosition=int(scale*(int(BaselineCyclesRevBiBlock[tmp_block_binary_reverse])*1.0/glv._get("BHiveCount")))
            tmpXPosition=int(scale*(int(BhiveCyclesRevBiBlock[tmp_block_binary_reverse])*1.0/glv._get("BHiveCount")))
            ic(tmpXPosition,tmpYPosition)
            if tmpXPosition > 0 and tmpXPosition < fineness and tmpYPosition > 0 and tmpYPosition < fineness:
                Z[tmpXPosition][tmpYPosition]+=tmpZ

    ic(Z.min(),Z.max())
    return Z

def drawPlt(X,Y,Z,taskName):
    fig, ax = plt.subplots()
    fig.set_size_inches(w=7.1413, h=5.75) #(8, 6.5)

    ax.set_title(taskName)
    ax.set_xlabel('Measured Throughput(Bhive)')
    ax.set_ylabel('Predicted Throughput(llvm-mca)')

    # Color: https://juejin.cn/post/6844904145032331272
    dotDensity=75
    dashLine = np.mgrid[0:10:complex(0, dotDensity)]
    ax.plot( dashLine, dashLine,        linewidth=0.25,linestyle=":",color='silver') 
    ax.plot( dashLine, 0.9*dashLine,    linewidth=0.25,linestyle=":",color='springgreen') 
    ax.plot( dashLine, 0.8*dashLine,    linewidth=0.25,linestyle=":",color='royalblue') 
    dashLine = np.mgrid[0:10/1.1:complex(0, dotDensity)]
    ax.plot( dashLine, 1.1*dashLine,    linewidth=0.25,linestyle=":",color='springgreen') 
    dashLine = np.mgrid[0:10/1.2:complex(0, dotDensity)]
    ax.plot( dashLine, 1.2*dashLine,    linewidth=0.25,linestyle=":",color='royalblue') 
    pcm = ax.pcolor(X, Y, Z-1.0,
                    norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
                    cmap='Blues')
    fig.colorbar(pcm, ax=ax)
    # fig.suptitle('Heatmaps for BHiveU for basic blocks with a measured throughput \n\
    #                 of less than 10 cycles/iteration on Kunpeng', fontsize=16)
    ax.set_aspect('equal') 
    plt.axis("equal")
    plt.xlim([X.min(), X.max()])
    plt.ylim([Y.min(), Y.max()])
    #设置坐标轴刻度
    my_x_ticks = np.arange(0, 10.1, 1)
    my_y_ticks = np.arange(0, 10.1, 1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    return plt

def generateHeatmapPic(taskName,dataDict):
    beginTime=timeBeginPrint(sys._getframe().f_code.co_name)
    fineness = 100 # xy轴的粒度
    XYMax=10
    scale = fineness/XYMax
    X, Y = np.around(np.mgrid[0:XYMax:complex(0, fineness), 0:XYMax:complex(0, fineness)], decimals=1)


    Z=X*0+1.0
    Z=Zfromllvm(Z,dataDict,scale,fineness)
    saveHeatmapDataForPaper(X,Y,Z,glv._get("excelOutPath")+"_data/"+taskName+'.HeatmapData')
    drawPlt(X,Y,Z,taskName)
    plt.savefig("./pictures/"+taskName+'.png')
    
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
    })
    plt.savefig("./pictures/"+taskName+'.pgf')

    Z=X*0+1.0
    Z=ZfromBaseline(Z,dataDict,scale,fineness)
    drawPlt(X,Y,Z,taskName+"_baseline")
    saveHeatmapDataForPaper(X,Y,Z,glv._get("excelOutPath")+"_data/"+taskName+'.baselineHeatmapData')
    plt.savefig("./pictures/"+taskName+'_baseline.png')

    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
    })
    plt.savefig("./pictures/"+taskName+'_baseline.pgf')

    plt.close('all')
    timeEndPrint(sys._getframe().f_code.co_name,beginTime)

def saveHeatmapDataForPaper(X,Y,Z,filename):
    fw = open(filename, 'w',encoding='utf-8')    #将要输出保存的文件地址
    saveDict={
    "x":X.tolist(),
    "y":Y.tolist(),
    "z":Z.tolist()
    }
    import json
    json.dump(obj=saveDict, fp=fw)
    fw.close()
