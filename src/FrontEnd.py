import subprocess
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowTitle('MOUCO')
        
        self.sliderValue = 0  # Variable to store the slider value
        # set the size of window
        self.Width = 920
        self.height = int(0.5 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = QPushButton('Jiggle', self)
        self.btn_2 = QPushButton('Click Burst', self)
        self.btn_3 = QPushButton('Macro', self)
        

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
       

        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
       
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
       

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ----------------- 
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)


    # ----------------- 
    # pages

    def ui1(self):
        main = QWidget()
        main_layout = QVBoxLayout(main)
        main_layout.addStretch(0)  # Add initial stretch for padding

        # Create label
        label = QLabel('Sleep Time')
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        # Create slider and input field layout
        slider_layout = QHBoxLayout()

        # Create slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(5)
        slider.setSingleStep(1)
        slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        slider_layout.addWidget(slider)

        # Create input field
        input_field = QLineEdit()
        input_field.setFixedWidth(25)
        slider_layout.addWidget(input_field)
        
        main_layout.addLayout(slider_layout)

        # Add stretch for vertical centering
        main_layout.addStretch(1)

        # Create button
        button = QPushButton('Jiggle')
        button.setObjectName('jiggleButton')
        main_layout.addWidget(button, alignment=Qt.AlignCenter)

        # Add stretch for padding at the bottom
        main_layout.addStretch(4)

        # Synchronize slider with input field and assign value to sliderValue
        def update_slider_value():
            value = input_field.text()
            if value.isdigit():
                slider.setValue(int(value))
                self.sliderValue = int(value)  # Assign value to sliderValue

        def update_input_field():
            value = str(slider.value())
            input_field.setText(value)
            self.sliderValue = slider.value()  # Assign value to sliderValue

        input_field.textChanged.connect(update_slider_value)
        slider.valueChanged.connect(update_input_field)

        # Print assigned value when button is clicked
        def print_slider_value():
            print(f"Assigned value: {self.sliderValue}")
            # subprocess.call("python src/Back_End/Jiggler.py", shell=True)
            
            
            from Back_End.Jiggler import main as Jiggler

            if __name__ == "__main__":
    
                Jiggler(self.sliderValue)


        button.clicked.connect(print_slider_value)
        return main



    def ui2(self): 
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 2'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())