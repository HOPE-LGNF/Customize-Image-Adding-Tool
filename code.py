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
from urllib.parse import urlparse
from PIL import Image
import requests
import sys, os
import webbrowser


def copy_file(old_path: str, new_path: str, is_byte: bool = False, encoding: str = "utf-8",
              allow_overwrite_file: bool = False) -> None or FileExistsError:
    """
    基于os模块
    复制文件的函数，将源文件的内容复制到目标文件中。支持文本文件和二进制文件的复制。

    :param old_path: 源文件路径(填写文件名)。
    :param new_path: 目标文件路径(填写文件名)。
    :param is_byte: 是否以二进制模式复制文件，默认为False。
    :param encoding: 编码格式，默认为"utf-8"。
    :param allow_overwrite_file: 是否允许覆盖目标文件，默认为False。

    :raises FileExistsError: 如果源文件或目标文件已存在且不允许覆盖文件，则引发此异常。
    :return: None
    """
    try:  # 检测是否有os模块
        _AsxzwdecSecavased_soa_jJSHNbnmxznJSnmLKS_vqlr = os.name
    except NameError:
        import os
        print("imported")

    if os.path.exists(new_path):
        allow = -1
    elif not os.path.exists(old_path):
        allow = -2
    else:
        allow = 1
    if allow_overwrite_file:
        allow = 1
    match allow:
        case 1:
            with open(old_path, f"r{'b' if is_byte else ''}", encoding=None if is_byte else encoding) as f:
                _temp = f.read()
            with open(new_path, f"w{'b' if is_byte else ''}", encoding=None if is_byte else encoding) as i:
                i.write(_temp)
        case -1:
            raise FileExistsError("[WinError 114514] 目标文件已存在")
        case -2:
            raise FileExistsError("[WinError 1919810] 源文件路径无效")


def trans_image_suffix_into_PNG(path: str, newname=None) -> None:
    """
    将图片文件转换为PNG格式文件。
    需要from PIL import Image

    :param path: 需要转换的图片文件的路径。
    :param newname: PNG文件的新名称。如果未提供，默认为原始文件名附带PNG扩展名。

    :return: None

    示例:trans_image_suffix_into_PNG('/path/to/image.jpg', 'new_image.png')
    """
    dir_, name = os.path.split(path)
    if newname is None:
        newname = name.split('.')[0] + '.png'  # new name for png file
    Image.open(path).save(os.path.join(dir_, newname))


