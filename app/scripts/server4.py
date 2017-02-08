from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
from urllib.parse import urlparse, parse_qs
# from PlanInterface import PlanInterface
from GenericPlanner import GenericPlannerInterface
from Problem import Problem 

#global planning interface to access optic
problem1 = GenericPlannerInterface("pfile3_satellite.txt")

class PlanningServer(BaseHTTPRequestHandler):

    def _set_headers(self, success):
        if success:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        else: 
            self.send_response(404)
            self.end_headers()

    def _parse_route(self):
        request = urlparse(self.path)
        route = request.path.split('/')[1]

        return route 

    def do_GET(self):
        print("i got here")
        route = self._parse_route()
        params = self.path.split("?")[1]
        #get the param from the url
        thisProblem = GenericPlannerInterface(params)

        if route == "problem_numerics": #get the current plan
            self._set_headers(True)
            #load the plan from a file
            #write the text to be returned as part of the request
            self.wfile.write(bytes(thisProblem.numericsToString(), "utf8")) 

        elif route == "problem_objects": #get the original problem file
            self._set_headers(True)
            #get the problem file
            #write the problem file
            self.wfile.write(bytes(thisProblem.objectsToString(), "utf8"))
        elif route == "problem_initStates":
            self._set_headers(True)

            self.wfile.write(bytes(thisProblem.initStatesToString(), "utf8"))

        elif route == "problem_goalStates":
            self._set_headers(True)

            self.wfile.write(bytes(thisProblem.goalStatesToString(), "utf8"))


        else:  #invalid path
            self._set_headers(False)

    def do_POST(self):
        route = self._parse_route()

        if route == "subgoals":
            #load the subgoals
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            subgoals = json.loads(self.data_string.decode())
            #trim the subgoals
            planner.simplifyGoals(subgoals)
            #call planner
            planner.plan()
            self._set_headers(True)
        else:
            #invalid path
            self._set_headers(False)


def run(server_class=HTTPServer, handler_class=PlanningServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()