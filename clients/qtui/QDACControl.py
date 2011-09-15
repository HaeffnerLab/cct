import sys
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
import os

#from QCustomLevelSpin import QCustomLevelSpin

class QDACControl(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        basepath = os.environ.get('LABRADPATH',None)
        if not basepath:
            raise Exception('Please set your LABRADPATH environment variable')
        path = os.path.join(basepath,'cct/clients/qtui/daccontrol.ui')

        uic.loadUi(path,self)

        #ex = QCustomLevelSpin('Ex',(0.0,100.0))
        #ey = QCustomLevelSpin('Ey',(0.0,100.0))
        
        #self.lex.addWidget(ex)
        #self.ley.addWidget(ey)

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    icon = QDACControl()
    icon.show()
    app.exec_()
