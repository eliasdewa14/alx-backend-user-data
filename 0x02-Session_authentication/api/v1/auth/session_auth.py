#!/usr/bin/env python3
"""Define a class SessionAuth that inherits from Auth"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Represents a session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """a method to creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id