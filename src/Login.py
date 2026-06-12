import os.path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLayout, QLineEdit, QMessageBox, QDialog
from PyQt5.QtCore import QTimer
from src.ui_login import Ui_Login
import users
from users import User


class Login_Window(QDialog, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.create_user)
        self.pushButton.setStyleSheet("""
          QPushButton {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border: 2px solid white;
                border-radius: 10px;
                padding: 4px;
                font-size: 12px;
            }
            
        """)
        self.setWindowTitle("Login")
        if os.path.exists("wyniki.txt"):
            with open("wyniki.txt","r",encoding="utf-8") as f:
                zawart=[line for line in f if line.strip()]
                if not zawart:
                    self.setStyleSheet("""
                               QDialog{
                                    border-image: url(":/resources/Tlo3.jpg") 0 0 0 0 stretch stretch;
                               }

                           """)
                else:
                    self.setStyleSheet("""
                        QDialog{
                            border-image: url(":/resources/Tlo4.png") 0 0 0 0 stretch stretch;
                        }

                    """)
        else:
            self.setStyleSheet("""
                                    QDialog{
                                        border-image: url(":/resources/Tlo4.png") 0 0 0 0 stretch stretch;
                                    }

                                """)







    def create_user(self):
        from Main import MillionerWindow, wczytaj_Pytania, current_quest
        username=self.lineEdit.text().strip()
        if not username:
            QMessageBox.warning(self,"Błąd","Brak nazwy")
        else:
            found=False
            if os.path.exists("wyniki.txt"):
                with open("wyniki.txt","r",encoding="utf-8")as f:
                    for line in f:
                        existing_name,_=line.strip().split(";")
                        if existing_name==username:

                            found=True
            self.user = User(username)
            if found==False:
                self.user.save_score()
                QMessageBox.information(self,"OK","Użytkownik zapisany")
                QMessageBox.information(self,"OK",f"{self.user.name},{self.user.score}")
                questions = current_quest(wczytaj_Pytania("Pytania.txt"), 5)
                print("wczytano pytania i wylosowano")
                self.main_win = MillionerWindow(questions, self.user)
                self.main_win.show()
                self.close()
            else:
                QMessageBox.information(self, "Ok", "Zalogowano")


                questions = current_quest(wczytaj_Pytania("Pytania.txt"), 5)
                print("wczytano pytania i wylosowano")
                self.main_win = MillionerWindow(questions, self.user)
                self.main_win.show()
                self.close()





