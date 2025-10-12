from flask import jsonify, make_response

class ResponseHandler:
    """
    Provides standardized HTTP responses for the API.
    Includes methods for success, creation, and error responses.
    """

    @staticmethod
    def success(data=None, message="Operation completed successfully", status_code=200):
        """
        Returns a standard success response.

        Args:
            data (dict, optional): Optional data payload to include in the response.
            message (str): Informational message for the client.
            status_code (int): HTTP status code (default 200).

        Returns:
            Flask Response: JSON response with success status and optional data.
        """
        body = {
            "success": True,
            "message": message
        }
        if data is not None:
            body["data"] = data
        return make_response(jsonify(body), status_code)

    @staticmethod
    def created(data=None, message="Resource created successfully"):
        """
        Returns a standard response for resource creation.

        Args:
            data (dict, optional): Optional data payload to include in the response.
            message (str): Informational message for the client.

        Returns:
            Flask Response: JSON response with success status and HTTP 201.
        """
        return ResponseHandler.success(data=data, message=message, status_code=201)

    @staticmethod
    def error(message="Internal server error", status_code=400, error_code=None, details=None):
        """
        Returns a standard error response.

        Args:
            message (str): Error message describing the problem.
            status_code (int): HTTP status code (default 400).
            error_code (str, optional): Optional internal error code.
            details (str, optional): Optional additional details for debugging.

        Returns:
            Flask Response: JSON response with error information.
        """
        body = {
            "success": False,
            "message": message
        }
        if error_code:
            body["error_code"] = error_code
        if details:
            body["details"] = details
        return make_response(jsonify(body), status_code)
