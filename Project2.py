from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
#worked with Christina Liggio


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    soup = BeautifulSoup(open('search_results.htm'), 'html.parser')
    books = []
    for book in soup.findAll('tr', itemtype="http://schema.org/Book"):
        items = book.findAll('span', itemprop = 'name')
        title = items[0].string.strip()
        author = items[1].string.strip()
        books.append((title, author))
    return books


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    books = soup.findAll('a', {'class': 'bookTitle'})
    urls = []
    for book in books[0:10]:
        urls.append('https://www.goodreads.com' + book['href'])
    return urls 
        


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1', id = "bookTitle").string.strip()
    author = soup.find('a', {'class': 'authorName'}).string.strip()
    pages = int(soup.find('span', itemprop = "numberOfPages").string.strip(" pages"))
    return (title, author, pages)
    


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    soup = BeautifulSoup(open(filepath), 'html.parser')
    categories = soup.findAll('div', {'class': 'category clearFix'})
    best_books = []
    for category in categories:
        name = category.find('h4', {'class': 'category__copy'}).string.strip()
        title = category.find('img', {'class': 'category__winnerImage'})['alt'].strip()
        url = category.find('a')['href'].strip()
        best_books.append((name, title, url))
    return best_books



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w') as file:
        file.write('Book title,Author Name\n')
        for line in data:
            file.write(','.join(line) + '\n')


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    soup = BeautifulSoup(open(filepath), 'html.parser')
    description = soup.find('div', id = 'description')
    description = description.findAll('span')[-1].text
    entities = re.findall(r'([A-Z][a-z]{2,})(( [A-Z][a-z]{2,})+)', description)
    entities = [''.join(words[0:-1]) for words in entities]
    return entities
    

class TestCases(unittest.TestCase):
    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        get_titles = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(get_titles), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(get_titles), list)

        # check that each item in the list is a tuple
        for item in get_titles:
            self.assertEqual(type(item), tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        first_tuple = get_titles[0]
        self.assertEqual(first_tuple[0], "Harry Potter and the Deathly Hallows (Harry Potter, #7)")
        self.assertEqual(first_tuple[1], "J.K. Rowling")

        # check that the last title is correct (open search_results.htm and find it)
        last_tuple = get_titles[-1]
        self.assertEqual(last_tuple[0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        self.assertEqual(last_tuple[1], "J.K. Rowling")
        

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for item in TestCases.search_urls:
            self.assertEqual(type(item), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.search_urls:
            self.assertEqual('https://www.goodreads.com/book/show/' in url, True)
 

    def test_get_book_summary(self):

        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in TestCases.search_urls:
            summary = get_book_summary(url)
            self.assertEqual(type(url), tuple)
            summaries.append(summary)

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

        # check that each item in the list is a tuple
        for items in summaries:
            self.assertEqual(type(items), tuple)

        # check that each tuple has 3 elements
        self.assertEqual(len(items), 3)

        # check that the first two elements in the tuple are string
        self.assertEqual(type(items[0]), str)
        self.assertEqual(type(items[1]), str)

        # check that the third element in the tuple, i.e. pages is an int
        self.assertEqual(type(items[2]), int)

        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books = summarize_best_books('best_books_2020.htm')

        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books), 20)

            # assert each item in the list of best books is a tuple
        for item in best_books:
            self.assertEqual(type(item), tuple)

            # check that each tuple has a length of 3
            self.assertEqual(len(item), 3)


        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0], ('Fiction', "The Midnight Library", "https://www.goodreads.com/choiceawards/best-fiction-books-2020"))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        result = get_titles_from_search_results('search_results.htm')

        # call write csv on the variable you saved and 'test.csv'
        write_csv(result, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv') as file:
            csv_lines = file.readlines()

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0].strip(), "Book title,Author Name")

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1].strip(), 'Harry Potter and the Deathly Hallows (Harry Potter, #7),J.K. Rowling')

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1].strip(), 'Harry Potter: The Prequel (Harry Potter, #0.5),J.K. Rowling')

    def test_extra_credit(self):
        entities = extra_credit('extra_credit.htm')
        print(entities)
        self.assertEqual(type(entities), list)
        self.assertEqual(len(entities), 9)


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



