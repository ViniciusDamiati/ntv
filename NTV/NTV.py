#! /usr/bin/env python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import pyfits as pf
import matplotlib.pyplot
import sys
import time
import scipy as sp

from NTV_UI import Ui_NTV
from details import Ui_Dialog
from header_ui import Ui_header
from threeD_ui import Ui_threeD

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



class header_view(QDialog,Ui_header):
    def __init__(self,cards,parent=None):
        super(header_view,self).__init__(parent)
        self.setupUi(self)
        for item in cards:
            item = str(item)
            self.cardlist.addItem(QListWidgetItem(item))         
        self.exec_()

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
        #set the inputs to class members and initialize some variables needed in plotting
        self.frame = frame
        self.framey,self.framex = self.frame.shape
        if self.framey > self.framex:
            self.flimit = self.framey/2.
        else:
            self.flimit = self.framex/2.
        self.clipmax = clipmax
        self.clipmin = clipmin
        self.color = color
        self.frameedit = frameedit
        self.cutsize = apsize*4
        self.apsize = apsize
        self.radin    = apsize*2
        self.radout   = apsize*3
        self.limit_check()
        #sets the variable that will be used to pick lines and make decisions
        self.artist = None
        #Create a temporary view to centroid with, will be overridden when the true center is found
        view = frame[realy-self.cutsize:realy+self.cutsize,realx-self.cutsize:realx+self.cutsize]
        maxy,maxx = np.where(view==view.max())
        maxy = int(realy-self.cutsize+maxy[0])
        maxx = int(realx-self.cutsize+maxx[0])
        view = frame[maxy-self.cutsize:maxy+self.cutsize,maxx-self.cutsize:maxx+self.cutsize]-np.median(frame[maxy-self.cutsize:maxy+self.cutsize,maxx-self.cutsize:maxx+self.cutsize])
        #Finding center and correcting for the cut size
        self.y,self.x = fitgaussian(view)[[1,2]]
        #this is a fail safe for if fitgaussian fails
        if np.abs(self.y) > 2*self.cutsize or np.abs(self.x) > 2*self.cutsize:
            self.y = self.cutsize
            self.x = self.cutsize
        self.totalx = maxx - self.cutsize + self.x
        self.totaly = maxy - self.cutsize + self.y
        self.xval.setText(str(self.totalx))
        self.yval.setText(str(self.totaly))
        
        self.radprof.canvas.fig.canvas.mpl_connect('pick_event',self.on_pic)
        self.radprof.canvas.fig.canvas.mpl_connect('button_release_event',self.button_release_callback)
        self.radprof.canvas.fig.canvas.mpl_connect('motion_notify_event',self.motion_notify_callback)
        QObject.connect(self,SIGNAL('paint'),self.radprof.repaint)
        #self.draw_canvas()
        #This thread is a hack to get the canvas to redraw properly on the first draw. futures redraws are handled by the draw_cancas itself.
        temp = myThread2(parent=self)
        temp.start()
        self.show()
    def limit_check(self):
        if self.cutsize >= self.flimit:
            self.cutsize = self.flimit-1
        if self.radout >= self.flimit:
            self.radout = 3*self.flimit/4.
        if self.radin >= self.radout:
            self.radin = self.flimit/2.
        if self.apsize >= self.flimit:
            self.apsize = self.flimit/4.
    
    def dummy(self):
        '''
        This is the function that facillitates the posponed drawing of the plot via the separate thread.
        '''
        self.radprof.canvas.fig.canvas.mpl_connect('draw_event',self.draw_callback)
        self.vis.canvas.ax.cla()
        self.vis.canvas.format_labels()
        self.draw_canvas()
        
    def draw_canvas(self):
        #Creating the new view based on the correct positions. This is the view the radial profile will be
        #generated from
        self.view = self.frame[self.totaly-self.cutsize:self.totaly+self.cutsize,self.totalx-self.cutsize:self.totalx+self.cutsize]
        #View 2 is view of the minimap. This is required to be separate since there may be either a maping of
        #log or linear scale
        self.view2 = self.frameedit[self.totaly-self.cutsize:self.totaly+self.cutsize,self.totalx-self.cutsize:self.totalx+self.cutsize]
        #Sow the view2 and set associated text
        self.vis.canvas.ax.imshow(self.view2,vmax=self.clipmax,vmin=self.clipmin,cmap=self.color)
        self.yin,self.xin= np.indices((self.view.shape))
        #create a distance array and create the radial profile, display this information to screen based on given
        #aperature size and anulus
        self.dist = ((self.cutsize-self.xin)**2+(self.cutsize-self.yin)**2)**0.5
        self.radprof.canvas.ax.plot(self.dist.flatten(),self.view.flatten(),'k.')
        #sum up the photons in anulus
        self.photons = np.sum(self.view[np.where(self.dist<self.apsize)])
        #get median backkground lvl
        self.bphotons = np.median(self.view[np.where(np.bitwise_and(self.dist>self.radin,self.dist<self.radout))])
        #update text and background
        self.background.setText(str(self.bphotons))
        self.photons -= len(np.where(self.dist<self.apsize))*self.bphotons
        self.counts.setText(str(self.photons))
        #Draw the interactive lines
        self.ap = self.radprof.canvas.ax.axvline(self.apsize,color="g",label="Aperture",picker=5,animated=True)
        self.rad1 = self.radprof.canvas.ax.axvline(self.radin,color="r",label="Annulus",picker=5,animated=True)
        self.rad2 = self.radprof.canvas.ax.axvline(self.radout,color="r",picker=5,animated=True)
        self.leg = self.radprof.canvas.ax.legend()
        #format and draw the canvas
        self.radprof.canvas.format_labels()
        self.radprof.canvas.draw()
        self.vis.canvas.draw()
        self.radprof.canvas.format_labels()
        #emit a paint signal to make sure the window is redrawn properly
        self.emit(SIGNAL('paint'))

    def on_pic(self,event):
        '''
        This function is called when one of the vertical lines is selected, set the line selected
        to the line to be edited.
        '''
        self.artist = event
    
    def draw_callback(self,event):
        #grab the current state of the canvas, inorder to quickly blit the background
        self.bg = self.radprof.canvas.fig.canvas.copy_from_bbox(self.radprof.canvas.ax.bbox)
        #redraw each of the member elements during dragging.
        self.radprof.canvas.ax.draw_artist(self.ap)
        self.radprof.canvas.ax.draw_artist(self.rad1)
        self.radprof.canvas.ax.draw_artist(self.rad2)
        self.radprof.canvas.ax.draw_artist(self.leg)
        self.radprof.canvas.fig.canvas.blit(self.radprof.canvas.ax.bbox)
        #emit a paint signal to make sure the window is redrawn properly
        self.emit(SIGNAL('paint'))
    
    
    def button_release_callback(self,event):
        '''
        called when a button is released
        '''
        if self.artist != None:
            #Set the artist to none, so that mouse motion events will be turned off.
            self.artist = None
            # get the current radii for the ap and annulus inorder to redraw the figure
            self.apsize = self.ap.get_data()[0][0]
            self.radin = self.rad1.get_data()[0][0]
            self.radout = self.rad2.get_data()[0][0]
            #rescale the view size based on the current aperature size
            self.cutsize = 4*int(self.apsize)
            #check that the annulus rings are in proper orientation, ie inside the cutview, and r1 < r2
            if self.rad1.get_data()[0][0] < self.apsize or self.rad1.get_data()[0][0] > 1.5*self.cutsize:
                self.radin = 2*self.apsize
            if self.rad2.get_data()[0][0] < self.radin or self.rad2.get_data()[0][0] > 1.5*self.cutsize:
                self.radout = self.radin+self.apsize
            #clear and format the axis to prevent memory overflow
            self.radprof.canvas.ax.cla()
            self.radprof.canvas.format_labels()
            self.limit_check()
            #redraw the canvas
            self.draw_canvas()

    def motion_notify_callback(self,event):
        '''
        This function gets called as the mouse moves when a line artist has been selected, it
        updates the the lines as they get dragged around
        '''
        #check to make sure there is a line selected
        if self.artist != None:
            #get the current x and y mouse positions
            x,y = event.xdata,event.ydata
            #make sure the mouse is in the canvas
            if x != None:
                #make sure you dont move past zero, as negitive radius is meaningless
                if x >0:
                    #update the position of selected artist and blit the figure. not really a full
                    #redraw
                    self.artist.artist.set_xdata([x,x])
                    self.radprof.canvas.fig.canvas.restore_region(self.bg)
                    self.radprof.canvas.ax.draw_artist(self.ap)
                    self.radprof.canvas.ax.draw_artist(self.rad1)
                    self.radprof.canvas.ax.draw_artist(self.rad2)
                    self.radprof.canvas.ax.draw_artist(self.leg)
                    self.radprof.canvas.fig.canvas.blit(self.radprof.canvas.ax.bbox)
    
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
        #change the scope of the pipe object in order for it to be referenced from other parts of the class
        self.pipe = pipe
        
        #Constants used by program, funloaded gets set to 1 when there is a file loaded, provides a check for manipulating functions
        #previewsize is a constant used to get the size of the cut for the minimap. cid is to initialize a check of weather the pic star
        #button has been clicked yet or not.
        self.funloaded = 0
        self.previewsetting = 20
        self.previewsize = self.previewsetting
        self.rebinfactor = 200/self.previewsize/2
        self.cid = None
        self.head = None
        self.imagecube = None
        
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
        QObject.connect(self.actionHeader,SIGNAL('triggered()'),self.header)
        QObject.connect(self.actionQuit,SIGNAL('triggered()'),self.close)
        QObject.connect(self.pushButton,SIGNAL('clicked()'),self.getclick)
        
        #fuctions for minimap scaling
        self.lin = lambda x,max,min: (255/(max-min))*x-(255*max/(max-min))+255
        self.func = self.lin

        #This checks for files loaded with the program from the command line
        if file != None:
            if file.find('fits') != -1 or file.find('FIT')!=-1:
                self.path = file
                self.loadinfo()
            else:
                self.filelab.setText('<font color=red>Invalid Format</font>')
    def check_preview(self):
        if self.image.shape[0]<self.previewsize*2 or self.image.shape[1]<self.previewsize*2:
            self.previewsize = 5
            self.rebinfactor=200/self.previewsize/2
    def change_frame(self,newnum):
        self.image = self.imagecube[newnum]
        self.scale()
    def header(self):
        '''
        This function serves to create a header_view instance to show the header information in a dialog box
        '''
        if self.funloaded ==1:
            if self.head != None:
                self.head_view = header_view(self.head.ascardlist())
    def rec_data(self,array):
        '''
        This is the fucntion that is used to update the image variable of the class if the program is used in embeded mode, and an array is passed to the pipe.
        '''
        self.pipe = None
        #Load the data into a cube and set the image to the first entry, if it is a threed cube
        if len(array.shape) == 3:
            #this will close a pre existing window if one is open.
            if self.imagecube != None:
                self.threed_win.close()
            self.image = array[0]
            self.imagecube = array
        else:
            self.image = array
        self.loadinfo()
    
    def getclick(self):
        '''
        This is just a wrapper class to pass the get star button event to the drawbox function. Uses the mpl backend to connect to the canvas object and get the event.
        '''
        if self.funloaded == 1:
            #This if statement is a check to make sure to clear if the pick star box was clicked more than once
            if self.cid != None:
                self.imshow.canvas.fig.canvas.mpl_disconnect(self.cid)
            self.cid = self.imshow.canvas.fig.canvas.mpl_connect('button_press_event',self.drawbox)
            
        
    def drawbox(self,event):
        '''
        This function recives an event from the mpl canvas and passes certain data to the constructor function of the details view class
        '''
        if self.funloaded == 1:
            #get aperature size from size of cut widget
            cutv = int(self.sizeofcut.text())
            #create an instance of details_view class
            details_view(self.image,self.imageedit,event.xdata,event.ydata,cutv,self.mx,self.imageedit.min(),self.z)
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
                #This next bit is to handle the preview problem at the boundary. it will create the preview based
                #on mouse position, and boundary value if you get close to boundary.
                ystart = event.ydata-self.previewsize
                ystop  = event.ydata+self.previewsize
                xstart = event.xdata-self.previewsize
                xstop  = event.xdata+self.previewsize
                ydif = 0
                xdif = 0
                if event.ydata<self.previewsize:
                    ystart = 0
                    ystop = self.previewsize*2
                    ydif = self.previewsize-event.ydata
                if event.ydata>self.image.shape[0]-1-self.previewsize:
                    ystart = self.image.shape[0]-1-self.previewsize*2
                    ystop = self.image.shape[0]-1
                    ydif = (self.image.shape[0]-1-event.ydata)-self.previewsize
                if event.xdata<self.previewsize:
                    xstart = 0
                    xstop  = self.previewsize*2
                    xdif = self.previewsize-event.xdata
                if event.xdata>self.image.shape[1]-1-self.previewsize:
                    xstart = self.image.shape[1]-1-self.previewsize*2
                    xstop  = self.image.shape[1]-1
                    xdif = (self.image.shape[1]-1-event.xdata)-self.previewsize
                if np.abs(ydif) > self.previewsize-3:
                    ydif = self.previewsize-3
                    if ydif <0:
                        ydif = -1*ydif
                if np.abs(xdif) > self.previewsize-3:
                    ydif = self.previewsize-3
                    if xdif <0:
                        xdif = -1*xdif
                self.impix = self.imageedit[ystart:ystop,xstart:xstop].copy()
                #This next few lines is to simply set the values of several pixels to white in order to draw a cross hair
                self.impix[self.previewsize-2-ydif,self.previewsize-xdif] = 255
                self.impix[self.previewsize-1-ydif,self.previewsize-xdif] = 255
                self.impix[self.previewsize+1-ydif,self.previewsize-xdif] = 255
                self.impix[self.previewsize+2-ydif,self.previewsize-xdif] = 255
                self.impix[self.previewsize-ydif,self.previewsize-2-xdif] = 255
                self.impix[self.previewsize-ydif,self.previewsize-1-xdif] = 255
                self.impix[self.previewsize-ydif,self.previewsize+1-xdif] = 255
                self.impix[self.previewsize-ydif,self.previewsize+2-xdif] = 255
                #This rebins the numpy array larger so that it will better be a preview and will fit the QLabel
                self.impix = rebin(self.impix,self.rebinfactor)
                #This next bit is to convert the numpy array into something that can be displayed as a pixmap, It needs to be updated to
                #applying the colormap!
                self.impix = self.func(self.impix,self.mx,self.imageedit.min())
                self.impix[np.where(self.impix>255)] = 255
                gray = np.require(self.impix, np.uint8, 'C')
                h, w = gray.shape
                result = QImage(gray.data, w, h, QImage.Format_Indexed8)
                result.ndarray = gray
                #COLORTABLE = [~((i + (i<<8) + (i<<16))) for i in range(255,-1,-1)]
                for i in range(256):
                    result.setColor(i, QColor(i, i, i).rgb())
                #result.setColorTable(COLORTABLE)
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
        Load in a file if no in embeded mode. Function updates labels accordingly
        '''
        self.previewsize = self.previewsetting
        self.rebinfactor = 200/self.previewsize/2
        #Load info if not in embed mode
        if self.imagecube != None:
            self.threed_win.close()
            self.imagecube = None
        if self.pipe == None:
            #close a threed window if one is open
            self.filelab.setText("<font color=blue>"+self.path+"</font>")
            self.image,self.head = pf.getdata(self.path,header=True)
            #This section loads the threed data if there is any. sets the frame as the first element,
            #similar behaivor happens from the embed side function
            if len(self.image.shape) == 3:
                self.imagecube = self.image
                self.image = self.image[0]
        #Set label according to embed mode
        if self.pipe != None:
            self.filelab.setText("<font color=blue>Numpy Array</font>")
            #set pipe to none to allow data to be loaded from the program.
            self.pipe = None
        #start up the window that will allow changes to which image in the cube user is viewing
        if self.imagecube != None:
            self.threed_win = three_d(len(self.imagecube),parent=self)
            self.threed_win.show()
        self.imageedit = self.image
        self.lincheck.setChecked(1)
        #Set funloaded to 1 to turn on interactions with UI elements
        self.funloaded = 1
        #make sure default position for clip slide bar is maximum, can change this behaivor later if need be
        self.clipslide.setValue(self.clipslide.maximum())
        #set associated information
        self.minlab.setText(str(self.image.min()))
        self.maxlab.setText(str(self.image.max()))
        self.xdim.setText(str(self.image.shape[1]))
        self.ydim.setText(str(self.image.shape[0]))
        self.check_preview()
        self.drawim()

    def drawim(self):
        '''
        This fucntion actually handles the drawing of the imshow mpl canvas. It pulls the required elements from the ui on each redraw
        '''
        #Clear and update the axis on each redraw, this is nessisary to avoid a memory leak
        self.imshow.canvas.ax.cla()
        self.imshow.canvas.format_labels()
        #The next two lines are a bit hacky but are required to properly turn the color map from the listbox to an object so that the map
        #can be updated accordingly
        self.ctext = str(self.cmapbox.currentText())
        exec('self.z = matplotlib.pyplot.cm.'+self.ctext)
        #This next line sets the maximum value in the image according to what vale the slider bar is at, basicaly its the maximum value times
        #the ratio of of the silder position over 100 added to the minimum value
        self.mx = (self.imageedit.max()-self.imageedit.min())*self.clipslide.value()/100. + self.imageedit.min()
        #updated the canvas and draw
        self.imdata = self.imshow.canvas.ax.imshow(self.imageedit,vmax=float(self.mx),vmin=self.imageedit.min(),cmap=self.z,interpolation=None,alpha=1)
        self.imshow.canvas.draw()

class three_d(QDialog,Ui_threeD,NTV):
    def __init__(self,length,parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.going = 0
        self.length = length
        self.fnumber.setText('0')
        self.fnumbar.setMinimum(0)
        self.fnumbar.setMaximum(self.length)
        QObject.connect(self.fnumbar,SIGNAL('sliderReleased()'),self.go)
        QObject.connect(self.play,SIGNAL('clicked()'),self.playback)
        QObject.connect(self,SIGNAL('changeim'),parent.change_frame)
        
    def go(self):
        self.newnum = int(self.fnumbar.value())
        self.fnumber.setText(str(self.newnum))
        self.emit(SIGNAL('changeim'),self.newnum)
    def playback(self):
        if self.going == 0:
            self.going = 1
            self.play.setText('stop')
            self.speed = float(self.delay.text())
            self.pthread = playThread(self.length,self.speed,parent=self)
            self.pthread.start()
            QObject.connect(self,SIGNAL('die'),self.pthread.kill,Qt.QueuedConnection)
        else:
            self.going = 0
            self.play.setText('play')
            self.emit(SIGNAL('die'))
            
    def update_slider(self,val):
        self.fnumbar.setValue(val)
        self.go()
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
                if len(self.data.shape) == 2 or len(self.data.shape) == 3:
                    self.emit(SIGNAL('got_it'),self.data)
            time.sleep(1)
            
class myThread2(QThread,details_view):
    '''
    This class is for internal use only, It simply delays the drawing of the radial profile till after the details view
    instance has been created. This solves a problem where the axes were getting blacked out and a repaint was in need to 
    be forced.
    '''
    def __init__(self,parent):
        QThread.__init__(self)
        QObject.connect(self,SIGNAL('redraw'),parent.dummy)
    def run(self):
        time.sleep(0.1)
        self.emit(SIGNAL('redraw'))

class playThread(QThread,three_d):
    def __init__(self,length,sleep,parent):
        QThread.__init__(self)
        self.bol = True
        self.length = length
        self.sleep = sleep
        self.setTerminationEnabled(True)
        self.connect(self,SIGNAL('update'),parent.update_slider)
    def run(self):
        while self.bol:
            for num in range(self.length):
                self.emit(SIGNAL('update'),num)
                time.sleep(self.sleep)
    def kill(self):
        self.terminate()

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
Change the cursor to reflect white or black depending on background
implement virtical and horizontal cut views in the details view
implement more dialog information such as s/n calc, ap and an positions, fwhm
need to put together an about page
fix background color
get wiki and doc writer
update readme
ask to see if, people would prefer multiple windows, or one window for deatils view, may
make toggle option.
look at weird minimap behaivor due to small array sizes
need to update some comments in the code for the new features.
stop three D window from closing
add circles to view in display window
''' 