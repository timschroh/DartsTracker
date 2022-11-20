from time import sleep
import const
import numpy 
from board_extraction import transform_point, deserialize_calib, serialize_calib, calib
from dart_extraction import get_dart_coordinates, get_dart_score, detect_dart
import cv2
import os
from PyQt5.QtCore import QThread, Qt
from PyQt5 import QtCore, QtGui, QtWidgets

aktiver_spieler = 0
Punktzahl = 501
Spieler_Punktzahl = [Punktzahl, Punktzahl]
Spieler_counter = 0 # spieler 1 = 0, Spieler 2 = 1
dart_counter = 0
transformation_matrices = []
ergebnis = 0

last_scores = [0,0,0],[0,0,0]

DartThread_active = False

cap1 = cv2.VideoCapture(3)#links
cap2 = cv2.VideoCapture(0)#rechts
cap3 = cv2.VideoCapture(1)#oben 

def img_resize(img):
    img = cv2.resize(img, (const.length, const.width))
    return img

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 603)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.spieler1_textbox = QtWidgets.QTextEdit(self.centralwidget)
        self.spieler1_textbox.setGeometry(QtCore.QRect(30, 20, 151, 41))
        self.spieler1_textbox.setObjectName("spieler1_textbox")
        self.spieler2_textbox = QtWidgets.QTextEdit(self.centralwidget)
        self.spieler2_textbox.setGeometry(QtCore.QRect(430, 20, 151, 41))
        self.spieler2_textbox.setObjectName("spieler2_textbox")
        self.letzteWuerfe1_label = QtWidgets.QLabel(self.centralwidget)
        self.letzteWuerfe1_label.setGeometry(QtCore.QRect(20, 100, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.letzteWuerfe1_label.setFont(font)
        self.letzteWuerfe1_label.setObjectName("letzteWuerfe1_label")
        self.last1_1_label = QtWidgets.QLabel(self.centralwidget)
        self.last1_1_label.setGeometry(QtCore.QRect(40, 130, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.last1_1_label.setFont(font)
        self.last1_1_label.setObjectName("last1_1_label")
        self.last2_1_label = QtWidgets.QLabel(self.centralwidget)
        self.last2_1_label.setGeometry(QtCore.QRect(40, 150, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.last2_1_label.setFont(font)
        self.last2_1_label.setObjectName("last2_1_label")
        self.last3_1_label = QtWidgets.QLabel(self.centralwidget)
        self.last3_1_label.setGeometry(QtCore.QRect(40, 170, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.last3_1_label.setFont(font)
        self.last3_1_label.setObjectName("last3_1_label")
        self.verbleibend1_label = QtWidgets.QLabel(self.centralwidget)
        self.verbleibend1_label.setGeometry(QtCore.QRect(160, 100, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.verbleibend1_label.setFont(font)
        self.verbleibend1_label.setObjectName("verbleibend1_label")
        self.remScore1_label = QtWidgets.QLabel(self.centralwidget)
        self.remScore1_label.setGeometry(QtCore.QRect(170, 120, 241, 91))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.remScore1_label.setFont(font)
        self.remScore1_label.setObjectName("remScore1_label")
        self.auswertung_label = QtWidgets.QLabel(self.centralwidget)
        self.auswertung_label.setGeometry(QtCore.QRect(10, 260, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.auswertung_label.setFont(font)
        self.auswertung_label.setObjectName("auswertung_label")
        self.dart1_label = QtWidgets.QLabel(self.centralwidget)
        self.dart1_label.setGeometry(QtCore.QRect(180, 310, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dart1_label.setFont(font)
        self.dart1_label.setObjectName("dart1_label")
        self.dart2_label = QtWidgets.QLabel(self.centralwidget)
        self.dart2_label.setGeometry(QtCore.QRect(380, 310, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dart2_label.setFont(font)
        self.dart2_label.setObjectName("dart2_label")
        self.dart3_label = QtWidgets.QLabel(self.centralwidget)
        self.dart3_label.setGeometry(QtCore.QRect(570, 310, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dart3_label.setFont(font)
        self.dart3_label.setObjectName("dart3_label")
        self.score1_label = QtWidgets.QTextEdit(self.centralwidget)
        self.score1_label.setGeometry(QtCore.QRect(150, 350, 111, 41))
        self.score1_label.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.score1_label.setObjectName("score1_label")
        self.score2_label = QtWidgets.QTextEdit(self.centralwidget)
        self.score2_label.setGeometry(QtCore.QRect(350, 350, 111, 41))
        self.score2_label.setObjectName("score2_label")
        self.score3_label = QtWidgets.QTextEdit(self.centralwidget)
        self.score3_label.setGeometry(QtCore.QRect(540, 350, 111, 41))
        self.score3_label.setObjectName("score3_label")
        self.gesamt_label = QtWidgets.QLabel(self.centralwidget)
        self.gesamt_label.setGeometry(QtCore.QRect(190, 450, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.gesamt_label.setFont(font)
        self.gesamt_label.setObjectName("gesamt_label")
        self.last3_2_label = QtWidgets.QLabel(self.centralwidget)
        self.last3_2_label.setGeometry(QtCore.QRect(440, 170, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.last3_2_label.setFont(font)
        self.last3_2_label.setObjectName("last3_2_label")
        self.remScore2_label = QtWidgets.QLabel(self.centralwidget)
        self.remScore2_label.setGeometry(QtCore.QRect(570, 120, 251, 91))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.remScore2_label.setFont(font)
        self.remScore2_label.setObjectName("remScore2_label")
        self.verbleibend2_label = QtWidgets.QLabel(self.centralwidget)
        self.verbleibend2_label.setGeometry(QtCore.QRect(560, 100, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.verbleibend2_label.setFont(font)
        self.verbleibend2_label.setObjectName("verbleibend2_label")
        self.letzteWuerfe2_label = QtWidgets.QLabel(self.centralwidget)
        self.letzteWuerfe2_label.setGeometry(QtCore.QRect(420, 100, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.letzteWuerfe2_label.setFont(font)
        self.letzteWuerfe2_label.setObjectName("letzteWuerfe2_label")
        self.last2_2_label = QtWidgets.QLabel(self.centralwidget)
        self.last2_2_label.setGeometry(QtCore.QRect(440, 150, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.last2_2_label.setFont(font)
        self.last2_2_label.setObjectName("last2_2_label")
        self.last1_2_label = QtWidgets.QLabel(self.centralwidget)
        self.last1_2_label.setGeometry(QtCore.QRect(440, 130, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.last1_2_label.setFont(font)
        self.last1_2_label.setObjectName("last1_2_label")
        self.gesScore_label = QtWidgets.QLabel(self.centralwidget)
        self.gesScore_label.setGeometry(QtCore.QRect(340, 420, 241, 91))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.gesScore_label.setFont(font)
        self.gesScore_label.setObjectName("gesScore_label")
        self.nextPlayer_button = QtWidgets.QPushButton(self.centralwidget)
        self.nextPlayer_button.setGeometry(QtCore.QRect(660, 490, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nextPlayer_button.setFont(font)
        self.nextPlayer_button.setObjectName("nextPlayer_button")
        self.neuesSpiel_button = QtWidgets.QPushButton(self.centralwidget)
        self.neuesSpiel_button.setGeometry(QtCore.QRect(10, 520, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.neuesSpiel_button.setFont(font)
        self.neuesSpiel_button.setObjectName("neuesSpiel_button")
        self.kalibrierungs_button = QtWidgets.QPushButton(self.centralwidget)
        self.kalibrierungs_button.setGeometry(QtCore.QRect(10, 490, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.kalibrierungs_button.setFont(font)
        self.kalibrierungs_button.setObjectName("kalibrierungs_button")
        self.doubleOut1_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.doubleOut1_checkbox.setGeometry(QtCore.QRect(270, 40, 81, 17))
        self.doubleOut1_checkbox.setObjectName("doubleOut1_checkbox")
        self.doubleIn1_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.doubleIn1_checkbox.setGeometry(QtCore.QRect(270, 20, 81, 17))
        self.doubleIn1_checkbox.setObjectName("doubleIn1_checkbox")
        self.doubleIn2_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.doubleIn2_checkbox.setGeometry(QtCore.QRect(670, 20, 81, 17))
        self.doubleIn2_checkbox.setObjectName("doubleIn2_checkbox")
        self.doubleOut1_checkbox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.doubleOut1_checkbox_2.setGeometry(QtCore.QRect(670, 40, 81, 17))
        self.doubleOut1_checkbox_2.setObjectName("doubleOut1_checkbox_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 220, 781, 20))
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(180, 400, 441, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(380, 10, 20, 221))
        self.line_3.setLineWidth(5)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.spieler1_textbox.raise_()
        self.spieler2_textbox.raise_()
        self.letzteWuerfe1_label.raise_()
        self.last1_1_label.raise_()
        self.last2_1_label.raise_()
        self.last3_1_label.raise_()
        self.verbleibend1_label.raise_()
        self.remScore1_label.raise_()
        self.auswertung_label.raise_()
        self.dart1_label.raise_()
        self.dart2_label.raise_()
        self.dart3_label.raise_()
        self.score1_label.raise_()
        self.score2_label.raise_()
        self.score3_label.raise_()
        self.gesamt_label.raise_()
        self.last3_2_label.raise_()
        self.remScore2_label.raise_()
        self.verbleibend2_label.raise_()
        self.letzteWuerfe2_label.raise_()
        self.last2_2_label.raise_()
        self.last1_2_label.raise_()
        self.gesScore_label.raise_()
        self.nextPlayer_button.raise_()
        self.neuesSpiel_button.raise_()
        self.kalibrierungs_button.raise_()
        self.doubleOut1_checkbox.raise_()
        self.doubleIn1_checkbox.raise_()
        self.doubleIn2_checkbox.raise_()
        self.doubleOut1_checkbox_2.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        self.line.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menubar.setObjectName("menubar")
        self.menuGame = QtWidgets.QMenu(self.menubar)
        self.menuGame.setObjectName("menuGame")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionStart_new_game = QtWidgets.QAction(MainWindow)
        self.actionStart_new_game.setObjectName("actionStart_new_game")
        self.actionSave_game = QtWidgets.QAction(MainWindow)
        self.actionSave_game.setObjectName("actionSave_game")
        self.actionLoad_game = QtWidgets.QAction(MainWindow)
        self.actionLoad_game.setObjectName("actionLoad_game")
        self.menuGame.addAction(self.actionStart_new_game)
        self.menuGame.addAction(self.actionSave_game)
        self.menuGame.addAction(self.actionLoad_game)
        self.menubar.addAction(self.menuGame.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.spieler1_textbox.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Spieler 1</span></p></body></html>"))
        self.spieler2_textbox.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Spieler 2</span></p></body></html>"))
        self.letzteWuerfe1_label.setText(_translate("MainWindow", "letzte Würfe:"))
        self.last1_1_label.setText(_translate("MainWindow", "last 1"))
        self.last2_1_label.setText(_translate("MainWindow", "last 2"))
        self.last3_1_label.setText(_translate("MainWindow", "last 3"))
        self.verbleibend1_label.setText(_translate("MainWindow", "Verbleibend:"))
        self.remScore1_label.setText(_translate("MainWindow", "-"))
        self.auswertung_label.setText(_translate("MainWindow", "Auswertung Spieler 1/2"))
        self.dart1_label.setText(_translate("MainWindow", "Dart 1"))
        self.dart2_label.setText(_translate("MainWindow", "Dart 2"))
        self.dart3_label.setText(_translate("MainWindow", "Dart 3"))
        self.score1_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"left\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">0</span></p></body></html>"))
        self.score2_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"left\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">0</span></p></body></html>"))
        self.score3_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"left\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">0</span></p></body></html>"))

        self.gesamt_label.setText(_translate("MainWindow", "Gesamt:"))
        self.last3_2_label.setText(_translate("MainWindow", "last 3"))
        self.remScore2_label.setText(_translate("MainWindow", "-"))
        self.verbleibend2_label.setText(_translate("MainWindow", "Verbleibend:"))
        self.letzteWuerfe2_label.setText(_translate("MainWindow", "letzte Würfe:"))
        self.last2_2_label.setText(_translate("MainWindow", "last 2"))
        self.last1_2_label.setText(_translate("MainWindow", "last 1"))
        self.gesScore_label.setText(_translate("MainWindow", "Score"))
        self.nextPlayer_button.setText(_translate("MainWindow", "Nächster Spieler"))
        self.neuesSpiel_button.setText(_translate("MainWindow", "Neues Spiel"))
        self.kalibrierungs_button.setText(_translate("MainWindow", "Kalibrierung"))
        self.doubleOut1_checkbox.setText(_translate("MainWindow", "Double out"))
        self.doubleIn1_checkbox.setText(_translate("MainWindow", "Double in"))
        self.doubleIn2_checkbox.setText(_translate("MainWindow", "Double in"))
        self.doubleOut1_checkbox_2.setText(_translate("MainWindow", "Double out"))
        self.menuGame.setTitle(_translate("MainWindow", "Game"))
        self.actionStart_new_game.setText(_translate("MainWindow", "Start new game"))
        self.actionSave_game.setText(_translate("MainWindow", "Save game"))
        self.actionLoad_game.setText(_translate("MainWindow", "Load game"))
        
        
        self.score1_label.textChanged.connect(self.score1_callback)
        self.score2_label.textChanged.connect(self.score2_callback)
        self.score3_label.textChanged.connect(self.score3_callback)
        
        self.nextPlayer_button.pressed.connect(self.nextPlayer_callback)
        self.kalibrierungs_button.pressed.connect(self.calib_callback)
        self.neuesSpiel_button.pressed.connect(self.newGame_callback)
        
        self.resetAllScores()
        
        
        global transformation_matrices
        if (os.path.exists(const.path_calib)):
                transformation_matrices = deserialize_calib()

        else: 
                ret, board_img_1 = cap1.read()
                ret, board_img_2 = cap2.read()
                ret, board_img_3 = cap3.read()
                calib(board_img_1, board_img_2, board_img_3)
             
                serialize_calib()
        

    def auswertung(self):    
        global dart_counter
        global ergebnis 
        global DartThread_active
        
        self.kalibrierungs_button.setEnabled(False)
        self.neuesSpiel_button.setEnabled(False)  
        
        self.dart_thread = dart_thread()
        self.dart_thread.start()
        
        red = QtWidgets.QGraphicsColorizeEffect()
        red.setColor(Qt.red)
        self.score1_label.setGraphicsEffect(red) 
        while (True):
                red = QtWidgets.QGraphicsColorizeEffect()
                red.setColor(Qt.red)
                black = QtWidgets.QGraphicsColorizeEffect()
                black.setColor(Qt.black)
                
                if(DartThread_active == True):
                        continue          

                if(dart_counter == 0):
                        self.score1_label.setGraphicsEffect(red)                        
                        continue                        
                elif(dart_counter == 1):                     
                        self.score1_label.setGraphicsEffect(black)                        
                        self.score2_label.setGraphicsEffect(red)                        
                        self.score1_label.setText(str(ergebnis))
                        QtWidgets.QApplication.processEvents()                       
                        self.dart_thread.start()
                elif(dart_counter == 2):
                        self.score2_label.setGraphicsEffect(black)                        
                        self.score3_label.setGraphicsEffect(red)                        
                        self.score2_label.setText(str(ergebnis))
                        QtWidgets.QApplication.processEvents()
                        self.dart_thread.start()
                elif(dart_counter == 3):
                        self.score3_label.setGraphicsEffect(black)                        
                        self.score3_label.setText(str(ergebnis))
                        QtWidgets.QApplication.processEvents()
                        break               

        self.kalibrierungs_button.setDisabled(False)
        self.neuesSpiel_button.setDisabled(False)



    def nextPlayer_callback(self, *args):
        global aktiver_spieler
        global Spieler_counter
        global Spieler_Punktzahl
        global dart_counter
        
        gesScore = self.gesScore_label.text()
                
        scoreDif = Spieler_Punktzahl[aktiver_spieler] - int(gesScore)
        if(scoreDif > 0): # normal
                Spieler_Punktzahl[aktiver_spieler] = scoreDif
        elif(scoreDif == 0): # sieg?
                Spieler_Punktzahl[aktiver_spieler] = 0
                # ToDo: double out checken (Erweiterung)
                self.nextPlayer_button.setEnabled(False)
        else: # überworfen
                Spieler_Punktzahl[aktiver_spieler] = Spieler_Punktzahl[aktiver_spieler]
                
        if (aktiver_spieler == 0):        
                self.remScore1_label.setText(str(Spieler_Punktzahl[aktiver_spieler]))
        else:
                self.remScore2_label.setText(str(Spieler_Punktzahl[aktiver_spieler]))
                
        self.addLastScores(gesScore)        
        self.resetDartScores()
        Spieler_counter = Spieler_counter + 1
        aktiver_spieler = Spieler_counter % 2
                
        self.auswertung_label.setText("Auswertung Spieler " + str(aktiver_spieler+1) + ":")
        dart_counter = 0
        QtWidgets.QApplication.processEvents()
              
        self.auswertung()


    def resetAllScores(self):               
        global Punktzahl
        self.remScore1_label.setText(str(Punktzahl))
        self.remScore2_label.setText(str(Punktzahl))
        
        global last_scores
        last_scores = [0,0,0],[0,0,0]
        self.last1_1_label.setText(str(last_scores[0][0]))
        self.last2_1_label.setText(str(last_scores[0][1]))
        self.last3_1_label.setText(str(last_scores[0][2]))
        self.last1_2_label.setText(str(last_scores[1][0]))
        self.last2_2_label.setText(str(last_scores[1][1]))
        self.last3_2_label.setText(str(last_scores[1][2]))
        
        global ergebnis
        ergebnis = 0
        
        global dart_counter
        dart_counter = 0
        
        global aktiver_spieler
        global Spieler_counter
        global Spieler_Punktzahl
        aktiver_spieler = 0
        Spieler_Punktzahl = [Punktzahl, Punktzahl]
        Spieler_counter = 0 # spieler 1 = 0, Spieler 2 = 1

        
    def resetDartScores(self):
        self.score1_label.setText("0")
        self.score2_label.setText("0")
        self.score3_label.setText("0")
        
    def calib_callback(self, *args):
        ret, board_img_1 = cap1.read()
        ret, board_img_2 = cap2.read()
        ret, board_img_3 = cap3.read()
        calib(board_img_1, board_img_2, board_img_3) 
        
        serialize_calib()

    def newGame_callback(self, *args):
        # Spieler 1 ist dran
        self.nextPlayer_button.setDisabled(False) 
        self.resetAllScores()
        self.resetDartScores()
        self.auswertung_label.setText("Auswertung Spieler " + str(aktiver_spieler+1) + ":")
        QtWidgets.QApplication.processEvents()
        
        self.auswertung()
   
        
    def addLastScores(self, gesScore):
            
        last_scores[aktiver_spieler][2] = last_scores[aktiver_spieler][1]
        last_scores[aktiver_spieler][1] = last_scores[aktiver_spieler][0]
        
        last_scores[aktiver_spieler][0] = gesScore
        
        if (aktiver_spieler == 0):
                self.last1_1_label.setText(str(last_scores[aktiver_spieler][0]))
                self.last2_1_label.setText(str(last_scores[aktiver_spieler][1]))
                self.last3_1_label.setText(str(last_scores[aktiver_spieler][2]))
        if (aktiver_spieler == 1):
                self.last1_2_label.setText(str(last_scores[aktiver_spieler][0]))
                self.last2_2_label.setText(str(last_scores[aktiver_spieler][1]))
                self.last3_2_label.setText(str(last_scores[aktiver_spieler][2]))
        
    
    def score1_callback(self, *args):
        text = self.score1_label.toPlainText()
        try:
                val = int(text)
                if (val >= 0 and val <= 60):
                        self.update_gesScore()
                else:
                        self.score1_label.setText("0")
        except ValueError:
                self.score1_label.setText("0")
                
        font = QtGui.QFont()
        font.setPointSize(16)
        self.score1_label.setFont(font)
                
    def score2_callback(self, *args):
        text = self.score2_label.toPlainText()
        try:
                val = int(text)
                if (val >= 0 and val <= 60):
                        self.update_gesScore()
                else:
                        self.score2_label.setText("0")
        except ValueError:
                self.score2_label.setText("0")

        font = QtGui.QFont()
        font.setPointSize(16)
        self.score2_label.setFont(font)

    def score3_callback(self, *args):
        text = self.score3_label.toPlainText()
        try:
                val = int(text)
                if (val >= 0 and val <= 60):
                        self.update_gesScore()
                else:
                        self.score3_label.setText("0")
        except ValueError:
                self.score3_label.setText("0")

        font = QtGui.QFont()
        font.setPointSize(16)
        self.score3_label.setFont(font)
        
        
    def update_gesScore(self, *args):
        try:
                score1 = int(self.score1_label.toPlainText())                
                score2 = int(self.score2_label.toPlainText())
                score3 = int(self.score3_label.toPlainText())
                
                sum = score1 + score2 + score3
                self.gesScore_label.setText(str(sum))

        except:
                self.gesScore_label.setText("Fehler")
        
class dart_thread(QThread):
        def run(self):
                global dart_counter
                global ergebnis
                self.ThreadActive = True
                
                global DartThread_active
                DartThread_active = True
                
                global cap1, cap2, cap3, transformation_matrices

                print("-----Board Bilder machen")
                ret, board_cam_0 = cap1.read()
                ret, board_cam_1 = cap2.read()
                ret, board_cam_2 = cap3.read()
                                
                board_cam_0 = img_resize(board_cam_0)
                board_cam_1 = img_resize(board_cam_1)
                board_cam_2 = img_resize(board_cam_2)           

                
                # Darts detektieren und Bilder aufnehmen
                # gibt das Bild von allen drei Kameras, sobald neuer Pfeil in Scheibe steckt (wenn kein unterschiedsbild mehr drin ist)
                print("-----Detect Dart Methode starten")
                dart_cam_0, dart_cam_1, dart_cam_2 =  detect_dart(cap1, cap2, cap3)
                
                dart_cam_0 = img_resize(dart_cam_0)
                dart_cam_1 = img_resize(dart_cam_1)
                dart_cam_2 = img_resize(dart_cam_2)       

                print("-----Bilder auswerten")
                
                try:
                        ## Koordinaten aus 2 unterschiedsbildern bestimmen
                        dart_coordinates_cam_0 = get_dart_coordinates(board_cam_0, dart_cam_0)
                        dart_coordinates_cam_1 = get_dart_coordinates(board_cam_1, dart_cam_1)
                        dart_coordinates_cam_2 = get_dart_coordinates(board_cam_2, dart_cam_2)

                        ## Koordinaten transformieren
                        dart_coordinates_transformed_cam_0 = transform_point(dart_coordinates_cam_0, transformation_matrices[0], board_cam_0)
                        dart_coordinates_transformed_cam_1 = transform_point(dart_coordinates_cam_1, transformation_matrices[1], board_cam_1)
                        dart_coordinates_transformed_cam_2 = transform_point(dart_coordinates_cam_2, transformation_matrices[2], board_cam_2)

                        ## Score aus transformierten Koordinaten bestimmen
                        score_cam_0, field_type, score_raw_cam_0 = get_dart_score(dart_coordinates_transformed_cam_0)
                        print("score_cam_0: " + str(score_cam_0))
                        score_cam_1, field_type, score_raw_cam_1 = get_dart_score(dart_coordinates_transformed_cam_1)
                        print("score_cam_1: " + str(score_cam_1))
                        score_cam_2, field_type, score_raw_cam_2 = get_dart_score(dart_coordinates_transformed_cam_2)
                        print("score_cam_2: " + str(score_cam_2))
        
        
                        # Welche Kamera ist für was verantwortlich
                        # 0 - links
                        # 1 - rechts
                        # 2 - oben
                        cam_score_dict = {1 : 2,
                                2 : 1,
                                3 : 1,
                                4 : 2,
                                5 : 2,
                                6 : 1,
                                7 : 0,
                                8 : 0,
                                9 : 2,
                                10 : 1,
                                11 : 0,
                                12 : 2,
                                13 : 1,
                                14 : 0,
                                15 : 1,
                                16 : 0,
                                17 : 1,
                                18 : 2,
                                19 : 0,
                                20 : 2}
                        ## Auswertung der 3 scores:
                        # --> wenn mind. 2 gleich sind, wird der score genommen                
                        if(score_cam_0 == score_cam_1):
                                ergebnis = score_cam_0
                        elif(score_cam_0 == score_cam_2):
                                ergebnis = score_cam_0
                        elif(score_cam_1 == score_cam_2):
                                ergebnis = score_cam_1
                                
                        # --> wenn alle unterschiedlich, wird die näheste Kamera genommen                
                        else: #  Scoreauswertung gewichten: Je nach Kamera position
                                if(cam_score_dict[score_raw_cam_0] == 0): 
                                        ergebnis = score_cam_0 
                                elif(cam_score_dict[score_raw_cam_1] == 1):
                                        ergebnis = score_cam_1
                                else:
                                        ergebnis = score_cam_2
                except:
                        ergebnis = 0
                
                dart_counter = dart_counter+1        
                DartThread_active = False                
                

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




