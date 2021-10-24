import cv2
import numpy as np
from scipy import ndimage,stats
import statistics
import math


def get_extra(img1,img2):

  edge1=get_edges(img1,50,150)
  circles1=get_circle(edge1)
  x1,y1,radius1 = circles1[0,:][0]
  print(radius1)

  edge2=get_edges(img2,50,150)
  circles2=get_circle(edge2)
  x2,y2,radius2 = circles2[0,:][0]
  print(radius2)

  ratio= radius1/radius2
  print("ratio:",ratio)
  if ratio>1:
    img1 = cv2.resize(img1,(math.floor(img1.shape[1]*(1/ratio)),math.floor(img1.shape[0]*(1/ratio))), interpolation = cv2.INTER_AREA)
    edge1=get_edges(img1,50,150)
    circles1=get_circle(edge1)
    x1,y1,radius1 = circles1[0,:][0]
  else:
    img2 = cv2.resize(img2,(math.floor(img2.shape[1]*ratio),math.floor(img2.shape[0]*ratio)), interpolation = cv2.INTER_AREA)
    edge2=get_edges(img2,50,150)
    circles2=get_circle(edge2)
    x2,y2,radius2 = circles2[0,:][0]
  print(radius1)
  print(radius2)


  extra = img1.shape[0]-y1 + img2.shape[1]-x2
  extra1= img1[img1.shape[0]-extra:, x1-radius1:x1]
  only1= img1[:img1.shape[0]-extra, x1-radius1:x1]

  extra2= img2[y2-radius2:y2,img2.shape[1]-extra:]
  only2= img2[y2-radius2:y2,:img2.shape[1]-extra]
  extra2=cv2.rotate(extra2, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
  only2=cv2.rotate(only2, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
  quad1= img1[y1-radius1:y1,x1-radius1:x1]
  quad2= img2[y2-radius2:y2,x2-radius2:x2]
  quad2=cv2.rotate(quad2, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

  return extra1, extra2,only1,only2,quad1,quad2