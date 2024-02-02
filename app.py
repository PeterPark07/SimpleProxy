from flask import Flask, request, Response, render_template
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

app = Flask(__name__)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def modify_links(base_url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(['a', 'img'], href=True):
        old_url = tag['href']

        if '//' not in old_url:
            new_url = f'{base_url}/{old_url.lstrip("/")}'
            tag['href'] = new_url

    return str(soup)


@app.route('/source/<path:url>')
def source(url):
    try:
        request = Request(url, headers=headers)
        response = urlopen(request)
        content_type = response.getheader('Content-Type')
        html_content = response.read()

        # Pretty format the HTML source
        pretty_html = BeautifulSoup(html_content, 'html.parser').prettify()
        formatted_html = f'<pre>{pretty_html}</pre>'

        return Response(formatted_html, content_type='text/plain')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
