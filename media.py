# Lesson 3.4: Make Classes
# Mini-Project: Movies Website

# In this file, you will define the class Movie. You could do this
# directly in entertainment_center.py but many developers keep their
# class definitions separate from the rest of their code. This also
# gives you practice importing Python files.

import webbrowser

class Video():

    '''
    Class Video has the instance variables of
    title, storyline, poster image, trailer youtube'''

    def __init__(self, title, storyline,
                 poster_image_url, trailer_youtube_url):
        self.title = title
        self.storyline = storyline
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url

class Movie(Video):
    ''' In class Movie, which is a child of Video.
    This class provides a way to store movie related information, for this
    child class duration and rating are instance variables
    for this particular class only. ''' 
    def __init__(self, title, storyline, poster_image_url,
                 trailer_youtube_url, duration, rating):
        # initialize instance of class Movie
        Video.__init__(self, title, storyline,
                       poster_image_url, trailer_youtube_url)
        self.duration = duration
        self.rating = rating