import globals

import os
import shutil
import hashlib
import configparser
import filecmp
from datetime import datetime


# log

def log(string, _times_called=[0]):
    # _times_called argument should be left blank on function call

    def format_time(time_units):
        """Makes sure time is shown with two digits even if hour < 10 or minute < 10"""
        if len(str(time_units)) == 1:
            formatted_time = '0' + str(time_units)
        else:
            formatted_time = str(time_units)
        return formatted_time

    timed_string = '(' + format_time(datetime.now().time().hour) + ':' + format_time(datetime.now().time().minute) + ')    ' + string
    if os.path.isfile(globals.settings.LOG_FILE_NAME):
        if _times_called[0] > 0:
            with open(globals.settings.LOG_FILE_NAME, 'a') as log_file:
                log_file.write(timed_string + '\n')
        else:
            with open(globals.settings.LOG_FILE_NAME, 'w') as log_file:
                log_file.write(timed_string + '\n')
    if globals.prompt_ref is not None:
        globals.prompt_ref.setText(timed_string)
    _times_called[0] += 1


# File Manager
class FileManager:
    """Core module of File Butler, manages files in selected paths (copy or move)
    file_type - the type of file this managers manage (audio, video, etc ...)
    full list of types can be found in globals.py under MANAGER_TYPES
    """
    def __init__(self, file_type, is_enabled=True):
        self._check_input(file_type)
        self.type = file_type.lower()
        self.extensions = globals.EXTENSIONS[self.type]
        self.enabled = is_enabled
        self.path = getattr(globals.settings, self.path_attribute_name())
        self.files = []    # list of hash values of files managed by this manager

    @staticmethod
    def _check_input(file_type):
        if not isinstance(file_type, str):
            log('FileManager input must be a string!')
            raise TypeError
        try:
            globals.EXTENSIONS[file_type.lower()]
        except KeyError:
            log('Error in type of file! Must accept viable file types (audio, video, document, etc ...')

    def manage_files(self, search_paths, keep_copy=True):
        if self.enabled:
            if getattr(globals.settings, self.type.upper() + '_ACTIVE'):
                if self.path != '':
                    self._update_managed_files_list(search_paths)
                    target_path = format_path(self.path)
                    for file in self.files:
                        for ext in self.extensions:
                            if is_file_of_type(file, ext):
                                if not self._file_copy_not_modified(file, target_path):
                                    if keep_copy:
                                        shutil.copy(file, target_path)
                                    else:
                                        shutil.move(file, target_path)

    def _update_managed_files_list(self, search_paths):
        all_files = []
        if self.path != '':
            target_path = format_path(self.path)
            files = []
            for search_path in search_paths:
                if search_path != '':
                    formatted_search_path = format_path(search_path)  # This makes sure path ends with '/'
                    local_files = os.listdir(formatted_search_path)
                    files_with_path = [(lambda f: formatted_search_path + f)(file) for file in local_files]
                    files = files + files_with_path
            for file in files:
                all_files.append(file)
        self.files = all_files

    @staticmethod
    def _file_copy_not_modified(file, path):
        """Returns False if copy does not exists or if
        the copy is different from the original. If the copy is
        identical, returns True"""
        file_name = file_path_to_file_name(file)
        if os.path.isfile(path + file_name):
            if filecmp.cmp(file, path + file_name):
                return True
        else:
            return False

    def path_attribute_name(self):
        return self.type.upper() + '_PATH'


