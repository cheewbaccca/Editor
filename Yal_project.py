import sys
from PyQt5.Qt import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QTextEdit, QFileDialog, QFontComboBox, \
    QComboBox, QLabel, QColorDialog, QDialogButtonBox, QMessageBox


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Word v. 0.2')
        self.setGeometry(400, 200, 1000, 800)
        self.file = ''
        self.text = QTextEdit()
        self.setCentralWidget(self.text)

        self.status = QLabel('Количество слов: 0\nКоличество линий:0', self)
        self.status.adjustSize()
        self.colors = {"Чёрный": QColor('#000000'),
                       "Красный": QColor('#ff0000'),
                       "Зеленый": QColor('#008000'),
                       "Синий": QColor('#0000ff'),
                       "Серый": QColor('#808080')}

        self.createMenubar()
        self.fonts()
        self.formattingbar()

        self.text.cursorPositionChanged.connect(self.counter)

    def resizeEvent(self, event):
        self.status.move(5, self.height() - 50)

    def closeEvent(self, event):
        if len(self.text.toPlainText().split()) != 0:
            otvet = QMessageBox.question(self, 'Editor',
                                         'Сохранить изменения?', QMessageBox.Yes, QMessageBox.No)
        else:
            return
        if otvet == QMessageBox.Yes:
            self.save()
            event.accept()

    def counter(self):
        c = self.text.textCursor()
        self.status.setText(f"Количество слов: {len(self.text.toPlainText().split())}\nКоличество линий:"
                            f"{c.blockNumber()}")
        self.status.adjustSize()

    def createMenubar(self):  # создание меню
        menu = self.menuBar()

        file = menu.addMenu('Файл')
        edit = menu.addMenu('Редактировать')

        newfile = QAction('Создать', self)
        openfile = QAction('Открыть', self)
        savefile = QAction('Сохранить', self)

        file.addAction(newfile)
        file.addAction(openfile)
        file.addAction(savefile)

        newfile.triggered.connect(self.new)
        openfile.triggered.connect(self.open)
        savefile.triggered.connect(self.save)

    def new(self):  # функции для нового файла,открытия и сохранения файла
        file = Editor()
        file.show()

    def open(self):  # открытие
        try:
            self.file = QFileDialog.getOpenFileName(self, 'Открыть файл', ".", "(*.txt)")[0]
            with open(self.file, 'r') as f:
                self.text.setText(f.read())
        except FileNotFoundError:
            pass

    def save(self):
        try:
            if not self.file:  # если файл ещё без имени
                self.file = QFileDialog.getSaveFileName(self, 'Сохранить файл', ".", "(*.txt)")[0]
            with open(self.file, 'w') as f:
                f.write(self.text.toPlainText())
        except FileNotFoundError:
            pass

    def fonts(self):  # тулбар шрифтов
        self.fontbar = self.addToolBar('Шрифты')

        fonts = QFontComboBox(self)  # ComboBox-ы шрифтов
        fonts_sizes = QComboBox(self)
        fonts_sizes.setEditable(True)
        font_color = QComboBox(self)
        italic = QAction('Italic', self)
        underline = QAction('Underline', self)             # ТОЖЕ ИКОНКИ!!!!
        choosebackground = QAction('Фон текста', self)

        self.fontbar.addWidget(fonts)  # добавление в menubar

        self.fontbar.addWidget(fonts_sizes)
        self.fontbar.addWidget(font_color)
        self.fontbar.addSeparator()
        self.fontbar.addAction(choosebackground)
        self.fontbar.addAction(italic)
        self.fontbar.addAction(underline)


        fonts.setToolTip('Выбрать шрифт')
        choosebackground.setToolTip('Выбрать фон шрифта')
        fonts_sizes.setToolTip('Выбрать размер шрифта')
        font_color.setToolTip('Выбрать цвет шрифта')
        italic.setToolTip('Курсив')
        underline.setToolTip('Подчёркивание')

        fonts.currentFontChanged.connect(self.fontchanged)
        choosebackground.triggered.connect(self.background)
        fonts_sizes.activated.connect(self.newsize)
        font_color.activated.connect(self.newcolor)
        italic.triggered.connect(self.italic)
        underline.triggered.connect(self.underline)

        sizes = ['8', '9', '10', '11', '12', '14', '16', '18',
                 '20', '22', '24', '26', '28', '36', '48', '72', '80', '96']  # размеры текста

        for i in sizes:
            fonts_sizes.addItem(i)

        for j in self.colors.keys():
            font_color.addItem(j)

    def fontchanged(self, newfont):
        self.text.setCurrentFont(newfont)

    def newsize(self, size):
        self.text.setFontPointSize(size)

    def newcolor(self, color):

        col = list(self.colors.keys())[color]
        self.text.setTextColor(self.colors[col])

    def background(self):
        bckground = QColorDialog.getColor()
        self.text.setTextBackgroundColor(bckground)

    def italic(self):
        if self.text.fontItalic():
            self.text.setFontItalic(False)
        else:
            self.text.setFontItalic(True)

    def underline(self):
        if self.text.fontUnderline():
            self.text.setFontUnderline(False)
        else:
            self.text.setFontUnderline(True)
    # ДАЛЬШЕ BOLD,ITALIC И ТД, ALLIGNMENT И ТД!!!!!!!!

    def formattingbar(self):  # тулбар форматирования             # здесь должны быть ИКОНКИ!!!!!
        self.fontbar = self.addToolBar('Форматирование')
        viravnivanie_left = QAction('left!', self)
        viravnivanie_left.triggered.connect(self.left)

        viravnivanie_center = QAction('center!', self)
        viravnivanie_center.triggered.connect(self.center)

        viravnivanie_right = QAction('right!', self)
        viravnivanie_right.triggered.connect(self.right)

        self.fontbar.addAction(viravnivanie_left)
        self.fontbar.addAction(viravnivanie_right)
        self.fontbar.addAction(viravnivanie_center)

    def left(self):
        self.text.setAlignment(Qt.AlignLeft)

    def right(self):
        self.text.setAlignment(Qt.AlignRight)

    def center(self):
        self.text.setAlignment(Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication([])
    edit = Editor()
    edit.show()
    sys.exit(app.exec_())
