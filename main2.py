from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.dialog.dialog import MDDialog
from kivymd.uix.button.button import MDFlatButton
import logging
from jnius import cast
from jnius import autoclass
#from android import mActivity, api_version
if platform == "android":
    from jnius import cast
    from jnius import autoclass
    #from android import mActivity, api_version



KV = '''
MDBoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: "MDFileManager"
        left_action_items: [['menu', lambda x: None]]
        elevation: 10

    MDFloatLayout:

        MDRoundFlatIconButton:
            text: "Open manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .6}
            on_release: app.file_manager_open()
'''


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

    def build(self):
        #self._show_validation_dialog()
        self.permissions_external_storage()
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


    def permissions_external_storage(self, *args):                  
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE,Permission.READ_MEDIA_IMAGES,
                                 Permission.MANAGE_EXTERNAL_STORAGE])
            logging.info("platform android ok")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            logging.info("pyactivity ok")
            #Environment = autoclass("android.os.Environment")
            logging.info("environment ok")
            Intent = autoclass("android.content.Intent")
            logging.info("intent ok")
            Settings = autoclass("android.provider.Settings")
            logging.info("settings ok")
            Uri = autoclass("android.net.Uri")
            logging.info("uri ok")
            """
            if api_version > 29:
                logging.info("get api version >29 ok")
                # If you have access to the external storage, do whatever you need
                if Environment:
                    logging.info("permission external storage environment ok")
                    # If you don't have access, launch a new activity to show the user the system's dialog
                    # to allow access to the external storage
                    pass
            else:
            """
            try:
                activity = mActivity.getApplicationContext()
                logging.info("get app context ok")
                uri = Uri.parse("package:" + activity.getPackageName())
                logging.info("uri ok")
                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri)
                logging.info("intent ok ok")
                currentActivity = cast(
                "android.app.Activity", PythonActivity.mActivity
                )
                currentActivity.startActivityForResult(intent, 101)
            except:
                logging.info("except ok")
                intent = Intent()
                intent.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
                logging.info("action manage all files access permission ok")
                currentActivity = cast(
                "android.app.Activity", PythonActivity.mActivity
                )
                currentActivity.startActivityForResult(intent, 101)
                #self.show_permission_popup.dismiss()
"""
    def _show_validation_dialog(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE,Permission.READ_MEDIA_IMAGES])
            Environment = autoclass("android.os.Environment")
            logging.info("show validation dialog ok")
            if not Environment:
                logging.info("show validation dialog environment ok")
                self.show_permission_popup = MDDialog(
                    title="Alert",
                    text="Permission to access your device's internal storage and files..",
                    size_hint=(0.6, 0.5),
                    buttons=[
                        MDFlatButton(
                            text="Allow", on_press=self.permissions_external_storage
                        ),
                        MDFlatButton(
                            text="Decline",
                            on_release=self._close_validation_dialog,
                        ),
                    ],
                )
                self.show_permission_popup.open()

    def _close_validation_dialog(self, widget):
        #Close input fields validation dialog
        self.show_permission_popup.dismiss()
"""    
Example().run()
