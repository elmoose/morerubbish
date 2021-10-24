import cv2
import numpy as np
import math

def get_edges(img,a,b):
  # Grayscale
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  #blur
  #gray = cv2.medianBlur(gray, 25)
  
  # Find Canny edges
  edged = cv2.Canny(gray, a, b)
  cv2.waitKey(0)
  
  # Finding Contours
  # since findContours alters the image
  _,contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
  #not enough values to unpack remove _

  #kernel = np.ones((9,9), np.uint8)
  kernel = np.ones((30, 30), np.uint8)
  mask = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
  #mask = cv2.morphologyEx(edged, cv2.MORPH_OPEN, kernel)
  edges = cv2.Canny(mask, 100, 200)
  #cv2_imshow(mask)
  # put mask into alpha channel of result
  result = img.copy()
  result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
  result[:, :, 3] = edged
  #cv2.imwrite(saveas, result)
  #return edged
  return edges

def get_circle(gray):
  #gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
  #gray = cv2.medianBlur(gray, 5)
  rows = gray.shape[0]
  circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows*2,
                               param1=200, param2=10,
                               minRadius=600, maxRadius=1800) # adjust this
  
    
    
  if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
      center = (i[0], i[1])
      # circle center
      cv2.circle(gray, center, 50, (255, 0, 255), 3)
      # circle outline
      radius = i[2]
      cv2.circle(gray, center, radius, (255, 0, 255), 3)
    cv2.imshow(gray)
  else:
    print("NOOooooOOoooOo")
    
    
  
  cv2.waitKey(0)
  return circles


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


