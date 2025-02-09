#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_movie.py

Usage: get_movie "movie_id" ["search_title"]

Show some info about the movie with the given movie_id (e.g. '0133093'
for "The Matrix"). Optionally, search for a movie title and select the best match
using Levenshtein distance.
"""

import sys
from Levenshtein import distance as levenshtein_distance

# Import the Cinemagoer package.
try:
    import imdb
except ImportError:
    print('You need to install the Cinemagoer package!')
    sys.exit(1)


def get_movie_info(movie_id):
    """Get and display information about a movie using its IMDb ID."""
    i = imdb.IMDb()

    try:
        # Get a Movie object with the data about the movie identified by the given movie_id.
        movie = i.get_movie(movie_id)
    except imdb.IMDbError as e:
        print("Error occurred while fetching movie information:")
        print(e)
        sys.exit(3)

    if not movie:
        print(f'It seems that there\'s no movie with movie_id "{movie_id}"')
        sys.exit(4)

    # Show the main info about the movie
    print(movie.summary())


def find_best_match(search_title):
    """Search for a movie title and select the best match using Levenshtein distance."""
    i = imdb.IMDb()

    try:
        # Search for the movie title
        results = i.search_movie(search_title)
    except imdb.IMDbError as e:
        print("Error occurred while searching for the movie:")
        print(e)
        sys.exit(5)

    if not results:
        print(f'No matches for "{search_title}", sorry.')
        sys.exit(0)

    # Filter results to include only movies
    movie_results = [result for result in results if result.get('kind') == 'movie']

    if not movie_results:
        print(f'No movie matches for "{search_title}", sorry.')
        sys.exit(0)

    # Choose the best match from the top two results based on Levenshtein distance
    top_two_results = movie_results[:2]
    best_match = min(
        top_two_results,
        key=lambda movie: levenshtein_distance(search_title, movie.get('title', '').lower())
    )

    # Print the best result
    print(f'Best match for "{search_title}":')
    print(best_match.summary())


def main():
    # التحقق من صحة الوسائط
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage: %s "movie_id" ["search_title"]' % sys.argv[0])
        sys.exit(2)

    movie_id = sys.argv[1].lower()

    # عرض معلومات الفيلم باستخدام movie_id
    get_movie_info(movie_id)

    # إذا تم توفير search_title، قم بالبحث عن أفضل تطابق
    if len(sys.argv) == 3:
        search_title = sys.argv[2].lower()
        find_best_match(search_title)


if __name__ == "__main__":
    main()
