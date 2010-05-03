#! /usr/bin/env python

class embed():
    '''
    This is a class that adds the ability for ntv to be used from with in a python interpriter.
    In order to use this you must be using python > 2.6 or have the multiprocessing package
    installed.
    To embed this do something like the following example
    #> python
    >>> from NTV.embed import embed
    >>> import numpy
    >>> x = numpy.arange(441)
    >>> x = x.reshape(21,21)
    >>> my_instance = embed()
    >>> my_instance.showArray(x)
    '''
    def __init__(self):
        #added thread for if multiprocess fails, still prefer process though, as this separates
        #cpu useage of ntv from the terminal
        from multiprocessing import Process, Pipe
        par,c = Pipe()
        self.par = par
        self.p = Process(target=self.run,args=(c,))
        self.p.start()
    def run(self,conn):
        exec('from NTV import *')
        import NTV as ntv
        self.app = QApplication(sys.argv)
        self.win = ntv.NTV(pipe=conn)
        self.win.show()
        self.app.exec_()
    def showArray(self,array):
        self.par.send(array)