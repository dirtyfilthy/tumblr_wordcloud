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
        if not "api_key" in next_url:
            next_url += f"&api_key={config.APIKEY}"
        r=requests.get(next_url)
        print(next_url)
        if r.status_code != 200:
            print("status code")
            print(r.status_code)
            break;
        json = r.json()
        links = json['response'].get('_links')
        next_maybe = None
        if links:
            next_maybe = links.get('next')
        if next_maybe and next_maybe.get('href'):
            next_maybe = "https://api.tumblr.com" + next_maybe['href']

        next_url = next_maybe
        
        #pp.pprint(json)
        these_posts = map(lambda p: p.get('body'), json['response']['posts'])
        posts.extend(these_posts)
        if len(posts) >= config.MAX_POSTS:
            break
    
    return posts


def clean_post(post):
    if post is None:
        return ""
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
    print(r"number of posts {}".format(len(posts)))
    return list(map(lambda p: clean_post(p), posts))

def get_text(blog, tag=None):
   return " ".join(clean_posts(get_posts(blog, tag))).strip()





