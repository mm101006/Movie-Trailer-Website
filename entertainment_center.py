import media
import fresh_tomatoes
import tmdbsimple as tmdb
import time
tmdb.API_KEY = '3d1b1c911f61a0abca6cf5a94c2c0944'

# accesses the movies api and obtains each obejct in now_playing
now_playing_query = tmdb.Movies().now_playing()

now_playing_ids = []
now_playing_title = []
now_playing_overview = []
now_playing_poster = []
now_playing_youtube = []
now_playing_runtime = []
now_playing_certification = []

def find_certification():
    certification = ''
    for country in countries:
        if (country['iso_3166_1'] == 'US') & (country['certification'] != ''):
            certification = country['certification']
    if certification == '':
        certification = "NR"
    else:
        certificaiton = certification
    return certification

# this while looping is looping through the objects and pulling the information
# from the api and appending the information to a list
count = 0
while (count <= len(now_playing_query['results'])-1):
    id = now_playing_query['results'][count]['id']
    title = now_playing_query['results'][count]['title']
    overview = now_playing_query['results'][count]['overview'].encode('utf-8')
    poster = now_playing_query['results'][count]['poster_path']
    youtube = tmdb.Movies(id).videos()['results'][0]['key']
    time.sleep(.5)
    runtime = tmdb.Movies(id).info()['runtime']
    countries = tmdb.Movies(id).releases()['countries']
    certification = find_certification()

    now_playing_ids.append(id)
    now_playing_title.append(title)
    now_playing_overview.append(overview)
    now_playing_poster.append(poster)
    now_playing_youtube.append(youtube)
    now_playing_runtime.append(runtime)
    now_playing_certification.append(certification)

    count += 1

# the objs variable is creating instances of the Movie Class by
# using a for each type statement running through each corresponding list.
objs = (media.Movie(now_playing_title[i],
                    now_playing_overview[i],
                    "https://image.tmdb.org/t/p/original/" +
                    str(now_playing_poster[i]),
                    "https://www.youtube.com/watch?v=" +
                    str(now_playing_youtube[i]),
                    str(now_playing_runtime[i]),
                    now_playing_certification[i])
        for i in range(len(now_playing_ids)))

entertainment = []

for obj in objs:
    entertainment.append(obj)


# call the function from the fresh_tomatoes.py script
# and pass in entertainment array.
fresh_tomatoes.open_movies_page(entertainment)
