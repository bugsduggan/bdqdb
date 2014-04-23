#!/usr/bin/env python

from bdqdb import app


app.run(host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'])
