# Read Configuration file for Wiki Dump
# Start Web Server using web.main(...........)

# In Web
import os
import multiprocessing
import tornado.ioloop
import tornado.web
import tornado.httpserver

NUMBER_OF_PROCESSES = max(1, multiprocessing.cpu_count() - 1)


def web_main(index, port=8080):
    pool = multiprocessing.Pool(NUMBER_OF_PROCESSES)
    
    # Give each pool initial piece of work so that they initialize.
    ans_eng = AnswerEngine(index, 'bird sing', 0, 1, 2.16)
    
    for x in xrange(NUMBER_OF_PROCESSES * 2):
        pool.apply_async(answer_engine.get_answers, (ans_eng,))
    del ans_eng
    
    application = tornado.web.Application([(r"/", MainHandler),(r"/cause/", QueryHandler),],
    									 template_path=os.path.join(os.path.dirname(__file__), "templates"),
        								 static_path=os.path.join(os.path.dirname(__file__), "static"),index=index,pool=pool)
        								 
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    
    
web_main()

