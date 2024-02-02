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
    modified_urls = []

    for a_tag in soup.find_all('a', href=True):
        old_url = a_tag['href']
        
        # Check if the URL is relative and doesn't have http:// or https://
        if not old_url.startswith(('http')):
            if old_url.startswith(('/')):
                new_url = f'{base_url}{old_url}'
            else:
                new_url = f'{base_url}/{old_url}'
            a_tag['href'] = new_url
            modified_urls.append((old_url, new_url))

    updated_html = str(soup)
    return updated_html, modified_urls

@app.route('/<path:url>')
def proxy(url):
    try:
        request = Request(url, headers=headers)
        response = urlopen(request)
        content_type = response.getheader('Content-Type')
        html_content = response.read()

        updated_html, modified_urls = modify_links(url, html_content)

        return Response(updated_html, content_type=content_type)
    except Exception as e:
        return str(e)






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
