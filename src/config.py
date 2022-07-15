import global_variable as glv
from collections import defaultdict
import time

glv._init()

glv._set("useBhiveHistoryData", "no") # 是否重用 历史文件里的Bhive数据
glv._set("useBaselineHistoryData", "no") # 是否重用 历史文件里的llvm-mca Baseline数据
glv._set("HistoryDataFile", "/home/shaojiemike/blockFrequency/Summary_BHiveCount5002022-07-15-16-15-36_tsj.xlsx") # for test
# glv._set("HistoryDataFile", "/home/shaojiemike/blockFrequency/Summary_BHiveCount5002022-07-14-13-05-29_tsj.xlsx") # Full

glv._set("taskfilePath", "/home/shaojiemike/blockFrequency") # 输入文件集合所在的目录
# glv._set("taskList",{"tensorflow_test_5":"test"})
# glv._set("taskList",{"tensorflow_test_5":"test"})
# glv._set("taskList",{"tensorflow_test_100":"test"})
# glv._set("taskList",{"test_insns_blockFrequency_skip_2":"test_insns"})
# glv._set("taskList",{"Gzip_all_skip_2":"Gzip"})
# glv._set("taskList",{"tensorflow_41Gdir_00all_skip_2":"Tensorflow"})
glv._set("taskList",{
            "tensorflow_test_100":"tensorflow_1",
            "tensorflow_test_5":"tensorflow_2",
            "tensorflow_test_3":"tensorfw_3"})
# glv._set("taskList", 
#                 {        

#                 "ffmpeg_useFileNum_1_skipNum_0":"ffmpeg",
#                 "FFTW_useFileNum_1_skipNum_0":"FFTW",
#                 "fftw_runLog":"FFTW_runLog",
#                 # "lapack_useFileNum_1_skipNum_0":"lapack(dgetrf)", #DGETRF computes an LU factorization of a general M-by-N matrix A
#                 "lapack_runLog":"lapack_runLog(dgetrf)",
#                 "openblas_utest_useFileNum_4_skipNum_0":"OpenBLAS",
#                 "OpenBLAS_level1_ddot_N8398":"OpenBLAS_level1_ddot",
#                 "OpenBLAS_level3_dgemm_N9523":"OpenBLAS_level3_dgemm",
#                 "OpenBLAS_level3_zgemm_N7470":"OpenBLAS_level3_zgemm"
#                 "EmbreeHello_useFileNum_1_skipNum_0":"Embree",
#                 "EmbreeHello_runLog":"Embree_runLog",
#                 "tensorflow_41Gdir_00all_skip_2":"Tensorflow",
#                 "tensorflow_20W_runLog":"Tensorflow_runLog_skip0",
#                 # "clang_harness_00all_skip_2":"Clang",
#                 "clang_make_runLog":"Clang_runLog",
#                 "MM_median_all_skip_2":"Eigen_MM_Middle",
#                 "Eigen_MM_Big_N4582":"Eigen_MM_Big"
#                 "Gzip_all_skip_2":"Gzip",
#                 "Gzip_clang_85G_N5443":"Gzip_85G_runLog",
#                 "redis_r1000000_n2000000_P16_all_skip_2":"Redis",
#                 "redis_r100000_n200000_N8452":"Redis_skip0",
#                 "test_insns_blockFrequency_skip_2":"test_insns"}) # 输入文件名的前缀，和在excel里的名称
glv._set("taskfilenamesubfix","log") # 输入文件名的后缀
glv._set("OSACAPath","/home/qcjiang/softwares/anaconda3/bin/osaca") # OSACA 的测量对比暂时不再支持
glv._set("LLVM_mcaPath","/home/shaojiemike/github/MyGithub/llvm-project/build/bin/llvm-mca")
glv._set("LLVM_mcaBaselinePath","/home/shaojiemike/Download/llvm-project-llvmorg-13.0.0/build/bin/llvm-mca")
glv._set("BHivePath","/home/shaojiemike/test/bhive-re/bhive-reg/bhive")
glv._set("BHiveCount",500)
glv._set("ProcessNum",20)
glv._set("failedRetryTimes",1)
glv._set("timeout",10)
glv._set("excelOutPath",glv.GLOBALS_DICT["taskfilePath"]+'/Summary_BHiveCount'+str(glv.GLOBALS_DICT["BHiveCount"])+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+'_tsj.xlsx')
glv._set("debug","yes")

def pasteFullFileName(taskfilenameprefixWithoutPath):
    taskfilenamesubfix=glv._get("taskfilenamesubfix")
    taskfilePath=glv._get("taskfilePath")
    taskfilenameprefix="{}/{}".format(taskfilePath,taskfilenameprefixWithoutPath)
    return "{}.{}".format(taskfilenameprefix,taskfilenamesubfix)


