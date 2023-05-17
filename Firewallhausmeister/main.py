from main_window import *
import os
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))


main_window = MainWindow()
main_window.start()