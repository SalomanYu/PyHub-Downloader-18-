import sys
from hub_main import download_video, get_info
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView


class App(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setupGui()
    
    def setupGui(self):
        
        self.frame = QFrame(self)
        self.frame.setGeometry(QRect(0,10,640,91))

        self.logo_label = QLabel(self.frame)
        self.logo_label.setObjectName('logo')
        self.logo_label.setGeometry(QRect(0,0,151,81))
        self.logo_label.setPixmap(QPixmap('media/logo.png'))
        self.logo_label.setScaledContents(True)
        self.logo_label.resize(151, 87)

        self.url_line = QLineEdit(self.frame)
        self.url_line.clearFocus()
        self.url_line.setGeometry(QRect(150,30,371,31))

        self.url_line.setPlaceholderText('Please paste url')

        self.download_btn = QPushButton(self.frame)
        self.download_btn.setGeometry(QRect(520,30,71,31))

        icon = QIcon()
        icon.addPixmap(QPixmap('media/image_downloader.png'))
        self.download_btn.setIcon(icon)
        self.download_btn.clicked.connect(self.video_information)

        #Hidden

        self.title_label = QLabel(self)
        self.title_label.setGeometry(QRect(10, 100, 591, 61))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWordWrap(True)

        self.main_image = QWebView(self)
        self.main_image.setGeometry(QRect(160, 160, 300, 230))

        self.select_label = QLabel('Выберите качество', self)
        self.select_label.setGeometry(QRect(110,390,381,31))
        self.select_label.setStyleSheet("color:rgb(255, 153, 0)")
        self.select_label.setAlignment(Qt.AlignCenter)

        self.box_formats = QComboBox(self)
        self.box_formats.setGeometry(QRect(250,430,111,31))

        self.save_btn = QPushButton('Загрузить', self)
        self.save_btn.setGeometry(QRect(230,510,151,31))
        self.save_btn.clicked.connect(self.save)
        

        self.widgets = (self.title_label, self.main_image, self.box_formats, self.select_label, self.save_btn)
        for widget in self.widgets: widget.hide()

        # self.setStyleSheet('background-color:black;')
        self.setGeometry(600,400,640,571)
        self.show()

    def save(self):
        url=self.url_line.text()
        format=self.box_formats.currentText()

        try:
            download_video(url=url, format=format)
            QMessageBox.about(self, 'Уведомление', 'Скачивание завершено!')
            for widget in self.widgets: widget.hide()
            self.url_line.clear()
            self.box_formats.clear()

        except Exception as error:
            QMessageBox.about(self, 'Уведомление', 'Ошибка. Проверьте вашу ссылку')


    def video_information(self):
        url = self.url_line.text()
        self.box_formats.clear()
        try:
            if len(url) > 0:
                video = get_info(url)

                self.title_label.setText(video['title'])
                self.main_image.setUrl(QUrl(video['thumbnail']))
                
                for key, value in video['formats'].items():
                    self.box_formats.addItem(value)
        
                for widget in self.widgets: widget.show()

            else:
                QMessageBox.about(self, 'Уведомление', 'Вы не выбрали ссылку')
                
                # error_message = QErrorMessage(self)
                # error_message.setObjectName('nig')
                # error_message.showMessage('<h4>Неправильная ссылка!</h4>')
        except Exception:
            QMessageBox.about(self, 'Уведомление', 'Ошибка. Проверьте вашу ссылку')


#for testing urls
# https://rt.pornhub.com/view_video.phttps://rt.pornhub.com/view_video.php?viewkey=1048712502hp?viewkey=1048712502
# https://rt.pornhub.com/view_video.php?viewkey=ph5cadead5e80d5
run_app = QApplication(sys.argv)
app = App()
style = ' '
with open('style.css', 'r') as file:
    for line in file:
        style += line

app.setStyleSheet(style)
sys.exit(run_app.exec_())
