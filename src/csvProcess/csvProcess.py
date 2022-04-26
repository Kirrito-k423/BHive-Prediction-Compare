import csv
from tsjPython.tsjCommonFunc import *
# clang_harness_00all_skip_2_count10000_0221newOSACA_OSACAVSLLVMVSBHive.csv
# Gzip_all_skip_2_count10000_0221newOSACA_OSACAVSLLVMVSBHive.csv
# MM_median_all_skip_2_count10000_0221newOSACA_OSACAVSLLVMVSBHive.csv
# MM_median_all_skip_2_count10000_0222newOSACAagain_OSACAVSLLVMVSBHive.csv
# redis_r1000000_n2000000_P16_all_skip_2_count10000_0221newOSACA_OSACAVSLLVMVSBHive.csv
# tensorflow_41Gdir_00all_skip_2_count10000_0221newOSACA_OSACAVSLLVMVSBHive.csv
# tensorflow_test_100_count10000_0221newOSACA_OSACAVSLLVMVSBHive.csv
path="/home/shaojiemike/blockFrequency/"
filename="tensorflow_test_100_count10000_0222newOSACAagain_OSACAVSLLVMVSBHive.csv"
cycleNum=10000

csv_reader = csv.reader(open(path+filename))
OSACAErrorSum=0
OSACANumSum=0
screeningResults=[]
for line in csv_reader:
    # print(line[-1][0])
    if line[-1][0]=='w' or line[0][0]=='v' or line[0][0]=='a' or float(line[0])==0:
        continue
    else:
        yellowPrint(line[0])
        count=float(line[2])
        OSACAMax=float(line[3])
        OSACACP=float(line[4])
        llvm=float(line[5])
        realBHive=float(line[6])
        tmp=(OSACAMax+OSACACP)/2 * cycleNum - realBHive
        OSACAErrorSum+=abs(tmp)/realBHive * count
        OSACANumSum+=count

OSACAError=OSACAErrorSum/OSACANumSum
passPrint(OSACAError)