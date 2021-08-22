import sys
from random import randint
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QStyleFactory,
    QGroupBox,
    QComboBox,
    QDialog,
    QTabWidget,
    QSizePolicy,
    QGridLayout,
    QHBoxLayout,
    QTableWidget,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QTextEdit,
    QLineEdit,
    QMessageBox,
)


class Member:
    def __init__(self, name, points):
        self.name = name
        self. points = points


aksel = Member('Aksel', 0)
kenneth = Member('Kenneth', 0)
roger = Member('Roger', 0)

all_members = [aksel, kenneth, roger]
#scoreboard = QLabel("Init")
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Create pop up windows =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class AddMemberWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Add new member")
        self.label1 = QLabel("Name")
        self.name_member = QLineEdit()
        self.label2 = QLabel("Amount of starting points. Default: 0")
        self.start_points = QLineEdit()
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.clicked.connect(lambda: self.submit_new_member())

        layout.addWidget(self.label)
        layout.addWidget(self.label1)
        layout.addWidget(self.name_member)
        layout.addWidget(self.label2)
        layout.addWidget(self.start_points)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def submit_new_member(self):
        global all_members
        temp = []
        for member in all_members:
            temp.append(member.name)
        if self.name_member.text() in temp:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('Error! Member: ' + self.name_member.text() + " already exists")
        else:
            if self.start_points.text() == "":  # If the user do not admit a starting point; default 0 points
                self.start_points.text = "0"

            new_member = Member(self.name_member.text(), int(self.start_points.text))
            all_members.append(new_member)
            QMessageBox.question(self, "", "You have added member: " + self.name_member.text() + " with " +
                                 self.start_points.text + " points", QMessageBox.Ok, QMessageBox.Ok)
            self.close()
            for member in all_members:
                print("Name: " + member.name + " Points: " + str(member.points))


class RemoveMemberWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Name of member to remove")
        self.member_remove = QLineEdit()
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.clicked.connect(lambda: self.submit_removal())

        layout.addWidget(self.label)
        layout.addWidget(self.member_remove)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def submit_removal(self):  # This function has been tested and works as intended
        global all_members
        removed_member = False
        for member in all_members:
            if member.name.upper() == self.member_remove.text().upper():
                all_members.remove(member)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Successfully removed " + member.name + " from the quiz!")
                msg.setWindowTitle("Success")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                removed_member = True
                self.close()  # Close window

        if removed_member is not True:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('Error! Could not find submitted member to remove. Please try again')


class GrantPointsWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Grant Points to a member")
        self.pointmember = QLineEdit()
        self.label2 = QLabel("Member: ")
        self.label3 = QLabel("How many points will you grant? Give numbers only")
        self.points = QLineEdit()
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.clicked.connect(lambda: self.grant_points())

        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.pointmember)
        layout.addWidget(self.label3)
        layout.addWidget(self.points)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def grant_points(self):
        global all_members
        i = 1
        for member in all_members:
            if member.name != self.pointmember.text():
                if i == len(all_members):  # The function of this if statement is to only spawn one new window
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.showMessage('Error! Could not find submitted member. Please try again')
                i += 1

            elif member.name == self.pointmember.text():
                all_members.remove(member)
                member.points += int(self.points.text())
                all_members.append(member)

                # Update scoreboard
                update_scoreboard(self)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("You have granted " + self.points.text() + " points to " + member.name)
                msg.setDetailedText(member.name + " has now a total of " + str(member.points) + " points")
                msg.setWindowTitle("Success")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                self.close()  # Close window
                break


class RemovePointsWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Remove points to a member")
        self.pointmember = QLineEdit()
        self.label2 = QLabel("Member: ")
        self.label3 = QLabel("How many points will you remove? Give numbers only")
        self.points = QLineEdit()
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.clicked.connect(lambda: self.remove_points())

        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.pointmember)
        layout.addWidget(self.label3)
        layout.addWidget(self.points)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def remove_points(self):  # This function has been tested and works as intended
        global all_members, scoreboard
        i = 1
        for member in all_members:
            if member.name != self.pointmember.text():
                if i == len(all_members):  # The function of this if statement is to only spawn one new window
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.showMessage('Error! Could not find submitted member. Please try again')
                i += 1

            elif member.name == self.pointmember.text():
                all_members.remove(member)
                member.points -= int(self.points.text())
                all_members.append(member)

                update_scoreboard(self)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("You have removed " + self.points.text() + " points from " + member.name)
                msg.setDetailedText(member.name + " has now " + str(member.points) + " points")
                msg.setWindowTitle("Success")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                self.close()  # Close window
                break


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        # These are pop up windows from the buttons
        self.add_member_window = AddMemberWindow()
        self.remove_member_window = RemoveMemberWindow()
        self.grant_points_window = GrantPointsWindow()
        self.remove_points_window = RemovePointsWindow()

        self.setWindowTitle('Quiz Bot')

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopMiddleGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomMiddleGroupBox()
        self.createBottomRightGroupBox()

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
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()

        else:
            window.show()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Create group boxes =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Members")

        layout = QVBoxLayout()
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopMiddleGroupBox(self):
        global playing_quiz
        self.topMiddleGroupBox = QGroupBox("Current Question")

        gm = QLabel("Gamemode: " + "bot.current_gamemode")
        next_question = QPushButton("Next Question")
        question = QLabel('Question: playing = ' + "bot.gamemode[0]")
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

        command_label = QLabel("Commands")  # Used to separate the different buttons.

        add_member_btn = QPushButton("Add member", self)
        add_member_btn.setDefault(False)
        add_member_btn.clicked.connect(
                lambda checked: self.toggle_window(self.add_member_window)
             )

        remove_member_btn = QPushButton("Remove member")
        remove_member_btn.setDefault(False)
        remove_member_btn.clicked.connect(
                lambda checked: self.toggle_window(self.remove_member_window)
             )

        give_points_btn = QPushButton("Grant points")
        give_points_btn.setDefault(False)
        give_points_btn.clicked.connect(
                lambda checked: self.toggle_window(self.grant_points_window)
             )

        remove_points_btn = QPushButton("Remove points")
        remove_points_btn.setDefault(False)
        remove_points_btn.clicked.connect(
                lambda checked: self.toggle_window(self.remove_points_window)
             )

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
        global all_members, scoreboard

        scores = update_scoreboard(self)
        self.bottomMiddleGroupBox = QGroupBox("Scoreboard")


        leader = QLabel("Current leader: Aksel")

        layout = QVBoxLayout()
        layout.addWidget(scores)
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
        self.log = QLabel("str(bot.logs)")
        layout = QVBoxLayout()
        layout.addWidget(self.log)
        self.bottomRightGroupBox.setLayout(layout)


def update_scoreboard(self):
    global all_members
    scoreboard = QLabel("Init")
    new_scores = []
    # Update scoreboard
    for updated_member in all_members:
        new_scores.append(updated_member.name)
        new_scores.append(updated_member.points)
    scoreboard.setText(str(new_scores))
    return scoreboard


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
