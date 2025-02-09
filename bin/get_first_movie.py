#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_first_movie.py

Usage: get_first_movie "movie title"

Search for the given title and print the best matching result.
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
    print('  %s "movie title"' % sys.argv[0])
    sys.exit(2)

title = sys.argv[1].lower()


i = imdb.IMDb()

try:
    # Do the search, and get the results (a list of Movie objects).
    results = i.search_movie(title)
except imdb.IMDbError as e:
    print("Probably you're not connected to Internet.  Complete error report:")
    print(e)
    sys.exit(3)

if not results:
    print('No matches for "%s", sorry.' % title)
    sys.exit(0)

# Filter results to include only movies
movie_results = [result for result in results if result.get('kind') == 'movie']

if not movie_results:
    print('No movie matches for "%s", sorry.' % title)
    sys.exit(0)

# Choose the best match from the top two results based on Levenshtein distance
top_two_results = movie_results[:2]
best_match = min(top_two_results, key=lambda movie: levenshtein_distance(title, movie.get('title', '').lower()))

# Print the best result
print('    Best match for "%s"' % title)

# This is a Movie instance.
movie = best_match

# So far the Movie object only contains basic information like the
# title and the year; retrieve main information:
i.update(movie)

print(movie.summary())
