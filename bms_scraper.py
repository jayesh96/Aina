from bs4 import BeautifulSoup
import requests
url = 'https://in.bookmyshow.com/national-capital-region-ncr/movies'
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data,"lxml")

type = soup.find('div',attrs={"class":"mv-row"}).findAll('div',attrs={"class":"wow fadeIn movie-card-container"})
# val = soup.findAll("a",class_="__movie-name")

movie_data = []

for movie in type:
    movie_details = {}
    movie_name = movie.find('div',attrs={"class":"detail"}).find('a',attrs={"class":"__movie-name"}).get('title')
    movie_genres_unedited = movie.get('data-genre-filter').split("|")[1:]
    movie_language_unedited = movie.get('data-language-filter').split("|")[1:]
    
    print movie
    
    if not movie_genres_unedited:
        movie_genres_unedited.append("ALL")
        
    movie_details["movie_name"] = str(movie_name)
    movie_details["genre"] = movie_genres_unedited
    movie_details["language"] = movie_language_unedited
    
        
    movie_data.append(movie_details)

    
print movie_data

print "------------------------"


import json
_moviedata = json.dumps(movie_data)


print(_moviedata)
