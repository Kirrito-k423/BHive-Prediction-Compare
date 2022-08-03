# Bhive VS llvm-mca (vs OSACA) on ARMv7


[![OSCS Status](https://www.oscs1024.com/platform/badge/Kirrito-k423/BHive-Prediction-Compare.svg?size=small)](https://www.oscs1024.com/project/Kirrito-k423/BHive-Prediction-Compare?ref=badge_small)

Reimplementation of the BHive profiler on ARMv7 kunpeng processor. The original can be found here: https://github.com/ithemal/bhive.

## 仓库功能

![](https://shaojiemike.oss-cn-hangzhou.aliyuncs.com/img/20220712154020.png)

该仓库属于流程图的淡紫色模块的实现。

## 安装
### 安装Bhive
代码位于 `./bhive-reg`下，`make`产生`bhive`可执行文件。

安装完，测试如下：
```
qcjiang@brainiac1:~/tests$ bhive \xc1\x02\x40\xb9\xe0\x03\x01\x2a\x00\x00\x18\xca\x00\xfc\x41\xd3\xd6\x12\x00\x91\xc1\x02\x40\xb9\xe0\x03\x01\x2a

[CHILD] Test block and tail copied.
[CHILD] Aux. page mapped at 0x700000000000.
[PARENT] Child stack at 0xfffff407ff90 saved.
Signo: 19
Addr: 0x3ed0011e114
Event num: 229
```
### 安装llvm-mca
优化后代码在https://github.com/qcjiang/llvm-project，有个tsv110的branch，直接在github上fork这个仓库，执行如下代码安装。(基准代码下载官方llvm13.0.0版本，安装方法相同)
```
mkdir build && cd build
cmake -DLLVM_TARGETS_TO_BUILD="AArch64" -DCMAKE_BUILD_TYPE=Debug ../llvm
make llvm-mca -j VERBOSE=1
```
安装完，测试如下：
```
> echo "neg     x1, x20
cmp     x0, x19
" | ~/github/MyGithub/llvm-project/build/bin/llvm-mca --timeline -iterations=500 |head -10
Iterations:        500
Instructions:      1000
Total Cycles:      337
Total uOps:        1000

Dispatch Width:    4
uOps Per Cycle:    2.97
IPC:               2.97
Block RThroughput: 0.5
```

### 安装OSACA
下载：https://github.com/qcjiang/OSACA，开发相关的branch在feature/tsv110，直接在github上fork这个仓库，执行如下代码安装。
```
python setup.py build
python setup.py install
```
安装完，测试如下：
```
> cat test.s
add     x1, x0, #0x8b0
sub     w28, w21, #0x41
ldur    w0, [x11, #-4]

> osaca --arch TSV110 ./test.s
Open Source Architecture Code Analyzer (OSACA) - 0.4.8
Analyzed file:      ./test.s
Architecture:       TSV110
Timestamp:          2022-08-03 08:20:03


 P - Throughput of LOAD operation can be hidden behind a past or future STORE instruction
 * - Instruction micro-ops not bound to a port
 X - No throughput/latency information for this instruction in data file


Combined Analysis Report
------------------------
                          Port pressure in cycles
     |  0   |  1   |  2   |  3   |  4   |  5   |  6   |  7   ||  CP  | LCD  |
-----------------------------------------------------------------------------
   1 | 0.33 | 0.33 | 0.33 |      |      |      |      |      ||      |      |   add x1, x0, #0x8b0
   2 | 0.33 | 0.33 | 0.33 |      |      |      |      |      ||      |      |   sub     w28, w21, #0x41
   3 |      |      |      |      |      |      | 0.50 | 0.50 ||  4.0 |      |   ldur w0, [x11, #-4]

       0.67   0.67   0.67                        0.50   0.50     4.0    0.0
```
### 安装python库
```
pip install -r requirements.txt
```

## 运行
### 运行前必须修改config选项
执行文件路径等信息在`./src/config.py`下。(必须修改Bhive，llvm-mca,OSACA可执行文件路径为上面的安装路径)。


| 参数		|说明	|
|---		|---	|
|HistoryDataFile	    |复用已生成数据的excel路径(下一节交代具体使用方法)
|taskfilePath		      |输入文件集合所在的目录
|taskList			        |输入文件名 及其 对应的excel任务名
|OSACAPath			      |OSACA可执行文件路径
|LLVM_mcaPath		      |优化后llvm-mca可执行文件路径
|LLVM_mcaBaselinePath|基准llvm-mca可执行文件路径
|BHivePath            |Bhive可执行文件路径
|BHiveCount           |Bhive指令展开次数
|ProcessNum           |并行核数
|failedRetryTimes     |调用Bhive,llvm_mca,OSACA返回错误值时，重试次数
|failedSleepTime      |重试的间隔时间(单位为秒，主要防止Bhive由于资源占用返回错误值)
|timeout              |调用Bhive,llvm_mca,OSACA超时kill的时限(单位为秒)
|excelOutPath         |输出excel路径(默认在输入目录下)
|debug                |是否打印debug信息(除非是单进程，小样例，否则不建议开启)


### 查看选项
python命令的选项优先级高于`config.py`
```
> python3 ./src/main.py -h
In addition to entering some parameters, you can also modify all parameters in config.py
usage: main.py [-h] [-b BHIVECOUNT] [-p PROCESSNUM] [-t TIMEOUT] [-d {yes,no}] -hB {yes,no} -hl {yes,no} -k {yes,no} -hb {yes,no} -hO {yes,no} [-pu {yes,no}]

please enter some parameters

optional arguments:
  -h, --help            show this help message and exit
  -b BHIVECOUNT, --BHiveCount BHIVECOUNT
                        Bhive执行时代码展开次数
  -p PROCESSNUM, --ProcessNum PROCESSNUM
                        并行核数
  -t TIMEOUT, --timeout TIMEOUT
                        子进程超时的时限(单位秒)
  -d {yes,no}, --debug {yes,no}
                        是否打印Debug信息
  -hB {yes,no}, --historyBhive {yes,no}
                        是否使用HistoryDataFile的excel里的Bhive历史数据
  -hl {yes,no}, --historyLLVM {yes,no}
                        是否使用HistoryDataFile的excel里的llvm-mca历史数据
  -k {yes,no}, --KendallIndex {yes,no}
                        是否计算KendallIndex
  -hb {yes,no}, --historyBaseline {yes,no}
                        是否使用HistoryDataFile的excel里的llvm-mca基准历史数据 
  -hO {yes,no}, --historyOSACA {yes,no}
                        是否使用HistoryDataFile的excel里的OSACA历史数据 
  -pu {yes,no}, --printUnsupportedBlock {yes,no}
                        excel文件是否保留llvm-mca，Bhive或者OSACA不支持的基本块
```
### 推荐运行
第一次运行，需要计算Bhive,llvm-mca,OSACA的所有数据
```
python3 ./src/main.py -p 30 -hB no -hb no -hO no -hl no -k no -d no
```
假如修改了llvm-mca,想重新计算该部分，重用其余部分的数据
```
python3 ./src/main.py -p 30 -hB yes -hb yes -hO yes -hl no -k no -d no
```
## features

1. base on armV7
2. compare OSACA, LLVM-mca, Bhive
3. multiProcess progress bar
4. result in excel file with graph
5. icecream for debug

## 其余补充说明

### 已有的输入文件
在`log`文件夹下提供了config默认任务列表需要的精简汇编数据。文件后缀的简单解释如下

| 后缀		|说明	|
|---		|---	|
|runLog	      |是补测数据时采取实时处理DynamoRIO输出的汇编的方法测量的
|N4582		      |代表有4582个基本块
|skipNum_0      |基本块指令数大于1
|其余后缀       |和应用的运行参数有关，不深入解释了

### 关于运行时间估计(20核并行)

1. 将我们提供的输入文件全部从头运行一遍大约 20~30h. 其中Bhive占据了主要时间(由于Bhive是实际运行，并行的资源占用，对其准确率有影响，为此调整了并行的密度)
2. 只重新计算llvm-mca，重用其余数据，运行一遍时长2~3h。

### 关于数据重用的实现中间文件

虽然excel存储了所需的数据，但是依次读取速度太慢了。实际数据以JSON格式存储在输出excel文件名添加`_data`后缀的文件夹下。

### 关于OSACA中间文件

在输入目录下会生成`tmpOSACAfiles`文件夹存储OSACA所需的临时汇编文件

