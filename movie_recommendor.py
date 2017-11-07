import time
import operator
from itertools import islice, compress,ifilterfalse
from collections import namedtuple, defaultdict
from sets import Set
import itertools

all_genres = ['unknown', 'Action', 'Adventure', 'Animation', 'Children', 
    'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
    'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
    'War', 'Western']

def _parse_movies(movie_file):
    movie_attrs = ['id', 'name', 'release_date', 'unknown_field', 'imdb_url']
    movies = {}
    for line in movie_file:
        tokens = line.split('|')
        if not tokens or len(tokens) < 3:
            continue
        
        movie = dict(zip(movie_attrs, tokens))
        genre_bools = map(int, tokens[len(movie_attrs) : len(tokens)])
        genres = Set(compress(all_genres, genre_bools))
        movie['genres'] = genres
        movie['release_date'] = coerce_date(movie['release_date'])
        movie['number_of_ratings'] = 0
        movie['sum_of_ratings'] = 0
        
        id = movie['id'] = int(movie['id'])
        movies[id] = movie
    
    return movies

def coerce_date(date_as_str):
    date_as_str = date_as_str.strip()
    if date_as_str:
        return time.strptime(date_as_str, '%d-%b-%Y')
    else:
        return None

Rating = namedtuple('Rating', ['userid', 'movieid', 'rating', 'timestamp'])
def _ratings_iterator(ratings_file):
    for line in ratings_file:
        tokens = line.split()
        if not tokens:
            continue
        tokens = map(long, tokens)
        rating = Rating(*tokens)
        yield rating

def get_movies(movie_file, ratings_file):
    movies = _parse_movies(movie_file)
    ratings = _ratings_iterator(ratings_file)
    ratings_for_valid_movies = filter(lambda x : x.movieid in movies, ratings)

    for rating in ratings_for_valid_movies:
        movies[rating.movieid]['sum_of_ratings'] += rating.rating
        movies[rating.movieid]['number_of_ratings'] += 1
    
    return movies

def most_watched_movie(movies):
    return max(movies, key=(lambda m : m['number_of_ratings']))

def most_watched_genre(movies):
    by_genre = defaultdict(int)
    for movie in movies:
        for genre in movie['genres']:
            by_genre[genre] += movie['number_of_ratings']
    
    return max(by_genre.iterkeys(), key=(lambda genre : by_genre[genre]))
    
def most_popular_movie(movies):
    return max(movies, key=(lambda m : m['sum_of_ratings']))

def most_popular_movie_for_genre(movies, genre):
    movies_in_genre = itertools.ifilter(lambda m : genre in m['genres'], movies)
    return most_popular_movie(movies_in_genre)

def most_popular_movie_for_genre_and_year(movies, genre, year):
    movies_with_release_date = itertools.ifilter(lambda m : operator.truth(m['release_date']), movies)
    movies_in_year = itertools.ifilter(lambda m : m['release_date'].tm_year == year, movies_with_release_date)
    movies_in_year_in_genre = itertools.ifilter(lambda m : genre in m['genres'], movies_in_year)
    
    movies_in_year_in_genre = tuple(movies_in_year_in_genre)
    if movies_in_year_in_genre:
        return most_popular_movie(movies_in_year_in_genre)
    else:
        return None        
    
def get_all_years(movies):
    movies_with_release_date = itertools.ifilter(lambda m : operator.truth(m['release_date']), movies)
    years_possibly_duplicate = itertools.imap(lambda m : m['release_date'].tm_year, movies_with_release_date)
    return sorted(list(unique_everseen(years_possibly_duplicate)))
    
def unique_everseen(iterable, key=None):
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element
                
def main():
    movies = get_movies(open('movies/movie.data'), open('movies/ratings.data'))
    
    movies = movies.values()
    print("Most Popular Movie : %s" % most_popular_movie(movies)['name'])
    print

    print("Most Watched Movie : %s" % most_watched_movie(movies)['name'])
    print
    
    print("Most Watched Genre : %s" % most_watched_genre(movies))
    print
    
    print("Popular Movie By Genre")
    print("=========================")
    for genre in all_genres:
        print("%s : %s" % (genre, most_popular_movie_for_genre(movies, genre)['name']))
    print   
    
    for year in get_all_years(movies):
        print
        print("Year %s" % year)
        print("=========================")
        for genre in all_genres:
            movie = most_popular_movie_for_genre_and_year(movies, genre, year)
            if movie:
                movie_name = movie['name']
            else:
                movie_name = "No Movie"
            print("%s : %s" % (genre, movie_name))
    
        

if __name__ == '__main__':
    main()
