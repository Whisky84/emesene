# -*- coding: utf-8 -*-
'''This module contains the Picture Handler class'''

from PyQt4          import QtGui
from PyQt4.QtCore   import Qt

from gui   import base


class PictureHandler (base.PictureHandler): 
    '''This is a class provides to the core the means to manipulate
    images through the toolkit used, if possible, without having to
    to depend on third-party stuff when unnecessary'''
    NAME = 'PictureHandler'
    DESCRIPTION = 'An object to manipulate images using ' \
                   'gui toolkit\'s facilities'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''
    
    def __init__(self, source_filename=None):
        '''Constructor'''
        base.PictureHandler.__init__(self, source_filename)
        self._is_animated = False
        
        if not source_filename:
            return
        
        file_format = QtGui.QImageReader(source_filename).format()
        if file_format in ['gif', 'pbm', 'pgm']:
            self._is_animated = True
        else:
            self._qimage = QtGui.QImage(source_filename)
        
    
    
    def _resize(self, new_size):
        '''Resizes to new_size the given avatar pix. Overrides base's 
        class abstract method.'''
        self._qimage = self._qimage.scaled(new_size, new_size, 
                                               Qt.IgnoreAspectRatio, 
                                               Qt.SmoothTransformation)
        
            
    def _save(self, dest_filename):
        '''Saves the image to disk'''
        self._qimage.save(dest_filename, 'png')
        self._source_filename = dest_filename
        
        
    def can_handle(self):
        '''Returns true if the image is an animation'''
        return not self._is_animated
        
    @staticmethod
    def from_toolkit(pix):
        '''Builds a PictureHandler object from a pix object, whose type
        is gtk.gdk.Pixbuf.'''
        picturehandler = PictureHandler()
        picturehandler._qimage = QtGui.QImage(pix)
        return picturehandler
