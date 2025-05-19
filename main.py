#coding=utf-8

import sys
import logging.config
import os.path

import configparser

from PySide6.QtCore import (
    QStandardPaths,
)

from PySide6.QtGui import *
from PySide6.QtWidgets import *


default_address = 'http://teacher.eagleplan.fun'


class AddressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("版本切换")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Option group
        option_layout = QHBoxLayout()
        self.radio_default = QRadioButton("默认地址")
        self.radio_custom = QRadioButton("自定义地址")
        self.radio_default.setChecked(True)
        option_group = QButtonGroup(self)
        option_group.addButton(self.radio_default)
        option_group.addButton(self.radio_custom)
        option_layout.addWidget(self.radio_default)
        option_layout.addWidget(self.radio_custom)
        main_layout.addLayout(option_layout)

        # Address input
        address_layout = QHBoxLayout()
        self.line_edit = QLineEdit()
        self.line_edit.setDisabled(True)
        self.line_edit.setPlaceholderText(default_address)
        
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
        self.ok_button.clicked.connect(self.on_accepted)
        self.cancel_button.clicked.connect(self.reject)

    def update_line_edit_state(self):
        if self.radio_custom.isChecked():
            self.line_edit.setDisabled(False)
        else:
            self.line_edit.setDisabled(True)

    def get_ini_file(self):
        try:
            user_data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
            pp = os.path.join(user_data_dir, "golive-studio", "global.ini")
            logging.info(f"golive ini file should be: {pp}")
            if not os.path.exists(pp):
                logging.info("golive not found")
                return ""
            return pp
        except Exception as e:
            logging.exception("golive not found")
        return ""

    def has_golive(self):
        pp = self.get_ini_file()
        if not pp:
            QMessageBox.warning(self, "Warning", "请启动 Golive Studio 并关闭，再打开此程序")
            return False
        return True

    def show_warn(self, msg="golive not found"):
        QMessageBox.warning(self, "Warning", "请输入合理地址")
        self.line_edit.setFocus()

    def valid_check(self):
        txt = self.line_edit.text()
        if txt == "":
            self.show_warn()
            return False
        if not txt.startswith("http://") and not txt.startswith("https://"):
            self.show_warn()
            return False
        return True

    def write_ini(self, fn, address):
        ## 把 fn 作为 ini 文件，写入配置
        ## 写入如下区块 
        # Golive
        # ChatURL=
        
        p = configparser.ConfigParser()
        p.read(fn)
        if "Golive" not in p.sections():
            p.add_section("Golive")
            
        p.set("Golive", "ChatURL", address)
        with open(fn, "w") as f:
            p.write(f)

        QMessageBox.information(self, "Information", "写入配置成功")

    def on_accepted(self):
        logging.info("on_accepted")
        if not self.has_golive():
            logging.info("golive not found")
            return

        addr = default_address
        if self.radio_default.isChecked():
            addr = default_address
        else:
            if not self.valid_check():
                logging.info("not valid address")
                return
            addr = self.line_edit.text()
        logging.info(f"address set to: {addr}")
        pp = self.get_ini_file()
        self.write_ini(pp, addr)
        return None


def cfgLogging():
    LOGGING = {
               'version': 1,
               'disable_existing_loggers': True,
               'formatters': {
                              'default': {'format': '[%(asctime)-25s] [%(relativeCreated)-15s] %(name)-12s pid:%(process)d %(message)s'},
                               # default': {
                               #           'format' : '%(asctime)s %(message)s',
                               #           'datefmt' : '%Y-%m-%d %H:%M:%S'
                               # }
                },
               'handlers': {
                            'console':{
                                       'level':'INFO',
                                       'class':'logging.StreamHandler',
                                       'formatter': 'default'
                            },
                            'file': {
                                     'level': 'DEBUG',
                                     'class': 'logging.handlers.RotatingFileHandler',
                                     'formatter': 'default',
                                     'filename' : 'run.log',
                                     'maxBytes':    20 * 1024 * 1024,  # 10M
                                     'backupCount': 5,
                                     'encoding' : 'utf8',
                            }
                },
               'loggers' : {
                            # 定义了一个logger
                            '' : {
                                          'level' : 'DEBUG',
                                          'handlers' : ['console', 'file'],
                                          'propagate' : True
                            }
                }
    }
    logging.config.dictConfig(LOGGING)


def main():
    print("main")
    logging.info("main")
    app = QApplication(sys.argv)
    dialog = AddressDialog()
    dialog.exec()
    

if __name__ == "__main__":
    try:
        cfgLogging()
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")