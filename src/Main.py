import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLayout, QDialog, QMessageBox, QPushButton,QVBoxLayout
from PyQt5.QtCore import QTimer
from src.ui_untitled import Ui_MainWindow
from Login import Login_Window


import users
from users import  User
from Login import Login_Window

class MillionerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, questions,user):
        super().__init__()
        self.setupUi(self)
        self.user=user
        self.buttons=[
            self.Odpowiedz1,
            self.Odpowiedz2,
            self.Odpowiedz3,
            self.Odpowiedz4
        ]
        for idx, btn in enumerate(self.buttons):
            btn.clicked.connect(lambda checked, i=idx: self.check_answers(i))
        self.questions=questions
        #Koła ratunkowe
        self.fortyforty=QPushButton("pół na pół:100000",self)
        self.fortyforty.setGeometry(0,200,150,50)
        self.fortyforty.clicked.connect(self.ftyfty)
        self.friends=QPushButton("Telefon do przyjaciela:50000",self)
        self.friends.setGeometry(0,300,200,50)
        self.friends.clicked.connect(self.fnds)
        #
        self.setWindowTitle("Milionerzy")
        self.current_question=self.questions
        self.currennt_index=0
        self.show_questions()
        Przyjaciele(correct=self.questions[self.currennt_index]["correct"], game_window=self)
        self.o = Przyjaciele(correct=self.questions[self.currennt_index]["correct"], game_window=self)
        #o.exec_()
        self.Pytanie.setStyleSheet("""
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border: 2px solid white;
                border-radius: 10px;
                padding: 4px;
                font-size: 12px;
                """)
        self.setStyleSheet("""
         QMainWindow{
         border-image:url(":/resources/Tlo5.jpg") 0 0 0 0 stretch stretch;
         }  
         QPushButton{
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border: 2px solid white;
                border-radius: 10px;
                padding: 2px;
                font-size: 12px;
         
         } 
       """ )
        self.Pytanie.setGeometry(10, 20, 201, 16)
        self.Pytanie.setFixedSize(500, 40)
        self.gridLayoutWidget.setGeometry(0, 460, 331, 111)
        self.Nr_pytania.setGeometry(0, 420, 64, 23)
        self.Ile_za_pytanie.setGeometry(0, 370, 64, 23)
        self.Ile_za_pytanie.setFixedSize(80,50)
        self.Nr_pytania.setFixedSize(80,40)
        self.Suma.setGeometry(350, 430, 81, 51)
        self.Suma.setFixedSize(200,140)
        self.Suma.setDigitCount(10)
        self.Ile_za_pytanie.setDigitCount(6)
        font = self.Pytanie.font()
        font.setPointSize(11)
        self.Pytanie.setFont(font)
        self.show_answers()
        self.Ile_za_pytanie.setEnabled(True)
        self.Nr_pytania.setEnabled(True)
    def porazka(self):
        print("porazka")
        QMessageBox.information(self, "Porażka!",f"Przegrałeś z wynikiem{self.Suma.intValue()}")
        self.close()
    def fnds(self):
        if self.Suma.intValue()>=50000:
            self.setStyleSheet("""
                        QMainWindow{
                            border-image:url(":/resources/KR.jpg") 0 0 0 0 stretch stretch;
                        }  
                    """)
            QMessageBox.information(self,"Ostrzeżenie","3 wybory dają prawidłową odpowiedź z 75% prawdopodobieństwem ale jeden zawsze daje złą")
            teraz=self.Suma.intValue()
            pozniej=teraz-50000
            self.Suma.display(pozniej)
            self.o.exec_()
        else:
            QMessageBox.information(self,"Odmowa","Nie stać cię")
    def ftyfty(self):
        if self.Suma.intValue()>=100000:
            self.setStyleSheet("""
                        QMainWindow{
                            border-image:url(":/resources/KR.jpg") 0 0 0 0 stretch stretch;
                        }  
                    """)
            correct=self.questions[self.currennt_index]["correct"]
            wrong=[i for i in range(4) if i!=correct]
            podswietl=random.sample(wrong,2)
            for i in podswietl:
                self.buttons[i].setStyleSheet("""
                     background-color: rgba(255, 0, 0, 100); 
                    color: white;
                    border: 1px solid darkred;
                    font-style: italic;
                """)
            aktualna=self.Suma.intValue()
            nowa=aktualna-100000
            self.Suma.display(nowa)
        else:
            QMessageBox.information(self,"Odmowa","Nie stać cię")


    def show_questions(self):
        for btn in self.buttons:
            btn.setStyleSheet("")
        q=self.current_question[self.currennt_index]
        self.Pytanie.setText(q["text"])
        self.Ile_za_pytanie.display(2000+self.currennt_index*99000)
        self.Nr_pytania.display(self.currennt_index+1)

    def show_answers(self):
        a=self.current_question[self.currennt_index]
        odp=a["answers"]
        for i, btn in enumerate(self.buttons):
            btn.setText(odp[i])
    def check_answers(self,answer_index):
        c=self.current_question[self.currennt_index]
        podp=c["correct"]
        print(podp)
        print(answer_index)
        if answer_index==podp:
            self.buttons[answer_index].setStyleSheet("background-color: lightgreen;")

            if self.currennt_index==0:
                self.Suma.display(2000)
            else:
                aktualna=self.Suma.intValue()
                nowa=aktualna+99000*self.currennt_index +2000
                self.Suma.display(nowa)
            self.currennt_index += 1
            print(f"Index: {self.currennt_index}")
            print(f"Aktualna suma: {self.Suma.intValue()}")

            if self.currennt_index>=len(self.questions):
                self.setStyleSheet("""
                                    QMainWindow{
                                        border-image:url(":/resources/Wygrana.jpg") 0 0 0 0 stretch stretch;
                                    }   
                                """)
                QMessageBox.information(self,"Gratulacje",f"Wygrałeś {self.Suma.intValue()} złotych")

                self.user.update_score(self.Suma.intValue())
                QTimer.singleShot(1000, QApplication.quit)
                
            else:
                QTimer.singleShot(1000,self.show_questions)
                self.show_answers()

        else:
            self.buttons[answer_index].setStyleSheet("background-color: lightcoral;")
            QApplication.processEvents()
            self.user.update_score(self.Suma.intValue())
            if self.Suma.intValue()==0:
                self.setStyleSheet("""
                    QMainWindow{
                        border-image:url(":/resources/Wstyd.png") 0 0 0 0 stretch stretch;
                    }   
                """)
            QTimer.singleShot(3000,self.porazka)


