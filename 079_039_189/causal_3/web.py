
import os
import multiprocessing

import tornado.ioloop
import tornado.web
import tornado.httpserver

import answer_engine
from answer_engine import AnswerEngine


# How many response worker threads to use
NUMBER_OF_PROCESSES = max(1, multiprocessing.cpu_count() - 1)


class MainHandler(tornado.web.RequestHandler):
    

    def get(self):
        self.render("index.html")


class QueryHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.pool = self.application.settings.get('pool')
        self.index = self.application.settings.get('index')

    def prepare(self):
        self.query = None
        self.ans_eng = None

    @tornado.web.asynchronous
    def get(self):
        
        self.query = self.get_argument('q')
        num_top = int(self.get_argument('top', default=5))
        self.num = int(self.get_argument('num', default=100))
        start = int(self.get_argument('start', default=0))
        lch = float(self.get_argument('lch', default=2.16))
        self.log_training = bool(self.get_argument('train', default=False))
        self.ans_eng = AnswerEngine(self.index, self.query, start, num_top, lch)
        self.pool.apply_async(answer_engine.get_answers, (self.ans_eng,),
                              callback=self.callback)

    def callback(self, args):
        answers, ir_query_tagged = args
        # Display result
        self.render("answer.html",
                    query=self.query,
                    ir_query=' '.join(self.ans_eng.ir_query),
                    ir_query_tagged=ir_query_tagged,
                    num_pages=self.ans_eng.num_pages,
                    num_answers=len(answers),
                    answers=answers[:self.num])
        # Log answer details
        if self.log_training:
            with open('log_training.txt'.format(self.num), mode='a') as f:
                f.write('\t'.join([' '.join(self.ans_eng.ir_query),
                                   self.query]) + '\t0')
                for rank, answer in enumerate(answers, start=1):
                    f.write('\t' + '\t'.join([str(rank)] + [str(x) for x in
                                                            answer._features]))
                f.write('\n')


def main(index, port=8080):
    pool = multiprocessing.Pool(NUMBER_OF_PROCESSES)
    # Give each pool initial piece of work so that they initialize.
    ans_eng = AnswerEngine(index, 'bird sing', 0, 1, 2.16)
    for x in xrange(NUMBER_OF_PROCESSES * 2):
        pool.apply_async(answer_engine.get_answers, (ans_eng,))
    del ans_eng
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/cause/", QueryHandler),
        ], template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        index=index,
        pool=pool)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
