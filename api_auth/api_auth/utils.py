"""Assorted general utilities."""
from flask import jsonify


class JSONError(Exception):
    """Represent errors that have a payload that should be a jsonified response."""

    def __init__(self, payload):
        """Create a new ValidationError with the payload to jsonify."""
        super().__init__()
        self.payload = payload

    def get_response(self):
        """Get the jsonified response of the payload."""
        return jsonify(self.payload)
