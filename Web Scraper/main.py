from bs4 import BeautifulSoup
import requests
import inquirer
from random import randint

url = "https://quotes.toscrape.com/"
html_text = requests.get(url).text

# Get top ten tags from site homepage
def get_tags(text):
    soup = BeautifulSoup(text, 'lxml')
    tag_box = soup.find('div', class_ = 'col-md-4 tags-box')
    tags = []
    for tag in tag_box.find_all('a', class_ = 'tag'):
        tags.append(tag.text)

    return tags

# Create multiple choice select from tags
def get_options(tags):
    options = [
        inquirer.List('tags', message= "What type of quote would you like?", choices=tags)
    ]

    return options

# Get random quote from selected category page 
def get_quote(category):
    tag_url = 'https://quotes.toscrape.com/tag/' + category
    tag_html_text = requests.get(tag_url).text
    soup = BeautifulSoup(tag_html_text, 'lxml')
    quotes = soup.find_all('div', class_ = 'quote')
    rand_int = randint(0, len(quotes) - 1)
    quote = quotes[rand_int]
    quote_text = quote.find('span', class_ = 'text').text
    quote_author = quote.find('small', class_ = 'author').text

    return quote_text + '\n' + quote_author


select = inquirer.prompt(get_options(get_tags(html_text)))

famous_quote = get_quote(select.get('tags'))

print(famous_quote)