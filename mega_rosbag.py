#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 14:59:12 2018

@author: yukan
"""


"""
one-click
"""

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

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('--spath', help='enter the source directory of the images')
    parser.add_argument('--dpath', help='enter the destination directory of the images')
    parser.add_argument('--interval', help='interval of the images selection')
    parser.add_argument('--bagname', help='put the name of the rosbag here')
    args = parser.parse_args()

    if args.spath[-1] != '/':
        args.spath = args.spath + '/'

    if args.dpath[-1] != '/':
        args.dpath = args.dpath + '/'

    if(os.path.isdir(args.dpath) == False):
        command = 'mkdir' + ' ' + args.dpath
        os.system(command)


    """
    change the index of the image names

    """

    print("*****************************starting copy images***********************************")
    seqlist = list()
    files = os.listdir(args.spath)
    for f in files:
        if f[-3:] != 'jpg':
            continue
        seqlist.append(f)
    for seq in seqlist:
        s = seq.split('_')
        time_index_str = s[0]
        cam_index_str = s[1]
        cam_index_str_geringer = str(int(cam_index_str) - 1)
        seq_geringer = 'cam' + cam_index_str_geringer + '_' + time_index_str + '.jpg'
        command = 'cp' + ' ' + args.spath + seq + ' ' +  args.dpath + seq_geringer
        os.system(command)


    print("*****************************starting delete images***********************************")
    #do the data check and image secletion
    dfiles = os.listdir(args.dpath)
    dseqlist = list()
    for df in dfiles:
        if df[-3:] != 'jpg':
            continue
        dseqlist.append(df)
    dseqlist = sorted(dseqlist)

    if(len(dseqlist)%4 != 0):
        print("CHECK DATA")

    dseqlist_selection = list()
    #interval = 5
    interval = int(args.interval)
    for i in range(0, len(dseqlist)/4, interval):
        dseqlist_selection.append(dseqlist[i])
        dseqlist_selection.append(dseqlist[i + len(dseqlist)/4])
        dseqlist_selection.append(dseqlist[i + 2 * len(dseqlist)/4])
        dseqlist_selection.append(dseqlist[i + 3 * len(dseqlist)/4])

    for dseq in dseqlist:
        if dseqlist_selection.count(dseq) == 0:
            command = 'rm' + ' ' + args.dpath + dseq
            os.system(command)



    print("*****************************starting to make ros bag***********************************")

    #bagname = 'test.bag'
    bagname = args.bagname

    bag_indexlist = list()
    bag_files = os.listdir(args.dpath)
    for bag_f in bag_files:
        s = (bag_f.split('_')[1])[:-4]
        bag_indexlist.append(s)
    reduced_bag_indexlist = bag_indexlist[0:len(bag_indexlist):4]

    bridge = CvBridge()
    bag = rosbag.Bag(bagname, 'w')


    try:
        finish = 0.0
        for bagseq in reduced_bag_indexlist:
            timestamp = rospy.rostime.Time.from_sec(time.time())
            time.sleep(1/1e2)
            for cam in range(0, 4, 1):
                jpgname = (args.dpath + "cam{:d}_{:s}.jpg").format(cam, bagseq)
                if os.path.isfile(jpgname):
                    imcv = read_image_cv(jpgname)
                else:
                    imcv = np.zeros(shape=(720, 1280), dtype=np.uint8)

                simg = bridge.cv2_to_imgmsg(imcv, encoding="mono8")
                simg.header.frame_id = "cam{:d}".format(cam)
                simg.header.seq = int(bagseq)
                simg.header.stamp = timestamp
                simg.encoding = 'mono8'
                bag.write("/cam{:d}/image_raw".format(cam), simg, timestamp)
            finish += 1
            print "{0:.000%}".format(finish/len(reduced_bag_indexlist))
    finally:
        bag.close()

















