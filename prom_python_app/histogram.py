import http.server
import random
import time
from prometheus_client import start_http_server, Histogram

#for seeing the request latency
REQUEST_RESPOND_TIME = Histogram('app_response_latency_seconds','Response latency in seconds', buckets=[0.1,0.5,1,2,3,4,5,10])
#we have a service level agreement(SLA) to serve 90% of the requests with max 200ms latency, so for this SLA how will you if your 90%
#quantile is 200ms, in that case we can have a histogram with a bucket of upper limit 0.2 seconds, the we can directly express the relative amount of requests
#served within 200ms and afterwards we can generate a alert if the value falls below 0.90

#How many buckets should we add, when doing manually?
#ans -> more number of buckets means more acuracy, but each bucket come with an extra timeseries to be stored, so it depends on the use case how many buckets we should consider.


APP_PORT = 8000
METRICS_PORT = 8001

class HandleRequests(http.server.BaseHTTPRequestHandler):
    
    @REQUEST_RESPOND_TIME.time()
    def do_GET(self):
        #start_time = time.time()
        time.sleep(1)
        self.send_response(200) 
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>First Application</title></head><body style='color: #333; margin-top: 30px;'><center><h2>Welcome to our first Prometheus-Python application.</center></h2></body></html>", "utf-8"))
        self.wfile.close()
        #time_taken = time.time() - start_time
        #REQUEST_RESPOND_TIME.observe(time_taken)

if __name__ == "__main__":
    start_http_server(METRICS_PORT)
    server = http.server.HTTPServer(('localhost', APP_PORT), HandleRequests)
    server.serve_forever()