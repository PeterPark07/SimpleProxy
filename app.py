from flask import Flask, request, Response, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
root = os.getenv('url')

def modify_links(base_url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    modified_urls = []

    for a_tag in soup.find_all('a', href=True):
        old_url = a_tag['href']
        
        # Check if the URL is relative and doesn't have http:// or https://
        if not old_url.startswith(('http')):
            new_url = f'{base_url}/{old_url}'
            new_url = new_url.replace('//','/')
            a_tag['href'] = new_url
            modified_urls.append((old_url, new_url))

    updated_html = str(soup)
    return updated_html, modified_urls

def add_root_to_all_links(html_content, root):
    soup = BeautifulSoup(html_content, 'html.parser')

    for a_tag in soup.find_all('a', href=True):
        old_url = a_tag['href']
        new_url = f'{root}/{old_url}'
        new_url = new_url.replace('//','/')
        a_tag['href'] = new_url

    return str(soup)

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

        return Response(pretty_html, content_type='text/html')
    except Exception as e:
        return str(e)

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

        # Add root part to all URLs
        final_html = add_root_to_all_links(updated_html, root)

        return Response(final_html, content_type=content_type)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
