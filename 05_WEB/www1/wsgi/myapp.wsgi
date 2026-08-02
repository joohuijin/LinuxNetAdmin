context = 'WSGI Test Page'

def html():
    return f'''
    <html>
      <body>
        <center><h1>{context}</h1></center>
      </body>
    </html>
    '''.encode("utf-8")

def application(environ, start_response):
    output = html()

    status = '200 OK'
    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
