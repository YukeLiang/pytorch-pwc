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

def get_optical_flow(frame_list, output_dir):
    status = False
   
    print('START GENERATING OPTICAL FLOW!')
    first_img = frame_list[0]
    for f in frame_list:
        second_img = f
        if frame_list.index(f) == 0:
            print("Skip generating optical flow for the first frame.")
            continue
        output_file = '%s%06d.flo'%(output_dir, frame_list.index(f))
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
        # Update the first image  passed to optical flow file
        first_img = second_img
        print('Finished getting flow field for {:d}th frames of {:d} frames.'.format(frame_list.index(f), len(frame_list))) 

    status = True
    return status, 'FINISHED GENERATING OPTICAL FLOW!'


def main(video_dir, output_dir):
    final_status = False
    # list all subfolders, i.e., videos
    video_list = sorted(glob.glob(os.path.join(video_dir, '*/')))
    print('Found {:d} videos'.format(len(video_list)))
    
    #create output folder if necessary
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for video_folder in video_list:
        frame_list = sorted(glob.glob(os.path.join(video_folder, 'img', "*.jpg")))
    
        if len(frame_list) == 0:
        # empty folder
            print("{:s} empty folder!".format(video_folder))
            return True, 'Empty'
        else:
            print("{:d} frames in {:s}".format(len(frame_list), video_folder))
        
        print('READY TO GENEARTE OPTICAL FLOW!')
        get_optical_flow(frame_list, output_dir)

    final_status = True
    return final_status



if __name__ == '__main__':
    description = 'Helper script for running detector over video frames.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('video_dir', type=str,
                   help='video frames directory where each video has a folder.')
    p.add_argument('output_dir', type=str,
                   help='Output directory where detection results will be saved.')   
    main(**vars(p.parse_args()))
