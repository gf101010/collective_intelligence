from recommendations import *
import csv

def loadMovieLens(path='./ml-latest-small/'):
    # Files
    movie_file = path + 'movies.csv'
    rating_file = path + 'ratings.csv'
    # Get movie title
    movies = {}
    with open(movie_file, newline='') as moviesfile:
        reader = csv.reader(moviesfile)
        head = True
        for row in reader:
            if head:
                head = False
                continue # Skip header
            # movieId, title, genres
            movies[int(row[0])] = row[1]

    # Load ratings
    prefs = {}
    with open(rating_file, newline='') as ratingsfile:
        reader = csv.reader(ratingsfile)
        head = True
        for row in reader:
            if head:
                head = False
                continue # Skip header
            # userId, movieId, rating, timestamp
            prefs.setdefault(int(row[0]), {})
            prefs[int(row[0])][movies[int(row[1])]] = float(row[2])

    return prefs

