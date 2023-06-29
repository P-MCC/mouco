import Front_End.WindowDesign as wd
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = wd.Window()
    ex.show()
    sys.exit(app.exec_())