def filename_catcher(url: str) -> tuple[str, str]:
    """
    从给定的URL中提取文件名和文件后缀。
    (需要from urllib.parse import urlparse导入)

    :param url: 包含文件名的URL字符串。
    :return: tuple[Filename, Filesuffix] 返回提取的文件名和文件后缀。
    """
    a = urlparse(url)
    file_name = os.path.basename(a.path)
    _, file_suffix = os.path.splitext(file_name)
    return file_name, file_suffix


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initwindget()

        validator = QRegExpValidator(QRegExp('[^\\\\/:*?"<>|\r\n]+$'))
        self.ui.hint_input.setValidator(validator)
        self.imagePath = ""
        self.mode = 0

    def initwindget(self):
        self.ui.add_file.clicked.connect(self.Add)
        self.ui.fandomLinkButton_2.clicked.connect(self.Link_Fandom)
        self.ui.esixLinkButton.clicked.connect(self.Link_e621)
        self.ui.preview_btn.clicked.connect(self.change_webviewer_url)
        self.ui.mode_changer_combobox.currentIndexChanged.connect(self.change_mode)
        self.ui.choose_img_file_path_btn.clicked.connect(self.imageOpenDialog)

    def change_webviewer_url(self):
        try:
            self.ui.ImagewebPreViewer.load(QUrl(self.ui.downloadfilepathEdit.text()))
        except Exception as e:
            self.Dialogue("出问题了!", e, 2)

    @staticmethod
    def Link_Fandom():
        webbrowser.open("https://www.pexels.com/zh-cn")

    @staticmethod
    def Link_e621():
        webbrowser.open("https://yandex.com/images")

    def change_mode(self):
        # todo 国际化
        self.mode = self.ui.mode_changer_combobox.currentIndex()
        match self.mode:
            case 0:
                self.ui.downloadfilepathEdit.setText("")
                print("0case")
                self.ui.choose_img_file_path_btn.setEnabled(False)
                # self.ui.preview_btn.setEnabled(True)
                self.ui.label_3.setText("下载地址")
                self.ui.add_file.setText("下载并添加")
                self.ui.downloadfilepathEdit.setPlaceholderText("链接必须为以http://或https://开头的网址,部分网址可能无法下载")
            case 1:
                self.ui.downloadfilepathEdit.setText("")
                print("1case")
                self.ui.choose_img_file_path_btn.setEnabled(True)
                # self.ui.preview_btn.setEnabled(False)
                self.ui.label_3.setText("本地图片")
                self.ui.add_file.setText("添加")
                self.ui.downloadfilepathEdit.setPlaceholderText("需填写绝对路径")
            case _:
                print(self.mode)

    def imageOpenDialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, "打开", f"{os.path.join(os.environ['USERPROFILE'],'Pictures')}", "PNG图片文件(*.png)")
        if fname:
            self.imagePath = fname
        self.ui.downloadfilepathEdit.setText(self.imagePath)  # mode 2

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

    def Add(self):
        savefilename = self.ui.hint_input.text()
        try:
            # 检查 PICTURES_CARD 文件夹
            if not os.path.exists(f"{os.getcwd()}\\PICTURES_CARD"):
                os.mkdir("PICTURES_CARD")
                self.Dialogue("信息", "未检测到PICTURES_CARD文件夹,已创建")

            # 检查 hints.txt
            if not os.path.exists("hints.txt"):
                self.Dialogue("通知", "未检测到hint文件,已创建", 0)
                open("hints.txt", "w", encoding="utf-8").close()

            with open("hints.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
            for i in lines:
                if savefilename == i:
                    raise ValueError("此hint条目已存在")

            if self.ui.downloadfilepathEdit.text() == "":
                raise ValueError("未输入地址!")
            if self.ui.hint_input.text() == "":
                raise ValueError("未输入“你知道吗”内容!")

            # 匹配模式
            match self.mode:
                case 0:  # 下载模式
                    res = requests.get(self.ui.downloadfilepathEdit.text())
                    filename:str = filename_catcher(self.ui.downloadfilepathEdit.text())[0]  # filename包含后缀
                    if not os.path.exists(f"{os.getenv('TEMP')}\\ImageAddingTool\\"):
                        os.makedirs(f"{os.getenv('TEMP')}\\ImageAddingTool\\")
                    with open(f"{os.getenv('TEMP')}\\ImageAddingTool\\{filename}", 'wb') as file:  # download to TEMP
                        file.write(res.content)

                    self.Dialogue("喜报", f"{savefilename}下载完成", 0)

                    trans_image_suffix_into_PNG(f"{os.getenv('TEMP')}\\ImageAddingTool\\{filename}")  # change imgsuffix

                    copy_file(f"{os.getenv('TEMP')}\\ImageAddingTool\\{os.path.splitext(filename)[0]}.png",  # todo attention
                              f'{os.getcwd()}\\PICTURES_CARD\\{savefilename}.png', is_byte=True)
                    print(f'{os.getcwd()}\\PICTURES_CARD\\{savefilename}.png')
                case 1:  # 本地模式
                    if not os.path.isabs(self.imagePath):
                        raise ValueError("路径不是绝对路径")
                    copy_file(self.imagePath, f"{os.getcwd()}\\PICTURES_CARD\\{savefilename}.png", is_byte=True)
                case _:
                    raise NotImplementedError("more modes")

        except Exception as e:
            self.Dialogue("出问题了!", f"错误原因: {str(e)}", 2)
        else:
            with open("hints.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{self.ui.hint_input.text()}")
            self.Dialogue("喜报", f"{savefilename}添加完成", 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




