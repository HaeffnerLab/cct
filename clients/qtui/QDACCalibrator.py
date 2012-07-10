import sys
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
import os

class QDACCalibrator(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #basepath = os.environ.get('LABRADPATH',None)
        basepath = '/home/cct/LabRAD'
        if not basepath:
            raise Exception('Please set your LABRADPATH environment variable')
        path = os.path.join(basepath,'cct/clients/qtui/daccalib.ui')

        uic.loadUi(path,self)

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    icon = QDACCalibrator()
    icon.show()
    app.exec_()
