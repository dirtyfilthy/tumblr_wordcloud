import requests
import pprint
import html
import string
import re
import config
from htmllaundry import strip_markup



pp = pprint.PrettyPrinter(indent=4)


def get_posts(blog, tag=None):

    if tag == "":
        tag = None

    url = f"https://api.tumblr.com/v2/blog/{blog}/posts?api_key={config.APIKEY}"

    if tag:
        url = url + f"&tag={tag}"

    posts = []

    next_url = url

    while(next_url):

        r=requests.get(next_url)
        if r.status_code != 200:
            break;
        json = r.json()
        next_maybe = json['response']['_links'].get('next')
        if next_maybe and next_maybe.get('href'):
            next_maybe = "https://api.tumblr.com" + next_maybe['href']

        next_url = next_maybe
        these_posts = map(lambda p: p['body'], json['response']['posts'])
        posts.extend(these_posts)
        if len(posts) >= config.MAX_POSTS:
            break
    
    return posts


def clean_post(post):
    post = html.unescape(post)
    post = post.replace("-", " ")
    post = post.replace("<p>", "\n")
    post = post.replace('<br>', "\n")
    post = post.replace('<br/>', "\n")
    post = post.replace('<br />', "\n")
    post = post.lower()
    post = strip_markup(post)
    post = post.translate(str.maketrans('', '', string.punctuation))
    post = re.sub(r'[^a-zA-Z0-9 \n]', '', post)

    return post


def clean_posts(posts):
    return list(map(lambda p: clean_post(p), posts))

def get_text(blog, tag=None):
   return " ".join(clean_posts(get_posts(blog, tag))).strip()





