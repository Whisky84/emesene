# -*- coding: utf-8 -*-

'''a module that defines the api of objects that display dialogs'''


from PyQt4  import QtGui
from PyQt4  import QtCore
from PyQt4.QtCore  import Qt

import gui
import extension

from gui.qt4ui import widgets



class Dialog(object):
    '''a class full of static methods to handle dialogs, dont instantiate it'''
    NAME = 'Dialog'
    DESCRIPTION = 'Class to show all the dialogs of the application'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''


#    @classmethod
#    def new_window(cls, title, response_cb=None, *args):
#        '''build a window with the default values and connect the common
#        signals, return the window'''
#
#        window = QtGui.QDialog()
#        window.set_title(title)
#        window.set_role("dialog")
#        window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
#        window.set_default_size(150, 100)
#        window.set_position(gtk.WIN_POS_CENTER)
#        window.set_border_width(8)
#        window.set_icon(utils.safe_gtk_image_load(gui.theme.logo).get_pixbuf())
#
#        vbox = gtk.VBox(spacing=4)
#        hbox = gtk.HBox(spacing=4)
#        bbox = gtk.HButtonBox()
#        bbox.set_spacing(4)
#        bbox.set_layout(gtk.BUTTONBOX_END)
#
#        vbox.pack_start(hbox, True, True)
#        vbox.pack_start(bbox, False)
#
#        window.add(vbox)
#
#        setattr(window, 'vbox', vbox)
#        setattr(window, 'hbox', hbox)
#        setattr(window, 'bbox', bbox)
#
#        args = list(args)
#        args.insert(0, stock.CLOSE)
#        window.connect('delete-event', cls.close_cb, window,
#            response_cb, *args)
#
#        vbox.show_all()
#
#        return window

    @classmethod
    def add_contact(cls, groups, group_selected, response_cb,
        title="Add user"):
        '''show a dialog asking for an user address, and (optional)
        the group(s) where the user should be added, the response callback
        receives the response type (stock.ADD, stock.CANCEL or stock.CLOSE)
        the account and a tuple of group names where the user should be
        added (give a empty tuple if you don't implement this feature,
        the controls are made by the callback, you just ask for the email,
        don't make any control, you are just implementing a GUI! :P'''
        print response_cb
        dialog      = OkCancelDialog()
        text_label  = QtGui.QLabel("E-mail:")
        text_edit   = QtGui.QLineEdit()
        group_label = QtGui.QLabel("Group:")
        group_combo = QtGui.QComboBox()
        
        lay = QtGui.QGridLayout()
        lay.addWidget(text_label,   0, 0)
        lay.addWidget(text_edit,    0, 1)
        lay.addWidget(group_label,  1, 0)
        lay.addWidget(group_combo,  1, 1)
        dialog.setLayout(lay)
        
        
        dialog.setWindowTitle(title)
        text_label.setAlignment(Qt.AlignRight |
                                Qt.AlignVCenter)
        group_label.setAlignment(Qt.AlignRight |
                                 Qt.AlignVCenter)
        dialog.setMinimumWidth(300)
        
        print groups
        groups = list(groups)
        print groups
        groups.sort()
        
        group_combo.addItem('<i>No Group</i>', '')
        for group in groups:
            group_combo.addItem(group.name, group.name)
        
        response = dialog.exec_()
        
        if response == QtGui.QDialog.Accepted:
            response = gui.stock.ACCEPT
        elif response == QtGui.QDialog.Rejected:
            response = gui.stock.CANCEL
        print response
        
        email = unicode(text_edit.text())
        group = group_combo.itemData(group_combo.currentIndex()).toPyObject()
        print '[%s,%s]' % (email, group)
        response_cb(response, email, group )
        
        
    @classmethod
    def add_group(cls, response_cb, title="Add group"):
        '''show a dialog asking for a group name, the response callback
        receives the response (stock.ADD, stock.CANCEL, stock.CLOSE)
        and the name of the group, the control for a valid group is made
        on the controller, so if the group is empty you just call the
        callback, to make a unified behaviour, and also, to only implement
        GUI logic on your code and not client logic
        cb args: response, group_name'''
        print response_cb
        dialog = OkCancelDialog()
        group_label = QtGui.QLabel('New group\'s name:')
        group_edit  = QtGui.QLineEdit()
        
        lay = QtGui.QHBoxLayout()
        lay.addWidget(group_label)
        lay.addWidget(group_edit)
        dialog.setLayout(lay)
        
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(380)
        
        response = dialog.exec_()
        
        if response == QtGui.QDialog.Accepted:
            response = gui.stock.ACCEPT
        elif response == QtGui.QDialog.Rejected:
            response = gui.stock.CANCEL
        print response
        
        group_name = unicode(group_edit.text())
        
        response_cb(response, group_name)
        
    @classmethod
    def crop_image(cls, response_cb, filename, title='Select image area'):
        dialog = OkCancelDialog(expanding=True)
        
        # Actions
        act_dict = {}
        act_dict['rotate_left' ] = QtGui.QAction('Rotate Left'    , dialog)
        act_dict['rotate_right'] = QtGui.QAction('Rotate right'   , dialog)
        act_dict['fit_zoom']     = QtGui.QAction('Zoom to fit'    , dialog)
        act_dict['fit_zoom']     = QtGui.QAction('Zoom to fit'    , dialog)
        act_dict['reset_zoom']   = QtGui.QAction('Reset zoom'     , dialog)
        act_dict['select_all']   = QtGui.QAction('Select All'     , dialog)
        act_dict['select_unsc']  = QtGui.QAction('Select Unscaled', dialog)
        
        # widgets
        toolbar = QtGui.QToolBar()
        scroll_area = QtGui.QScrollArea()
        area_selector = extension.get_and_instantiate(
                                'image area selector', QtGui.QPixmap(filename))
        
        # layout
        lay = QtGui.QVBoxLayout()
        lay.addWidget(toolbar)
        lay.addWidget(scroll_area)
        dialog.setLayout(lay)
        
        # widget setup
        dialog.setWindowTitle(title)
        toolbar.addAction(act_dict['rotate_left'])
        toolbar.addAction(act_dict['rotate_right'])
        toolbar.addSeparator()
        toolbar.addAction(act_dict['fit_zoom'])
        toolbar.addAction(act_dict['reset_zoom'])
        toolbar.addSeparator()
        toolbar.addAction(act_dict['select_all'])
        toolbar.addAction(act_dict['select_unsc'])
        scroll_area.setWidget(area_selector)
        scroll_area.setWidgetResizable(True)
        
        # Signal connection:
        act_dict['rotate_left'].triggered.connect(area_selector.rotate_left)
        act_dict['rotate_right'].triggered.connect(area_selector.rotate_right)
        act_dict['fit_zoom'].triggered.connect(area_selector.fit_zoom)
        act_dict['reset_zoom'].triggered.connect(
                                            lambda: area_selector.set_zoom(1))
        act_dict['select_all'].triggered.connect(area_selector.select_all)
        act_dict['select_unsc'].triggered.connect(
                                            area_selector.select_unscaled)
                                            
        # test:
        if (False):
            preview = QtGui.QLabel()
            lay.addWidget(preview)
            area_selector.selection_changed.connect(
                lambda: preview.setPixmap(area_selector.get_selected_pixmap()))
            
            zoom_sli = QtGui.QSlider(Qt.Horizontal)
            zoom_sli.setMinimum(1)
            zoom_sli.setMaximum(40)
            zoom_sli.setValue(20)
            zoom_sli.setSingleStep(1)
            lay.addWidget(zoom_sli)
            zoom_sli.valueChanged.connect(
                lambda z:area_selector.set_zoom(z/10.0))
                                            
        # Dialog execution:
        response = dialog.exec_()
        
        if response == QtGui.QDialog.Accepted:
            response = gui.stock.ACCEPT
        elif response == QtGui.QDialog.Rejected:
            response = gui.stock.CANCEL
        print response
        
        selected_pixmap = area_selector.get_selected_pixmap()
        
        response_cb(response, selected_pixmap)
        

    @classmethod
    def login_preferences(cls, service, service_host, service_port, 
                          callback, use_http, proxy):
        """
        display the preferences dialog for the login window

        cls -- the dialog class
        service -- the service string identifier (for example 'gtalk')
        callback -- callback to call if the user press accept, call with the
            new values
        use_http -- boolean that indicates if the e3 should use http
            method
        proxy -- a e3.Proxy object
        """
        def on_session_changed(*args):
            service = str(session_cmb.currentText())
            session_id, ext = name_to_ext[service]
            server_host_edit.setText(ext.SERVICES[service]['host'])
            server_port_edit.setText(ext.SERVICES[service]['port'])
            
        def on_use_auth_toggled(is_enabled, is_checked):
            '''called when a check button is toggled, receive a set
            of entries, enable or disable them deppending on the state
            of the check button'''
            auth_settings = (user_lbl, user_edit, pwd_lbl, pwd_edit)
            state = (is_enabled and is_checked)
            for widget in auth_settings:
                widget.setEnabled(state)
                
                
        def on_use_proxy_toggled(is_checked, *args):
            proxy_settings = (host_lbl, proxy_host_edit, port_lbl, 
                              proxy_port_edit, auth_chk)
            print 'upt'
            for widget in proxy_settings:
                widget.setEnabled(is_checked)
            on_use_auth_toggled(is_checked, auth_chk.isChecked())
                    
        def response_cb(response):
            '''called on any response (close, accept, cancel) if accept
            get the new values and call callback with those values'''
            if response == gui.stock.ACCEPT:
                use_http = http_chk.isChecked()
                use_proxy = proxy_chk.isChecked()
                use_auth = auth_chk.isChecked()
                proxy_host = str(proxy_host_edit.text())
                proxy_port = str(proxy_port_edit.text())
                server_host = str(server_host_edit.text())
                server_port = str(server_port_edit.text())
                user = str(user_edit.text())
                passwd = str(pwd_edit.text())

                service = str(session_cmb.currentText())
                session_id, ext = name_to_ext[service]
                print session_id
                callback(use_http, use_proxy, proxy_host, proxy_port, use_auth,
                        user, passwd, session_id, service, server_host, server_port)
            dialog.hide()
                    

        
        dialog           = OkCancelDialog()
        session_lbl      = QtGui.QLabel(_('Session'))
        session_cmb      = QtGui.QComboBox()
        server_host_lbl  = QtGui.QLabel(_('Server'))
        server_host_edit = QtGui.QLineEdit()
        server_port_lbl  = QtGui.QLabel(_('Port'))
        server_port_edit = QtGui.QLineEdit()
        http_chk         = QtGui.QCheckBox(_('Use HTTP method'))
        proxy_chk        = QtGui.QCheckBox(_('Use proxy'))
        host_lbl         = QtGui.QLabel(_('Host'))
        proxy_host_edit  = QtGui.QLineEdit()
        port_lbl         = QtGui.QLabel(_('Port'))
        proxy_port_edit  = QtGui.QLineEdit()
        auth_chk         = QtGui.QCheckBox(_('Use authentication'))
        user_lbl         = QtGui.QLabel(_('User'))
        user_edit        = QtGui.QLineEdit()
        pwd_lbl          = QtGui.QLabel(_('Password'))
        pwd_edit         = QtGui.QLineEdit()
        
        grid_lay = QtGui.QGridLayout()
        grid_lay.setHorizontalSpacing(20)
        grid_lay.setVerticalSpacing(4)
        grid_lay.addWidget(session_lbl, 0, 0)
        grid_lay.addWidget(session_cmb, 0, 2)
        grid_lay.addWidget(server_host_lbl, 1, 0)
        grid_lay.addWidget(server_host_edit, 1, 2)
        grid_lay.addWidget(server_port_lbl, 2, 0)
        grid_lay.addWidget(server_port_edit, 2, 2)
        grid_lay.addWidget(http_chk, 3, 0, 1, -1)
        grid_lay.addWidget(proxy_chk, 4, 0, 1, -1)
        grid_lay.addWidget(host_lbl, 5, 0)
        grid_lay.addWidget(proxy_host_edit, 5, 2)
        grid_lay.addWidget(port_lbl, 6, 0)
        grid_lay.addWidget(proxy_port_edit, 6, 2)
        grid_lay.addWidget(auth_chk, 7, 0, 1, -1)
        grid_lay.addWidget(user_lbl, 8, 0)
        grid_lay.addWidget(user_edit, 8, 2)
        grid_lay.addWidget(pwd_lbl, 9, 0)
        grid_lay.addWidget(pwd_edit, 9, 2)
        dialog.setLayout(grid_lay)
        
        dialog.setWindowTitle('Preferences')
        server_host_edit.setText(service_host)
        server_port_edit.setText(service_port)
        proxy_host_edit.setText(proxy.host or '')
        proxy_port_edit.setText(proxy.port or '')
        user_edit.setText(proxy.user or '')
        pwd_edit.setText(proxy.passwd or '')
        #pwd_edit.setVisible(False)
        http_chk.setChecked(use_http)
        
        index = 0
        count = 0
        name_to_ext = {}
        session_found = False
        default_session_index = 0
        default_session = extension.get_default('session')
        for ext_id, ext in extension.get_extensions('session').iteritems():
            if default_session.NAME == ext.NAME:
                default_session_index = count
            for service_name, service_data in ext.SERVICES.iteritems():
                if service == service_name:
                    index = count
                    server_host_edit.setText(service_data['host'])
                    server_port_edit.setText(service_data['port'])
                    session_found = True
                session_cmb.addItem(service_name)
                name_to_ext[service_name] = (ext_id, ext)
                count += 1
        if session_found:
            session_cmb.setCurrentIndex(index)
        else:
            session_cmb.setCurrentIndex(default_session_index)
            
        
        
        session_cmb.currentIndexChanged.connect(on_session_changed)
        proxy_chk.toggled.connect(on_use_proxy_toggled)
        auth_chk.toggled.connect(lambda checked: 
                        on_use_auth_toggled(auth_chk.isEnabled(), checked))
        
        # putting these there to trigger the slots:
        proxy_chk.setChecked(not proxy.use_proxy)
        proxy_chk.setChecked(proxy.use_proxy)
        auth_chk.setChecked(not proxy.use_auth)
        auth_chk.setChecked(proxy.use_auth)


        dialog.resize(300, 300)
        dialog.show()

        #for widget in proxy_settings:
            #widget.hide()
            
        response = dialog.exec_()
        
        if response == QtGui.QDialog.Accepted:
            response = gui.stock.ACCEPT
        elif response == QtGui.QDialog.Rejected:
            response = gui.stock.CANCEL
        print response
        
        response_cb(response)

        
        
        

        

        

        

        

        

        




