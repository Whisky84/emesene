# -*- coding: utf-8 -*-

'''This module contains menu widgets' classes'''

import PyQt4.QtGui      as QtGui

import extension

ICON = QtGui.QIcon.fromTheme

class MainMenu(QtGui.QMenuBar):
    '''A widget that represents the main menu of the main window'''
    # pylint: disable=W0612
    NAME = 'Main Menu'
    DESCRIPTION = 'The Main Menu of the main window'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''
    # pylint: enable=W0612
    

    def __init__(self, handlers, config, parent=None):
        '''Constructor'''
        QtGui.QMenuBar.__init__(self, parent)
        print 'Main Menu'
#        #
#        self.addAction('Ciao')
#        self.addAction('Come')
#        self.addAction('Stai')
#        self.addAction('?')
#        return
#        #
        
        self._handlers = handlers
        
        file_menu_cls       = extension.get_default('menu file')
        actions_menu_cls    = extension.get_default('menu actions')
        options_menu_cls    = extension.get_default('menu options')
        help_menu_cls       = extension.get_default('menu help')
        
        self.file_menu    =    file_menu_cls(self._handlers.file_handler)
        self.actions_menu = actions_menu_cls(self._handlers.actions_handler)
        self.options_menu = options_menu_cls(self._handlers.options_handler, 
                                             config)
        self.help_menu    =    help_menu_cls(self._handlers.help_handler)
        
        self.addMenu(self.file_menu)
        self.addMenu(self.actions_menu)
        self.addMenu(self.options_menu)
        self.addMenu(self.help_menu)
        
        
        
        
        
class FileMenu(QtGui.QMenu):
    '''A widget that represents the File popup menu located on the main menu'''

    def __init__(self, handler, parent=None):
        '''
        constructor

        handler -- e3common.Handler.FileHandler
        '''
        QtGui.QMenu.__init__(self, 'File', parent)
        print 'Menu Bar'
        self._handler = handler
        status_menu_cls = extension.get_default('menu status')
        
        self.status_menu = status_menu_cls(handler.on_status_selected)
        disconnect_action = QtGui.QAction(ICON('network-disconnect'),
                                          'Disconnect', self)
        quit_action = QtGui.QAction(ICON('application-exit'),'Quit', self)
        
        self.addMenu(self.status_menu)
        self.addAction(disconnect_action)
        self.addSeparator()
        self.addAction(quit_action)
        
        disconnect_action.triggered.connect(
                        lambda *args: self._handler.on_disconnect_selected())
        
        quit_action.triggered.connect(
                        lambda *args: self._handler.on_quit_selected())





class ActionsMenu(QtGui.QMenu):
    '''A widget that represents the Actions 
    popup menu located on the main menu'''

    def __init__(self, handler, parent=None):
        '''
        constructor

        handler -- e3common.Handler.ActionsHandler
        '''
        QtGui.QMenu.__init__(self, 'Actions', parent)
        print 'Actions Menu'
        self._handler = handler

        contacts_menu_cls = extension.get_default('menu contact')
        group_menu_cls = extension.get_default('menu group')
        profile_menu_cls = extension.get_default('menu profile')

        self.contact_menu    = contacts_menu_cls(self._handler.contact_handler)
        self.group_menu      = group_menu_cls(self._handler.group_handler)
        self.my_profile_menu = profile_menu_cls(
                                            self._handler.my_account_handler)

        self.addMenu(self.contact_menu)
        self.addMenu(self.group_menu)
        self.addMenu(self.my_profile_menu)





class OptionsMenu(QtGui.QMenu):
    '''A widget that represents the Options 
    popup menu located on the main menu'''

    def __init__(self, handler, config, parent=None):
        '''
        constructor

        handler -- e3common.Handler.OptionsHandler
        '''
        QtGui.QMenu.__init__(self, 'Options', parent)
        print 'Options Menu'
        self.handler = handler

        # "Show" submenu
        self.show_menu = QtGui.QMenu('Show...')

        show_offline =      QtGui.QAction('Show _offline contacts', self)
        show_empty_groups = QtGui.QAction('Show _empty groups', self)
        show_blocked =      QtGui.QAction('Show _blocked contacts', self)
        show_offline.setChecked(config.b_show_offline)
        show_empty_groups.setChecked(config.b_show_empty_groups)
        show_blocked.setChecked(config.b_show_blocked)
        
        self.show_menu.addAction(show_offline)
        self.show_menu.addAction(show_empty_groups)
        self.show_menu.addAction(show_blocked)
        # ----
        
        order_action_group = QtGui.QActionGroup(self)
        by_status = QtGui.QAction('Order by _status', self)
        by_group  = QtGui.QAction('Order by _group', self)
        order_action_group.addAction(by_status)
        order_action_group.addAction(by_group)
        by_group.setChecked(config.b_order_by_group)
        by_status.setChecked(not config.b_order_by_group)

        group_offline = QtGui.QAction('G_roup offline contacts', self)
        preferences = QtGui.QAction(ICON('preferences-other'),
                                    'Preferences...', self)
        group_offline.setChecked(config.b_group_offline)
        
        self.addAction(by_status)
        self.addAction(by_group)
        self.addSeparator()
        self.addMenu(self.show_menu)
        self.addAction(group_offline)
        self.addSeparator()
        self.addAction(preferences)
        
        preferences.triggered.connect(
            lambda *args: self.handler.on_preferences_selected())

        by_status.toggled.connect(
            lambda *args: self.handler.on_order_by_status_toggled(
                self.by_status.isChecked()))
        by_group.toggled.connect(
            lambda *args: self.handler.on_order_by_group_toggled(
                self.by_group.isChecked()))
        show_empty_groups.toggled.connect(
            lambda *args: self.handler.on_show_empty_groups_toggled(
                self.show_empty_groups.isChecked()))
        show_offline.toggled.connect(
            lambda *args: self.handler.on_show_offline_toggled(
                self.show_offline.isChecked()))
        group_offline.toggled.connect(
            lambda *args: self.handler.on_group_offline_toggled(
                self.group_offline.isChecked()))
        show_blocked.toggled.connect(
            lambda *args: self.handler.on_show_blocked_toggled(
                self.show_blocked.isChecked()))



        

class HelpMenu(QtGui.QMenu):
    '''A widget that represents the Help popup menu located on the main menu'''

    def __init__(self, handler, parent=None):
        '''
        constructor

        handler -- e3common.Handler.HelpHandler
        '''
        QtGui.QMenu.__init__(self, 'Help', parent)
        print 'Help Menu'
        self.handler = handler

        self.website = QtGui.QAction('_Website', self)
        self.about = QtGui.QAction('About', self)
        self.debug = QtGui.QAction('Debug', self)
        
        self.addAction(self.website)
        self.addAction(self.about)
        self.addAction(self.debug)  
        
        self.website.triggered.connect(
            lambda *args: self.handler.on_website_selected())
        
        self.about.triggered.connect(
            lambda *args: self.handler.on_about_selected())
       
        self.debug.triggered.connect(
            lambda *args: self.handler.on_debug_selected())

            

        
        
        
        
        
        
        
        
