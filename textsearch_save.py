# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:58:50 2018

This script aim to take a text from a .txt file, acquire the (interesting) 
words that appears in it and count their occurence.
Then words are selected randomly with an associated duration, 
both the selection probability and the duration of a word are related to the
 frequency of the word in the text.
The images are displayed using a simple matplotilib figure+animation, and saved
as a video.

Parameters for the duration of the video and the what .txt file to use
 can be adjusted. The display can be adjusted in the functions defining the
 figure.
 
 This project was made for the course
 UWAS-C0037 Microscopic View at Aalto University
 
@author: Bastien
"""
# import some usefull  libraries
import numpy as np
import scipy as sp
import os
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def get_words(filepath, removed_list):
    """ This function takes a filepath to a text file and a list of character
    to remove as input. It remove those characters from the lines, put
    everything in lowercase and creat a list with the words in the file.
    The list is returned. The file is not modified."""
    # create an empty list to contain the words
    words_list = []
    # open the file (create a handle)
    text = open(filepath)
    # create a map that replace the character in to_remove by "None"
    remove_map = dict.fromkeys(map(ord, '_:;!?,.)(_"$“”'+"'"), None)
    # for each line available in the file...
    for line in text:
        # we put everything in lowercase,...
        line = line.lower()
        # we aply the map (removing some characters)...
        line_removed = line.translate(remove_map)
        # and we split the line into words
        words = line_removed.split()
        # for each word in the words of the line...
        for word in words:
            # if the word is not in the list of words to be removed
            if (word in removed_list)==False:
                # we add the word to the list of words
                words_list.append(word)
    # the list of words is the output
    return words_list, remove_map

def word_count(words_list):
    """This function takes a list of words as inout. It creates a dictionnary
    associating the different words contained in the list and their number of
    occurences. The dictionnary is returned."""
    # create an empty dictionnary
    word_count_dict = {}
    # for each word in the list...
    for word in words_list:
        #...we try...
        try:
            #...to add one to the counter associated with the word
            word_count_dict[word] = word_count_dict[word]+1
            #but if this return an error (there's no counter for this word),...
            # (as it is the first time it is encountered)
        except KeyError :
            # ...,then we create a counter with value 1 associated to this word
            word_count_dict[word] = 1  
    # we return the dictionnary as output
    return word_count_dict
    
# define a function creating instructions for a random video
def create_random_words_video(max_duration, scale,\
                                                 words_list, word_count_dict):
    # we defined the total duration of the video
    # we defined a scale for the duration of words
    # initialize the duration of the video being created to 0
    total_duration = 0
    # initialize a list that will contain the images and their duration
    video_list = []
    # how many words (in total, not accounting for degeneracies) were counted
    nb_words = len(words_list)
    # we will add frames until the video has the required duration
    while total_duration < max_duration:
        # choose an index randomly
        index = int(np.floor(random.uniform(0, nb_words)))
        # take the words at that index,
        # the words that appear more often are more likely to be chosen
        word = words_list[index]
        # the duration is the number of occurence of that word in the text,
        # with a bit of random noise and scaled
        duration = int(np.floor(scale*word_count_dict[word]*\
                        random.uniform(0.5, 1.5)))
        # add the word and "duration" times to the list(the script)of video
        for i in range(duration):
            video_list.append([word, duration])
        # ajust the new total duration
        total_duration = total_duration + duration
    # at the end, return the instructions for creating the video
    return video_list

# define the name of the file to open (in the current working directory)
filename = "questions.txt"
# define the required total lenght of the video
max_duration = 60000 # seconds
# define a scale for the duration of words
scale = 2

# what is the current working directory
directory = os.getcwd()
# the complete path to the file is then
filepath = directory+"/"+ filename
filepath_removed = directory+"/words_removed.txt"
        
# define a list of words to remove (not count)
removed_list, remove_map = get_words(filepath_removed, [])
# the defined function are applied to the chosen file
words_list, remove_map = get_words(filepath, removed_list)
word_count_dict = word_count(words_list)
video_list = create_random_words_video(max_duration, scale, words_list,\
 word_count_dict)

# create a figure
fig = plt.figure()
# create a plotting area on the figure
ax = fig.add_subplot(111)
# plot an empty str, defining the plotting parameters
hfont = {'fontname':'TeXGyreHeros'}
fig_word = ax.text(0.1, 0.5, '', fontsize=25, color='white',fontweight='bold',\
                                **hfont)
# no axis please
ax.axis('off')
# background to be blue as it can gets
fig.set_facecolor([0,0,1])

# deine the function that start the video (that is,
# to assign an empty str to the plot) [this step is optionnal by the way]
def init_fig():
    fig_word.set_text('')
    return fig_word

# define the function that update the video at the i^th iteration/frame
def updatefig(i):
    # take the i^th word+duration
    word, duration = video_list[i][0], video_list[i][1]
    # plot the word
    fig_word.set_text(word.upper())
#    # change position randomly
#    fig_word.set_position((random.gauss(0.1, 0.05), random.gauss(0.5, 0.1)))
    # return the result to the video
    return fig_word
#    # wait for the duration before next update
#    time.sleep(duration)
    

# create a video from the function defined
ani = animation.FuncAnimation(fig, updatefig, frames=len(video_list),\
                             init_func=init_fig)#, blit=True)
## show the video
#plt.show()   
# save the video as .mp4 [unfortunatly a proprietary format...],
# specifying what process is used to encode and the background color
ani.save("test.mp4", writer=animation.FFMpegWriter(fps=5),\
             savefig_kwargs={'transparent': True, 'facecolor': [0,0,1]})
            

