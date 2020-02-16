from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget, QCheckBox, QTextBrowser, QPushButton, QFileDialog,\
    QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from utilities import log
import globals


class PathList(QListWidget):

    def __init__(self, parent):
        super(PathList, self).__init__(parent)
        for path in globals.settings.PATHS_TO_SCAN:
            self.addItem(path)

    def paths(self):
        paths = []
        if self.count() > 0:
            for i in range(self.count()):
                paths.append(self.item(i).text())
        return paths

    def add_path(self, new_path):
        new_item = QListWidgetItem(new_path, self)
        self.addItem(new_item)
        log(f'added path: {new_path}')
        globals.settings.save_settings()


class ManagerPathSetter(QWidget):
    def __init__(self, parent, settings, manager):
        super(QWidget, self).__init__(parent)
        self.manager = manager
        self.type = manager.type
        self.settings = settings

        self.initUI()

    def initUI(self):
        self.resize(600, 50)
        hbox = QHBoxLayout()
        inner_vbox1 = QVBoxLayout()
        inner_vbox2 = QVBoxLayout()
        self._create_checkbox()
        self._create_textbox()
        self._create_button_path_selector()
        self._create_button_path_discarder()
        self._create_frame()
        self._create_label()

        inner_vbox1.addWidget(self.label)
        inner_vbox1.addWidget(self.textbox)

        inner_vbox2.addWidget(self.button_browse)
        inner_vbox2.addWidget(self.button_discard)

        hbox.addLayout(inner_vbox1)
        hbox.addLayout(inner_vbox2)
        hbox.addWidget(self.checkbox)
        hbox.addWidget(self.frame)
        self.setLayout(hbox)

    def _create_checkbox(self):
        self.checkbox = QCheckBox("Enable", self)
        state = getattr(globals.settings, self.checkbox_attribute_name())
        self.checkbox.setChecked(state)
        self.checkbox.resize(15, 15)
        self.checkbox.stateChanged.connect(self._checkbox_change_manager_state)

    def _create_textbox(self):
        self.textbox = QTextBrowser(self)
        self.textbox.resize(100, 20)
        self.textbox.setStyleSheet("background-color: lightgray;")
        self.textbox.setText(getattr(globals.settings, self.type.upper() + '_PATH'))

    def _create_button_path_selector(self):
        self.button_browse = QPushButton('Browse', self)
        self.button_browse.setToolTip('Select a path for file type to be sorted into')
        self.button_browse.resize(self.button_browse.sizeHint())
        self.button_browse.move(200, 50)
        self.button_browse.clicked.connect(self._select_path_for_textbox)

    def _create_button_path_discarder(self):
        self.button_discard = QPushButton('Discard', self)
        self.button_discard.setToolTip('Deletes currently assigned path')
        self.button_discard.resize(self.button_browse.sizeHint())
        self.button_discard.move(200, 50)
        self.button_discard.clicked.connect(self._discard_path_for_textbox)

    def _create_frame(self):
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLineWidth(0.6)

    def _create_label(self):
        label_text = (self.type + ' Butler').title()
        self.label = QLabel(label_text, self)

    def _select_path_for_textbox(self):
        log('Selecting directory for ' + self.type + ' manager:')
        new_path = str(QFileDialog.getExistingDirectory(self, "Choose " + self.type.title() + " Manager Path", 'C:/ButlerTest/'))
        self._set_path(new_path)

    def _discard_path_for_textbox(self):
        new_path = ''
        self._set_path(new_path, discard=True)

    def _set_path(self, path, discard=False):
        self.textbox.setText(path)
        if self.type in globals.MANAGER_TYPES:
            setattr(globals.settings, self.path_attribute_name(), path)
            self.manager.path = path
            if discard:
                log(self.type.title() + ' directory discarded')
            else:
                log(self.type.title() + ' directory set to ' + path)
        globals.settings.save_settings()

    def _checkbox_change_manager_state(self, state):
        if state == Qt.Checked:
            self.manager.enabled = True
            setattr(globals.settings, self.checkbox_attribute_name(), True)
            on_off = 'ON'
        else:
            self.manager.enabled = False
            on_off = 'OFF'
        setattr(globals.settings, self.checkbox_attribute_name(), self.manager.enabled)
        globals.settings.save_settings()
        print(globals.settings.DOCUMENT_ACTIVE)
        log(self.type.title() + ' manager toggled ' + on_off)

    def checkbox_attribute_name(self):
        return self.type.upper() + '_ACTIVE'

    def path_attribute_name(self):
        return self.type.upper() + '_PATH'
