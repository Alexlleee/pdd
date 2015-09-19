# -*- coding: utf-8 -*-
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

class MainNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    class Meta:
        # Allowed actions for namespace (READ, CREATE, DELETE, etc.)
        allowed_methods = None
        # url path
        path = None

    def initialize(self):
        self.allowed_methods = self.Meta.allowed_methods

    def is_method_allowed(self, action):
        if self.Meta.allowed_methods is None:
            return True
        else:
            return action in self.Meta.allowed_methods
