# -*- coding: gbk -*-
import os
import re
import string

path =  os.getcwd()

print 'current path : ' , path.decode('gbk').encode('utf8')

suffix = ''


files = os.listdir(path)

for f in files:
    olddir=os.path.join(path, f) #ԭ�����ļ�·��
    if os.path.isdir(olddir):
        continue                     #������ļ���������
    if re.findall('\..{2,4}$', f)[0] == '.srt':
        # newdir = os.path.join(path, f[: -3] + 'srt') #�µ��ļ�·��
        # print f
        # os.rename(olddir, newdir)    #������
        fread = open(os.path.join(path, f))
        file = fread.read()
        fread.close()
        fwrite = open(os.path.join(path, f), 'w')
        fwrite.write(file[8:])
        fwrite.close()


