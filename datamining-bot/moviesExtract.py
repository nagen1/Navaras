import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from database import Movies, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///navaras_dev.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

#get the urls for telugu movies - https://en.wikipedia.org/wiki/Lists_of_Telugu-language_films - complete
#get the urls for BOllywood movies - https://en.wikipedia.org/wiki/Lists_of_Bollywood_films
#https://en.wikipedia.org/wiki/List_of_Bollywood_films_of_1962
# fix for lxml issue - STATIC_DEPS=true sudo pip install lxml

def getalllinks():
    urls = []
    html = urlopen("https://en.wikipedia.org/wiki/Lists_of_Bollywood_films")
    bsObj = BeautifulSoup(html, "html.parser")

    print("1 - Collecting links.....")

    for link in bsObj.find("div", {"id":"mw-content-text"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            temp = link.attrs['href']
            if 'wiki/List_of_Bollywood_films_of_' in temp and temp not in urls \
                and 'wiki/List_of_Bolloywood_films_of_the_' not in temp:
                urls.append("https://en.wikipedia.org" + temp)

    print("2 - Links Collection complete.")
    return urls

#Scrap the HTML for tables in each url in the urls list
def getMoviesData(url):

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        None

    try:
        soup = BeautifulSoup(r.text, 'lxml')
        tables = soup.findAll("table", {"class" : "wikitable"})

        print("3 - Scraping url: %s", url)
        if tables is not None:  #working code when the values are picked up as TEXT
            for table in tables:
                tableheader = []
                for rows in table.find_all('tr'):
                    for header in rows.find_all('th'):
                        tableheader.append(header.text)

                    tablerowdata = []
                    movieUrl = ''
                    movietitle = ''
                    for row in rows.find_all('td'):

                        for tag in row.find_all('i'):
                            movietitle = tag.text

                            for atag in tag.find_all('a'):
                                if 'index.php' not in atag['href']:
                                    movieUrl = atag['href']

                        if movietitle:
                            tablerowdata.append(movietitle)
                            movietitle = ''
                        if 'rowspan' not in row.attrs and 'style' not in row.attrs and 'id' not in row.attrs and row is not None:
                            tablerowdata.append(row.text)

                    if tablerowdata:
                        if tablerowdata[0] == tablerowdata[1]:
                            tablerowdata.pop(0)
                        if 'Open' in tableheader[0] or '' == tableheader[0] or 'Starting' in tableheader[0]:
                            tableheader.pop(0)
                        movie = Movies()

                        if 'Title' in tableheader[0]:
                            movie.title = tablerowdata[0]
                        if 'Direct' in tableheader[1]:
                            movie.directedBy = tablerowdata[1]
                        if 'Cast' in tableheader[2]:
                            movie.starringBy = tablerowdata[2]

                        if len(tableheader) > 3 or tablerowdata > 3:
                            if 'Genre' in tableheader[3]:
                                movie.genre = tablerowdata[3]
                            if 'Music' in tableheader[3]:
                                movie.musicBy = tablerowdata[3]
                        if len(tableheader) > 4:
                            if 'Music' in tableheader[4] and len(tablerowdata) > 4:
                                movie.musicBy = tablerowdata[4]
                            elif 'Produ' in tableheader[4] or 'Notes' in tableheader[4] and len(tablerowdata) > 4:
                                movie.producedBy = tablerowdata[4]
                        year = re.findall('\d+', url)
                        movie.year = year[0]
                        movie.ref = movieUrl
                        movie.language_id = 2
                        #dbsession.add(movie)
                        #dbsession.commit()
    except AttributeError as e:
        None

    print("4 - Scraping Complete: %s", url)

    return None

#url = 'https://en.wikipedia.org/wiki/List_of_Telugu_films_of_2017'
#data = getMoviesData(url)

teluguurls = getalllinks()              #["https://en.wikipedia.org/wiki/List_of_Telugu_films_of_1990", "https://en.wikipedia.org/wiki/List_of_Telugu_films_of_2000"]
telugu_yr_urls = list(set(teluguurls))  # pick only unique values from list
telugu_yr_urls.sort()                   # sort the Urls in the list

for url in telugu_yr_urls:
    data = getMoviesData(url)