# coding=utf8
from flask import Flask, request, escape, render_template, flash
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from time import sleep

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__, template_folder='template')
app.secret_key ="kspilchfi"
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/result', methods=["POST", "GET"])
def book():
    book_name = str(request.form["book_name_input"])

    i = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    # to search
    query = "download" + book_name + " book pdf"

    sites = []
    data = []
    for j in search(query, num=15, stop=15, pause=2):
        sites.append(j)

    for site in sites:
        x = urlparse(site)

        if x.path[-4:] == ".pdf":
            print("found")
            drive_ur = x.geturl()
            data.append(drive_ur)
        else:
            None

    links_list = []
    for site in sites:
        url = site

        try:
            read = requests.get(url, timeout=5)

        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
        except requests.exceptions.ConnectionError as e:
            raise SystemExit(e)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        html_content = read.content
        soup = BeautifulSoup(html_content, "html.parser", from_encoding="iso-8859-1")

        site_content = soup.find_all('a')
        links_list.clear()

        for link in site_content:
            # original html links
            links_list.append(link.get('href'))

        for pdf_link in links_list:
            u = urlparse(pdf_link)

            if u.netloc[0:17] == "drive.google.com":
                in_site = u.geturl()
                data.append(in_site)
            else:
                None
            if u.path[-4:] == ".pdf":
                in_site_url = u.geturl()
                data.append(in_site_url)
            else:
                None
               

    return render_template("result.html", data = data)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
