# Main file for presentation tier
# Written by: Bilal Suleman

import sqlite3
import objecttier

dbConn = sqlite3.connect("MovieLens.db")

def print_welcome():
    totalMovies = objecttier.num_movies(dbConn)
    totalReviews = objecttier.num_reviews(dbConn)
    print("** Welcome to the MovieLens app **")
    print()
    print("General Stats:")
    print("  # of movies: {:,}".format(totalMovies))
    print("  # of reviews: {:,}".format(totalReviews))
    print()

def cmd1():
    pattern = input("Enter movie name (wildcards _ and % supported): ")
    movies = objecttier.get_movies(dbConn, pattern)
    if movies is None:
        print("No movies found")
        return
    print()
    print("# of movies found: ", len(movies))
    print()
    if len(movies) > 100:
        print()
        print("There are too many movies to display, please narrow your search and try again...")
        print()
        return
    for x in movies:
        print(x.Movie_ID,":", x.Title, "({0})".format(x.Release_Year))
    print()

def printRows(details, rowName, x1):
    print(rowName, end="")
    if x1 == 1:
        for x in details.Genres:
            print(x, end=", ")
        print()
    elif x1 == 2:
        for x in details.Production_Companies:
            print(x, end=", ")
        print()

def cmd2():
    print()
    id = input("Enter movie id: ")
    print()
    details = objecttier.get_movie_details(dbConn, id)
    if details is None:
        print("No such movie...")
        return
    print(details.Movie_ID, ":", details.Title)
    print(" Release date:", details.Release_Date)
    print(" Runtime:", details.Runtime, "(mins)")
    print(" Orig Language:", details.Original_Language)
    print(" Budget: ${:,} (USD)".format(details.Budget))
    print(" Revenue: ${:,} (USD)".format(details.Revenue))
    print(" Num reviews:", details.Num_Reviews)
    print(" Avg rating:", "{:.2f}".format(details.Avg_Rating), "(0..10)")
    printRows(details, " Genres: ", 1)
    printRows(details, " Production companies: ", 2)
    print(" Tagline:", details.Tagline)

def cmd3():
    print()
    n = int(input("N? "))
    if n < 1:
        print("Please enter a positive value for N...")
        return
    minNumber = int(input("min number of reviews? "))
    if minNumber < 1:
        print("Please enter a positive value for min number of reviews...")
        return
    print()
    movieList = objecttier.get_top_N_movies(dbConn, n, minNumber)
    for x in movieList:
        print(x.Movie_ID, ":", x.Title, "({0}),".format(x.Release_Year),
             "avg rating =", "{:.2f}".format(x.Avg_Rating), "({0} reviews)".format(x.Num_Reviews))

def cmd4():
    rating = int(input("Enter rating (0..10): "))
    if rating < 0 or rating > 10:
        print("Invalid rating...")
        print()
        return
    movie_ID = int(input("Enter movie id: "))
    mod = objecttier.add_review(dbConn, movie_ID, rating)
    if mod == 0:
        print()
        print("No such movie...")
        return
    else:
        print()
        print("Review successfully inserted")
    

def cmd5():
    tagline = input("tagline? ")
    movie_ID = int(input("movie id? "))
    mod = objecttier.set_tagline(dbConn, movie_ID, tagline)
    if mod == 0:
        print()
        print("No such movie...")
    else:
        print()
        print("Tagline successfully set")
    

print_welcome()
cmd = 0
while (cmd != 'x'):
    cmd = input("Please enter a command (1-5, x to exit): ")
    if cmd == '1':
        print()
        cmd1()
        print()
    elif cmd == '2':
        print()
        cmd2()
        print()
    elif cmd == '3':
        print()
        cmd3()
        print()
    elif cmd == '4':
        print()
        cmd4()
        print()
    elif cmd == '5':
        print()
        cmd5()
        print()
    elif cmd == 'x':
        break
