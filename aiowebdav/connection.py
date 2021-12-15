import ssl
from os.path import exists

import aiohttp

from aiowebdav.exceptions import *
from aiowebdav.urn import Urn


class ConnectionSettings:
    def is_valid(self):
        """
        Method checks is settings are valid
        :return: True if settings are valid otherwise False
        """
        pass

    def valid(self):
        try:
            self.is_valid()
        except OptionNotValid:
            return False
        else:
            return True


class WebDAVSettings(ConnectionSettings):
    ns = "webdav:"
    prefix = "webdav_"
    keys = {'hostname', 'login', 'password', 'token', 'root', 'ssl', 'recv_speed', 'send_speed',
            'verbose', 'disable_check', 'override_methods', 'timeout', 'chunk_size', 'proxy', 'proxy_auth'}

    def __init__(self, options: dict):
        self.hostname = None
        self.login = None
        self.password = None
        self.token = None
        self.root = None
        self.ssl = None  # type: ssl.SSLContext
        self.recv_speed = None
        self.send_speed = None
        self.verbose = None
        self.disable_check = False
        self.override_methods = {}
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.chunk_size = 65536
        self.proxy = None
        self.proxy_auth = None

        self.options = {}

        for key in self.keys:
            value = options.get(key, '')
            if not (self.__dict__[key] and not value):
                self.options[key] = value
                self.__dict__[key] = value

        self.root = Urn(self.root).quote() if self.root else ''
        self.root = self.root.rstrip(Urn.separate)
        self.hostname = self.hostname.rstrip(Urn.separate)
        self.ssl = None if not self.ssl else self.ssl
        if isinstance(self.timeout, (int, float)):
            self.timeout = aiohttp.ClientTimeout(self.timeout)

    def is_valid(self):
        if not self.hostname:
            raise OptionNotValid(name="hostname", value=self.hostname, ns=self.ns)

        if self.cert_path and not exists(self.cert_path):
            raise OptionNotValid(name="cert_path", value=self.cert_path, ns=self.ns)

        if self.key_path and not exists(self.key_path):
            raise OptionNotValid(name="key_path", value=self.key_path, ns=self.ns)

        if self.key_path and not self.cert_path:
            raise OptionNotValid(name="cert_path", value=self.cert_path, ns=self.ns)

        if self.password and not self.login:
            raise OptionNotValid(name="login", value=self.login, ns=self.ns)
        return True
