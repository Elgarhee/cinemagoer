#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_movie.py

Usage: get_movie "movie_id"

Show some info about the movie with the given movie_id (e.g. '0133093'
for "The Matrix", using 'http' or 'mobile').
Notice that movie_id, using 'sql', are not the same IDs used on the web.
"""

import sys
from Levenshtein import distance as levenshtein_distance

# Import the Cinemagoer package.
try:
    import imdb
except ImportError:
    print('You need to install the Cinemagoer package!')
    sys.exit(1)


if len(sys.argv) != 2:
    print('Only one argument is required:')
    print('  %s "movie_id"' % sys.argv[0])
    sys.exit(2)

movie_id = sys.argv[1].lower()

i = imdb.IMDb()

try:
    # Get a Movie object with the data about the movie identified by the given movie_id.
    movie = i.get_movie(movie_id)
except imdb.IMDbError as e:
    print("Probably you're not connected to Internet. Complete error report:")
    print(e)
    sys.exit(3)


if not movie:
    print('It seems that there\'s no movie with movie_id "%s"' % movie_id)
    sys.exit(4)

# Show the main info about the movie
print(movie.summary())

# Additional code to demonstrate Levenshtein distance for movie title selection
if len(sys.argv) == 3:
    search_title = sys.argv[2].lower()
    results = i.search_movie(search_title)

    if results:
        # Filter results to include only movies
        movie_results = [result for result in results if result.get('kind') == 'movie']

        if movie_results:
            # Choose the best match from the top two results based on Levenshtein distance
            top_two_results = movie_results[:2]
            best_match = min(top_two_results, key=lambda movie: levenshtein_distance(search_title, movie.get('title', '').lower()))

            # Print the best result
            print(f'    Best match for "{search_title}":')
            print(best_match.summary())
        else:
            print(f'No movie matches for "{search_title}", sorry.')
    else:
        print(f'No matches for "{search_title}", sorry.')
