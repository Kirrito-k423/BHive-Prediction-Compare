import time
from  multiprocessing import Process

def foo(i):
    time.sleep(1)
    print (p.is_alive(),i,p.pid)
    time.sleep(1)

if __name__ == '__main__':
    p_list=[]
    for i in range(10):
        p = Process(target=foo, args=(i,))
        #p.daemon=True
        p_list.append(p)

    for p in p_list:
        p.start()
    # for p in p_list:
    #     p.join()

    print('main process end')
# 怎么返回值呢？