from icecream import ic
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
# import fontmanager

dataPath="/home/shaojiemike/blockFrequency/Summary_BHiveCount5002022-08-18-11-19-58_tsj.xlsx_data/"

picName2fileDict={  
                    # "Tensorflow":"Tensorflow_runLog_skip0",
                    # "Clang":"Clang_runLog",
                    # "Embree":"Embree",
                    # "ffmpeg":"ffmpeg",
                    # "Gzip":"Gzip",
                    # "OpenBLAS":"OpenBLAS_level3_dgemm",
                    # "FFTW":"FFTW_runLog",
                    # "lapack(dgetrf)":"lapack_runLog(dgetrf)",
                    # "Eigen_MM":"Eigen_MM_Middle",
                    # "Eigen_MV":"Eigen_MV",
                    "Redis":"Redis_skip0"
                    }

def drawPlt(X,Y,Z,taskName):
    fig, ax = plt.subplots()
    fig.set_size_inches(w=7.1413, h=5.75) #(8, 6.5)

    fontSize=16
    ax.set_title(taskName,fontsize=fontSize,fontfamily="Times New Roman")
    ax.set_xlabel('Measured Throughput(Bhive)',fontsize=fontSize,fontfamily="Times New Roman")
    ax.set_ylabel('Predicted Throughput(llvm-mca)',fontsize=fontSize,fontfamily="Times New Roman")

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

def readDataFromJson(filename):
    rf = open(filename,'r',encoding='utf-8')
    readDict=json.load(fp=rf)
    X = np.array(readDict['x'])
    Z = np.array(readDict['z'])
    Y = np.array(readDict['y'])
    return [X,Y,Z]
    
def main():
    ic(matplotlib.matplotlib_fname())
    # ic(fontmanager.get_cachedir())
    # ic(fontmanager._fmcache)
    for key,filename in picName2fileDict.items():
        ic(key,filename)
        [X,Y,Z]=readDataFromJson(dataPath+filename+".HeatmapData")
        drawPlt(X,Y,Z,key)
        plt.savefig("./test/heatMapPic/"+key+'.png',bbox_inches="tight")
    
if __name__ == "__main__":
    main()