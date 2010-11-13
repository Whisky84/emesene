# -*- coding: utf-8 -*-

''' This module contains classes to represent the login page '''

from PyQt4          import QtGui
from PyQt4          import QtCore
from PyQt4.QtCore   import Qt

import extension
import e3
import gui



class ConnectingPage(QtGui.QWidget):
    ''' The page shown during the connection process'''
    # pylint: disable=W0612
    NAME = 'ConnectingPage'
    DESCRIPTION = 'The widget displayed while connecting'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''
    # pylint: enable=W0612
    
    def __init__(self, on_cancel_login, avatar_path, config, parent=None):
        '''Constructor'''
        QtGui.QWidget.__init__(self, parent)
        
        self._on_cancel_login = on_cancel_login
        self._avatar_path = avatar_path
        self._config = config
        self._reconnect_txt = u'Reconnecting in %d seconds'
        self._reconnect_time = None
        self._timer = QtCore.QTimer(self)
        
        self._widget_d = {}
        self._setup_ui()
        self.clear_connect()
        
        
    def _setup_ui(self):
        '''Instantiates the widgets, and sets the layout'''
        widget_d = self._widget_d
        avatar_cls = extension.get_default('avatar')
        widget_d['display_pic']  = avatar_cls(default_pic=gui.theme.logo,
                                             clickable=False)
        widget_d['label']        = QtGui.QLabel()
        widget_d['progress_bar'] = QtGui.QProgressBar()
        widget_d['cancel_btn']   = QtGui.QPushButton('Cancel login')
        
        lay = QtGui.QVBoxLayout()
        lay.addSpacing(40)
        lay.addWidget(widget_d['display_pic'], 0, Qt.AlignCenter)
        lay.addStretch()
        lay.addWidget(widget_d['label'], 0, Qt.AlignCenter)
        lay.addWidget(widget_d['progress_bar'], 0, Qt.AlignCenter)
        lay.addSpacing(35)
        lay.addStretch()
        lay.addWidget(widget_d['cancel_btn'], 0, Qt.AlignCenter)
        lay.addSpacing(45)
        

        hor_lay = QtGui.QHBoxLayout()
        hor_lay.addStretch()
        hor_lay.addSpacing(40)
        hor_lay.addLayout(lay)
        hor_lay.addSpacing(40)
        hor_lay.addStretch()
        self.setLayout(hor_lay)
        
        widget_d['display_pic' ].set_display_pic_from_file(self._avatar_path)
        widget_d['progress_bar'].setMinimum(0)
        widget_d['progress_bar'].setMaximum(0)
        widget_d['progress_bar'].setMinimumWidth(220)
        
    
    def clear_connect(self):
        self._timer.stop()
        self._widget_d['label'].setText(u'Please wait while signing in...')
        self._widget_d['cancel_btn'].setText(u'Cancel login')
        try:
            self._widget_d['cancel_btn'].clicked.disconnect()
        except TypeError:
            pass
        self._widget_d['cancel_btn'].clicked.connect(self._on_cancel_login)
        
        
    def on_reconnect(self, callback, account, session_id,
                     proxy, use_http, service):
        print callback
        self._widget_d['label'].setText(self._reconnect_txt % 30)
        self._widget_d['cancel_btn'].setText(u'Reconnect now')
        self._widget_d['cancel_btn'].clicked.disconnect()
        self._widget_d['cancel_btn'].clicked.connect(self._on_reconnect_now)
        
        self._reconnect_time = 30
        self._timer.timeout.connect(
            lambda: self._on_timer_timeout(callback, account, session_id, 
                                           proxy, use_http, service))
        self._timer.start(1000)
        
        
    def _on_timer_timeout(self, callback, account, session_id, 
                               proxy, use_http, service):
        self._reconnect_time -= 1
        
        if self._reconnect_time <= 0:
            self._timer.stop()
            callback(account, session_id, proxy, use_http,
                     service[0], service[1], on_reconnect=True)
        else:    
            self._widget_d['label'].setText(self._reconnect_txt % 
                                            self._reconnect_time)
        
                         
    def _on_reconnect_now(self):
        self._reconnect_time = -1
        
        

