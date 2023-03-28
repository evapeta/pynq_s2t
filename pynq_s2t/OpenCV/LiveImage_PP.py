# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file hosts the post processing functions for the output .json files from rev.ai.       #
# Functions held are:                                                                         #
#                                                                                             #
#        1. 'structuredsub' which outputs the correct timing for the subtitles and            #
#            their respective timings;                                                        #
#                                                                                             #
#        2. 'framenumber' which outputs the corresponding frames from the different subtitle  #
#            starting times;                                                                  #
#                                                                                             #
#        3. 'subtitle_output' which displays the subtitles on the clear frame in a visable    #
#            way, before overlay.                                                             #
#                                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

## Importing Relavent Modules:
import json
import math
import cv2
import numpy as np

# 1. 
def structuredsub(filename):

    import json
    import math

    with open(filename) as f:
        dictionary = json.load(f) # loading in file as dictionary
       
    elements = dictionary['monologues'][0]['elements']
    sub_len = len(elements)

    # Subtitle Content for Extraction
    subtitles_value = [0] * sub_len 
    subtitles_start = [0] * sub_len
    subtitles_end   = [0] * sub_len
    
    # Getting the subtitle value and its timing 
    for i in range(0, sub_len):
        sub = elements[i]
            
        # Value of Subtitle in Dictionary
        sub_val  = sub['value']
        subtitles_value[i] = sub_val
        
        # Start times and durations
        if 'ts' in sub.keys():
            start_t =  sub['ts']
            end_t   =  sub['end_ts']
            
            subtitles_start[i] = start_t
            subtitles_end[i]   = end_t
            
        else:
            subtitles_start[i] = 0
            subtitles_end[i]   = 0

    # Start and Ending Times of Captioning:
    end_Time = end_t
    start_Time = subtitles_start[0]
    T = end_Time - start_Time
    
    # Using subtitling standard to define subtitle structure:
    length = 6 # change subtitles every 6s
    n = math.ceil(T/length)

    caption_list = [0] * n
    indices_list = [0] * n
    start_list   = [0] * n
    timing_list  = [0] * n
    
    j = 0
    Delta_t = 0
    indices = []
    captions = []

    for i in range(0, sub_len):
        ti = subtitles_start[i]
        tf = subtitles_end[i]
        occupied_t = round((tf - ti), 2) # time taken to say one word
        
        delta_t = round((Delta_t + occupied_t), 2)
        cap = subtitles_value[i]
        
        if math.ceil(delta_t) < 5:
            Delta_t = delta_t
            indices.append(i)
            captions.append(cap)
            
        elif math.ceil(delta_t) == 5:
            caption_list[j] = captions
            indices_list[j] = indices
            start_list[j]   = round((ti - round(delta_t, 2)), 2)
            timing_list[j]  = round(delta_t, 2)
            
            Delta_t = 0
            indices = []
            captions = []
            
            j += 1

    # Joining Subtitle Lists into one caption:
    subtitles = [0] * n
    for i in range(0, n):
        cc = ''.join(caption_list[i])
        subtitles[i] = cc
    
    return subtitles, start_list # returning the subtitles and the start time of each thread

# 2.
def framenumber(start_list, fps):
    frame_information = [0] * (len(start_list))
        
    for i in range(0, len(start_list)):
        time = start_list[i]
        frame = int((fps * time) - 30)
        frame_information[i] = frame
                   
    return frame_information

# 3.
def subtitle_output(sub, cap, frame):
    import cv2
    import numpy as np
    
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        
    if frame is None:
        # Creating a false transparent frame for overlay:
        Frame = np.zeros((height, width, 4), dtype=np.uint8)
        Frame[:,:,3] = 0
        return Frame

    if frame is not None:  

        # Font definitions for OpenCV putText function:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        
        # area of interest, where subtitles are placed:
            # RECTANGLE:
        tr = int(width - 10), int(height - 34)
        [a, b] = tr
        bl = 10, int(height - 3)
        [c, d] = bl
            # TEXT:
        x = int(10)
        y = int(height - 10)
        
        # Creating Blank Image:
        data = np.zeros((height, width, 4), dtype=np.uint8)
        
        # Drawing on Blank Image:
        img = cv2.rectangle(data, tr, bl, (0, 0, 0), -1)
        image = cv2.putText(img, sub, (x, y), font, font_scale, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Ensuring only reigon of interest is transparent:
        for h in range(0, height):
            for w in range(0, width):
                if c <= w < a and b <= h < d:
                    data[h, w, 3] = 255
                else:
                    data[h, w, 3] = 0
                    
        # Returning overlay for frame:
        return image
    
# 3.
def test_subtitle_output(sub, frame):
 
    height, width = frame.shape[:2]
    
    # Defining the false overlay image:
    data = np.zeros((height, width, 4), dtype=np.uint8)
    
    # font constraints for opencv put text:
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    
    # area of interest, where subtitles are placed:
    tr = int(width - 10), int(height - 34)
    [a, b] = tr
    bl = 10, int(height - 3)
    [c, d] = bl
    
    x = int(10)
    y = int(height - 10)
    
    img = cv2.rectangle(data, tr, bl, (0, 0, 0), -1)
    image = cv2.putText(img, sub, (x, y), font, font_scale, (255, 255, 255), 2, cv2.LINE_AA)

    for h in range(0, height):
        for w in range(0, width):
            if c <= w < a and b <= h < d:
                data[h, w, 3] = 255
            else:
                data[h, w, 3] = 0
        
    return image