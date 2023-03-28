# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file hosts the post processing functions for the output .json files from rev.ai.       #
# Functions held are:                                                                         #
#                                                                                             #
#        1. 'PostProcessing_Live' which collates the real time and 'Real' subtitles           #
#            their respective timings;                                                        #
#                                                                                             #
#        2. 'real_t' display the text rather than the json file;                              #
#                                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

## Importing realvent Modules
import json

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

    return sub
