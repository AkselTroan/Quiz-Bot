from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from PyQt5 import QtGui
import quizbot as bot


def run():
    class WidgetGallery(QDialog):
        def __init__(self, parent=None):
            super(WidgetGallery, self).__init__(parent)

            self.setFixedHeight(900)
            self.setFixedWidth(1100)

            self.originalPalette = QApplication.palette()
            self.setWindowTitle('Quiz Bot')
            self.setWindowIcon(QtGui.QIcon("Resources/icon.png"))
            styleComboBox = QComboBox()
            styleComboBox.addItems(QStyleFactory.keys())

            disableWidgetsCheckBox = QCheckBox("&Disable widgets")

            self.createTopLeftGroupBox()
            self.createTopMiddleGroupBox()
            self.createTopRightGroupBox()
            self.createBottomLeftTabWidget()
            self.createBottomMiddleGroupBox()
            self.createBottomRightGroupBox()
            self.createProgressBar()

            disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
            disableWidgetsCheckBox.toggled.connect(self.topMiddleGroupBox.setDisabled)
            disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
            disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
            disableWidgetsCheckBox.toggled.connect(self.bottomMiddleGroupBox.setDisabled)
            disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

            mainLayout = QGridLayout()
            mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
            mainLayout.addWidget(self.topMiddleGroupBox, 1, 1)
            mainLayout.addWidget(self.topRightGroupBox, 1, 2)
            mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
            mainLayout.addWidget(self.bottomMiddleGroupBox, 2, 1)
            mainLayout.addWidget(self.bottomRightGroupBox, 2, 2)
            mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
            mainLayout.setRowStretch(1, 1)
            mainLayout.setRowStretch(2, 1)
            mainLayout.setColumnStretch(0, 1)
            mainLayout.setColumnStretch(1, 1)
            self.setLayout(mainLayout)


        def advanceProgressBar(self):
            curVal = self.progressBar.value()
            maxVal = self.progressBar.maximum()
            self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

        def advanceLog(self):
            global new_log
            temp = self.log
            new_logs = new_log
            temp.append(new_logs)
            self.bottomRightGroupBox.log.setText(temp)


        def createTopLeftGroupBox(self):
            self.topLeftGroupBox = QGroupBox("Members")

            radioButton1 = QRadioButton("Radio button 1")
            radioButton2 = QRadioButton("Radio button 2")
            radioButton3 = QRadioButton("Radio button 3")
            radioButton1.setChecked(True)

            checkBox = QCheckBox("Tri-state check box")
            checkBox.setTristate(True)
            checkBox.setCheckState(Qt.PartiallyChecked)

            layout = QVBoxLayout()
            layout.addWidget(radioButton1)
            layout.addWidget(radioButton2)
            layout.addWidget(radioButton3)
            layout.addWidget(checkBox)
            layout.addStretch(1)
            self.topLeftGroupBox.setLayout(layout)

        def createTopMiddleGroupBox(self):
            global playing_quiz
            self.topMiddleGroupBox = QGroupBox("Current Question")

            gm = QLabel("Gamemode: " + bot.current_gamemode)
            next_question = QPushButton("Next Question")
            question = QLabel('Question: playing = ' + bot.gamemode[0])
            answer = QLabel('Answer: asdwsdfsd')

            layout = QVBoxLayout()
            layout.addWidget(gm)
            layout.addWidget(question)
            layout.addWidget(answer)
            layout.addWidget(next_question)
            self.topMiddleGroupBox.setLayout(layout)

        def createTopRightGroupBox(self):
            self.topRightGroupBox = QGroupBox("Game settings")

            start_quiz_btn = QPushButton("Start quiz")
            start_quiz_btn.setDefault(False)

            stop_quiz_btn = QPushButton("Stop quiz")
            stop_quiz_btn.setDefault(False)

            pause_quiz_btn = QPushButton("Pause quiz")
            pause_quiz_btn.setDefault(False)

            command_label = QLabel("Commands")
            add_member_btn = QPushButton("Add member")
            add_member_btn.setDefault(False)

            remove_member_btn = QPushButton("Remove member")
            remove_member_btn.setDefault(False)

            give_points_btn = QPushButton("Give points")
            give_points_btn.setDefault(False)

            remove_points_btn = QPushButton("Remove points")
            remove_points_btn.setDefault(False)

            gamemode_label = QLabel("Gamemodes")
            free_for_all_btn = QPushButton("Free for All")
            free_for_all_btn.setDefault(False)


            layout = QVBoxLayout()
            layout.addWidget(start_quiz_btn)
            layout.addWidget(pause_quiz_btn)
            layout.addWidget(stop_quiz_btn)
            layout.addWidget(command_label)
            layout.addWidget(add_member_btn)
            layout.addWidget(remove_member_btn)
            layout.addWidget(give_points_btn)
            layout.addWidget(remove_points_btn)
            layout.addWidget(gamemode_label)
            layout.addWidget(free_for_all_btn)
            layout.addStretch(1)
            self.topRightGroupBox.setLayout(layout)

        def createBottomMiddleGroupBox(self):
            score = 'Aksel: 12'
            self.bottomMiddleGroupBox = QGroupBox("Scoreboard")

            aksScore = QLabel('Aksel 2 poeng')
            leader = QLabel("Current leader: Aksel")

            layout = QVBoxLayout()
            layout.addWidget(aksScore)
            layout.addWidget(leader)
            self.bottomMiddleGroupBox.setLayout(layout)

        def createBottomLeftTabWidget(self):
            self.bottomLeftTabWidget = QTabWidget()
            self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                    QSizePolicy.Ignored)

            tab1 = QWidget()
            tableWidget = QTableWidget(10, 10)

            tab1hbox = QHBoxLayout()
            tab1hbox.setContentsMargins(5, 5, 5, 5)
            tab1hbox.addWidget(tableWidget)
            tab1.setLayout(tab1hbox)

            tab2 = QWidget()
            textEdit = QTextEdit()

            textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                                  "How I wonder what you are.\n" 
                                  "Up above the world so high,\n"
                                  "Like a diamond in the sky.\n"
                                  "Twinkle, twinkle, little star,\n" 
                                  "How I wonder what you are!\n")

            tab2hbox = QHBoxLayout()
            tab2hbox.setContentsMargins(5, 5, 5, 5)
            tab2hbox.addWidget(textEdit)
            tab2.setLayout(tab2hbox)

            self.bottomLeftTabWidget.addTab(tab1, "&Table")
            self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

        def createBottomRightGroupBox(self):
            self.bottomRightGroupBox = QGroupBox("Log")
            self.log = QLabel(bot.logs)
            layout = QVBoxLayout()
            layout.addWidget(self.log)
            self.bottomRightGroupBox.setLayout(layout)

        def createProgressBar(self):
            self.progressBar = QProgressBar()
            self.progressBar.setRange(0, 10000)
            self.progressBar.setValue(0)

            timer = QTimer(self)
            timer.timeout.connect(self.advanceProgressBar)
            timer.start(1000)


    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()

    from asyncqt import QEventLoop
    loop = QEventLoop(app)

    while loop:
        new_log = input("Insert new log: ")
    sys.exit(app.exec_())
