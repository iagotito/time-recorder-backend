from urllib.parse import urlparse

from . rest import app

url = urlparse('http://0.0.0.0:8001')
host, port = url.hostname, url.port
app.run(host=host, port=port, debug=True)
