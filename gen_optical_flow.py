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
    for idx, frame in enumerate(frame_list):
        first_frame = frame
        if idx == len(frame_list) - 1:
            print('Finished getting flow field for {:d} frames.'.format(len(frame_list))) 
            break
        second_frame = frame_list[idx + 1]
        output_file = '%s%06d.flo'%(output_dir, idx)
        flow_cmd = ['python pytorch-pwc/run.py',
                    '--model', 'default',
                    '--first', first_frame,
                    '--second', second_frame,
                    '--out', output_file]
        flow_cmd = ' '.join(flow_cmd)
        try: 
            print('Processing...')
            subprocess.run(flow_cmd, shell=True)
        except subprocess.CalledProcessError as err:
            return status, err.output

    status = True
    return status, 'FINISHED GENERATING OPTICAL FLOW!'


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
    p.add_argument('video_dir', type=str,
                   help='video frames directory where each video has a folder.')
    p.add_argument('output_dir', type=str,
                   help='Output directory where detection results will be saved.')   
    main(**vars(p.parse_args()))
