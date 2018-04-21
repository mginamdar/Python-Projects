#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 14:44:21 2018

@author: malhar
"""
#Get url details
from requests import get
url='https://www.imdb.com/search/title?release_date=2018&sort=num_votes,desc&ref_=rlm_yr'
response=get(url)
print(response.text[:500])

#Use Parser
from bs4 import BeautifulSoup
html_soup=BeautifulSoup(response.text,'html.parser')
type(html_soup)

#Use find all
movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
print(type(movie_containers))
print(len(movie_containers))

#Extract data for a single movie
#Name
first_movie=movie_containers[0]
first_name=first_movie.h3.a.text
first_name
#Year of Movie release
first_year=first_movie.h3.find('span',class_='lister-item-year text-muted unbold')
first_year=first_year.text
first_year
#IMDB rating
first_imdb=float(first_movie.strong.text)
first_imdb
#Metadata
first_metadata=first_movie.find('span',class_='metascore favorable')
first_metadata=int(first_metadata.text)
first_metadata
#Votes
first_votes=first_movie.find('span',{'name':'nv'})
first_votes=int(first_votes['data-value'])
first_votes

#Remove all movies without a metascore
fourth_movie_mscore = movie_containers[3].find('div', class_ = 'ratings-metascore')
type(fourth_movie_mscore)

#Collect Data of a Single Page
names=[]
years=[]
imdb_ratings=[]
metadata_ratings=[]
votes=[]

for container in movie_containers:
    if container.find('div', class_ = 'ratings-metascore') is not None:
        
        name= container.h3.a.text
        names.append(name)
        
        year=container.h3.find('span',class_='lister-item-year').text
        years.append(year)
        
        imdb_rating=float(container.strong.text)
        imdb_ratings.append(imdb_rating)
        
        metadata_rating=container.find('span',class_='metascore').text
        metadata_ratings.append(int(metadata_rating))
        
        vote=container.find('span',{'name':'nv'})['data-value']
        votes.append(int(vote))

#test Pandas
import pandas as pd

test_df = pd.DataFrame({'movie': names,
                       'year': years,
                       'imdb': imdb_ratings,
                       'metascore': metadata_ratings,
                       'votes': votes})
print(test_df.info())
test_df

#export to csv
test_df.to_csv('out.csv')

#Create page and release year urls
pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2000,2018)]

#full code to scrape IMDB
from time import time, sleep
import random
import sys
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from requests import get
from random import randint
from IPython.core.display import clear_output


names=[]
years=[]
imdb_ratings=[]
metadata_ratings=[]
votes=[]

start_time = time()
requests=0

for year_url in years_url:
    for page in pages:
        response = get('https://www.imdb.com/search/title?release_date=' + year_url + '&sort=year,asc&page=' + page + '&ref_=adv_prv')
        
        #Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)
        
        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')  
            break 
        
        page_html = BeautifulSoup(response.text, 'html.parser')
        
        movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

        
        for container in movie_containers:
            if container.find('div', class_ = 'ratings-metascore') is not None:
        
                name= container.h3.a.text
                names.append(name)
        
                year=container.h3.find('span',class_='lister-item-year').text
                years.append(year)
                
                imdb_rating=float(container.strong.text)
                imdb_ratings.append(imdb_rating)
        
                metadata_rating=container.find('span',class_='metascore').text
                metadata_ratings.append(int(metadata_rating))
        
                vote=container.find('span',{'name':'nv'})['data-value']
                votes.append(int(vote))

test_df = pd.DataFrame({'movie': names,
                       'year': years,
                       'imdb': imdb_ratings,
                       'metascore': metadata_ratings,
                       'votes': votes})
print(test_df.info())
test_df

#export to csv
test_df.to_csv('out.csv')
test_df['year'].unique()
test_df.loc[:, 'year'] = test_df['year'].str[-5:-1].astype(int)
test_df['year'].head