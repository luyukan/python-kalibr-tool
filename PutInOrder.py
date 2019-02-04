import time, sys, os
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--spath', help='enter the source directory of the images')
    parser.add_argument('--dpath', help='enter the destination directory of the images')
    args = parser.parse_args()

    if args.spath[-1] != '/':
        args.spath = args.spath + '/'

    if args.dpath[-1] != '/':
        args.dpath = args.dpath + '/'

    if(os.path.isdir(args.dpath) == False):
        command = 'mkdir' + ' ' + args.dpath
        os.system(command)

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
        seq_geringer = time_index_str + '_' + 'cam' + cam_index_str_geringer + '.jpg'
        command = 'cp' + ' ' + args.spath + seq + ' ' + args.dpath + seq_geringer
        os.system(command)
