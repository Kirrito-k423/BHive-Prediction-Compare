import global_variable as glv

glv._init()

glv._set("taskfilePath", "/home/shaojiemike/blockFrequency")
# glv._set("taskList",{"tensorflow_test_1":"test"})
glv._set("taskList",{\
            "tensorflow_test_100":"tensorflow_1",
            "tensorflow_test_5":"tensorflow_2",
            "tensorflow_test_3":"tensorflow_3"})
# glv._set("taskList", 
#                 {        
#                 "tensorflow_41Gdir_00all_skip_2":"Tensorflow",
#                 "clang_harness_00all_skip_2":"Clang",
#                 "MM_median_all_skip_2":"Eigen",
#                 "Gzip_all_skip_2":"Gzip",
#                 "redis_r1000000_n2000000_P16_all_skip_2":"Redis"})
glv._set("taskfilenamesubfix","log")
glv._set("OSACAPath","/home/qcjiang/softwares/anaconda3/bin/osaca")
glv._set("LLVM_mcaPath","/home/shaojiemike/github/MyGithub/llvm-project/build/bin/llvm-mca")
glv._set("BHivePath","/home/shaojiemike/test/bhive-re/bhive-reg/bhive")
glv._set("BHiveCount",500)
glv._set("ProcessNum",20)
glv._set("timeout",120)
glv._set("excelOutPath",glv.GLOBALS_DICT["taskfilePath"]+'/Summary_BHiveCount'+str(glv.GLOBALS_DICT["BHiveCount"])+'_tsj.xlsx')

def pasteFullFileName(taskfilenameprefixWithoutPath):
    taskfilenamesubfix=glv._get("taskfilenamesubfix")
    taskfilePath=glv._get("taskfilePath")
    taskfilenameprefix="{}/{}".format(taskfilePath,taskfilenameprefixWithoutPath)
    return "{}.{}".format(taskfilenameprefix,taskfilenamesubfix)



# # taskList={\
# #             "tensorflow_test_100":"tensorflow_1",
# #             "tensorflow_test_5":"tensorflow_2",
# #             "tensorflow_test_3":"tensorflow_3"}
# # taskList={           "test_insns_blockFrequency_skip_2":"test_insns"}
# # taskList={ "test_insns_test_5":"test"}
