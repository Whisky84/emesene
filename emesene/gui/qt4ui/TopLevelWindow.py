# -*- coding: utf-8 -*-

''' This module contains the top level window class '''

import PyQt4.QtGui as QtGui

import extension
import gui

class TopLevelWindow (QtGui.QMainWindow):
    ''' Class representing the main window '''
    # pylint: disable=W0612
    NAME = 'TopLevelWindow'
    DESCRIPTION = 'The window used to contain all the _content of emesene'
    AUTHOR = 'Gabriele Whisky Visconti'
    WEBSITE = ''
    # pylint: enable=W0612

    def __init__(self, cb_on_close):
        print 'Creating a new main window!'
        QtGui.QMainWindow.__init__(self)
        self._content_type = 'empty'
        if cb_on_close:
            self._cb_on_close = cb_on_close
        else: # we're the main window
            self._cb_on_close = self.hide
        self._content = None

        self.setObjectName('mainwindow')
        #self.setWindowIcon(KdeGui.KIcon('im-user'))
        self._page_stack = QtGui.QStackedWidget()
        self.setCentralWidget(self._page_stack)
        
    def __del__(self):
        print "adieu TLW!!!"

    def clear(self): #emesene's
        '''remove the content from the main window'''
        pass
        
    def present(self): # emesene's
        '''(Tries to) raise the window'''
        #QtGui.QMainWindow.show(self)
        QtGui.QMainWindow.activateWindow(self)

    def set_location(self, width, height, posx, posy): #emesene's
        '''Sets size and position on screen '''
        self.resize(width, height)
        self.move(posx, posy)

    def get_dimensions(self): #emesene's
        '''
        Returns a tuple containing width, height, x coordinate, y coordinate
        '''
        size = self.size()
        position = self.pos()
        return size.width(), size.height(), position.x(), position.y()

    def go_connect(self, on_cancel_login, avatar_path, config):
        '''does nothing'''
        print "GO CONNECT! ^_^"
        
    def go_conversation(self, session):
        '''Adds a conversation page to the top level window and shows it'''
        print "GO CONVERSATION! ^_^"
        conversation_window_cls = extension.get_default('conversation window')
        conversation_page = conversation_window_cls(session, 
                            on_last_close=self._on_last_tab_close, parent=self)
        self._content_type = 'conversation'
        self._switch_to_page(conversation_page)
        self._content = conversation_page
        self.menuBar().hide()

    # TODO: don't reinstantiate existing pages, or don't preserve old pages.
    def go_login(self, callback, on_preferences_changed, config=None, 
                 config_dir=None, config_path=None, proxy=None, use_http=None, 
                 session_id=None, cancel_clicked=False, no_autologin=False):
               #emesene's
        # pylint: disable=R0913
        '''Adds a login page to the top level window and shows it'''
        print "GO LOGIN! ^_^"
        login_window_cls = extension.get_default('login window')
        login_page = login_window_cls(callback, on_preferences_changed, config,
                                      config_dir, config_path, proxy,use_http, 
                                      session_id, cancel_clicked, no_autologin)
        self._content_type = 'login'
        self._switch_to_page(login_page)
        self.menuBar().hide()

    def go_main(self, session, on_new_conversation,
            on_close, on_disconnect):
        '''Adds a main page (the one with the contact list) to the top
        level window and shows it'''
        print "GO MAIN! ^_^"
        main_window_cls = extension.get_default('main window')
        print main_window_cls
        main_page = main_window_cls(session, on_new_conversation, on_close, 
                                    on_disconnect, self.setMenuBar)
        print main_page
        self._content_type = 'main'
        print self._content_type
        self._switch_to_page(main_page)
        self._setup_main_menu(session, main_page.contact_list, 
                              on_close, on_disconnect)
        print '***'
        
    
    def _get_content(self):
        '''Getter method for propery "content"'''
        print "Getting 'content'"
        return self._content
        
    content = property(_get_content)
    
    def _get_content_type(self):
        ''' Getter method for "content_type" property'''
        return self._content_type

    content_type = property(_get_content_type) #emesene's
    
    def _on_last_tab_close(self):
        '''Slot called when the user closes the last tab in 
        a conversation window'''
        self._cb_on_close()
        self.hide()
        
    def _setup_main_menu(self, session, contact_list, on_close, on_disconnect):
        '''build all the menus used on the client'''
        
        # retrieving classes:
        dialog_cls = extension.get_default('dialog_cls')
        avatar_manager_cls = extension.get_default('avatar manager')
        # creating the avatar manager:
        avatar_manager = None #avatar_manager_cls(self._session)
        
        # create menu handlers
        menu_hnd = gui.base.MenuHandler(session, dialog_cls, 
                                        contact_list, avatar_manager, 
                                        on_disconnect, on_close)

        contact_hnd = gui.base.ContactHandler(session, dialog_cls,
                                              contact_list)
        group_hnd = gui.base.GroupHandler(session, dialog_cls,
                                          contact_list)
        # retrieve menu classes
        main_menu_cls = extension.get_default('main menu')
        contact_menu_cls = extension.get_default('menu contact')
        group_menu_cls = extension.get_default('menu group')
        
        # instantiate menu objects:
        menu = main_menu_cls(menu_hnd, session.config)

#        self._contact_menu = contact_menu_cls(contact_hnd)
#        self._group_menu = group_menu_cls(group_hnd)
#        self._contact_menu.show_all()
#        self._group_menu.show_all()
        self.setMenuBar(menu)

    
    def _switch_to_page(self, page_widget):
        ''' Shows the given page '''
        index = self._page_stack.indexOf(page_widget)
        if index == -1:
            index = self._page_stack.addWidget(page_widget)
        self._page_stack.setCurrentIndex(index)
        self._content = page_widget


# -------------------- QT_OVERRIDE

    def closeEvent(self, event):
        # pylint: disable=C0103
        ''' Overrides QMainWindow's close event '''
        print 'TopLevelWindow\'s close event: %s, %s' % (
                                    self.content, str(self._cb_on_close))
        self._cb_on_close()
        # FIXME: dirty HACK. when we close the conversation window, 
        # self._cb_on_close closes each conversation tab without checking 
        # if it isclosing the last tab, so _on_last_tab_close doesn't get 
        #called and the conversation window remains opened and empty.
        if str(self._cb_on_close).find(
                'Controller._on_conversation_window_close') > -1:
            self.hide()
        event.ignore()
        
