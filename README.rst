RestDoc.py
==========

Provides a ``restdoc`` package that will contain both client and server
implementations, though for now it's only client oriented.

Installing
----------

For end-user use::

  git clone https://github.com/RestDoc/restdoc.py
  pip install restdoc.py

For development::

  git clone https://github.com/RestDoc/restdoc.py
  cd restdoc.py
  python setup.py develop

If you aren't already, consider using virtualenv to isolate projects.

Interactive Shell
-----------------

To fire up the interactive shell use the ``rdc`` command. All of the commands
are documented in the shell itself, but here is a quick example::

  => rdc
  Welcome to the RestDoc shell!
  Use the 'server' command to specify a server, or 'help' to see all commands.
  (localhost:5000) help

  Documented commands (type help <topic>):
  ========================================
  delete  get   options  post  reload   resources
  doc     head  patch    put   request  server   

  Undocumented commands:
  ======================
  help

  (localhost:5000) reload
  (localhost:5000) resources
  +-----+-------+-----------------+-------------+
  |  id |  path |     methods     | description |
  +-----+-------+-----------------+-------------+
  | App | /:app | ['POST', 'GET'] |     None    |
  +-----+-------+-----------------+-------------+
  (localhost:5000) doc App
  {'id': 'App',
   'methods': {'GET': {'description': 'Gets the app'},
               'POST': {'description': 'Updates the app'}},
   'params': {'app': {'description': 'the app entry id', 'required': True}},
   'path': '/:app'}
  (localhost:5000) get App -t app=foobar
  200 OK
  transfer-encoding: chunked
  connection: keep-alive
  x-powered-by: Express


  (localhost:5000) 
