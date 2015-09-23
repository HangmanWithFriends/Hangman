'''
This is the main file to run from the command line 
to start up the CherryPy webserver. This will also 
house the dispatcher to handle HTTP(S) requests.
'''

import cherrypy
import os
from page_handler import Page_Handler


def start_service():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    conf = {'global': 
                {
                    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                    'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
                }, 
            
            '/' : 
                {
                    'request.dispatch' : dispatcher, 
                },
            '/css': 
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': 'css'
                },
            '/js':
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': 'js'
                },
            '/img':
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': 'img'
                }
    }
    
    
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    
    page_handler = Page_Handler()
    
    dispatcher.connect('get_login_page','/login',controller=page_handler, action='get_login_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_lobby_page','/lobby',controller=page_handler, action='get_lobby_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_request_phrase_page','/phrase',controller=page_handler, action='get_request_phrase_html',conditions=dict(method=['GET']))
    dispatcher.connect('handle_login','/login',controller=page_handler, action='handle_login_request',conditions=dict(method=['POST']))
    
    cherrypy.quickstart(app)
    
if __name__ == '__main__':
    start_service()
