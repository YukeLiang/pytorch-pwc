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
    status = False
   
    print('START GENERATING OPTICAL FLOW!')
    # first_img = frame_list[0]
    for idx, frame in enumerate(frame_list):
        prev_idx = idx - 1
        if prev_idx < 0:
            continue
        second_img = frame
        first_img = frame_list[prev_idx]
        # Be careful, named with source frame
        output_file = '%s%06d.flo'%(output_dir, idx)
        flow_cmd = ['python run.py',
                    '--model', 'default',
                    '--first', first_img,
                    '--second', second_img,
                    '--out', output_file]
        flow_cmd = ' '.join(flow_cmd)
        try: 
            print('Processing...')
            subprocess.run(flow_cmd, shell=True)
        except subprocess.CalledProcessError as err:
            return status, err.output
        print('Finished getting flow field from {:d}th frame to {:d}th frame.'
        .format(idx, idx+1))

    status = True
    return status, 'FINISHED GENERATING OPTICAL FLOW!'


def main(video_root):
    final_status = False
    
    #create output folder if necessary
    flow_folder = video_root + "flow/"
    if not os.path.exists(flow_folder):
        os.mkdir(flow_folder)

    frame_list = sorted(glob.glob(os.path.join(video_root, 'img', "*.jpg")))
    
    if len(frame_list) == 0:
    # empty folder
        print("empty folder!")
        return False, 'Empty'
    else:
        print("{:d} frames in {:s}".format(len(frame_list), video_root))
        
    print('READY TO GENEARTE OPTICAL FLOW!')
    get_optical_flow(frame_list, flow_folder)

    final_status = True
    return final_status



if __name__ == '__main__':
    description = 'Helper script for running detector over video frames.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('video_root', type=str,
                   help='video frames directory where each video has a folder.')  
    main(**vars(p.parse_args()))
