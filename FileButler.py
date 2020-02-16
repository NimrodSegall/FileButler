import utilities
from gui.WindowMain import create_GUI
import globals


def main():
    globals.settings = utilities.Settings()
    managers_collection = utilities.FileManagersCollection()
    create_GUI(managers_collection, globals.settings)


if __name__ == '__main__':
    main()