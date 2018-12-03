#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

root = 'D:\Videos\Coursera'  # root directory

def change_suffix(root):
    """
    :param root: root directory of all subtitles
    convert the suffix from .vtt to .srt
    """
    for (dirname, dirs, files) in os.walk(root):    # recurse all files in root directory
        flag = True
        for filename in files:     # traverse all files in one folder
            if filename.endswith('vtt') :
                file_before = os.path.join(dirname,filename)
                delete_first_line(file_before)    #delete the first line 'WEBVTT'
                new_filename = filename[: -3] + 'srt'
                file_after = os.path.join(dirname,new_filename)
                os.renames(file_before, file_after)     # rename files
                if flag:    # neat printing
                    print 'DIR: ' + dirname
                    flag = False
                print filename + ' -----> ' + new_filename


def delete_first_line(filename):
    """
    :param filename: subtitle filename
    delete the first line 'WEBVTT' from .vtt subtitle file
    """
    lines = open(filename).readlines()
    open(filename, 'w').writelines(lines[2:])


# delete_first_line('E:\Video\Coursera\Machine Learning\Week 2\Linear Regression with Multiple Variables\\1.Multiple Features.vtt')
change_suffix(root)