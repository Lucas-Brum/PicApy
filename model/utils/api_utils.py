from flask import jsonify, make_response, Response
from typing import Any, Optional


class ResponseHandler:
    """
    Provides standardized HTTP responses for the API.
    Includes methods for success, creation, and error responses.
    """

    @staticmethod
    def success(
        data: Optional[Any] = None,
        message: str = "Operation completed successfully",
        status_code: int = 200,
    ) -> Response:
        """
        Returns a standard success response.

        Args:
            data (dict, optional): Optional data payload to include in the response.
            message (str): Informational message for the client.
            status_code (int): HTTP status code (default 200).

        Returns:
            Flask Response: JSON response with success status and optional data.
        """
        body = {"success": True, "message": message}
        if data is not None:
            body["data"] = data
        return make_response(jsonify(body), status_code)

    @staticmethod
    def created(
        data: Optional[Any] = None, message: str = "Resource created successfully"
    ) -> Response:
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
    def error(
        message: str = "Internal server error",
        status_code: int = 400,
        error_code: Optional[str] = None,
        details: Optional[str] = None,
    ) -> Response:
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
        body = {"success": False, "message": message}
        if error_code is not None:
            body["error_code"] = error_code
        if details is not None:
            body["details"] = details
        return make_response(jsonify(body), status_code)
