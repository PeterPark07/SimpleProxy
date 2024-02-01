from flask import Flask, request, Response, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)

user_site = ""

def pretty_format_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.prettify()

@app.route('/set/<path:site>')
def set_site(site):
    global user_site
    user_site = site
    return f"User site set to: {user_site}"

@app.route('/<path:url>')
def proxy(url):
    global user_site
    full_url = user_site + '/' + url
    try:
        response = urlopen(full_url)
        content_type = response.getheader('Content-Type')
        html_content = response.read()

        return Response(html_content, content_type=content_type)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
