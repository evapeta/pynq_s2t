# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file hosts the post processing functions for the output .json files from rev.ai.       #
# Functions held are:                                                                         #
#                                                                                             #
#        1. 'PostProcessing_Live' which collates the real time and 'Real' subtitles           #
#            their respective timings;                                                        #
#                                                                                             #
#        2. 'real_t' display the text rather than the json file;                              #
#                                                                                             #
#        2. 'overlaid_image' placing the black area for subtitles;                            #
#                                                                                             #
#        4. 'sub_outputt' which displays the subtitles on the clear frame in a visable        #
#            way, before overlay.                                                             #
#                                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

## Importing Relavent Modules:
import json
import numpy as np
import cv2

## 1. 
def PostProcessing_Live(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(json.loads(line))

    real_t = []     
    real_st = []   
    subtitles = []
    subtitles_st = []

    for i in range(len(data)):
        response = data[i]
        elements = response["elements"]
        start_t = response["end_ts"]

        subtitle = []
        
        init_dict = elements[0]["value"][0]
        if init_dict.isupper() is True:
            
            for i in range(0, len(elements)):
                dicts = elements[i]
                value = dicts["value"]
                val = value.strip('\"')
                subtitle.append(val)
        
            sub = ''.join(subtitle)
            subtitles.append(sub)
            subtitles_st.append(start_t)
            
        elif init_dict.isupper() is False:
            for i in range(0, len(elements)):
                dicts = elements[i]
                value = dicts["value"]
                val = value.strip('\"')
                subtitle.append(val)
        
            sub = ' '.join(subtitle)
            real_t.append(sub)
            real_st.append(start_t)

    return real_t, real_st, subtitles, subtitles_st

# 2.
def real_t(data):
    response = json.loads(data)
    elements = response["elements"]
    init_dict = elements[0]["value"][0] # first character of the first word
    
    subtitle = []
        
    init_dict = elements[0]["value"][0]
    if init_dict.isupper() is True:
            
        for i in range(0, len(elements)):
            dicts = elements[i]
            value = dicts["value"]
            val = value.strip('\"')
            subtitle.append(val)
        
        sub = ''.join(subtitle)
            
    elif init_dict.isupper() is False:
        for i in range(0, len(elements)):
            dicts = elements[i]
            value = dicts["value"]
            val = value.strip('\"')
            subtitle.append(val)
        
        sub = ' '.join(subtitle)
        
    if len(sub) > 39:
        overlap = len(sub) - 39 # find out how much the subtitle is over the maximum display value
        sub =  sub[overlap : ] # Shift the subtitles to remove the start of them
        n = sub.index(" ")
        sub =  sub[(n + 1) : ] # Trimming array to be the from 1st "full" word in text
    return sub

## 3.
def overlaid_image(frame):
    # Getting the height and width of the dummy frame:
    height, width = frame.shape[:2]

    # Defining the false overlay image:
    data = np.zeros((height, width, 4), dtype=np.uint8)

    # area of interest, where subtitles are placed:
    tr = int(width - 10), int(height - 34)
    [a, b] = tr
    bl = 10, int(height - 3)
    [c, d] = bl

    img = cv2.rectangle(data, tr, bl, (0, 0, 0), -1)

    for h in range(0, height):
        for w in range(0, width):
            if c <= w < a and b <= h < d:
                data[h, w, 3] = 255
            else:
                data[h, w, 3] = 0
    return img

## 4. 
def sub_output(sub, faux_frame):
    # Making a Copy of the Frame in order for no Overwriting:
    clone = faux_frame.copy()
    
    # Frame Dimensions:
    height, width = faux_frame.shape[:2]
    
    # font constraints for opencv put text:
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    
    # Image Variables to display text on rectangle:
    x = int(10)
    y = int(height - 10)
    image = cv2.putText(clone, sub, (x, y), 
                        font, font_scale, (255, 255, 255), 
                        2, cv2.LINE_AA)
    return image

## 5. Collection of functions 3 and 4
def subtitle_output(sub, frame):
    clone = frame.copy()
    
    # Frame Dimensions:
    height, width = frame.shape[:2]
    
    # area of interest, where subtitles are placed:
    tr = int(width - 10), int(height - 34)
    bl = 10, int(height - 3)

    img = cv2.rectangle(clone, tr, bl, (0, 0, 0), -1)
    
    # font constraints for opencv put text:
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    
    # Image Variables to display text on rectangle:
    x = int(10)
    y = int(height - 10)
    image = cv2.putText(img, sub, (x, y), font, font_scale, (255, 255, 255), 2, cv2.LINE_AA)
        
    return image

def video_output(sub, videoIn):
    ret, frame_vga = videoIn.read()

    if (ret):
        outframe = hdmi_out.newframe()
        outframe[:] = frame_vga

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8

        # area of interest, where subtitles are placed:
        tr = int(frame_in_w - 10), int(frame_in_h - 34)
        bl = 10, int(frame_in_h - 3)

        x = int(10)
        y = int(frame_in_h - 10)

        img = cv2.rectangle(outframe, tr, bl, (0, 0, 0), -1)
        image = cv2.putText(img, sub, (x, y), font, font_scale, (255, 255, 255), 2, cv2.LINE_AA)

        hdmi_out.writeframe(img)
    else:
        raise RuntimeError("Error while reading from camera.")