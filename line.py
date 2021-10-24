import cv2
import numpy as np
import statistics
import math

def get_colour(img,lower=[100,45,0],upper=[200,255,255]):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  lower_range = np.array(lower)
  upper_range = np.array(upper)
  mask = cv2.inRange(hsv, lower_range, upper_range)
  return mask

def get_lines(img,minlen=300,maxgap=50):
  lines = cv2.HoughLinesP(img, rho =1, theta= np.pi / 180, threshold = 100, lines=None,minLineLength = minlen, maxLineGap = maxgap)
  #lines =sorted(lines, key=lambda k: (-k[2], -k[0]))
  angles = []
  '''
  minLineLength - Minimum length of line. Line segments shorter than this are rejected.
  maxLineGap - Maximum allowed gap between line segments to treat them as a single line.
  '''
  for [[x1,y1,x2,y2]] in lines:
    cv2.line(img,(x1,y1),(x2,y2),(255,255,255), 3)
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    angles.append(angle)
  return lines,angles,img


