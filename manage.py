#!/usr/bin/env python3
from flask.ext.script import Manager, Server

from neobug import neobug

manager = Manager(neobug)
manager.add_command("debug", Server(use_debugger=True, use_reloader=True))
if __name__ == '__main__':
    manager.run()
