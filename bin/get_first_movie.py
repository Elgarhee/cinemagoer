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


def main():
    # التحقق من صحة الوسائط
    if len(sys.argv) != 2:
        print('Usage: %s "movie title"' % sys.argv[0])
        sys.exit(2)

    title = sys.argv[1].lower()

    # إنشاء كائن IMDb
    i = imdb.IMDb()

    try:
        # البحث عن الأفلام
        results = i.search_movie(title)
    except imdb.IMDbError as e:
        print("Error occurred while searching for the movie:")
        print(e)
        sys.exit(3)

    # التحقق من وجود نتائج
    if not results:
        print('No matches for "%s", sorry.' % title)
        sys.exit(0)

    # فلترة النتائج لتشمل الأفلام فقط
    movie_results = [result for result in results if result.get('kind') == 'movie']

    if not movie_results:
        print('No movie matches for "%s", sorry.' % title)
        sys.exit(0)

    # اختيار أفضل تطابق من أول نتيجتين باستخدام Levenshtein distance
    top_two_results = movie_results[:2]
    best_match = min(
        top_two_results,
        key=lambda movie: levenshtein_distance(title, movie.get('title', '').lower())
    )

    # طباعة أفضل نتيجة
    print('Best match for "%s":' % title)

    # تحديث معلومات الفيلم
    i.update(best_match)

    # طباعة ملخص الفيلم
    print(best_match.summary())


if __name__ == "__main__":
    main()
