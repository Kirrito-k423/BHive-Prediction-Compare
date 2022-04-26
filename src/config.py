import global_variable as glv

glv._init()

glv._set("taskfilePath", "/home/qcjiang/tests/bb_test/blockFrequency")
glv._set("taskList", 
                {        
                "tensorflow_41Gdir_00all_skip_2":"Tensorflow",
                "clang_harness_00all_skip_2":"Clang",
                "MM_median_all_skip_2":"Eigen",
                "Gzip_all_skip_2":"Gzip",
                "redis_r1000000_n2000000_P16_all_skip_2":"Redis"})
glv._set("taskfilenamesubfix","log")
glv._set("OSACAPath","/home/qcjiang/softwares/anaconda3/bin/osaca")
glv._set("LLVM_mcaPath","/home/qcjiang/codes/llvm-project/build/bin/llvm-mca")
glv._set("BHivePath","/home/qcjiang/codes/KunpengWorkload/micro_benchmarks/bhive-reg/main")
glv._set("BHiveCount",500)
glv._set("ProcessNum",20)
glv._set("timeout",120)
glv._set("excelOutPath",glv.GLOBALS_DICT["taskfilePath"]+'/Summary_BHiveCount'+str(glv.GLOBALS_DICT["BHiveCount"])+'_tsj.xlsx')

def pasteFullFileName(taskfilenameprefixWithoutPath):
    taskfilenamesubfix=glv._get("taskfilenamesubfix")
    taskfilePath=glv._get("taskfilePath")
    taskfilenameprefix="{}/{}".format(taskfilePath,taskfilenameprefixWithoutPath)
    return "{}.{}".format(taskfilenameprefix,taskfilenamesubfix)


# taskfilePath=""
# # taskList={\
# #             "tensorflow_test_100":"tensorflow_1",
# #             "tensorflow_test_5":"tensorflow_2",
# #             "tensorflow_test_3":"tensorflow_3"}
# # taskList={           "test_insns_blockFrequency_skip_2":"test_insns"}
# # taskList={ "test_insns_test_5":"test"}
# # taskList={ 
# taskList={        
#                 "tensorflow_41Gdir_00all_skip_2":"Tensorflow",
#                 "clang_harness_00all_skip_2":"Clang",
#                 "MM_median_all_skip_2":"Eigen",
#                 "Gzip_all_skip_2":"Gzip",
#                 "redis_r1000000_n2000000_P16_all_skip_2":"Redis"}

# # OSACAPath="/home/shaojiemike/github/OSACA-feature-tsv110/newOSACA/bin/osaca "
# OSACAPath="/home/qcjiang/softwares/anaconda3/bin/osaca"
# LLVM_mcaPath="/home/qcjiang/codes/llvm-project/build/bin/llvm-mca"
# BHivePath="/home/qcjiang/codes/KunpengWorkload/micro_benchmarks/bhive-reg/main"
# #          /home/qcjiang/codes/KunpengWorkload/micro_benchmarks/bhive-reg/main
# saveInfo="0326newOSACAagain"
# BHiveCount=500
# excelOutPath = taskfilePath+'/Summary_BHiveCount'+str(BHiveCount)+'_tsj.xlsx'
# ProcessNum=20
# # sencond
# timeout=60