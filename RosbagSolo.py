import time, sys, os
from ros import rosbag
import numpy as np
import roslib
import rospy
from sensor_msgs.msg import Image
import ImageFile
import cv2
from cv_bridge import CvBridge, CvBridgeError
import argparse



def read_image_cv(file_name):
    img = cv2.imread(file_name)
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    return img

bagname = '0122.bag'

directory = '/home/yukan/Pictures/20190117/front_0122/'
file_list = os.listdir(directory)

idlist = list()
seqlist = list()
for f in file_list:
    s = f.split('_')
    if f[-3:] != 'jpg':
        continue
    seqlist.append(f)
    idlist.append(s[0])

seqlist = sorted(seqlist)
idlist = sorted(idlist)

bridge = CvBridge()
bag = rosbag.Bag(bagname, 'w')

finish = 0.0

for i in range(len(seqlist)):
    timestamp = rospy.rostime.Time.from_sec(time.time())
    time.sleep(1 / 1e2)
    jpgname = directory + seqlist[i]
    print(jpgname)
    if os.path.isfile(jpgname):
        imcv = read_image_cv(jpgname)
    else:
        imcv = np.zeros(shape=(720, 1280), dtype=np.uint8)
    simg = bridge.cv2_to_imgmsg(imcv, encoding="mono8")
    simg.header.frame_id = "cam0"
    simg.header.seq = int(idlist[i])
    print(simg.header.seq)
    simg.header.stamp = timestamp
    simg.encoding = 'mono8'
    bag.write("/cam0/image_raw", simg, timestamp)
    print("{0:.000%}".format(finish / len(seqlist)))
    finish += 1