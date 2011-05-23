# -*- coding: utf-8 -*-

'''This module contains the ContactList class'''
                            
import PyQt4.QtGui      as QtGui
import PyQt4.QtCore     as QtCore

import extension
import gui

from gui.qt4ui.widgets import ContactListDelegate
from gui.qt4ui.widgets import ContactListModel
from gui.qt4ui.widgets import ContactListProxy
from gui.qt4ui.widgets.ContactListModel import Role


class ContactList (gui.ContactList, QtGui.QTreeView):
    '''A Contactlist Widget'''
    # pylint: disable=W0612
    NAME = 'MainPage'
    DESCRIPTION = 'The widget used to to display the contact list'
    AUTHOR = 'Gabriele Whisky Visconti'
    WEBSITE = ''
    # pylint: enable=W0612
    
    new_conversation_requested = QtCore.pyqtSignal(basestring)
    
    def __init__(self, session, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        dialog = extension.get_default('dialog')
        # We need a model *before* callig gui.ContactList's costructor!!
        self._model = ContactListModel.ContactListModel(session.config, self)
        self._pmodel = ContactListProxy.ContactListProxy(session.config, self)
        gui.ContactList.__init__(self, session, dialog)
        
        self._pmodel.setSourceModel(self._model)
        self.setModel(self._pmodel)
        delegate = ContactListDelegate.ContactListDelegate(session, self)
        delegate.set_nick_formatter(self.format_nick)
        self.setItemDelegate(delegate)
        self.setAnimated(True)
        self.setRootIsDecorated(False)
        self.setHeaderHidden(True)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setSortingEnabled(True)
        self.viewport().setStyleSheet( "QWidget{                    \
            background-attachment: fixed;           \
            background-origin: content;             \
            background-position: bottom left;       \
            background-repeat: no-repeat;           \
            background-clip: content;               \
            background-image: url(amsn2/ui/front_ends/kde4/background.png);}" )
            # background-color: rgb(178, 216, 255);   \
        #self.verticalScrollBar().setStyleSheet("QScrollBar:vertical{}")
        self.setIndentation(0)
        self.doubleClicked.connect(self._on_item_double_clicked)

    
    # [START] -------------------- GUI.CONTACTLIST_OVERRIDE
    
    def add_contact(self, contact, group=None):
        '''Add a contact to the view. Resent to model.'''
        self._model.add_contact(contact, group)
        
    def update_contact(self, contact):
        '''Update a contact in the view. Resent to model'''
        self._model.update_contact(contact)
        
    def remove_contact(self, contact, group=None):
        '''remove a contact from the specified group, if group is None
        then remove him from all groups'''
        print 'remove contact: [%s,%s]' % (contact, group)
        
    def add_group(self, group):
        '''Add a group to the view. Resent to model.'''
        self._model.add_group(group)
    
    def fill(self, clear=True): # emesene's
        '''Fill the contact list. Resent to model'''
        print "redirecting to base's fill"
        gui.ContactList.fill(self, clear)
        
    def get_contact_selected(self):
        print '*** GET CONTACT SELECTED ***'
        idx_list = self.selectedIndexes()
        if len(idx_list) != 1 :
            print 'Returning None because of len!=1'
            return None
        index = idx_list[0]
        print index
        print ' --> (%d, %d)[%s]' % (index.row(), index.column(), index.isValid())
        if not index.parent().isValid():
            print "Returning None because of group."
            return None
        print 'Returning %s' % self._pmodel.data(index, Role.DataRole).toPyObject()
        return self._pmodel.data(index, Role.DataRole).toPyObject()
        
    def get_group_selected(self):
        idx_list = self.selectedIndexes()
        index = idx_list[0]
        print '*** GET GROUP SELECTED ***'
        print index
        print ' --> (%d, %d)[%s]' % (index.row(), index.column(), index.isValid())
        if len(idx_list) > 1 :
            print 'Returning None because of len>1'
            return None
        if index.parent().isValid():
            print "Returning None because of contact."
            return None
        print 'Returning %s' % self._pmodel.data(index, Role.DataRole).toPyObject()
        return self._pmodel.data(index, Role.DataRole).toPyObject()
    
    def clear(self):
        '''Clears the contact list. Resent to model.'''
        self._model.clear()
        return True
        
    def refilter(self):
        pass
        
    # [END] -------------------- GUI.CONTACTLIST_OVERRIDE
        

    def _on_item_double_clicked(self, index):
        '''Slot called when the user double clicks a contact. requests
        a new conversation'''
        print self._pmodel.data(index, Role.UidRole).toPyObject()
        if index.parent().isValid():
            contact = self._pmodel.data(index, Role.DataRole).toPyObject()
            self.new_conversation_requested.emit(str(contact.account))
        else:
            group = self._pmodel.data(index, Role.DataRole).toPyObject()
            if not group:
                return
            if self.isExpanded(index):
                print 'Expanded: %s' % group.name
                self.on_group_expanded(group)
            else:
                print 'Collapsed: %s' % group.name
                self.on_group_collapsed(group)
            





