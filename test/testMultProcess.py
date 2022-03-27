from __future__ import print_function
import multiprocessing as mp
import traceback
import time

class Process(mp.Process):
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = mp.Pipe()
        self._exception = None

    def run(self):
        try:
            mp.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))
            # raise e  # You can still rise this exception if you need to

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


def target():
    i=2
    while i>0:
        i-=1
        time.sleep(5)
    print(1/0)

def target2():
    i=2
    while i>0:
        i-=1
        time.sleep(1)
    # raise ValueError('Something2 went wrong...')

pList=[]
pList.append(Process(target = target))
pList.append(Process(target = target2))
for p in pList:
    p.start()
while 1:
    print(mp.active_children())
    print(len(mp.active_children()))
    for p in pList:
        if p.exception:
            error, traceback = p.exception
            print(2)
            print(traceback)
            raise TypeError(traceback)
    time.sleep(1)
p.join()

