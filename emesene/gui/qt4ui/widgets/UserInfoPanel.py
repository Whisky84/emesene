# -*- coding: utf-8 -*-

'''This module contains the UserInfoPanel class.'''

import PyQt4.QtCore     as QtCore
import PyQt4.QtGui      as QtGui
from PyQt4.QtCore   import Qt


import gui
from gui.qt4ui import Utils


class UserInfoPanel (QtGui.QWidget):
    '''This class represents a label widget showing
    other contact's info in a conversation window'''
    # pylint: disable=W0612
    NAME = 'MainPage'
    DESCRIPTION = 'The widget used to to display contact\'s info in ' \
                  'the conversation widget'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''
    # pylint: enable=W0612
    
    def __init__(self, parent=None):
        '''Constructor'''
        QtGui.QWidget.__init__(self, parent)
        
        self._account = ''
        self._emblem_lbl        = QtGui.QLabel()
        self._display_name_lbl  = QtGui.QLabel()
        self._message_lbl       = QtGui.QLabel()
        self._timeline          = QtCore.QTimeLine()
        self._blur              = QtGui.QGraphicsBlurEffect()
        
        lay = QtGui.QGridLayout()
        lay.addWidget(self._emblem_lbl,         0, 0)
        lay.addWidget(self._display_name_lbl,   0, 1)
        lay.addWidget(self._message_lbl,        1, 1)
        lay.setColumnStretch(0, 0)
        lay.setColumnStretch(1, 1)
        self.setLayout(lay)
        
        self._display_name_lbl.setTextFormat(Qt.RichText)
        self._message_lbl.setTextFormat(Qt.RichText)
        self._timeline.setFrameRange(0, 100)
        self._blur.setBlurRadius(0)
        self.setGraphicsEffect(self._blur)
        
        self._timeline.frameChanged.connect(self._update_size)
        

    def set_all(self, status, nick, message, account):
        '''Updates the infos shown in the panel'''
        self._account = account
        icon          = gui.theme.get_image_theme().status_icons[status]
        self.set_icon(icon)
        self.set_nick(nick)
        self.set_message(message)
        
        
    def set_icon(self, icon):
        '''Updates the icon'''
        pixmap = QtGui.QPixmap(icon)
        self._emblem_lbl.setPixmap(pixmap)
        
        
    def set_nick(self, nick):
        '''Updates the nick'''
        nick = Utils.escape(nick)
        nick = Utils.parse_emotes(unicode(nick))
        nick = nick + (u'&nbsp;&nbsp;&nbsp;&nbsp;[%s]' % self._account)
        self._display_name_lbl.setText(nick)
        
        
    def set_message(self, message):
        '''Updates the message'''
        message = Utils.escape(message)
        message = Utils.parse_emotes(unicode(message))
        self._message_lbl.setText(message)
        
        
    def _update_size(self, step_n):
        size_hint  = QtGui.QWidget.sizeHint(self)
        new_height = step_n / 100. * size_hint.height() 
        
        QtGui.QWidget.resize(self, size_hint.width(), new_height)
        self.setMinimumHeight(new_height)
        self.setMaximumHeight(new_height)
        self._blur.setBlurRadius(100 - step_n)
        
        if self.height() == 0:
            self.hide()
        else:
            self.show()
        
                        
    def shrink(self):
        self._timeline.setDirection(QtCore.QTimeLine.Backward)
        self._timeline.start()
        
        
    def grow(self):
        self._timeline.setDirection(QtCore.QTimeLine.Forward)
        self._timeline.start()
        
        
        
