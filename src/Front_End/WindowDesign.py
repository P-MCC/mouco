import subprocess
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt
import os


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
        slider.setMinimum(1)
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
            
            subprocess.call(f"python src/Back_End/Jiggler.py {self.sliderValue} main", shell=True)
            
            

        button.clicked.connect(print_slider_value)
        return main



    def ui2(self): 
        main = QWidget()
        main_layout = QVBoxLayout(main)
        main_layout.addStretch(0)  # Add initial stretch for padding

        # Create label
        label = QLabel('Clicks Per Second')
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        # Create slider and input field layout
        slider_layout = QHBoxLayout()

        # Create slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(10000)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(100)
        slider.setSingleStep(1)
        slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        slider_layout.addWidget(slider)

        # Create input field
        input_field = QLineEdit()
        input_field.setFixedWidth(40)
        slider_layout.addWidget(input_field)
        
        main_layout.addLayout(slider_layout)

        # Add stretch for vertical centering
        main_layout.addStretch(1)

        # Create button
        button = QPushButton('Burst')
        button.setObjectName('burstButton')
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
            
            subprocess.call(f"python src/Back_End/ClickBurster.py {(1/self.sliderValue)} main", shell=True)
            
            

        button.clicked.connect(print_slider_value)
        return main


    def ui3(self):
        main_layout = QVBoxLayout()  # Use QVBoxLayout for the main layout

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create the buttons
        button1 = QPushButton("Execute Macros")
        button2 = QPushButton("Record Macros")

        # Create a stacked widget to hold the content widgets
        stacked_widget = QStackedWidget()

        # Create the content widgets for each button
        widget1 = QWidget()
        widget2 = QWidget()

        # Create the layouts for the content widgets
        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()

        # Create the labels for each widget
        label1 = QLabel("Button 1 Widget")
        label2 = QLabel("Button 2 Widget")

        # Add the labels to the corresponding layouts
        layout1.addWidget(label1)
        layout2.addWidget(label2)

        # Set the layouts for the content widgets
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)

        # Add the content widgets to the stacked widget
        stacked_widget.addWidget(widget1)
        stacked_widget.addWidget(widget2)

        # Slot function to switch the visible widget based on the clicked button
        def switch_widget(button):
            if button == button1:
                stacked_widget.setCurrentWidget(widget1)
                dropdown.setVisible(True)
                execute_button.setVisible(True)
                label1.setVisible(True)
                select_record_label.setVisible(True)
                record_label.setVisible(False)
                record_input.setVisible(False)
                record_button.setVisible(False)
            elif button == button2:
                stacked_widget.setCurrentWidget(widget2)
                dropdown.setVisible(False)
                execute_button.setVisible(False)
                label1.setVisible(False)
                select_record_label.setVisible(False)
                record_label.setVisible(True)
                record_input.setVisible(True)
                record_button.setVisible(True)
                

        # Connect the clicked signal of each button to the slot function
        button1.clicked.connect(lambda: switch_widget(button1))
        button2.clicked.connect(lambda: switch_widget(button2))

        # Add the buttons to the horizontal layout
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Create a horizontal layout for the widgets
        widget_layout = QHBoxLayout()

        # Create the dropdown box
        dropdown = QComboBox()

        # Construct the directory path relative to the current file
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        directory_path = os.path.join(current_file_dir, "..", "..", "Saved_Macros")

        # Populate the dropdown box with file names from the directory
        file_names = os.listdir(directory_path)
        dropdown.addItems(file_names)

        # Create the "Execute Macros" button
        execute_button = QPushButton("Execute")

        # Slot function to handle the execution of macros
        def execute_macros():
            selected_file = dropdown.currentText()
            # Implement the logic to execute the selected macro file
            print(f"Executing macro: {selected_file}")
            subprocess.call(f"python src/Back_End/MacroExecutor.py {(selected_file)} main", shell=True)

        # Connect the clicked signal of the button to the execute_macros slot function
        execute_button.clicked.connect(execute_macros)
        
        select_record_label = QLabel("Select Macro Record:")

        # Create a widget to hold the dropdown box and button
        widget = QWidget()
        widget_layout.addWidget(select_record_label)
        widget_layout.addWidget(dropdown)
        widget_layout.addWidget(execute_button, alignment=Qt.AlignCenter)
        widget.setLayout(widget_layout)

        # Create a vertical layout for the record widget
        record_layout = QVBoxLayout()

        # Create a horizontal layout for the label and input area
        record_input_layout = QHBoxLayout()

        # Create the label for the record input
        record_label = QLabel("Record Name:")

        # Create the input area
        record_input = QLineEdit()

        # Create the "Record" button
        record_button = QPushButton("Record")
        
        def record_macros():
            new_macro_file = record_input.text()
            # Implement the logic to execute the selected macro file
            print(f"New macro: {new_macro_file}")
            subprocess.call(f"python src/Back_End/MacroSaver.py {(new_macro_file)} main", shell=True)
        
        record_button.clicked.connect(record_macros)

        # Add the label and input area to the record input layout
        record_input_layout.addWidget(record_label)
        record_input_layout.addWidget(record_input)

        # Add the input area and button to the record layout
        record_layout.addLayout(record_input_layout)
        record_layout.addWidget(record_button, alignment=Qt.AlignCenter)
        

        # Create a widget to hold the record layout
        record_widget = QWidget()
        record_widget.setLayout(record_layout)

        # Add the widgets to the main layout
        main_layout.addWidget(widget)
        main_layout.addWidget(record_widget)

        # Add the stacked widget to the main layout
        main_layout.addWidget(stacked_widget)

        # Set the initial state as button1 clicked (widget1 visible)
        switch_widget(button1)

        # Create a widget to hold the layout
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        return main_widget
