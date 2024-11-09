:tocdepth: 2
API
===

This part of the documentation lists the full API reference of all classes and functions.

WSGI
----

.. autoclass:: whitesmith.wsgi.ApplicationLoader
   :members:
   :show-inheritance:

Config
------

.. automodule:: whitesmith.config

.. autoclass:: whitesmith.config.application.Application
   :members:
   :show-inheritance:

.. autoclass:: whitesmith.config.redis.Redis
   :members:
   :show-inheritance:

.. automodule:: whitesmith.config.gunicorn

CLI
---

.. automodule:: whitesmith.cli

.. autofunction:: whitesmith.cli.cli.cli

.. autofunction:: whitesmith.cli.utils.validate_directory

.. autofunction:: whitesmith.cli.serve.serve

App
---

.. automodule:: whitesmith.app

.. autofunction:: whitesmith.app.asgi.on_startup

.. autofunction:: whitesmith.app.asgi.on_shutdown

.. autofunction:: whitesmith.app.asgi.get_application

.. automodule:: whitesmith.app.router

Controllers
~~~~~~~~~~~

.. automodule:: whitesmith.app.controllers

.. autofunction:: whitesmith.app.controllers.ready.readiness_check

Models
~~~~~~

.. automodule:: whitesmith.app.models

Views
~~~~~

.. automodule:: whitesmith.app.views

.. autoclass:: whitesmith.app.views.error.ErrorModel
   :members:
   :show-inheritance:

.. autoclass:: whitesmith.app.views.error.ErrorResponse
   :members:
   :show-inheritance:

Exceptions
~~~~~~~~~~

.. automodule:: whitesmith.app.exceptions

.. autoclass:: whitesmith.app.exceptions.http.HTTPException
   :members:
   :show-inheritance:

.. autofunction:: whitesmith.app.exceptions.http.http_exception_handler

Utils
~~~~~

.. automodule:: whitesmith.app.utils

.. autoclass:: whitesmith.app.utils.aiohttp_client.AiohttpClient
   :members:
   :show-inheritance:

.. autoclass:: whitesmith.app.utils.redis.RedisClient
   :members:
   :show-inheritance:
