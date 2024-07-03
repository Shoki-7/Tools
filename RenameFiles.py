import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QCheckBox, QFileDialog, QMessageBox

def remove_text_from_filename(file_name, remove_text):
    if remove_text:
        new_file_name = file_name.replace(remove_text, "")
    else:
        new_file_name = file_name
    return new_file_name

def replace_text_in_filename(file_name, old_text, new_text):
    new_file_name = file_name.replace(old_text, new_text)
    return new_file_name

def rename_files_in_directory(directory_path, remove_or_replace, old_text="", new_text="", subdirectories=False):
    if subdirectories:
        files = []
        for root, dirs, filenames in os.walk(directory_path):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    else:
        files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

    for file_path in files:
        if remove_or_replace == "remove":
            new_file_name = remove_text_from_filename(os.path.basename(file_path), old_text)
        elif remove_or_replace == "replace":
            new_file_name = replace_text_in_filename(os.path.basename(file_path), old_text, new_text)
        else:
            return "Invalid selection."

        new_path = os.path.join(os.path.dirname(file_path), new_file_name)
        os.rename(file_path, new_path)
    
    return "File renaming completed."

class FileRenamerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Directory selection
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit()
        dir_button = QPushButton("Browse")
        dir_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(QLabel("Directory:"))
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(dir_button)
        layout.addLayout(dir_layout)

        # Operation selection
        self.remove_radio = QRadioButton("Remove")
        self.replace_radio = QRadioButton("Replace")
        layout.addWidget(self.remove_radio)
        layout.addWidget(self.replace_radio)

        # Text inputs
        self.old_text_input = QLineEdit()
        layout.addWidget(QLabel("Text to remove/replace:"))
        layout.addWidget(self.old_text_input)

        self.new_text_input = QLineEdit()
        layout.addWidget(QLabel("New text (for replace):"))
        layout.addWidget(self.new_text_input)

        # Subdirectories option
        self.subdirs_check = QCheckBox("Include subdirectories")
        layout.addWidget(self.subdirs_check)

        # Rename button
        rename_button = QPushButton("Rename Files")
        rename_button.clicked.connect(self.rename_files)
        layout.addWidget(rename_button)

        self.setLayout(layout)
        self.setWindowTitle('File Renamer')
        self.show()

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.dir_input.setText(directory)

    def rename_files(self):
        directory = self.dir_input.text()
        if not directory:
            QMessageBox.warning(self, "Error", "Please select a directory.")
            return

        if self.remove_radio.isChecked():
            remove_or_replace = "remove"
        elif self.replace_radio.isChecked():
            remove_or_replace = "replace"
        else:
            QMessageBox.warning(self, "Error", "Please select Remove or Replace.")
            return

        old_text = self.old_text_input.text()
        new_text = self.new_text_input.text()
        subdirectories = self.subdirs_check.isChecked()

        result = rename_files_in_directory(directory, remove_or_replace, old_text, new_text, subdirectories)
        QMessageBox.information(self, "Result", result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileRenamerApp()
    sys.exit(app.exec_())