# modified from https://nitratine.net/blog/post/how-to-hash-files-in-python/
def hash_file(file_path, block_size=65536):
    file_hash = hashlib.sha256()      # Create the hash object
    with open(file_path, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(block_size)       # Read from the file. Take in the amount block_size
        while len(fb) > 0:            # While there is still data being read from the file
            file_hash.update(fb)      # Update the hash
            fb = f.read(block_size)   # Read the next block from the file
    return file_hash.hexdigest()      # Get the hexadecimal digest of the hash


def file_path_to_file_name(file_path):
    """Given a full path (string) to a file,
    returns the name of the file"""
    if '/' in file_path:
        return file_path.split('/')[-1]
    else:
        return file_path


class FileManagersCollection:
    """Creates a collection of managers and allows easy access to them by name, \
    for example: fmc = FileManagerCollection
    audio_manager = fmc['audio']"""
    def __init__(self):
        self.managers = self.create_file_managers()

    def __getitem__(self, manager_type):
        if isinstance(manager_type, str):
            for manager in self.managers:
                if manager_type.lower() in manager.type:
                    return manager
        else:
            log('manager_type must be a string (FileManagersCollection.__getitem__()')
        return None

    def create_file_managers(self):
        """Create default file managers for filetypes specified in globals.MANAGER_TYPES"""
        log('Creating File Managers ...')
        managers = []
        for file_type in globals.MANAGER_TYPES:
            managers.append(FileManager(file_type))
        self.managers = managers
        log('File managers created!')
        return managers


def is_file_of_type(file_name, ext):
    """Takes file name and an extension as strings
    return true iff file ends with the extension"""
    type_length = len(ext)
    if len(file_name) > type_length:
        file_extension = file_name[-type_length:]
        if file_extension.lower() == ext.lower():
            return True
    return False


def format_path(path):
    """Makes sure a path string ends with '/'"""
    formatted_path = path
    if len(path) > 0:
        if formatted_path[-1] != '/':
            formatted_path = formatted_path + '/'
    return formatted_path


# Settings
class Settings:
    """Holds the current settings of the user. Reads / writes settings file"""
    def __init__(self):
        self.IMAGE_PATH = globals.IMAGE_PATH
        self.AUDIO_PATH = globals.AUDIO_PATH
        self.VIDEO_PATH = globals.VIDEO_PATH
        self.DOCUMENT_PATH = globals.DOCUMENT_PATH

        self.IMAGE_ACTIVE = globals.IMAGE_ACTIVE
        self.AUDIO_ACTIVE = globals.AUDIO_ACTIVE
        self.VIDEO_ACTIVE = globals.VIDEO_ACTIVE
        self.DOCUMENT_ACTIVE = globals.DOCUMENT_ACTIVE

        self.DELAY_BETWEEN_SCANS = globals.DELAY_BETWEEN_SCANS  # Delay in ms

        self.LOG_FILE_NAME = globals.LOG_FILE_NAME
        self.PATHS_TO_SCAN = globals.PATHS_TO_SCAN
        self.MANAGED_FILES = globals.MANAGED_FILES
        self.load_settings()

    """ contains settings for the settings window"""
    def add_path_to_scan(self, path, path_qlist):
        self.PATHS_TO_SCAN.append(path)
        path_qlist.add_path(path)
        self.save_settings()

    def load_settings(self):

        def format_input_string_list(string_list):
            formatted_list = string_list
            if len(string_list) > 1:
                if string_list[0] == '[' and string_list[-1] == ']':
                    formatted_list = formatted_list[-1:]
                    formatted_list = formatted_list[1:]
            formatted_list = formatted_list.split(',')
            return formatted_list

        config = configparser.ConfigParser()
        files = os.listdir(os.getcwd())
        if globals.SETTINGS_FILE_NAME in files:
            config.read(globals.SETTINGS_FILE_NAME)
            if 'DEFAULT' in config.keys() and 'current' in config.keys():
                for attribute_name in config['current']:
                    attribute_type = type(getattr(self, attribute_name.upper()))
                    attribute_string = config['current'][attribute_name]
                    if attribute_type == list:
                        list_arg = format_input_string_list(attribute_string)
                        list_arg = [item for item in list_arg if len(item) > 0]
                        setattr(self, attribute_name.upper(), list_arg)
                    elif attribute_type == bool:
                        print(attribute_name.upper())
                        setattr(self, attribute_name.upper(), config['current'].getboolean(attribute_name))
                    elif attribute_type == dict:
                        pass
                    # if attribute is string
                    else:
                        setattr(self, attribute_name.upper(), attribute_type(attribute_string))
        else:
            settings_attributes = [atr for atr in dir(self) if atr.isupper()]
            for attribute_name in settings_attributes:
                setattr(self, attribute_name, getattr(globals, attribute_name))

    def save_settings(self):
        config = configparser.ConfigParser()
        settings_attributes = [atr for atr in dir(self) if atr.isupper()]
        config['DEFAULT'] = {}
        config['current'] = {}
        for attribute in settings_attributes:
            config['DEFAULT'][attribute] = str(getattr(globals, attribute))
            config['current'][attribute] = str(getattr(self, attribute))

        lists = [attribute for attribute in settings_attributes if isinstance((getattr(self, attribute)), list)]
        for list_atr in lists:
            config['DEFAULT'][list_atr] = ",".join(getattr(globals, list_atr.upper()))
            config['current'][list_atr] = ",".join(getattr(self, list_atr.upper()))

        dicts = [attribute for attribute in settings_attributes if isinstance((getattr(self, attribute)), dict)]
        for dict_atr in dicts:
            default_dict = getattr(globals, dict_atr.upper())
            current_dict = getattr(self, dict_atr.upper())
            default_list = dict_to_lists(default_dict)
            current_list = dict_to_lists(current_dict)
            config['DEFAULT'][dict_atr] = ",".join(default_list)
            config['current'][dict_atr] = ",".join(current_list)
            print(config['current'][dict_atr])

        with open(globals.SETTINGS_FILE_NAME, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def string_to_type(string, string_type):
        if string_type == 'string':
            return string
        elif string_type == 'boolean':
            return string == 'True'
        elif string_type == 'integer':
            return int(string)
        else:
            raise ValueError


def dict_to_lists(dic, delimiter=globals.DICT_DELIMITER):
    keys = list(dic.keys())
    vals = list(dic.values())
    return keys + [delimiter] + vals


