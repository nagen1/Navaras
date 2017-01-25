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
# fix for lxml issue - STATIC_DEPS=true sudo pip install lxml

def getalllinks():
    urls = []
    html = urlopen("https://en.wikipedia.org/wiki/Lists_of_Telugu-language_films")
    bsObj = BeautifulSoup(html, "html.parser")

    print("1 - Collecting links.....")

    for link in bsObj.find("div", {"id":"mw-content-text"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            temp = link.attrs['href']
            if 'wiki/List_of_Telugu_films_of_' in temp and temp not in urls \
                and 'wiki/List_of_Telugu_films_of_the_' not in temp:
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
                    for row in rows.find_all('td'):

                        if 'rowspan' not in row.attrs and 'style' not in row.attrs and 'id' not in row.attrs and row is not None:
                            for tag in row.find_all('i'):
                                movietitle = tag.text
                                movieUrl = ''

                                for atag in tag.find_all('a'):
                                    if 'index.php' not in atag['href']:
                                        movieUrl = atag['href']

                                if movieUrl:
                                    tablerowdata.append(movieUrl)
                                    movieUrl = ''
                                else:
                                    tablerowdata.append('None')

                            if movietitle:
                                tablerowdata.append(movietitle)
                                movietitle = ''
                            else:
                                tablerowdata.append(row.text)

                    year = re.findall('\d+', url)
                    if tablerowdata:
                        if 'Open' in tableheader[0]:
                            tableheader.pop(0)
                        movie = Movies()
                        movie.ref = tablerowdata[0]
                        movie.title = tablerowdata[1]
                        movie.directedBy = tablerowdata[2]
                        movie.starringBy = tablerowdata[3]
                        if tableheader[3] == 'Genre':
                            movie.genre = tablerowdata[4]
                        if 'Music' in tableheader[3]:
                            movie.musicBy = tablerowdata[4]
                        if len(tablerowdata) > 4:
                            if 'Music' in tableheader[4] and tablerowdata[5]:
                                movie.musicBy = tablerowdata[5]
                            elif 'Produ' in tableheader[4] or 'Note' in tableheader[4]:
                                movie.producedBy = tablerowdata[5]
                            if len(tableheader) > 5 and len(tablerowdata) > 5:
                                if 'Produ' in tableheader[5] or 'Notes' in tableheader[5]:
                                    movie.producedBy = tablerowdata[6]
                        movie.year = year[0]
                        #dbsession.add(movie)
                        #dbsession.commit()
    except AttributeError as e:
        None

    print("4 - Scraping Complete: %s", url)

    return None

url = 'https://en.wikipedia.org/wiki/List_of_Telugu_films_of_1961'
data = getMoviesData(url)

#header = "Title,Director,Cast,Genre, Production House"
#file = open(r"/Users/nagen/Documents/Python-Workspace/wiki-scraping/output.csv", "wb")
#file.write(bytes(header, encoding="UTF-8", errors="ignore"))

#teluguurls = getalllinks()              #["https://en.wikipedia.org/wiki/List_of_Telugu_films_of_1990", "https://en.wikipedia.org/wiki/List_of_Telugu_films_of_2000"]
#telugu_yr_urls = list(set(teluguurls))  # pick only unique values from list
#telugu_yr_urls.sort()                   # sort the Urls in the list

#for url in telugu_yr_urls:
#    data = getMoviesData(url)
    #file.write(bytes(data, encoding="UTF-8", errors="ignore"))

#file.close()