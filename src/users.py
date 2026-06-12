import  os
from venv import create

from PyQt5.QtWidgets import QApplication, QMessageBox


class User:
    def __init__(self,name,score=0):
        self.name=name
        self.score=score
        existing_score=self.load_score()
        if existing_score>score:
            self.score=existing_score
    def load_score(self):
        if not os.path.exists("wyniki.txt"):
            return 0
        else:
            with open("wyniki.txt","r",encoding="utf8") as f:
                for line in f:
                    uname,uscore=line.strip().split(";")
                    if uname==self.name:
                        return int(uscore)
            return 0
    def update_score(self,newscore):
       if newscore>self.score:
          self.score=newscore
          self.save_score()
    def save_score(self):
        print("save score")
        scores={}
        if os.path.exists("wyniki.txt"):
            with open("wyniki.txt","r",encoding="utf-8") as f:
                for line in f:
                    uname, uscore=line.strip().split(";")
                    scores[uname]=int(uscore)
        scores[self.name]=self.score
        with open("wyniki.txt","w",encoding="utf-8") as f:
            for uname,uscore in scores.items():
                f.write(f"{uname};{uscore}\n")


    @staticmethod
    def show_score():
        wyniki = []
        if os.path.exists("wyniki.txt"):
            with open("wyniki.txt", "r", encoding="utf-8") as file:
                for linia in file:
                    if ";" in linia:
                        nazwa, wynik = linia.strip().split(";")
                        wyniki.append((nazwa, int(wynik)))
        wyniki.sort(key=lambda x: x[1], reverse=True)
        return [f"{i + 1}. {n} — {w} pkt" for i, (n, w) in enumerate(wyniki)]










