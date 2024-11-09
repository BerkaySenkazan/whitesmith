"""Question generation and evaluation"""
import logging

from whitesmith.wsgi import ApplicationLoader
from whitesmith.version import __version__

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

__all__ = ("ApplicationLoader", "__version__")
