from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import manhattan_distances
from operator import itemgetter


#load data
#change the path name as needed
df_movies = pd.DataFrame()
df_movies = pd.read_csv('./ml-latest-small/movies.csv', encoding="utf-8-sig")

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
    tags = tags + " " + genres # + " "+ title
    d.append({ 'movieId': name,  'tags': tags})
df_tag_strings = pd.DataFrame(d)
#df_tag_strings=df_tag_strings.set_index('movieId')


data = []
for index, row in df_movies.iterrows():
            
    if ((row.movieId in df_tag_strings[:]['movieId'].unique()) == False):       
        genres = row['genres'].replace("|", " ")
        data.append({'movieId': row['movieId'], 'tags': genres})
        
    else:
        new_row = df_tag_strings[df_tag_strings[:]['movieId'] == row['movieId']]
        data.append({'movieId': new_row['movieId'].values[0], 'tags': new_row['tags'].values[0]})
   
    
df_tag_strings_new = pd.DataFrame(data)


#Part 3

# Count Vectorizer
vectorizer = CountVectorizer()
X_count = vectorizer.fit_transform(df_tag_strings_new.loc[:, 'tags'].values)
#print(X_count)
X_dense = X_count.todense()  # For euclidean distances


# TF-IDF
tf= TfidfVectorizer(stop_words = 'english')
tf_idf = tf.fit_transform(df_tag_strings_new['tags'])

#print (tf_idf)
#print (tf_idf.shape)


#Similarity/ Distance measures
cos_sim_count = cosine_similarity(X_count) # For count vectorizer

cos_sim_tfidf = linear_kernel(tf_idf,tf_idf)  # Dot Product because of TFIDF vectors and faster processing

man_dist_count = manhattan_distances(X_count)

euc_dist_count = euclidean_distances(X_dense)

euc_dist_tfidf = euclidean_distances(tf_idf)


#reverse lookup of title and movie indices
df_movie_indices = pd.Series(df_movies.index, index=df_movies['title']).drop_duplicates()

def recommend_content(title, similarity, matrix):  # Change cosine similarity matrices here (TFIDF/Count)
    
    index = df_movie_indices[title]
    

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(matrix[index]))

    # Sort the movies based on the similarity scores
    if (similarity == 'euc') or (similarity == 'man'):
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=False) # lower distance = higher similarity
    else:
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # cosine
        
    
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    

    # Return the top 10 most similar movies
    return df_movies['title'].iloc[movie_indices]


print ("Content Based Recommender: \n\n", recommend_content('Batman Forever (1995)', 'cos', cos_sim_tfidf))
print()


#Part 4 user recommendation

#Similarity/Distances
cosine_sim_ratings = cosine_similarity(df_ratings_matrix)
euc_dist_ratings = euclidean_distances(df_ratings_matrix)
man_dist_ratings = manhattan_distances(df_ratings_matrix)

df_ratings_matrix_new = df_ratings_matrix.values # nparray matrix for easier iteration

#Function for pairwise jaccard
def pairwise_jaccard(X):
    """Computes the Jaccard distance between the rows of `X`.
    """
    X = X.astype(bool).astype(int)

    intrsct = X.dot(X.T)
    row_sums = intrsct.diagonal()
    unions = row_sums[:,None] + row_sums - intrsct
    dist = 1.0 - intrsct / unions
    return dist

jac_dist_ratings = pairwise_jaccard(df_ratings_matrix_new)


    
def recommend_users(input_user, similarity, matrix):  # Change cosine similarity matrices here (TFIDF/Count)
       
    input_user = input_user-1
    
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(matrix[input_user]))

    # Sort the movies based on the similarity scores
    if (similarity == 'euc') or (similarity == 'man') or (similarity == 'jac'):
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=False) # lower distance = higher similarity
    else:
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # cosine
    
    
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    
    # Create a dataframe and -1 from the userids to solve indexing
    df_sim_scores = pd.DataFrame(sim_scores).rename(columns={0: 'userId', 1: 'Similarity/Distances'})
    df_sim_scores["userId"] = df_sim_scores["userId"].apply(lambda x: x - 1)
    

    # Return the top 10 most similar movies
    return df_sim_scores


print("10 Similar users (most to least): \n\n",  recommend_users(50, 'euc', euc_dist_ratings))
print()

#Part 4 movie recommendation (collaborative)

#df_ratings_new = df_ratings.as_matrix(columns = ['userId', 'movieId', 'rating'])
df_ratings_new = (df_ratings.sort_values('userId'))
df_ratings_new = df_ratings_new.as_matrix(columns = ['userId', 'movieId', 'rating'])


#Create Each Users ratings list
users_list = []
for i in range(1,611):
    list1 = []
    for j in range(0, len(df_ratings_new)):
        if df_ratings_new[j][0] == i:
            list1.append(df_ratings_new[j])
        else:
            break
    df_ratings_new = df_ratings_new[j:]
    users_list.append(list1)


def recommend_movies_collab(input_user, similarity, matrix):
    
    sim_user = int(recommend_users(input_user, similarity, matrix).loc[0]['userId'])
    
    #get sorted lists for users (highest rating to lowest)
    input_user_list = sorted(users_list[input_user -1], key=itemgetter(2), reverse = True)
    sim_user_list = sorted(users_list[sim_user], key=itemgetter(2), reverse = True)
    
    #Exclude common movies between users
    common_list = []
    full_list = []
    for i in input_user_list:
        for j in sim_user_list:
            if(int(i[1])== int(j[1])):
                common_list.append(int(j[1]))
            full_list.append(j[1])
    
    common_list = set(common_list)  
    full_list = set(full_list)
    recommendation = list(full_list.difference(common_list))
    
    #for Reverse lookup of movieIds and movie indices
    df_movieId_indices = pd.Series(df_movies.index, index=df_movies['movieId']).drop_duplicates()
    
    movieId_indices = [int(i) for i in recommendation]
    movie_indices = []
    
    
    #Get movie indices
    for i in movieId_indices:
        movie_indices.append(df_movieId_indices[i])
    
    return df_movies['title'].iloc[movie_indices]


print("Movies recommended by Collaborative approach: \n\n", recommend_movies_collab(50, 'euc', euc_dist_ratings) )
print()

