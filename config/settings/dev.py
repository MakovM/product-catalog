import socket

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = ["127.0.0.1"] + [ip[: ip.rfind(".")] + ".1" for ip in ips]