class OkCancelDialog (QtGui.QDialog):
    '''Skeleton for a dialog window having Ok and Cancel buttons'''
    def __init__(self, expanding=False, parent=None):
        '''Constructor'''

        QtGui.QDialog.__init__(self, parent)

        self.central_widget = QtGui.QWidget()
        button_box  = QtGui.QDialogButtonBox()

        vlay = QtGui.QVBoxLayout()
        vlay.addWidget(self.central_widget)
        vlay.addSpacing(10)
        vlay.addWidget(button_box)
        if not expanding:
            vlay.addStretch()
        QtGui.QDialog.setLayout(self, vlay)

        button_box.addButton(QtGui.QDialogButtonBox.Cancel)
        button_box.addButton(QtGui.QDialogButtonBox.Ok)

        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self._on_reject)
        
    def _on_accept(self):
        '''Slot called when Ok is clicked'''
        self.done(QtGui.QDialog.Accepted)
        
    def _on_reject(self):
        '''Slot called when Cancel is clicked'''
        self.done(QtGui.QDialog.Rejected)
        
# -------------------- QT_OVERRIDE
        
    def setLayout(self, layout):
        '''Overrides setLayout. Sets the layout directly on
        this dialog's central widget.'''
        # pylint: disable=C0103
        self.central_widget.setLayout(layout)
        
