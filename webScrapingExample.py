# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 22:45:12 2019

@author: campb

Example in Data Science from Scratch page 110
"""

from bs4 import BeautifulSoup
from time import sleep
from collections import Counter
import matplotlib.pyplot as plot
import requests
import re
url = "https://ssearch.oreilly.com/?i=1;m_Sort=searchDate;q=data;q1=Books;x1=t1;page="
soup = BeautifulSoup(requests.get(url).text, 'html5lib')

xNUM_PAGES = 104
books = []

# print len(articles) # to count number of book results
articles = soup('article', 'product-result')

""" 
START FUNCTIONS 

functions below return lists for areas of interest across whole scrape 
""" 

def find_title(articles):
    title_list = []
    for title in articles:
        titleText = title.find_all("p", {"class":"title"})
    
        for data in titleText:
            title = data.a.text.strip()
            title_list.append([title])
    
    return title_list
    
def find_author(articles):
    output = []
    for author in articles:
        authorName = author.find("p", {"class":"note"}).text
        # replaces all instances of "By " at the start of the author string
        # with ... nothing
        output.append([text.strip() for text in re.sub("^By ", "", authorName).split(",")])
        
    return output

def find_ISBN(articles):
    isbn = []
    """
    O'Reilly ISBN is in the URL
    """
    for article in articles:
        findISBN_loc = article.find("img", {"class":"book"})
        string = findISBN_loc['src']
        # re.match captures the regex within the () characters
        # in this use, it is .* which asks for all text in this section
        # group 1 requests the 1st () regex match, of which there is only 1
        isbn_true = re.match("//akamaicovers.oreilly.com/images/(.*)\/cat.gif", string).group(1)
        isbn.append(isbn_true)
        
    return isbn

def find_pubDate(articles):
    date = []
    
    for article in articles:
        find_date = [article.find("p",{"class": ["date2"]}).text.strip()]
        for item in find_date:
            # raw string 'word class and all letters, space, digit (x4)' 
            stripDate = re.search(r'[\w]+\s\d\d\d\d', item)
            #.group() converts match object to match text
            date.append(stripDate.group()) 
 
    return date        

""" 

END FUNCTIONS

"""

"""
this below statement is a way to tie in 2 lists
unit is list-ified so that say combinedList[n][1] will be the title
and that combinedList[n][2] will be the author(s)

Found also a way to iterate over the list if more than 1:
    print([<name1>[i] + [<name2>[i]] for i in range(len(<primaryList>))])
"""
# combinedList = [[unit[0]] + [unit[1]] for unit in zip(titles, authors)]
# combinedList = [titles[i] + [authors[i]] + [isbn[i] + pubDate[i]] for i in range(len(titles))]
# print(combinedList)


def book_info(article):
    """
    calls functions to find given info from a web result search page for books.
    This function returns books as a dict to be used for individual results
    """
    
    title = article.find("p", {"class":"title"}).a.text.strip()
    authorName = article.find("p", {"class":"note"}).text
    authors = [text.strip() for text in re.sub("^By ", "", authorName).split(",")]
    findISBN_loc = article.find("img", {"class":"book"})
    string = findISBN_loc['src']
    ISBN = re.match("//akamaicovers.oreilly.com/images/(.*)\/cat.gif", string).group(1)
    find_date = [article.find("p",{"class": ["date2"]}).text.strip()]
    def dates(find_date):
        return [re.search(r'[\w]+\s\d\d\d\d', item).group() for item in find_date]
    date = dates(find_date)
    
    return {
            "title" : title,
            "authors" : authors,
            "isbn" : ISBN,
            "date" : date
    }

#for article in articles:
    #print(book_info(article))
    
for page_number in range(1, NUM_PAGES + 1):
    print('scraping page', page_number,':', len(books), 'books found prior')
    new_page = url + str(page_number)
    soup = BeautifulSoup(requests.get(new_page).text, 'html5lib')
    
    for item in soup('article', 'product-result'):
        books.append(book_info(item))
    
    # being a good citizen and not hammering the page
    sleep(30)
    
def get_year(book):
    """
    A book date looks like ['Month Year'] so to grab year:
        Split on the space then take 2nd half
    """
    
    return int(book["date"][0].split()[1])

years = []
for _, book in enumerate(books): years.append(get_year(book))

year_counts = Counter(year for year in years
                      if year <= 2019)

# print("Year Counts: {}".format(year_counts))

year_axis = sorted(year_counts)
book_counts = [year_counts[year] for year in year_axis]
plot.plot(year_axis, book_counts)
plot.ylabel("# of 'Data' books")
plot.title("Data books published by Year")
plot.show()