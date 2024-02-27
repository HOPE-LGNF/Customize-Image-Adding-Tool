# -*- encoding: utf-8 -*- #
"""
Coding by using PyCharm
File: changed图片添加工具/code.py
Be created at 2024/02/25
Be created by HOPE
"""
from UI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import QUrl, QRegExp
from PyQt5.QtGui import QRegExpValidator
import requests
import sys, os
import webbrowser


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initwindget()

        validator = QRegExpValidator(QRegExp('[^\\\\/:*?"<>|\r\n]+$'))
        self.ui.hint_input.setValidator(validator)
        self.ui.savefilenameEdit.setValidator(validator)
        self.imagePath, self.DFP, self.savePath = "", "", ""

    def initwindget(self):
        self.ui.download_file.clicked.connect(self.Download)
        self.ui.downloadfilepathEdit.textChanged.connect(self.Auto_Change_Filename)
        self.ui.fandomLinkButton_2.clicked.connect(self.Link_Fandom)
        self.ui.esixLinkButton.clicked.connect(self.Link_e621)
        self.ui.preview_btn.clicked.connect(self.change_webviewer_url)
        self.ui.open_file_dir.clicked.connect(self.open_folder)
        self.ui.chooseimage.clicked.connect(self.imageOpenDialog)
        self.ui.pushButton.clicked.connect(self.Finally_Add)
        self.ui.choosesavepath.clicked.connect(self.folderOpenDialog)

    def change_webviewer_url(self):
        try:
            self.ui.ImagewebPreViewer.load(QUrl(self.DFP))
        except Exception as e:
            print(e)
            self.Dialogue("Error!", e, 2)

    def Auto_Change_Filename(self):
        """
        a: https://picx.zhimg.com/70/v2-23a56248e4148780e5a15b7f4ea77948_1440w.awebp
        a: https://static.wikia.nocookie.net/changed1449/images/9/93/179.png/revision/latest?cb=20220115225401
        a: https://www.baidu.com/favicon.ico
        """
        self.DFP = self.ui.downloadfilepathEdit.text()
        link = self.ui.downloadfilepathEdit.text()
        filename = "/".join(link.split("/")[3:]).split(".")[0].split("/")[-1] + "." + \
                   "/".join(link.split("/")[3:]).split(".")[-1].split("/")[0]
        self.ui.savefilenameEdit.setText(filename)

    @staticmethod
    def Link_Fandom():
        webbrowser.open("https://www.pexels.com/zh-cn")

    @staticmethod
    def Link_e621():
        webbrowser.open("https://yandex.com/images")

    def Download(self):
        savedir = self.ui.savepathEdit.text()
        savefilename = self.ui.savefilenameEdit.text()
        print(savefilename)
        try:
            if self.ui.downloadfilepathEdit.text() == "":
                raise ValueError("未输入下载地址!")
            if savedir == "":
                raise ValueError("未输入保存文件夹路径!")
            elif not os.path.exists(f"{savedir}"):
                raise FileNotFoundError("文件夹不存在!")
            if savefilename == "":
                raise ValueError("未输入保存文件名!")
            res = requests.get(self.ui.downloadfilepathEdit.text())
        except Exception as e:
            self.Dialogue("出问题了!", f"错误原因: {str(e)}", 2)
        else:

            print("OK")
            if savedir[-1] != '/':
                savedir += "\\"
            with open(f'{savedir}{savefilename}', 'wb') as file:
                file.write(res.content)
            self.Dialogue("喜报", f"{savefilename}下载完成", 0)

    def open_folder(self):
        print(os.path.exists(self.ui.savepathEdit.text()))
        if self.ui.savepathEdit.text() == "":
            pass
        elif not os.path.exists(self.ui.savepathEdit.text()):
            print("目录不存在")
        else:
            print(type(self.ui.savepathEdit.text()))
            os.startfile(f"{self.ui.savepathEdit.text()}")

    def Dialogue(self, title, text, mode=0):
        """
        mode:{0:  info
              1: warning
              2: Error
              3: question
        """
        if mode == 0:
            QMessageBox.information(self, title, text)
        elif mode == 1:
            QMessageBox.warning(self, title, text)
        elif mode == 2:
            QMessageBox.critical(self, title, text)
        elif mode == 3:
            QMessageBox.question(self, title, text)

    def imageOpenDialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, "打开", "C:\\", "图片文件(*.png *.jpg)")
        if fname:
            self.imagePath = fname
        self.ui.inagefilepathEdit.setText(self.imagePath)

    def folderOpenDialog(self):
        fname = QFileDialog.getExistingDirectory(self, "打开", "C:\\")
        if fname:
            self.savePath = fname
        self.ui.savepathEdit.setText(self.savePath)

    def Finally_Add(self):
        if self.ui.inagefilepathEdit.text():
            if self.ui.hint_input.text():
                if os.path.exists(f"{self.ui.inagefilepathEdit.text()}"):
                    if os.path.exists("hint.txt"):
                        with open("hint.txt", "a", encoding="utf-8") as f:
                            f.write(f"\n{self.ui.hint_input.text()}")
                    else:
                        with open("hint.txt", "w", encoding="utf-8") as f:
                            f.write(f"{self.ui.hint_input.text()}")

                    with open(self.ui.inagefilepathEdit.text(), "rb") as f:
                        bdata = f.read()
                    with open(f"{os.path.dirname(__file__)}\\PICTURES_CARD\\{self.ui.hint_input.text()}.{os.path.basename(self.ui.inagefilepathEdit.text()).split('.')[-1]}", "wb") as g:
                        g.write(bdata)
                else:
                    self.Dialogue("出问题了", "图片路径无效", 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
