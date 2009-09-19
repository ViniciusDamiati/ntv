#! /usr/bin/env python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import pyfits as pf
import matplotlib.pyplot
import sys
import time

from NTV_UI import Ui_NTV
from details import Ui_Dialog

#This function is used to scale up the side preview to the same size as the Qlabel,
#for better viewing
def rebin(thedata, factor,conserve=None):
    """
Rebins an array into an array with the same aspect ratio, but with
dimensions that are larger or smaller by a factor of 'factor'. Increase
or decrease of dimensions is determined by the sign of 'factor'.

If the conserve keyword is set, flux is conserved, and the total of
the output array will be equal (barring rounding errors) to the total 
of the input array.

Works for 2D arrays; would require more smarts to make it work for 
higher dimensions. 
    """
    assert abs(factor) != 1.0, "Rebinning at the same scale wastes cpu!"

    if factor < 0: # make the array smaller
        oldshape=thedata.shape
        factor=abs(factor)
        work=np.zeros(oldshape,thedata.dtype)
        for i in range(0,oldshape[0],factor):
            for j in range(0,oldshape[1],factor):
                if (conserve is None):
                    work[i,j]=thedata[i:i+factor,j:j+factor].mean(dtype=np.float64)
                else:
                    work[i,j]=thedata[i:i+factor,j:j+factor].sum(dtype=np.float64)
        return work[::factor,::factor]

    elif (factor > 0): # make the array bigger
        work= np.repeat( np.repeat(thedata, factor, axis=0), factor, axis=1)
        if (conserve is None):
            return work
        else:
            return work/(factor*factor)

