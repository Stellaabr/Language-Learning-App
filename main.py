import sys
import random
import pandas as pd
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont


class SplashScreen(QtWidgets.QWidget):
    """Загрузочный экран приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Language Learning App")
        self.setGeometry(100, 100, 1600, 1200)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")


        qt_rectangle = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())


        self.theme_switcher = QtWidgets.QCheckBox("Theme", self)
        self.theme_switcher.setGeometry(30, 30, 150, 30)
        self.theme_switcher.setStyleSheet("color: white;")
        self.theme_switcher.stateChanged.connect(self.toggle_theme)
        self.theme_dark = True


        self.button = QtWidgets.QPushButton("Start Learning", self)
        self.button.setGeometry(700, 500, 200, 200)
        self.button.setStyleSheet("""
            background-color: red; 
            border: none;
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        self.button.clicked.connect(self.open_main_window)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def toggle_theme(self):
        """Переключение между темами"""
        if self.theme_switcher.isChecked():
            self.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.theme_switcher.setStyleSheet("color: black;")
            self.button.setStyleSheet("background-color: red; color: black;")
            self.theme_dark = False
        else:
            self.setStyleSheet("background-color: rgb(0, 0, 0);")
            self.theme_switcher.setStyleSheet("color: white;")
            self.button.setStyleSheet("background-color: red; color: white;")
            self.theme_dark = True

    def open_main_window(self):
        """Открытие главного окна"""
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(self.theme_dark)
        self.ui.setupUi(self.main_window)
        self.main_window.show()
        self.close()


class Ui_MainWindow(object):
    """Пользовательский интерфейс главного окна"""

    def __init__(self, theme_dark):
        self.theme_dark = theme_dark
        try:
            self.df = pd.read_excel("languages.xlsx")
            self.previous_index = -1  # Для избежания повторений слов
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(None, "Error", "Could not find languages.xlsx file")
            sys.exit(1)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Ltranslate")
        MainWindow.setFixedSize(800, 600)


        if self.theme_dark:
            self.bg_color = "rgb(0, 0, 0)"
            self.text_color = "rgb(255, 255, 255)"
            self.border_color = "#555"
        else:
            self.bg_color = "rgb(255, 255, 255)"
            self.text_color = "rgb(0, 0, 0)"
            self.border_color = "#ddd"

        MainWindow.setStyleSheet(f"background-color: {self.bg_color};")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.button_style = f"""
            QPushButton {{
                background-color: qradialgradient(
                    spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                    stop:0 rgba(255, 235, 235, 206),
                    stop:0.35 rgba(255, 188, 188, 80),
                    stop:0.4 rgba(255, 162, 162, 80),
                    stop:0.425 rgba(255, 132, 132, 156),
                    stop:0.44 rgba(252, 128, 128, 80),
                    stop:1 rgba(255, 255, 255, 0)
                );
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                color: {self.text_color};
            }}
            QPushButton:hover {{
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(130, 0, 9, 150),
                    stop:1 rgba(90, 0, 9, 50)
                );
            }}
        """


        self.English = QtWidgets.QPushButton("English", self.centralwidget)
        self.English.setGeometry(QtCore.QRect(500, 400, 131, 111))

        self.German = QtWidgets.QPushButton("German", self.centralwidget)
        self.German.setGeometry(QtCore.QRect(500, 230, 131, 111))

        self.French = QtWidgets.QPushButton("French", self.centralwidget)
        self.French.setGeometry(QtCore.QRect(500, 70, 131, 111))


        for button in [self.English, self.German, self.French]:
            button.setStyleSheet(self.button_style)


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-370, 0, 1021, 591))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("at.jpg"))
        self.label.setObjectName("label")


        self.translation_label = QtWidgets.QLabel(self.centralwidget)
        self.translation_label.setGeometry(QtCore.QRect(30, 445, 270, 41))
        self.translation_label.setAlignment(QtCore.Qt.AlignCenter)

        self.word_label = QtWidgets.QLabel(self.centralwidget)
        self.word_label.setGeometry(QtCore.QRect(30, 100, 270, 80))
        self.word_label.setAlignment(QtCore.Qt.AlignCenter)


        self.word_label.setObjectName("word_label")
        self.translation_label.setObjectName("translation_label")


        label_style = f"""
            QLabel {{
                background-color: {self.bg_color};
                color: {self.text_color};
                border: 1px solid {self.border_color};
                border-radius: 5px;
                padding: 5px;
            }}
        """



        self.word_label.setStyleSheet(label_style)
        self.translation_label.setStyleSheet(label_style)
        font = QFont()
        font.setPointSize(17)
        self.word_label.setFont(font)


        # Порядок отображения элементов
        self.label.lower()
        for widget in [self.English, self.German, self.French,
                       self.translation_label, self.word_label]:
            widget.raise_()

        MainWindow.setCentralWidget(self.centralwidget)


        self.English.clicked.connect(self.english_translate)
        self.German.clicked.connect(self.german_translate)
        self.French.clicked.connect(self.french_translate)

    def get_random_index(self):
        """Получение случайного индекса, отличного от предыдущего"""
        if len(self.df) <= 1:
            return 0

        index = self.previous_index
        while index == self.previous_index:
            index = random.randint(0, len(self.df) - 1)
        self.previous_index = index
        return index

    def english_translate(self):
        r = self.get_random_index()
        self.word_label.setText(self.df.iloc[r]['English'])
        self.translation_label.setText(self.df.iloc[r]['Russian'])

    def german_translate(self):
        r = self.get_random_index()
        self.word_label.setText(self.df.iloc[r]['German'])
        self.translation_label.setText(self.df.iloc[r]['Russian'])

    def french_translate(self):
        r = self.get_random_index()
        self.word_label.setText(self.df.iloc[r]['French'])
        self.translation_label.setText(self.df.iloc[r]['Russian'])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
