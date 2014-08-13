#!/usr/bin/env python2
from flask.ext.script import Manager

from neobug import neobug

manager = Manager(neobug)
if __name__ == '__main__':
    manager.run()
