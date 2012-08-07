import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
import math

class QCustomLevelSpin(QtGui.QWidget):
    onNewValues = QtCore.pyqtSignal()
    def __init__(self, title, levelRange, parent=None):
        QtGui.QWidget.__init__(self, parent)
	basepath = os.path.dirname(__file__)
        #        basepath = os.environ.get('LABRADPATH',None)
#        if not basepath:
#            raise Exception('Please set your LABRADPATH environment variable')
        path = os.path.join(basepath,'levelspinslider.ui')
        uic.loadUi(path,self)
        #set widget properties
        self.title.setText(title)
        self.levelRange = levelRange
        #set ranges
        maxDifference = abs(levelRange[1] - levelRange[0])
        self.spinLevel.setRange(*levelRange)
        self.sliderLevel.setRange(100.*levelRange[0],100.*levelRange[1])
        #self.dict = {'level':0}
        self.level = 0
        #connect functions
        self.sliderLevel.valueChanged.connect(self.sliderLevelChanged)
        self.spinLevel.valueChanged.connect(self.spinLevelChanged)

    def setValues(self, level):
        self.disconnectAll()
        self.spinLevel.setValue(level)
        self.sliderLevel.setValue(100*level)
        self.level = level
        self.connectAll()
        
    def setStepSize(self, step):
        self.spinLevel.setSingleStep(step)

    def sliderLevelChanged(self,newlevel):
        #if the change results in outputs not within range then don't perform
        print "Slider level changed"
        oldlevel = self.level
        withinRange = self.checkRange(newlevel/100.)
        if withinRange:
            self.level = newlevel/100.
            self.disconnectAll()
            self.spinLevel.setValue(newlevel/100.)
            self.onNewValues.emit()
            self.connectAll()
        else:
            self.sliderLevel.setValue(oldlevel*100.)
    
    def spinLevelChanged(self, newlevel):
        oldlevel = self.level
        #withinRange = self.checkLevelTilt(newlevel, self.dict['tilt'])
        withinRange = self.checkRange(newlevel)
        if withinRange:
            self.level = newlevel
            self.disconnectAll()
            self.sliderLevel.setValue(newlevel*100)
            self.onNewValues.emit()
            self.connectAll()
        else:
            suggestedLevel = self.suggestLevel(newlevel)
            self.spinLevel.setValue(suggestedLevel)
    
    def suggestLevel(self, level):
        #if spin box value selected too high, goes to the highest possible value
        if level < self.levelRange[0]:
            suggestion = self.levelRange[0]
        if level > self.levelRange[1]:
            suggestion = self.levelRange[1]
        return suggestion
    
    def checkRange(self,val):
        if self.levelRange[0] <= val <= self.levelRange[1]:
            return True
        else:
            return False
    
    def checkBounds(self, val):
    	if val < self.levelRange[0]:
    	      output = self.levelRange[0]
    	elif val > self.levelRange[1]:
    	      output = self.levelRange[1]
    	else:
    	      output = val
    	return output
	
    def disconnectAll(self):
        self.sliderLevel.blockSignals(True)
        self.spinLevel.blockSignals(True)
    
    def connectAll(self):
        self.sliderLevel.blockSignals(False)
        self.spinLevel.blockSignals(False)
        
    def setValueNoSignal(self, value):
        self.spinLevel.blockSignals(True)
        self.sliderLevel.blockSignals(True)
        self.spinLevel.setValue(value)
        self.sliderLevel.setValue(value)
        self.spinLevel.blockSignals(False)
        self.sliderLevel.blockSignals(False)
        
if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	icon = QCustomLevelSpin('Control',(0.0,100.0))
	icon.show()
	app.exec_()

 
