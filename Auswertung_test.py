import const
from board_extraction import transform_point, deserialize_calib, calib_camera, calib, transformation_matrices
from dart_extraction import get_dart_coordinates, get_dart_score
import cv2
import numpy as np
import os


def img_read_resize(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (const.length, const.width))
    return img

# hier Auswertung mit Standbildern testen
# calib()

transformation_matrices = deserialize_calib()

board_cam_0 = img_read_resize(const.path_board) 
# board_cam_1 = img_read_resize(const.path_board) 
# board_cam_2 = img_read_resize(const.path_board) 

### eig Sammys Bilder Methode --> gibt das Bild von allen drei Kameras, sobald neuer Pfeil in Scheibe steckt (wenn kein unterschiedsbild mehr drin ist)
dart_cam_0 = img_read_resize(const.path_dart) 
# dart_cam_1 = img_read_resize(const.path_dart) 
# dart_cam_2 = img_read_resize(const.path_dart) 

# Bilder für nächste Auswertung abspeichern
# if dart_counter >= 1
# last_dart_cam_0 = dart_cam_0
    # last_dart_cam_1 = dart_cam_1
    # last_dart_cam_2 = dart_cam_2
# else
last_dart_cam_0 = board_cam_0
    # last_dart_cam_1 = board_cam_1
    # last_dart_cam_2 = board_cam_2

# Auswertung von 1 Pfeil: 

### Koordinaten aus 2 unterschiedsbildern bestimmen
dart_coordinates_cam_0 = get_dart_coordinates(last_dart_cam_0, dart_cam_0)
# dart_coordinates_cam_1 = get_dart_coordinates(last_dart_cam_1, dart_cam_1)
# dart_coordinates_cam_2 = get_dart_coordinates(last_dart_cam_3, dart_cam_2)

### Koordinaten transformieren
dart_coordinates_transformed_cam_0 = transform_point(dart_coordinates_cam_0, transformation_matrices[0], board_cam_0)
# dart_coordinates_transformed_cam_1 = transform_point(dart_coordinates_cam_1, transformation_matrices[1], board_cam_1)
# dart_coordinates_transformed_cam_2 = transform_point(dart_coordinates_cam_2, transformation_matrices[2], board_cam_2)

### Score aus transformierten Koordinaten bestimmen
score_cam_0 = get_dart_score(dart_coordinates_transformed_cam_0)
print(str(score_cam_0))
# score_cam_1 = get_dart_score(dart_coordinates_transformed_cam_1)
# score_cam_2 = get_dart_score(dart_coordinates_transformed_cam_2)

### Auswertung der 3 scores:
## --> wenn mind. 2 gleich sind, wird der score genommen
## --> wenn alle unterschiedlich, wird die näheste Kamera genommen
# if(score_cam_0 == score_cam_1)
    # score = score_cam_0
# else if(score_cam_0 == score_cam_2)
    # score = score_cam_0
# else if(score_cam_1 == score_cam_2)
    # score = score_cam_1
# else 
    #ToDo: Scoreauswertung gewichten? Je nach Kamera position

# dart_counter = dart_counter + 1
# score_ges = score_ges + score

### Logik von Punktzahl
# ToDo: Logik von Scores erweitern
# if score_ges > SpielerPunktzahl[aktiver_spieler]
    # score_ges = 0
    # weiter

# if score_ges == SpielerPunktzahl[aktiver_spieler]
    # Spieler hat gewonnen 
    # ToDo: hier evtl noch double out rein machen

### Spielerwechsel
# if dart_counter = 3 --> auf Weiter warten

# if weiter pressed 
#       Spieler_counter = Spieler_counter + 1
#       counter = 0
#       SpielerPunktzahl[aktiver_spieler] = SpielerPunktzahl[aktiver_spieler] - score_ges
