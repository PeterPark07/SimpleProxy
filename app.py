from flask import Flask, request, Response
from urllib.request import urlopen
from bs4 import BeautifulSoup  # Assuming you have BeautifulSoup installed

app = Flask(__name__)

def modify_links(base_url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    modified_urls = []

    for a_tag in soup.find_all('a', href=True):
        old_url = a_tag['href']
        new_url = f'{base_url}/{old_url}'
        a_tag['href'] = new_url
        modified_urls.append((old_url, new_url))

    updated_html = str(soup)
    return updated_html, modified_urls

@app.route('/<path:url>')
def proxy(url):
    try:
        response = urlopen(url)
        content_type = response.getheader('Content-Type')
        html_content = response.read()

        updated_html, modified_urls = modify_links(url, html_content)

        # Print out the modified URLs
        for old_url, new_url in modified_urls:
            print(f'Modified URL: {old_url} -> {new_url}')

        return Response(updated_html, content_type=content_type)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
