import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QComboBox,
    QLabel,
    QCheckBox,
    QFileDialog,
)
from PyQt5.QtGui import QIcon

class APIClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface with various widgets and layout.
        """
        # Set window title and geometry
        self.setWindowTitle("WikiPaper-UI-testing-version-1.0")
        self.setGeometry(100, 100, 400, 300)

        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), 'image.png')
        self.setWindowIcon(QIcon(icon_path))

        # Create and connect function_combobox
        self.function_combobox = QComboBox(self)
        self.function_combobox.addItems(["file", "upload", "list"])
        self.function_combobox.currentIndexChanged.connect(self.update_ui)

        # Create language_combobox and set placeholder text
        self.language_combobox = QComboBox(self)
        self.language_combobox.addItems(["es", "en"])
        self.language_combobox.setPlaceholderText("Language")

        # Create response_display and set as read-only
        self.response_display = QTextEdit(self)
        self.response_display.setReadOnly(True)

        # Create file_name_input and set placeholder text
        self.file_name_input = QLineEdit(self)
        self.file_name_input.setPlaceholderText("File Path")

        # Create progress_label
        self.progress_label = QLabel("Progress:")

        # Create list_button and connect to execute_function
        self.list_button = QPushButton("List Files", self)
        self.list_button.clicked.connect(self.execute_function)

        # Create switch checkbox
        self.switch = QCheckBox("Unofficial", self)

        # Create browse_button and connect to browse_file
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_file)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.function_combobox)
        layout.addWidget(self.language_combobox)
        layout.addWidget(self.file_name_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.switch)
        layout.addWidget(self.list_button)
        layout.addWidget(self.response_display)

        # Set layout
        self.setLayout(layout)
        self.update_ui()

    def update_ui(self):
        """
        Update the UI elements based on the selected function from the combobox.
        """
        # Get the selected function from the combobox
        selected_function = self.function_combobox.currentText()

        # Set visibility based on selected function
        self.switch.setVisible(selected_function in ("file", "list", "upload"))
        self.file_name_input.setVisible(selected_function in ("file"))
        self.browse_button.setVisible(selected_function == "upload")

        # Set text for the list_button based on selected function
        self.list_button.setText("List Files" if selected_function == "list" else "Execute")

    def execute_function(self):
        """
        Executes the selected function based on the value of the function_combobox.
        """
        selected_function = self.function_combobox.currentText()  # Get the selected function from the combobox
        if selected_function == "list":
            self.list_files()  # Call the list_files method
        elif selected_function == "file":
            self.execute_file()  # Call the execute_file method
        elif selected_function == "upload":
            self.execute_upload()  # Call the execute_upload method


    def list_files(self):
        """
        Retrieve a list of files based on the selected path and language, then display the response in the response_display.
        """
        # Determine the path based on the state of the switch
        path = "unofficial" if self.switch.isChecked() else "official"

        # Get the selected language from the language_combobox
        language = self.language_combobox.currentText()

        # Send a GET request to the server to retrieve the list of files
        response = requests.get(f"http://127.0.0.1:5000/list?path={path}&language={language}")

        # Update the response_display with the retrieved list of files
        self.response_display.setPlainText(response.text)


    def execute_file(self):
        """
        Executes the file based on the input file name, language, and folder type
        """
        # Get the file name from the input text
        file_name = self.file_name_input.text()

        # Get the selected language from the combobox
        language = self.language_combobox.currentText()

        # Determine the folder type based on the switch state
        folder = "unofficial" if self.switch.isChecked() else "official"

        # Construct the URL for the file based on the folder, file name, and language
        url = f"http://127.0.0.1:5000/file/{folder}/{file_name}?language={language}"

        # Send a GET request to the constructed URL
        response = requests.get(url)

        # Display the response text in the response display
        self.response_display.setPlainText(response.text)

    def execute_upload(self):
        """
        Executes the file upload process.
        """
        # Get the selected language from the combobox
        language = self.language_combobox.currentText()

        # Open a file dialog to select a file for upload
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'Text Files (*.txt);;Markdown Files (*.md)'
        )

        # If a file is selected, prepare the data and send a POST request to the server
        if file_path:
            # Prepare the file and language data
            files = {"file": open(file_path, "rb")}
            data = {"language": language}

            # Send a POST request to the server
            url = "http://127.0.0.1:5000/upload"
            response = requests.post(url, files=files, data=data)

            # Display the response in the response display
            self.response_display.setPlainText(response.text)

    def browse_file(self):
        """
        Opens a file dialog to browse and select a file, then updates the file input field with the selected file path.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'Text Files (*.txt);;Markdown Files (*.md)'
        )
        if file_path:
            self.file_name_input.setText(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = APIClientGUI()
    window.show()
    sys.exit(app.exec_())
