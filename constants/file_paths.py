# coding=utf-8
import os
import sys

base_folder=os.path.join(os.path.dirname(__file__),r'..')

level_location=os.path.join(base_folder,'resources','levels')
tile_folder=os.path.join(base_folder,'resources','tiles')
log_folder=os.path.join(base_folder,'logs')


if __name__ == '__main__':
    print(level_location)
    with open(os.path.join(level_location,r'level_0.txt'),'r') as f:
        for line in f:
            print(line)