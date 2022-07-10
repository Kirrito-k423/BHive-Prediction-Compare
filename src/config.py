import global_variable as glv
from collections import defaultdict
import time

glv._init()

glv._set("taskfilePath", "/home/shaojiemike/blockFrequency")
# glv._set("taskList",{"tensorflow_test_5":"test"})
# glv._set("taskList",{"tensorflow_test_5":"test"})
# glv._set("taskList",{"test_insns_blockFrequency_skip_2":"test_insns"})
# glv._set("taskList",{"Gzip_all_skip_2":"Gzip"})
# glv._set("taskList",{"tensorflow_41Gdir_00all_skip_2":"Tensorflow"})
# glv._set("taskList",{
#             "tensorflow_test_100":"tensorflow_1",
#             "tensorflow_test_5":"tensorflow_2",
#             "tensorflow_test_3":"tensorfw_3"})
glv._set("taskList", 
                {        
                "FFTW_useFileNum_1_skipNum_0":"FFTW",
                "lapack_useFileNum_1_skipNum_0":"lapack(dgetrf)", #DGETRF computes an LU factorization of a general M-by-N matrix A
                "openblas_utest_useFileNum_4_skipNum_0":"OpenBLAS",
                "EmbreeHello_useFileNum_1_skipNum_0":"Embree",
                "tensorflow_41Gdir_00all_skip_2":"Tensorflow",
                "clang_harness_00all_skip_2":"Clang",
                "MM_median_all_skip_2":"Eigen",
                "Gzip_all_skip_2":"Gzip",
                "redis_r1000000_n2000000_P16_all_skip_2":"Redis",
                "test_insns_blockFrequency_skip_2":"test_insns"})
glv._set("taskfilenamesubfix","log")
glv._set("OSACAPath","/home/qcjiang/softwares/anaconda3/bin/osaca")
glv._set("LLVM_mcaPath","/home/shaojiemike/github/MyGithub/llvm-project/build/bin/llvm-mca")
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


