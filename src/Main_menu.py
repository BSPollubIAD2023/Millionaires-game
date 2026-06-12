import sys
from fileinput import close
from logging import critical
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLayout, QDialog, QTabWidget, QMessageBox,  QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import QTimer
from src.ui_Main_menu import Ui_MainMenu
from Main import run_main_game
from users import User
from PyQt5.QtWidgets import  QVBoxLayout, QTextEdit



class MainMenu(QDialog,Ui_MainMenu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Milionerzy")
        self.Nowa_gra.clicked.connect(self.nowagra)
        self.Tabela_wynikow.clicked.connect(self.tabelawynikow)
        self.Wyjdz.clicked.connect(self.wyjdz)
        self.Dodaj_pytania.clicked.connect(self.dodajpyt)


    def nowagra(self):
        print("nowa gra")
        run_main_game()
    def tabelawynikow(self):
        print("mkfmdgs")
        w=User.show_score()
        print(w)
        tekst="\n".join(w[:10])
        okno=TabelaWynikowDialog(tekst,self)


        okno.exec_()
    def wyjdz(self):
        print("koniec")
        exit(0)
    def dodajpyt(self):
        otwor=Napytania(self)
        otwor.exec_()

class TabelaWynikowDialog(QDialog):
    def __init__(self, tekst, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tabela Wyników")
        self.resize(400, 300)
        self.setStyleSheet("""
        QDialog{
            border-image: url(":/resources/Tlo2.jpg") 0 0 0 0 stretch stretch;
           
                           
        }                   
        """)
        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText(tekst)
        self.flip=QPushButton("Odwróć",self)
        self.flip.clicked.connect(self.rvs)

        self.textEdit.setStyleSheet("""
                    QTextEdit {
                        background-color: rgba(255, 255, 255, 180); 
                        color: black;
                        font-size: 14px;
                        border-radius: 10px;
                        padding: 10px;
                    }
                """)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.flip)
        self.setLayout(layout)

    def rvs(self):
        tekst = self.textEdit.toPlainText()
        linie = tekst.strip().splitlines()
        linie.reverse()
        self.textEdit.setPlainText("\n".join(linie))


class Napytania(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lista")
        self.resize(600,500)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet("""
        QDialog{
            background-image: url(":/resources/Tlo1.jpg");
            background-repeat: no-repeat;
            background-position: center;
        
        }
        """)

        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 180); 
                color: black;
                font-size: 14px;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.textEdit.setPlaceholderText(
            "Pytania trzeba podawać tak: linijka na pytanie, format: treść;Odp1;Odp2;Odp3;Odp4;Poprawna \n"
            "białe znaki mogą być w pytaniu ale nie mogą być po ; czli: czy ala ma kota;A;B;C;D;0 ok ale już czy ala ma kota; A ;B;C;D;0 już nie"

        )
        layout.addWidget(self.textEdit)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.save_btn = QPushButton("Zapisz wszystkie pytania", self)
        self.save_btn.clicked.connect(self.save_questions)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def save_questions(self):
        raw = self.textEdit.toPlainText().strip()
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if not lines:
            QMessageBox.warning(self, "Brak danych", "Nie wprowadzono żadnych pytań.")
            return

        valid_lines = []
        for line in lines:
            parts = line.split(";")
            if len(parts) == 6:
                valid_lines.append(line)


        if valid_lines:
            try:
                file_path = 'Pytania.txt'
                needs_newline = os.path.exists(file_path) and os.path.getsize(file_path) > 0
                with open(file_path, 'a', encoding='utf-8') as f:
                    if needs_newline:
                        f.write(os.linesep)
                    for vl in valid_lines:
                        f.write(vl + os.linesep)
            except Exception as e:
                QMessageBox.critical(self, "Błąd zapisu", f"Nie udało się zapisać pliku: {e}")
                return

        QMessageBox.information(self, "Zapisano", f"Zapisano {len(valid_lines)} poprawnych linii.")
        if valid_lines:
            self.textEdit.clear()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMessageBox QLabel {
            color: lightdark;
            font-size: 16px;
        }
        QMessageBox QPushButton {
            background-color: rgba(0, 0, 0, 180);
            color: white;
            border: 2px solid white;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 12px;
        }
        QMessageBox {
            background-color: #222; 
            border-radius: 10px;
        }
    """)
    window=MainMenu()
    window.show()
    sys.exit(app.exec_())
