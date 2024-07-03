import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog, QMessageBox, QComboBox)
import ctypes

def get_file_extensions(directory_path):
    extensions = set()
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                extensions.add(ext.lower())
    return sorted(list(extensions))

def rename_files_in_directory(directory_path, old_text, new_text="", subdirectories=False, selected_extension=None):
    if subdirectories:
        files = []
        for root, dirs, filenames in os.walk(directory_path):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    else:
        files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

    renamed_count = 0
    for file_path in files:
        _, ext = os.path.splitext(file_path)
        if selected_extension and ext.lower() != selected_extension:
            continue

        if new_text:
            new_file_name = os.path.basename(file_path).replace(old_text, new_text)
        else:
            new_file_name = os.path.basename(file_path).replace(old_text, "")

        if new_file_name != os.path.basename(file_path):
            new_path = os.path.join(os.path.dirname(file_path), new_file_name)
            os.rename(file_path, new_path)
            renamed_count += 1
    
    return f"File rename completed.\n{renamed_count} files renamed."

class ModernButton(QPushButton):
    def __init__(self, text, parent=None, scaling_factor=1.0):
        super().__init__(text, parent)
        font_size = int(14 * scaling_factor)
        padding = int(6 * scaling_factor)
        border_radius = int(6 * scaling_factor)
        margin = int(1 * scaling_factor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #010066;
                border: none;
                color: white;
                padding: {padding}px {padding*2}px;
                text-align: center;
                text-decoration: none;
                font-size: {font_size}px;
                margin: {margin}px {margin}px;
                border-radius: {border_radius}px;
            }}
            QPushButton:hover {{
                background-color: #2A298A;
            }}
        """)

class ModernLineEdit(QLineEdit):
    def __init__(self, parent=None, scaling_factor=1.0):
        super().__init__(parent)
        border_width = int(2 * scaling_factor)
        border_radius = int(6 * scaling_factor)
        padding = int(3 * scaling_factor)
        self.setStyleSheet(f"""
            QLineEdit {{
                border: {border_width}px solid #010066;
                border-radius: {border_radius}px;
                padding: {padding}px;
                background-color: #f8f8f8;
                selection-background-color: #010066;
            }}
        """)

class ModernComboBox(QComboBox):
    def __init__(self, parent=None, scaling_factor=1.0):
        super().__init__(parent)
        border_width = int(2 * scaling_factor)
        border_radius = int(6 * scaling_factor)
        padding = int(5 * scaling_factor)
        self.setStyleSheet(f"""
            QComboBox {{
                border: {border_width}px solid #010066;
                border-radius: {border_radius}px;
                padding: {padding}px;
                background-color: #f8f8f8;
                selection-background-color: #f00000
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QListView {{
                background-color : #f8f8f8;
            }}
        """)

class FileRenameApp(QWidget):
    def __init__(self):
        super().__init__()
        self.scaling_factor = self.get_windows_display_scale()
        self.initUI()

    def initUI(self):
        font_size = int(14 * self.scaling_factor)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }}
            QLabel {{
                font-size: {font_size}px;
                color: #333;
            }}
            QCheckBox {{
                font-size: {font_size}px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(int(8 * self.scaling_factor))

        # Directory selection
        dir_layout = QHBoxLayout()
        self.dir_input = ModernLineEdit(scaling_factor=self.scaling_factor)
        dir_button = ModernButton("Browse", scaling_factor=self.scaling_factor)
        dir_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(QLabel("Directory:"))
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(dir_button)
        layout.addLayout(dir_layout)

        # Text inputs
        text_input_layout = QVBoxLayout()
        text_input_layout.setSpacing(0)
        self.old_text_input = ModernLineEdit(scaling_factor=self.scaling_factor)
        text_input_label = QLabel("Text to replace:")
        text_input_label.setContentsMargins(0, 0, 0, int(2 * self.scaling_factor))
        text_input_layout.addWidget(text_input_label)
        text_input_layout.addWidget(self.old_text_input)
        layout.addLayout(text_input_layout)

        new_text_input_layout = QVBoxLayout()
        new_text_input_layout.setSpacing(0)
        self.new_text_input = ModernLineEdit(scaling_factor=self.scaling_factor)
        new_text_input_label = QLabel("New text:")
        new_text_input_label.setContentsMargins(0, 0, 0, int(2 * self.scaling_factor))
        new_text_input_layout.addWidget(new_text_input_label)
        new_text_input_layout.addWidget(self.new_text_input)
        layout.addLayout(new_text_input_layout)

        # Extension selection
        extension_combo_layout = QVBoxLayout()
        extension_combo_layout.setSpacing(0)
        self.extension_combo = ModernComboBox(scaling_factor=self.scaling_factor)
        self.extension_combo.addItem("All Files")
        extension_combo_label = QLabel("Select file extension:")
        extension_combo_label.setContentsMargins(0, 0, 0, int(2 * self.scaling_factor))
        extension_combo_layout.addWidget(extension_combo_label)
        extension_combo_layout.addWidget(self.extension_combo)
        layout.addLayout(extension_combo_layout)

        # Subdirectories option
        self.subdirs_check = QCheckBox("Include subdirectories")
        layout.addWidget(self.subdirs_check)

        # Rename button
        rename_button = ModernButton("Rename Files", scaling_factor=self.scaling_factor)
        rename_button.clicked.connect(self.rename_files)
        layout.addWidget(rename_button)

        self.setLayout(layout)
        self.setWindowTitle('File Renamer')
        
        # Set fixed window size based on scaling factor
        width = int(400 * self.scaling_factor)
        height = int(200 * self.scaling_factor)
        self.setMinimumSize(width, height)
        
        self.show()

    def get_windows_display_scale(self):
        hdc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 is the constant for LOGPIXELSX
        ctypes.windll.user32.ReleaseDC(0, hdc)
        return dpi / 96.0  # 96 DPI is the standard scale 1.0

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.dir_input.setText(directory)
            self.update_extensions(directory)

    def update_extensions(self, directory):
        extensions = get_file_extensions(directory)
        self.extension_combo.clear()
        self.extension_combo.addItem("All Files")
        self.extension_combo.addItems(extensions)

    def rename_files(self):
        directory = self.dir_input.text()
        if not directory:
            QMessageBox.warning(self, "Error", "Please select a directory.")
            return

        old_text = self.old_text_input.text()
        if not old_text:
            QMessageBox.warning(self, "Error", "Please enter text to remove/replace.")
            return

        new_text = self.new_text_input.text()
        subdirectories = self.subdirs_check.isChecked()
        
        selected_extension = self.extension_combo.currentText()
        if selected_extension == "All Files":
            selected_extension = None

        result = rename_files_in_directory(directory, old_text, new_text, subdirectories, selected_extension)
        QMessageBox.information(self, "Result", result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = FileRenameApp()
    sys.exit(app.exec_())