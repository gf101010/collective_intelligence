from recommendations import *
import csv

def loadMovieLens(path='./ml-latest-small'):
    # Files
    movie_file = path + 'movies.csv'
    rating_file = path + 'ratings.csv'
    # Get movie title
    movies = {}
    with open(movie_file, newline='') as moviesfile:
        reader = csv.reader(moviesfile)
        colnum = 0
        for row in reader:
            if colnum == 0:
                continue # Skip header
            # movieId, title, genres
            movies[row[0]] = row[1]

    # Load ratings
    prefs = {}
    with open(rating_file, newline='') as ratingsfile:
        reader = csv.reader(ratingssfile)
        colnum = 0
        for row in reader:
            if colnum == 0:
                continue # Skip header
            # userId, movieId, rating, timestamp
            prefs.setdefault(row[0], {})
            prefs[row[0][movies[row[1]]] = float(row[2])

    return prefs
