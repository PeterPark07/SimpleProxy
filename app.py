from flask import Flask, request, Response
from urllib.request import urlopen
from bs4 import BeautifulSoup  # Assuming you have BeautifulSoup installed

app = Flask(__name__)

@app.route('/<path:url>')
def proxy(url):
    try:
        response = urlopen(url)
        content_type = response.getheader('Content-Type')
        html_content = response.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Update links in the HTML content to include the full external URL
        for a_tag in soup.find_all('a', href=True):
            a_tag['href'] = f'{url}/{a_tag["href"]}'

        # Update the HTML content
        updated_html = str(soup)

        return Response(updated_html, content_type=content_type)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
