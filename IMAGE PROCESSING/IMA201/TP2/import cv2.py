import cv2
import matplotlib.pyplot as plt
import numpy as np

path = r'C:\Users\giova\OneDrive\Área de Trabalho\IMA\TP2\femme.tif'

img = cv2.imread(path) 

print(type(img))