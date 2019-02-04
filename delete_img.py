import os

file_list = os.listdir('/home/yukan/Pictures/0117_modi/')
for f in file_list:
    print(f)
    s = f[:5] + "_1" + f[7:]
    print(s)
    befehl= 'cp ' + '/home/yukan/Pictures/0117_modi/' + f + ' ' + '/home/yukan/Pictures/0117_modify/' + s
    os.system(befehl)
    # if (f[6] != '3'):
    #     befehl = 'rm ' + '/home/yukan/Pictures/omni_apriltag/' + f
    #     os.system(befehl)