#pytania=[{"text":"1"},{"text":"2"}]
def wczytaj_Pytania(nazwa):
    pytania = []
    with open(nazwa, "r", encoding="utf8") as plik:
        for linia in plik:
            czesci = linia.strip().split(';')
            if len(czesci) == 6:
                pytania.append({
                    "text": czesci[0],
                    "answers": czesci[1:5],
                    "correct": int(czesci[5])
                })
            else:
                print(len(czesci))
                print("błąd wczytaj_Pytania")
        return pytania
def current_quest(questions,k):
    try:
        return random.sample(questions,5)
    except ValueError as e:
        raise ValueError("długość listy pytań mniejsza niż k") from e



def run_main_game():
    #app = QApplication(sys.argv)
    login = Login_Window()
    login.exec_()
    #sys.exit(app.exec_())

class Przyjaciele(QDialog):
    def __init__(self,correct,game_window,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Przyjaciele")
        self.resize(380,350)
        self.correct=correct
        self.game_window=game_window
        self.wrong=[i for i in range(4) if i!=correct]
        layout = QVBoxLayout()
        self.Liar_index = random.choice([0, 1, 2, 3])
        self.setStyleSheet("""
                        QDialog {
                            background-color: rgba(60, 60, 60, 160);
                            color: white;
                            font-size: 14px;
                            border: 2px solid rgba(255, 255, 255, 0.2);
                            border-radius: 12px;
                            padding: 10px;
                        }
        """)
        self.setLayout(layout)
        self.P1=QPushButton("",self)
        self.P1.setGeometry(0,0,150,150)
        self.P1.setStyleSheet("""
            border-image: url(":/resources/winnie.jpeg") 0 0 0 0 stretch stretch;
            
        """)
        self.P2=QPushButton("",self)
        self.P2.setGeometry(180,0,150,150)
        self.P2.setStyleSheet("""
             border-image: url(":/resources/Jp2.jpg") 0 0 0 0 stretch stretch;
        """)
        self.P3 = QPushButton("", self)
        self.P3.setGeometry(0, 155, 150, 150)
        self.P3.setStyleSheet("""
                    border-image: url(":/resources/Rmc.webp") 0 0 0 0 stretch stretch;
               """)
        self.P4 = QPushButton("", self)
        self.P4.setGeometry(180, 155, 150, 150)
        self.P4.setStyleSheet("""
                           border-image: url(":/resources/tom.jpg") 0 0 0 0 stretch stretch;
                      """)
        self.buttons = [self.P1, self.P2, self.P3, self.P4]

        self.P1.clicked.connect(lambda: self.friendcall(0))
        self.P2.clicked.connect(lambda: self.friendcall(1))
        self.P3.clicked.connect(lambda: self.friendcall(2))
        self.P4.clicked.connect(lambda: self.friendcall(3))
    def friendcall(self,index):
        if index==self.Liar_index:
            self.game_window.buttons[random.choice(self.wrong)].setStyleSheet("""
                background-color: rgba(0, 120, 255, 150);
                color: white;
                border: 1px solid white;
                font-weight: bold;
            """)
        else:
            pula=[self.correct]*9 + self.wrong
            self.game_window.buttons[random.choice(pula)].setStyleSheet("""
                background-color: rgba(0, 120, 255, 150);
                color: white;
                border: 1px solid white;
                font-weight: bold;
            """)
        self.close()






