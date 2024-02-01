from flask import Flask, request, Response, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)

def pretty_format_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.prettify()

@app.route('/source/<path:url>')
def source(url):
    try:
        response = urlopen(url)
        content_type = response.getheader('Content-Type')
        html_content = response.read()

        # Pretty format the HTML source
        pretty_html = pretty_format_html(html_content)
        formatted_html = f'<pre>{pretty_html}</pre>'

        return Response(formatted_html, content_type='text/plain')
    except Exception as e:
        return str(e)


@app.route('/<path:url>')
def proxy(url):
    try:
        response = urlopen(url)
        content_type = response.getheader('Content-Type')
        html_content = response.read()

        return Response(html_content, content_type=content_type)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
