"""
Authentication endpoint documentation.
"""

from typing import Any

LOGIN_USER_SUMMARY = "Authenticate a user"

LOGIN_USER_DESCRIPTION = """
Authenticate a user and issue a JWT access token.

This endpoint validates the provided user credentials and returns
a signed JWT access token that can be used to access protected
resources within the system.

Endpoint
--------
POST /login

Request Content Type
--------------------
multipart/form-data

Parameters
----------
email : EmailStr
    User email address.

password : str
    User password.

name : str
    User display name.

image : UploadFile, optional
    Optional profile image uploaded during authentication.

Returns
-------
TokenResponse
    Authentication result containing:

    - JWT access token
    - Token type
    - Authenticated user details

Authentication
--------------
No authentication is required.

Notes
-----
- Access tokens are generated using the application's configured
  JWT secret and expiration settings.
- The token expiration period is controlled by the
  ``ACCESS_TOKEN_EXPIRE_MINUTES`` configuration setting.
- The returned token should be supplied in the Authorization header
  using the Bearer authentication scheme.

Example
-------
Authorization: Bearer <access_token>
"""

LOGIN_USER_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        "description": ("User authenticated successfully and access token issued."),
    },
    401: {
        "description": ("Authentication failed due to invalid credentials."),
    },
    409: {
        "description": (
            "A user with the provided email already exists or a "
            "credential conflict occurred."
        ),
    },
    500: {
        "description": (
            "Unexpected server error while processing the authentication request."
        ),
    },
}
