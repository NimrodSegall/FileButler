from PyQt5.QtWidgets import QWidget, QVBoxLayout
from utilities import Settings
import gui.widgets


class WindowSettings(QWidget):

    def __init__(self, managers_collection, settings):
        super().__init__()
        self.settings = settings
        self.managers_collection = managers_collection

        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 120)
        self.resize(700, 120)
        self.setWindowTitle('Butler Settings')
        vbox = QVBoxLayout()
        self._create_default_managers_paths_widgets()
        vbox.addWidget(self.document_manager_path_widget)
        vbox.addWidget(self.image_manager_path_widget)
        vbox.addWidget(self.audio_manager_path_widget)
        vbox.addWidget(self.video_manager_path_widget)
        self.setLayout(vbox)

    def _create_default_managers_paths_widgets(self):
        self.document_manager_path_widget =\
            gui.widgets.ManagerPathSetter(self, settings=self.settings, manager=self.managers_collection['document'])
        self.image_manager_path_widget = \
            gui.widgets.ManagerPathSetter(self, settings=self.settings, manager=self.managers_collection['image'])
        self.audio_manager_path_widget =\
            gui.widgets.ManagerPathSetter(self, settings=self.settings, manager=self.managers_collection['audio'])
        self.video_manager_path_widget =\
            gui.widgets.ManagerPathSetter(self, settings=self.settings, manager=self.managers_collection['video'])

