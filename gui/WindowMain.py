import globals
from gui.WindowSettings import WindowSettings
from gui.widgets import PathList
from utilities import log

import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QFileDialog, QGridLayout, QTextBrowser
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer


class WindowMain(QWidget):

    def __init__(self, managers_collection, settings, delay=3000):
        super().__init__()

        self.managers_collection = managers_collection
        self.managers = managers_collection.managers
        self.delay = delay
        self.time_last_managed = 0
        self.manage_files = False

        self.settings_window = WindowSettings(self.managers_collection, settings)

        self.paths_qlist = PathList(self)

        self._start_manager_timer(delay)

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('File Butler')
        grid = QGridLayout()

        grid.addWidget(self._button_manager())
        grid.addWidget(self._button_settings())
        grid.addWidget(self._button_path_selector())
        grid.addWidget(self.paths_qlist)
        grid.addWidget(self._button_quit())
        grid.addWidget(self._create_prompt())

        globals.prompt_ref = self.prompt

        self.setLayout(grid)
        self.show()

    def _button_manager(self):
        btn = QPushButton('Toggle File Manager', self)
        btn.setToolTip('Toggles the file manager on / off')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        btn.clicked.connect(self._toggle_managers)
        return btn

    def _button_settings(self):
        btn = QPushButton('Settings', self)
        btn.setToolTip('Choose paths to manage, directories to store files in, etc ...')
        btn.resize(btn.sizeHint())
        btn.move(100, 20)
        btn.clicked.connect(self._open_settings)
        return btn

    def _button_path_selector(self):
        btn = QPushButton('Select path for File Butler', self)
        btn.setToolTip('Allows you to choose which directory file butler should keep tidy')
        btn.resize(btn.sizeHint())
        btn.move(200, 50)
        btn.clicked.connect(self._scan_path_selector)
        return btn

    def _button_quit(self):
        btn = QPushButton('Quit', self)
        btn.setToolTip('Quit File Butler')
        btn.clicked.connect(self.quit_program)
        btn.resize(btn.sizeHint())
        btn.move(100, 100)
        return btn

    def _create_prompt(self):
        self.prompt = QTextBrowser(self)
        self.prompt.resize(100, 20)
        self.prompt.setStyleSheet("background-color: lightgray;")
        return self.prompt

    def _scan_path_selector(self):
        new_path = str(QFileDialog.getExistingDirectory(self, "Add Path To Butler", 'C:/ButlerTest/'))
        if new_path not in self.settings_window.settings.PATHS_TO_SCAN:
            self.settings_window.settings.add_path_to_scan(new_path, self.paths_qlist)

    def _open_settings(self):
        self.settings_window.show()

    def _run_managers_copy(self):
        if self.manage_files:
            if self.paths_qlist.count() > 0:
                for manager in self.managers:
                    manager.manage_files(self.settings_window.settings.PATHS_TO_SCAN)
                log('Files managed!')
            else:
                log('Path list is empty, set path for file butler to check!')

    def _toggle_managers(self):
        self.manage_files = not self.manage_files
        log(f'Managers toggled to {self.manage_files}')

    def _start_manager_timer(self, delay):
        self._timer = QTimer()
        self._timer.setSingleShot(False)
        self._timer.timeout.connect(self._run_managers_copy)
        self._timer.start(delay)

    def prompt_text(self, string):
        self.prompt.setText(string)

    def quit_program(self):
        log('Closing File Butler. Goodbye!')
        QApplication.instance().quit()


def create_GUI(file_managers, settings):
    log('Starting main window, GUI main loop')
    app = QApplication(sys.argv)
    main_window = WindowMain(file_managers, settings)
    sys.exit(app.exec_())
    return main_window




