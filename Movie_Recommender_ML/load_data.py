# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:36:01 2019

@author: scates
"""
from sklearn.feature_extraction.text import CountVectorizer

import pandas as pd

#load data
#change the path name as needed
df_movies = pd.DataFrame()
df_movies = pd.read_csv('./ml-latest-small/movies.csv')

df_tags = pd.DataFrame()
df_tags = pd.read_csv('./ml-latest-small/tags.csv')

df_ratings = pd.DataFrame()
df_ratings = pd.read_csv('./ml-latest-small/ratings.csv')

#make a new data frame with rows for each user and columns for each movie
df_ratings_matrix = df_ratings.pivot(index = 'userId', columns ='movieId', values = 'rating').fillna(0)


#concatenate all the tags for each movie along with the genres
grouped = df_tags.groupby('movieId')
d=[]
for name, group in grouped:
    tags = pd.Series(group.tag).str.cat(sep=" ")
    row = df_movies[df_movies.movieId == name]
    #Uncomment this to also include the movie title with the tags
    #title = row.title.values[0][:-7]
    genres = row.genres.values[0].replace("|", " ")
    tags = tags + " " + genres #+ " "+ title
    d.append({ 'movieId': name,  'tags': tags})
df_tag_strings = pd.DataFrame(d)
df_tag_strings=df_tag_strings.set_index('movieId')

# Count Vectorizer
vectorizer = CountVectorizer()
X_count = vectorizer.fit_transform(data[:]['tags'].values)

X_occur = X_count
X_occur[X_count[:,:]>0]=1