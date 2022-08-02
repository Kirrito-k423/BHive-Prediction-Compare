import global_variable as glv
from collections import defaultdict
import time

glv._init()

glv._set("useBhiveHistoryData", "no") # 是否重用 历史文件里的Bhive数据
glv._set("useLLVMHistoryData", "no") # 是否重用 历史文件里的llvm-mca Baseline数据
glv._set("useBaselineHistoryData", "no") # 是否重用 历史文件里的llvm-mca Baseline数据
glv._set("HistoryDataFile", "/home/shaojiemike/blockFrequency/Summary_BHiveCount5002022-07-23-20-04-14_tsj.xlsx") # for test
# glv._set("HistoryDataFile", "/home/shaojiemike/blockFrequency/Summary_BHiveCount5002022-07-14-13-05-29_tsj.xlsx") # Full

glv._set("taskfilePath", "/home/shaojiemike/blockFrequency") # 输入文件集合所在的目录
# glv._set("taskList",{"tensorflow_test_5.log":"test"})
# glv._set("taskList",{"tensorflow_test_5.log":"test"})
# glv._set("taskList",{"tensorflow_test_100.log":"test"})
# glv._set("taskList",{"test_insns_blockFrequency_skip_2.log":"test_insns"})
# glv._set("taskList",{"Gzip_all_skip_2.log":"Gzip"})
# glv._set("taskList",{"tensorflow_41Gdir_00all_skip_2.log":"Tensorflow"})
# glv._set("taskList",{
#             "tensorflow_test_100.log":"tensorflow_1",
#             "tensorflow_test_5.log":"tensorflow_2",
#             "tensorflow_test_3.log":"tensorfw_3"})
glv._set("taskList", 
                {        
                "ffmpeg_useFileNum_1_skipNum_0.log":"ffmpeg",
                "FFTW_useFileNum_1_skipNum_0.log":"FFTW",
                "fftw_runLog.log":"FFTW_runLog",
                # "lapack_useFileNum_1_skipNum_0":"lapack(dgetrf)", #DGETRF computes an LU factorization of a general M-by-N matrix A
                "lapack_runLog.log":"lapack_runLog(dgetrf)",
                "openblas_utest_useFileNum_4_skipNum_0.log":"OpenBLAS",
                "OpenBLAS_level1_ddot_N8398.log":"OpenBLAS_level1_ddot",
                "OpenBLAS_level2_dgemv_N7561.log":"OpenBLAS_level2_dgemv",
                "OpenBLAS_level3_dgemm_N9523.log":"OpenBLAS_level3_dgemm",
                "OpenBLAS_level3_zgemm_N7470.log":"OpenBLAS_level3_zgemm",
                "EmbreeHello_useFileNum_1_skipNum_0.log":"Embree",
                "EmbreeHello_runLog.log":"Embree_runLog",
                "tensorflow_41Gdir_00all_skip_2.log":"Tensorflow",
                "tensorflow_20W_runLog.log":"Tensorflow_runLog_skip0",
                # "clang_harness_00all_skip_2.log":"Clang",
                "clang_make_runLog.log":"Clang_runLog",
                "MM_median_all_skip_2.log":"Eigen_MM_Middle",
                "Eigen_MM_Big_N4582.log":"Eigen_MM_Big",
                "Eigen_MV_N4255.log":"Eigen_MV",
                "Gzip_all_skip_2.log":"Gzip",
                "Gzip_clang_85G_N5443.log":"Gzip_85G_runLog",
                "redis_r1000000_n2000000_P16_all_skip_2.log":"Redis",
                "redis_r100000_n200000_N8452.log":"Redis_skip0",
                "test_insns_blockFrequency_skip_2.log":"test_insns"}) # 输入文件名的前缀，和在excel里的名称

glv._set("OSACAPath","/home/qcjiang/softwares/anaconda3/bin/osaca") # OSACA 的测量对比暂时不再支持
glv._set("LLVM_mcaPath","/home/shaojiemike/github/MyGithub/llvm-project/build/bin/llvm-mca")
glv._set("LLVM_mcaBaselinePath","/home/shaojiemike/Download/llvm-project-llvmorg-13.0.0/build/bin/llvm-mca")
glv._set("BHivePath","/home/shaojiemike/test/bhive-re/bhive-reg/bhive")
glv._set("BHiveCount",500)
glv._set("ProcessNum",16)
glv._set("failedRetryTimes",3)
glv._set("failedSleepTime",1)
glv._set("timeout",10)
glv._set("excelOutPath",glv.GLOBALS_DICT["taskfilePath"]+'/Summary_BHiveCount'+str(glv.GLOBALS_DICT["BHiveCount"])+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+'_tsj.xlsx')
glv._set("debug","yes")

def pasteFullFileName(taskfilenameWithoutPath):
    taskfilePath=glv._get("taskfilePath")
    taskfilename="{}/{}".format(taskfilePath,taskfilenameWithoutPath)
    return taskfilename


