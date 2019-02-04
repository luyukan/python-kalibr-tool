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
    print(file_name)
    img = cv2.imread(file_name)
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    return img


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dpath', help='enter the destination directory of the images')
    parser.add_argument('--interval', help='interval of the images selection')
    parser.add_argument('--bagname', help='put the name of the rosbag here')
    args = parser.parse_args()


    print("*****************************starting to make ros bag***********************************")

    bagname = args.bagname

    bag_files = os.listdir(args.dpath)
    dfiles = os.listdir(args.dpath)
    dfiles = sorted(dfiles)
    dseqlist = list()
    didlist = list()
    for df in dfiles:
        if df[-3:] != 'jpg':
            continue
        s = df.split('_')
        if(len(didlist) == 0):
            didlist.append(s[0])
        else:
            if(int(s[0]) != int(didlist[-1])):
                didlist.append(s[0])
        dseqlist.append(df)

    dseqlist = sorted(dseqlist)
    didlist = sorted(didlist)
    #if (len(dseqlist) % 4 != 0):
    #    print("CHECK DATA")


    interval = int(args.interval)
    bridge = CvBridge()
    bag = rosbag.Bag(bagname, 'w')



    try:
        finish = 0.0
        for i in range(int(len(didlist)/interval)):
            index = i * interval
            timestamp = rospy.rostime.Time.from_sec(time.time())
            time.sleep(1 / 1e2)
            for cam in range(0, 4, 1):
                jpgname = (args.dpath + "{:s}_cam{:d}.jpg").format(didlist[index],cam)
                if os.path.isfile(jpgname):
                    imcv = read_image_cv(jpgname)
                else:
                    imcv = np.zeros(shape=(720, 1280), dtype=np.uint8)

                simg = bridge.cv2_to_imgmsg(imcv, encoding="mono8")
                simg.header.frame_id = "cam{:d}".format(cam)
                simg.header.seq = int(didlist[i])
                simg.header.stamp = timestamp
                simg.encoding = 'mono8'
		bag.write("/cam{:d}/image_raw".format(cam), simg, timestamp)
            finish += 1
            print "{0:.000%}".format(finish / int(len(didlist)/interval))

    finally:
        bag.close()

    #
