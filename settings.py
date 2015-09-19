# -*- coding: utf-8 -*-
from pddtest.namespase import PddTestNamespace
SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 12000

NANESPACE_LIST = {
    PddTestNamespace,
}

NAMESPACES = {
    namespace.Meta.path: namespace for namespace in NANESPACE_LIST
}
