"""
Created on Thu May 30 14:08:41 2019

@author: laurent

MXNET-MODEL-SERVER
OPENCV
"""

import numpy as np
import cv2
from PIL import ImageGrab as ig
import time
from subprocess import Popen, PIPE
from PIL import Image
import json

# command curl prediction
curl_cmd = "curl -X POST http://127.0.0.1:8080/predictions/ssd -T /path/prediction.png"


x = 600
y = 600
last_time = time.time()
while(True):
    # capture screen
    screen = ig.grab(bbox=(x,y,x+300,y+300))
    screen = np.array(screen)
    #print('Loop took {} seconds',format(time.time()-last_time))
    # show camera
    
    # save img to png for prediction
    img = Image.fromarray(screen)   
    img.save('docs/images/prediction.png') 
    
    # Make predictions
    p = Popen(curl_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = p.communicate()
    output = output.decode("utf-8")

    bbox = json.loads(output)
    print(bbox)
    #time.sleep(1)
    if not bbox:
        continue
    else:
        img = cv2.imread("/path/prediction.png",0)
        cv2.rectangle(img,(bbox[0][1],bbox[0][2]),(bbox[0][3],bbox[0][4]),(255,255,255),3)
        
    cv2.imshow("image", img)
    last_time = time.time()
    time.sleep(5)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
