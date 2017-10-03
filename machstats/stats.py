import json
import traceback
import pymysql
import tornado.ioloop
import tornado.web
import tornado.websocket
import config

PEEPS = []

HIST = {}
HIST['data'] = None
DELAY = 1000


def get_data():
    """Connect to database and return either null or results in json."""
    try:
        connection = pymysql.connect(**config.pymysql_settings)
        cursor = connection.cursor()
        sql = ('YOUR QUERY HERE!') # PUT YOUR QUERY IN HERE 
        row = cursor.execute(sql)
        if row == 0:
            return '"null"'
        else:
            return json.dumps(cursor.fetchall())
    except Exception:
        traceback.print_exc()
        return '"null"'


class HomeHandler(tornado.web.RequestHandler):
    """Handle the request for index.html."""

    def get(self):
        """Render index.html template and load variable for home button into template."""
        self.render('index.html', home=config.pymysql_settings['host'])


class Thingy(tornado.websocket.WebSocketHandler):
    """Thingy class Handles websocket connections."""

    first = []
    waz = 0

    def check_origin(self, origin):
        """Check origin of request to prevent 'man in the middle' attacks."""
        return True

    def open(self):
        """On new opened connection add to peeps list and trigger callback."""
        if self not in PEEPS:
            PEEPS.append(self)
            if len(PEEPS) > 1 or len(PEEPS) == 0:
                print("{0} added to client list. Serving {1} people".format(
                    self, len(PEEPS)))
            else:
                print("{0} added to client list. Serving {1} person".format(
                    self, len(PEEPS)))
            self.callback = tornado.ioloop.PeriodicCallback(self.sock_send,
                                                            1000)
            self.callback.start()

    def on_message(self, message):
        """Pass, no message needed from client."""
        pass

    def on_close(self):
        """On closed connection remove from peeps list and stop callback."""
        if self in PEEPS:
            PEEPS.remove(self)
            self.first.remove(self)
            if len(PEEPS) > 1 or len(PEEPS) == 0:
                print("{0} removed from client list. Serving {1} people"
                      .format(self, len(PEEPS)))
            else:
                print("{0} removed from client list. Serving {1} person"
                      .format(self, len(PEEPS)))
            self.callback.stop()

    def sock_send(self):
        """Get data and send to PEEPS.

        If clients haven't been served yet they are messaged regardless of
        message data history changing. Also checks for closed sockets and acts
        accordingly.
        """
        message = get_data()
        for peep in PEEPS:
            if peep not in self.first:
                print("not yet served, sending {0}".format(message))
                self.first.append(peep)
                peep.write_message(message)
        if message == HIST['data']:
            pass
        else:
            print("changed 'message : {0}' and 'hist: {1}'".format(
                message, HIST['data']))
            if HIST['data'] is None:
                self.waz = 1
            HIST['data'] = message
            for peep in PEEPS:
                if not peep.ws_connection.stream.socket:
                    print("Socket closed!")
                    PEEPS.remove(peep)
                    self.first.remove(peep)
                else:
                    if self.waz == 1:
                        print("not sending")
                        self.waz = 0
                    else:
                        if peep not in self.first:
                            self.first.append(peep)
                        peep.write_message(message)
                        print("Sending {0}".format(message))


def main():
    """Set up handlers and application and start event loop."""
    handlers = [(r"/", HomeHandler),
                (r"/mach_sock", Thingy)]

    app = tornado.web.Application(handlers, **config.tornado_settings)

    app.listen(8080)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
