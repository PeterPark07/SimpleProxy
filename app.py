from flask import Flask, request, Response
import socketserver
import http.server
import urllib.request

app = Flask(__name__)

@app.route('/')
def proxy():
    url = request.args.get('url', '')
    try:
        with urllib.request.urlopen(url) as response:
            content_type = response.headers.get('Content-Type', 'text/plain')
            return Response(response.read(), content_type=content_type)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
