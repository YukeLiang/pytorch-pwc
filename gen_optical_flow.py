from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# insert current path to sys path
import os
import sys
sys.path.insert(0, os.getcwd())

import argparse
import glob
import time
import json
import numpy as np
import cv2
import subprocess

###### For https://github.com/sniklaus/pytorch-pwc
def get_optical_flow(frame_list, output_dir):

    print('START GENERATING OPTICAL FLOW!')
    # first_img = frame_list[0]
    for idx, frame in enumerate(frame_list):
        prev_idx = idx - 1
        if prev_idx < 0:
            continue
        second_img = frame
        first_img = frame_list[prev_idx]
        output_file = '%s%06d.flo'%(output_dir, idx)
        if(get_flow_pair(first_img, second_img, output_file)):
            print('Finished getting flow field from {:d}th frame to {:d}th frame.'
            .format(idx, idx+1))
        else:
            return False
        # Be careful, named with source frame
    return True

def get_flow_pair(first_img, second_img, output_file):

    flow_cmd = ['python run.py',
                '--model', 'default',
                '--first', first_img,
                '--second', second_img,
                '--out', output_file]
    flow_cmd = ' '.join(flow_cmd)
    try: 
        print('Processing...')
        subprocess.check_call(flow_cmd, shell=True)
    except KeyboardInterrupt:
        return False
    except subprocess.CalledProcessError as err:
        get_flow_pair(first_img, second_img, output_file)
    return True

def main(video_root, output_dir):
    final_status = False
    
    #create output folder if necessary
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    frame_list = sorted(glob.glob(os.path.join(video_root, 'img', "*.jpg")))
    
    if len(frame_list) == 0:
    # empty folder
        print("empty folder!")
        return False, 'Empty'
    else:
        print("{:d} frames in {:s}".format(len(frame_list), video_root))
        
    print('READY TO GENEARTE OPTICAL FLOW!')
    get_optical_flow(frame_list, output_dir)

    final_status = True
    return final_status



if __name__ == '__main__':
    description = 'Helper script for running detector over video frames.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('video_root', type=str,
                   help='video frames directory where each video has a folder.')  
    p.add_argument('output_dir', type=str,
                   help='video frames directory where each video has a folder.')  
    main(**vars(p.parse_args()))
