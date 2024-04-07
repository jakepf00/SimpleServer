import http.server
import os
import Cases

class RequestHandler(http.server.BaseHTTPRequestHandler):
    Cases = [Cases.case_no_file(),
             Cases.case_cgi_file(),
             Cases.case_existing_file(),
             Cases.case_directory_index_file(),
             Cases.case_directory_no_index_file(),
             Cases.case_always_fail()]

    Error_Page = '''\
<html>
<body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
</body>
</html>
'''

    # Classify and handle request
    def do_GET(self):
        try:
            # Figure out what exactly is being requested
            self.full_path = os.getcwd() + self.path

            # Figure out how to handle it
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break
            
        # Handle errors
        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path = self.path, msg = msg).encode("utf-8")
        self.send_content(content, 404)
    
    def send_content(self, content, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

#-----------------------------------------------------------
if __name__ == '__main__':
    serverAddress = ('', 8080) # '' = localhost
    server = http.server.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()