#These next three functions are used to fit a two dimentional Gaussian to a user defined object
#The accuracy of this fit should only be trusted to the tenths place, but it provides a good guess.
#This code was used from the scipy cookbook.
def gaussian(height, center_x, center_y, width_x, width_y):
    width_x = np.float(width_x)
    width_y = np.float(width_y)
    return lambda x,y: height*np.exp(-(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

def moments(data):
    total = data.sum()
    X, Y = np.indices(data.shape)
    x = (X*data).sum()/total
    y = (Y*data).sum()/total
    col = data[:, int(y)]
    width_x = np.sqrt(np.abs((np.arange(col.size)-y)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = np.sqrt(np.abs((np.arange(row.size)-x)**2*row).sum()/row.sum())
    height = data.max()
    return height, x, y, width_x, width_y

def fitgaussian(data):
    from scipy import optimize
    params = moments(data)
    errorfunction = lambda p: np.ravel(gaussian(*p)(*np.indices(data.shape)) - data)
    p, success = optimize.leastsq(errorfunction, params)
    return p

#This class implements the dialog box to display information on a particular object that a user
#defines by clicking on it.
class details_view(QDialog,Ui_Dialog):
    '''
    This class is mainly for internal use only. It is used to implement the pop up dialog window
    That displays information about the object that a user selects.
    '''
    def __init__(self,frame,frameedit,realx,realy,apsize,clipmax,clipmin,color,parent=None):
        super(details_view,self).__init__(parent)
        self.setupUi(self)
        cutsize = apsize*4
        apin    = apsize*2
        apout   = apsize*3
        #Create a temporary view to centroid with, will be overridden when the true center is found
        view = frame[realy-cutsize:realy+cutsize,realx-cutsize:realx+cutsize]
        #Finding center and correcting for the cut size
        self.y,self.x = fitgaussian(view)[[1,2]]
        self.totalx = realx - cutsize + self.x
        self.totaly = realy - cutsize + self.y
        #Creating the new view based on the correct positions. This is the view the radial profile will be
        #generated from
        view = frame[self.totaly-cutsize:self.totaly+cutsize,self.totalx-cutsize:self.totalx+cutsize]
        #View 2 is view of the minimap. This is required to be separate since there may be either a maping of
        #log or linear scale
        view2 = frameedit[self.totaly-cutsize:self.totaly+cutsize,self.totalx-cutsize:self.totalx+cutsize]
        #Sow the view2 and set associated text
        self.vis.canvas.ax.imshow(view2,vmax=clipmax,vmin=clipmin,cmap=color)
        self.yin,self.xin= np.indices((view.shape))
        self.xval.setText(str(self.totalx))
        self.yval.setText(str(self.totaly))
        #create a distance array and create the radial profile, display this information to screen based on given
        #aperature size and anulus
        self.dist = ((cutsize-self.xin)**2+(cutsize-self.yin)**2)**0.5
        self.radprof.canvas.ax.plot(self.dist.flatten(),view.flatten(),'k.')
        self.counts.setText(str(np.sum(view[np.where(self.dist<apsize)])))
        self.background.setText(str(np.median(view[np.where(np.bitwise_and(self.dist>2*apsize,self.dist<3*apsize))])))
        self.radprof.canvas.ax.axvline(apsize,color="g",label="Aperature")
        self.radprof.canvas.ax.axvline(apin,color="r",label="Anulus")
        self.radprof.canvas.ax.axvline(apout,color="r")
        self.radprof.canvas.ax.legend()
        self.exec_()

class NTV(QMainWindow,Ui_NTV):
    '''
    This is the main program. It implements the event loop, and handles user interaction.
    This can be either ran from the supplied script, or embeding it in a python session,
    see the embed class for details on how to do that. Data can be either loaded into the
    program with open from the file menu, by dragging and dropping files, invoking a file
    path from the command line, or using the showArray method if using in embed mode.
    '''
    def __init__(self,file=None,parent=None,pipe=None):
        super(NTV,self).__init__(parent)
        self.setupUi(self)
        
        #This checks for files loaded with the program from the command line
        if file != None:
            if file.find('fits') != -1 or file.find('FIT')!=-1:
                self.path = file
                self.loadinfo()
            else:
                self.filelab.setText('<font color=red>Invalid Format</font>')
        
        
        #Constants used by program, funloaded gets set to 1 when there is a file loaded, provides a check for manipulating functions
        #previewsize is a constant used to get the size of the cut for the minimap.
        self.funloaded = 0
        self.previewsize = 20
        
        #Set some UI elements
        self.sizeofcut.setText('3')
        
        #This handels dranging and dropping operations
        self.centy.dragEnterEvent = self.lbDragEnterEvent
        self.centy.dropEvent = self.lbDropEvent
        
        #set ui element
        self.filelab.setText("<font color=red>Load File</font>")
        
        #populate the colormap drop down box with available color maps
        self.cmaplist = matplotlib.cm.datad.keys()
        self.cmapbox.insertItems(0, self.cmaplist)
        self.cmapbox.setCurrentIndex(self.cmaplist.index('gray'))
        
        #change the scope of the pipe object in order for it to be referenced from other parts of the class
        self.pipe = pipe
        
        #Checks to see if a pipe was passes, ie if the program is being used in embeded mode, if so, starts the thread that will listen to the pipe
        if pipe != None:
            self.recive = myThread(self,self.pipe)
            self.recive.start()
        
        #These connect each of the UI elements with their associated action
        QObject.connect(self.cmapbox,SIGNAL('activated(int)'),self.cmapupdate)
        QObject.connect(self.clipslide,SIGNAL('sliderReleased()'),self.sliderupdate)
        self.imshow.canvas.fig.canvas.mpl_connect('motion_notify_event',self.mouseplace)
        QObject.connect(self.lincheck,SIGNAL('toggled(bool)'),self.scale)
        QObject.connect(self.logcheck,SIGNAL('toggled(bool)'),self.scale)
        QObject.connect(self.actionOpen,SIGNAL('triggered()'),self.open)
        QObject.connect(self.actionQuit,SIGNAL('triggered()'),self.close)
        QObject.connect(self.pushButton,SIGNAL('clicked()'),self.getclick)
    
    def rec_data(self,array):
        '''
        This is the fucntion that is used to update the image variable of the class if the program is used in embeded mode, and an array is passed to the pipe.
        '''
        self.image = array
        self.loadinfo()
    
    def getclick(self):
        '''
        This is just a wrapper class to pass the get star button event to the drawbox function. Uses the mpl backend to connect to the canvas object and get the event.
        '''
        if self.funloaded == 1:
            self.cid = self.imshow.canvas.fig.canvas.mpl_connect('button_press_event',self.drawbox)
        
    def drawbox(self,event):
        '''
        This function recives an event from the mpl canvas and passes certain data to the constructor function of the details view class
        '''
        if self.funloaded == 1:
            #get aperature size from size of cut widget
            cutv = int(self.sizeofcut.text())
            #create an instance of details_view class
            self.dbox = details_view(self.image,self.imageedit,event.xdata,event.ydata,cutv,self.mx,self.imageedit.min(),self.z)
            #disconnect the canvas from clicks, so that it can still be used for functions such as zooming etc.
            self.imshow.canvas.fig.canvas.mpl_disconnect(self.cid)

    def open(self):
        '''
        Impliments open from the file menu and updates the program accordingly
        '''
        file = str(QFileDialog.getOpenFileName(self,'Select Files to Process','~/'))
        if file.find('fits') != -1 or file.find('FIT')!=-1:
            self.path = file
            self.loadinfo()
        else:
            self.filelab.setText('<font color=red>Invalid Format</font>')
    
    def lbDragEnterEvent(self, event):
        '''
        updates the mouse for drop events. Should be updated in the future for proper handeling of file detection
        '''
        event.accept()
    def lbDropEvent(self, event):
        '''
        Gets a file that was dropped to the program, checks for compatability and up dates the image accordinly. TO DO: change file
        checking to its own separate function to call, was not an issue orrigionally
        '''
        link=event.mimeData().urls()
        file = str(link[0].toLocalFile())
        if file.find('fits') != -1 or file.find('FIT')!=-1:
            self.path = file
            self.loadinfo()
        else:
            #set error message
            self.filelab.setText('<font color=red>Invalid Format</font>')
   
    def mouseplace(self,event):
        '''
        Handels the mouse motion over the imshow mpl canvas object, TO DO: handel the edge events properly
        '''
        #checks to see if the data has been loaded
        if self.funloaded == 1:
            #makes sure the mouse is on the data canvas
            if event.ydata != None and event.xdata != None:
                #The try statement is to catch the problems that occur with cutting the numpy array on the boundary, aka
                #ignore the problems and just not update the image, yet not print out warnings to the terminal. In some future
                #version, it would be good to properly handle the edge events, to mantain preview
                try:
                    self.impix = self.image[event.ydata-self.previewsize:event.ydata+self.previewsize,event.xdata-self.previewsize:event.xdata+self.previewsize].copy()
                    #This next few lines is to simply set the values of several pixels to white in order to draw a cross hair
                    self.impix[18,20] = 255
                    self.impix[19,20] = 255
                    self.impix[21,20] = 255
                    self.impix[22,20] = 255
                    self.impix[20,18] = 255
                    self.impix[20,19] = 255
                    self.impix[20,21] = 255
                    self.impix[20,22] = 255
                    #This rebins the numpy array larger so that it will better be a preview and will fit the QLabel
                    self.impix = rebin(self.impix,5)
                except:
                    pass
                #This next bit is to convert the numpy array into something that can be displayed as a pixmap, It needs to be updated for clipping
                #and also applying the colormap!
                gray = np.require(self.impix, np.uint8, 'C')
                h, w = gray.shape
                result = QImage(gray.data, w, h, QImage.Format_Indexed8)
                result.ndarray = gray
                for i in range(256):
                    result.setColor(i, QColor(i, i, i).rgb())
                self.minipix.setPixmap(QPixmap(result))
                self.pixval.setText(str(self.image[event.ydata,event.xdata]))
    def sliderupdate(self):
        '''
        Updates the image clipping based on the value of the slider bar.
        '''
        if self.funloaded ==1:
            self.drawim()    
    
    def scale(self):
        '''
        Update the image accordingly to which option the user chooses for scaling, log or linear
        '''
        if self.funloaded == 1:
            if self.lincheck.isChecked():
                self.imageedit = self.image
                self.drawim()
            if self.logcheck.isChecked():
                self.imageedit = np.log(self.image)
                self.drawim()
    
    def cmapupdate(self):
        '''
        Simply redraw the canvas if the colormap is changed
        '''
        if self.funloaded == 1:
            self.drawim()
    
    def loadinfo(self):
        '''
        Load in a file if no in embeded mode. BUG and future TO DO, allow embeded mode to still accept drag and drops and file opens. Function updates labels accordingly
        '''
        #Load info if not in embed mode
        if self.pipe == None:
            self.filelab.setText("<font color=blue>"+self.path+"</font>")
            self.image = pf.getdata(self.path,header=False)
        #Set label according to embed mode
        if self.pipe != None:
            self.filelab.setText("<font color=blue>Numpy Array</font>")
        self.imageedit = self.image
        self.lincheck.setChecked(1)
        #Set funloaded to 1 to turn on interactions with UI elements
        self.funloaded = 1

        self.clipslide.setValue(self.clipslide.maximum())

        self.minlab.setText(str(self.image.min()))
        self.maxlab.setText(str(self.image.max()))
        self.xdim.setText(str(self.image.shape[1]))
        self.ydim.setText(str(self.image.shape[0]))
        self.drawim()

    def drawim(self):
        '''
        This fucntion actually handles the drawing of the imshow mpl canvas. It pulls the required elements from the ui on each redraw
        '''
        #Clear and update the axis on each redraw, this is nessisary to avoid a memory leak
        self.imshow.canvas.ax.cla()
        self.imshow.canvas.format_labels()
        #The next two lines are a bit hacky but are required to properly turn the color map from the listbox to an object so that the map
        #can be updated accordinglyyy
        self.ctext = str(self.cmapbox.currentText())
        exec('self.z = matplotlib.pyplot.cm.'+self.ctext)
        #This next line sets the maximum value in the image according to what vale the slider bar is at, basicaly its the maximum value times
        #the ratio of of the silder position over 100 added to the minimum value
        self.mx = (self.imageedit.max()-self.imageedit.min())*self.clipslide.value()/100. + self.imageedit.min()
        #updated the canvas and draw
        self.imshow.canvas.ax.imshow(self.imageedit,vmax=float(self.mx),vmin=self.imageedit.min(),cmap=self.z,interpolation=None)
        self.imshow.canvas.draw()

class myThread(QThread,NTV):
    '''
    This class is for internal use only. It inherets the QThread class, and is used to
    separate the listening of a pipe in interactive mode into its own thread, as to not
    tie up the main event loop
    '''
    import numpy as np
    def __init__(self,parent,pipe):
	QThread.__init__(self)
        self.conn = pipe
        QObject.connect(self,SIGNAL('got_it'),parent.rec_data)
    def run(self):
        while True:
            self.data = self.conn.recv()
            if type(self.data) == np.ndarray:
                if len(self.data.shape) == 2:
                    self.emit(SIGNAL('got_it'),self.data)
            time.sleep(1)

class embed():
    '''
    This is a class that adds the ability for ntv to be used from with in a python interpriter.
    In order to use this you must be using python > 2.6 or have the multiprocessing package
    installed.
    To embed this do something like the following example
    #> python
    >>> from NTV import *
    >>> import numpy
    >>> x = numpy.arange(441)
    >>> x = x.reshape(21,21)
    >>> my_instance = NTV.embed()
    >>> my_instance.showArray(x)
    '''
    def __init__(self):
        from multiprocessing import Process, Pipe
        par,c = Pipe()
        self.par = par
        self.p = Process(target=self.run,args=(c,))
        self.p.start()
    def run(self,conn):
        self.app = QApplication(sys.argv)
        self.win = NTV(pipe=conn)
        self.win.show()
        self.app.exec_()
    def showArray(self,array):
        self.par.send(array)

if __name__=="__main__":
    #This is a section to run the 
    import sys
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        filez = sys.argv[1]
    else:
        filez = None
    plot = NTV(file=filez)
    plot.show()
    sys.exit(app.exec_())       
    
'''
TO DO:
allow pipe mode to properly load in files via drag and drop events
Implement 3d array support!
''' 
