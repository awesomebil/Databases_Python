#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#   
# Completed by: Bilal Suleman
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
   def __init__(self, id, title, releaseYear):
       self._Movie_ID = id
       self._Title = title
       self._Release_Year = releaseYear
   
   @property
   def Movie_ID(self):
      return self._Movie_ID

   @property
   def Title(self):
      return self._Title

   @property
   def Release_Year(self):
      return self._Release_Year
   


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating(Movie):
   def __init__(self, id, title, releaseYear, numReviews, avgRating):
       super().__init__(id, title, releaseYear)
       self._Num_Reviews = numReviews
       self._Avg_Rating = avgRating
   
   @property
   def Num_Reviews(self):
      return self._Num_Reviews
   
   @property
   def Avg_Rating(self):
      return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails(MovieRating):
   def __init__(self, id, title, releaseYear, numReviews, avgRating
               , releaseDate, runtime, originalLanguage, budget, revenue
               , tagline, genres, productionCompanies):
       super().__init__(id, title, releaseYear, numReviews, avgRating)
       self._Release_Date = releaseDate
       self._Runtime = runtime
       self._Original_Language = originalLanguage
       self._Budget = budget
       self._Revenue = revenue
       self._Tagline = tagline
       self._Genres = genres
       self._Production_Companies = productionCompanies
   
   @property
   def Release_Date(self):
      return self._Release_Date
   
   @property
   def Runtime(self):
      return self._Runtime
   
   @property
   def Original_Language(self):
      return self._Original_Language
   
   @property
   def Budget(self):
      return self._Budget
   
   @property
   def Revenue(self):
      return self._Revenue
   
   @property
   def Tagline(self):
      return self._Tagline
   
   @property
   def Genres(self):
      return self._Genres

   @property
   def Production_Companies(self):
      return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
   sql = """select count(Movie_ID) from Movies"""
   row = datatier.select_one_row(dbConn, sql)
   return row[0]


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
   sql = """select count(Rating) from Ratings"""
   row = datatier.select_one_row(dbConn, sql)
   return row[0]


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
   sql = """select Movie_ID, Title, strftime('%Y', Release_Date) from Movies
            where Title like ?
            order by Title asc"""
   rows = datatier.select_n_rows(dbConn, sql, [pattern])
   if rows is None:
      return None

   movies = []

   for row in rows:
      id = row[0]
      title = row[1]
      releaseYear = row[2]
      movies.append(Movie(id, title, releaseYear))
   return movies


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
   sql = """select Title, strftime('%Y', Release_Date), date(Release_Date), Runtime, 
            Original_Language, Budget, Revenue
         from Movies
         where Movies.Movie_ID = ?
         group by Title"""

   row = datatier.select_one_row(dbConn, sql, [movie_id])
   sql = """select Tagline from Movie_Taglines
            where Movie_ID = ?"""
   tagline = datatier.select_one_row(dbConn, sql, [movie_id])
   sql = """select count(Rating) from Ratings
            join Movies on (Movies.Movie_ID = Ratings.Movie_ID)
            where Movies.Movie_ID = ?"""
   numReviews = datatier.select_one_row(dbConn, sql, [movie_id])
   sql = """select avg(Rating) from Ratings
            join Movies on (Movies.Movie_ID = Ratings.Movie_ID)
            where Movies.Movie_ID = ?"""
   avgRating = datatier.select_one_row(dbConn, sql, [movie_id])
   sql = """select Genre_Name from Genres
            join Movie_Genres on (Movie_Genres.Genre_ID = Genres.Genre_ID)
            where Movie_Genres.Movie_ID = ?
            order by Genre_Name asc"""
   genres = datatier.select_n_rows(dbConn, sql, [movie_id])
   sql = """select Company_Name from Companies
            join Movie_Production_Companies on (Movie_Production_Companies.Company_ID = Companies.Company_ID)
            where Movie_Production_Companies.Movie_ID = ?
            order by Company_Name asc"""
   companies = datatier.select_n_rows(dbConn, sql, [movie_id])
   if row is None:
      return None
   if len(row) == 0:
      return None
   if avgRating[0] is None:
      avgRating = (0,)
   if len(tagline) == 0:
      tagline = ("",)
   
   genreList = []
   companyList = []

   for r in genres:
      genreList.append(r[0])
   for r in companies:
      companyList.append(r[0])
   
   movieDetails = MovieDetails(movie_id, row[0], row[1], numReviews[0], avgRating[0],
                              row[2], row[3], row[4], row[5], row[6], tagline[0], genreList, companyList)
   return movieDetails
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
   sql = """select Movies.Movie_ID, Title, strftime('%Y', Release_Date), count(Rating), avg(Rating)
            from Movies join Ratings on (Movies.Movie_ID = Ratings.Movie_ID)
            group by Movies.Movie_ID
            having count(Rating) >= ?
            order by avg(Rating) desc
            limit ?"""
   rows = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
   if rows is None:
      return None
   
   movieRatings = []

   for row in rows:
      movieRatings.append(MovieRating(row[0], row[1], row[2], row[3], row[4]))
   return movieRatings


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
   sql = """insert into Ratings(Movie_ID, Rating)
            values(?, ?)"""

   mod = datatier.perform_action(dbConn, sql, [movie_id, rating])
   sql = """select Title from Movies
            where Movie_ID = ?"""
   row = datatier.select_one_row(dbConn, sql, [movie_id])
   if len(row) == 0:
      return 0
   if mod > 0:
      return 1
   else:
      return 0



##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
   sql = """update Movie_Taglines
            set Tagline = ?
            where Movie_ID = ?"""
   mod = datatier.perform_action(dbConn, sql, [tagline, movie_id])
   sql = """select Title from Movies
            where Movie_ID = ?"""
   movieFound = datatier.select_one_row(dbConn, sql, [movie_id])
   if len(movieFound) == 0:
      return 0
   if mod == 0:
      sql = """insert into Movie_Taglines(Tagline, Movie_ID)
               values(?, ?) """
      mod = datatier.perform_action(dbConn, sql, [tagline, movie_id])
   if mod > 0:
      return 1
   else:
      return 0
