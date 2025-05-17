import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup,
    QLabel, QLineEdit, QPushButton, QWidget, QSpacerItem, QSizePolicy
)

class AddressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("地址选择")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Option group
        option_layout = QHBoxLayout()
        self.radio_default = QRadioButton("A: 默认地址")
        self.radio_custom = QRadioButton("B: 自定义地址")
        self.radio_default.setChecked(True)
        option_group = QButtonGroup(self)
        option_group.addButton(self.radio_default)
        option_group.addButton(self.radio_custom)
        option_layout.addWidget(self.radio_default)
        option_layout.addWidget(self.radio_custom)
        main_layout.addLayout(option_layout)

        # Address input
        address_layout = QHBoxLayout()
        label = QLabel("地址：")
        self.line_edit = QLineEdit()
        self.line_edit.setDisabled(True)
        address_layout.addWidget(label)
        address_layout.addWidget(self.line_edit)
        main_layout.addLayout(address_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.ok_button)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Connect signals
        self.radio_default.toggled.connect(self.update_line_edit_state)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def update_line_edit_state(self):
        if self.radio_custom.isChecked():
            self.line_edit.setDisabled(False)
        else:
            self.line_edit.setDisabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AddressDialog()
    if dialog.exec():
        print("确定")
    else:
        print("取消")
