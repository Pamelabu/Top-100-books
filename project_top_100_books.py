from bs4 import BeautifulSoup as bs

import requests
import pandas as pd
import os
import sqlite3

os.environ['REQUESTS_CA_BUNDLE'] = 'C:/Users/Pamela.Buchwald/Desktop/Szkolenia Business Intelligence/notatki/Zscaler Root CA.crt' #certyfikat lokalny

page = 1

titles = []
avg_rates = []
no_of_votes = []

while page != 8:
    url = f"https://lubimyczytac.pl/top100?page={page}"
    response = requests.get(url)
    html = response.content
    soup = bs(html, 'html.parser')


    for a in soup.find_all('a', class_= 'authorAllBooks__singleTextTitle float-left'):
        titles.append(a.get_text(strip=True))

    for span in soup.find_all('span', class_= 'listLibrary__ratingStarsNumber'):
        avg_rates.append(float(span.get_text(strip=True).replace(',','.')))

    for div in soup.find_all('div', class_= 'listLibrary__ratingAll'):
        no_of_votes.append(int(div.get_text(strip=True).rstrip(' ocen')))

    page = page + 1

best_books = {'Title':titles, 'Average rate':avg_rates, 'No of votes':no_of_votes}
df_best_books = pd.DataFrame(best_books)


df_best_books.loc[df_best_books['Average rate'] <= 4, 'Is the book worth reading?'] = 'No.. it is a totally distaster'
df_best_books.loc[(df_best_books['Average rate'] > 4) & (df_best_books['Average rate'] <6), 'Is the book worth reading?'] = 'The book is not good, do not waste your time'
df_best_books.loc[(df_best_books['Average rate'] >= 6) & (df_best_books['Average rate'] <7.5), 'Is the book worth reading?'] = 'It seems to be an average book, you can find something better.'
df_best_books.loc[(df_best_books['Average rate'] >= 7.5) & (df_best_books['Average rate'] <9), 'Is the book worth reading?'] = 'It must be a fantastic book! Try it.'
df_best_books.loc[df_best_books['Average rate'] >=9, 'Is the book worth reading?'] = 'Rates are great. The book must be marvelous.'

df_best_books.loc[df_best_books['No of votes'] <= 100, 'Population of voters'] = 'So far, not many readers'
df_best_books.loc[(df_best_books['No of votes'] > 100) & (df_best_books['No of votes'] <500), 'Population of voters'] = 'Less than 500 readers, the book is not very popular'
df_best_books.loc[(df_best_books['No of votes'] >= 500) & (df_best_books['No of votes'] <2000), 'Population of voters'] = 'This book seems to have an average popularity.'
df_best_books.loc[(df_best_books['No of votes'] >= 2000) & (df_best_books['No of votes'] <10000), 'Population of voters'] = 'Ohh, this book may be very popular!'
df_best_books.loc[df_best_books['No of votes'] >=10000, 'Population of voters'] = 'This book already has 10 000 readers. Have you heard about it yet?.'


conn = sqlite3.connect('Top_100_books.sqlite')

df_best_books.to_sql('Top100_books', conn, if_exists='append', index=False)

conn.close()