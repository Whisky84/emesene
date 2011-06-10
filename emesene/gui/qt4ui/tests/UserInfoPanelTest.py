# -*- coding: utf-8 -*-
# run with: PYTHONPATH=".:gui/qt4ui"

'''Test module for ImageAreaSelector widget'''

import sys
import os
import gettext
# load translations
if os.path.exists('default.mo'):
    gettext.GNUTranslations(open('default.mo')).install()
elif os.path.exists('po/'):
    gettext.install('emesene', 'po/')
else:
    gettext.install('emesene')

from PyQt4 import QtCore
from PyQt4 import QtGui

import widgets
    
# test stuff:
class SessionStub (object):
    class ConfigDir (object):
        def get_path(*args):
            return  '/home/fastfading/src/emesene/emesene2/'\
                    'messenger.hotmail.com/'                \
                    'atarawhisky@hotmail.com/avatars/last'
    def __init__(self):
        self.config_dir = self.ConfigDir()

def main():
    '''Main method'''
    def test_stuff():
        '''Makes varios test stuff'''
        pass
    def response_cb(response, pixmap):
        print response, pixmap
        
    def shrow():
        uip_1.shrink()
        timer.timeout.connect(uip_1.grow)
        timer.start()
    
    def grink():
        uip_1.grow()
        timer.timeout.connect(uip_1.shrink)
        timer.start()
        
        
    test_stuff()
    os.putenv('QT_NO_GLIB', '1')
    qapp = QtGui.QApplication(sys.argv)
    
    timer = QtCore.QTimer(qapp)
    timer.setInterval(500)
    timer.setSingleShot(True)
    
    # free standing uip:
    #uip_3 = widgets.UserInfoPanel()
    #uip_3.set_all(0, 'ciao', 'konnichiha', 'a@b.c')
    
    # window containing the uip:
    window_1 = QtGui.QWidget()
    uip_1 = widgets.UserInfoPanel()
    textedit_1 = QtGui.QTextEdit()
    shrink_btn_1 = QtGui.QPushButton('Shrink')
    grow_btn_1   = QtGui.QPushButton('Grow')
    shrow_btn_1  = QtGui.QPushButton('Shrow')
    grink_btn_1  = QtGui.QPushButton('Grink')
    
    lay_1 = QtGui.QVBoxLayout()
    lay_1.addWidget(uip_1)
    lay_1.addWidget(textedit_1)
    lay_1.addWidget(shrink_btn_1)
    lay_1.addWidget(grow_btn_1)
    lay_1.addWidget(shrow_btn_1)
    lay_1.addWidget(grink_btn_1)
    window_1.setLayout(lay_1)
    
    uip_1.set_all(0, 'ciao', 'konnichiha', 'a@b.c')
    shrink_btn_1.clicked.connect(uip_1.shrink)
    #shrink_btn_1.clicked.connect(uip_3.shrink)
    grow_btn_1.clicked.connect(uip_1.grow)
    #grow_btn_1.clicked.connect(uip_3.grow)
    shrow_btn_1.clicked.connect(shrow)
    grink_btn_1.clicked.connect(grink)
    
    # window not containing the uip:
    window_2 = QtGui.QWidget()
    textedit_2 = QtGui.QTextEdit()
    shrink_btn_2 = QtGui.QPushButton('Shrink')
    grow_btn_2   = QtGui.QPushButton('Grow')
    
    lay_2 = QtGui.QVBoxLayout()
    lay_2.addWidget(textedit_2)
    lay_2.addWidget(shrink_btn_2)
    lay_2.addWidget(grow_btn_2)
    window_2.setLayout(lay_2)
    
    shrink_btn_2.clicked.connect(uip_1.shrink)
    #shrink_btn_2.clicked.connect(uip_3.shrink)
    grow_btn_2.clicked.connect(uip_1.grow)
    #grow_btn_2.clicked.connect(uip_3.grow)
    
    
    
    window_1.show()
    window_2.show()
    #uip_3.show()
    
    qapp.exec_()
    

if __name__ == "__main__":
    main()

