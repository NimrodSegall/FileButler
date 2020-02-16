"""This files contains the default settings of the program and references to
a settings variable and a prompt window, both of which need access from many
different parts of the software"""

# Default Settings
IMAGE_PATH = ''
AUDIO_PATH = ''
VIDEO_PATH = ''
DOCUMENT_PATH = ''
PATHS = {'image': IMAGE_PATH, 'audio': AUDIO_PATH, 'video': VIDEO_PATH, 'document': DOCUMENT_PATH}

IMAGE_ACTIVE = True
AUDIO_ACTIVE = True
VIDEO_ACTIVE = True
DOCUMENT_ACTIVE = True

DELAY_BETWEEN_SCANS = 3000   # Delay in ms
LOG_FILE_NAME = 'log.txt'
PATHS_TO_SCAN = ['']
MANAGED_FILES = {''}

# Constants
SETTINGS_FILE_NAME = 'ButlerSettings.ini'
MANAGER_TYPES = ['document', 'image', 'audio', 'video']
DOCUMENT_EXTENSIONS = ['.txt', '.pdf', '.doc', '.docx', '.dot', '.docm', '.csv', '.xml', '.xls', '.xlw', '.xlt',
                       '.xlsx', '.xlsm', '.xltx', 'xltm', '.xlsb', '.rtf', '.dbf', '.uos', '.uof', '.ppt', '.pps',
                       '.pot', '.pptx', '.pptm', '.potx', '.potm']
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.pgm', '.sgf', '.eps', '.psd', '.sgv']
AUDIO_EXTENSIONS = ['.mp3', '.wma', '.wav', '.aa', '.aac', '.flac', '.m4a', '.m4b', '.m4p', ]
VIDEO_EXTENSIONS = ['.mp4', '.m4p', '.m4v', '.avi', '.wmv', '.mov', '.flv', '.mkv', '.mpg', '.mpeg', '.mp2', '.mpe',
                    '.mpv', '.f4v', '.f4p', '.f4a', '.f4b']
EXTENSIONS = {'image': IMAGE_EXTENSIONS, 'audio': AUDIO_EXTENSIONS, 'video': VIDEO_EXTENSIONS,
              'document': DOCUMENT_EXTENSIONS}

DICT_DELIMITER = '*;:;*'

# References
settings = None
prompt_ref = None


