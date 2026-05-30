"""
Current user profile endpoint documentation.
"""

from typing import Any

GET_MY_PROFILE_SUMMARY = "Retrieve the current user's profile"

GET_MY_PROFILE_DESCRIPTION = """
Retrieve the profile of the currently authenticated user.

This endpoint returns the profile associated with the access token
used to authenticate the request.

Endpoint
--------
GET /me

Authentication
--------------
Bearer token required.

Returns
-------
UserRead
    Profile information for the authenticated user.

Notes
-----
- The user identifier is derived from the JWT access token.
- Users can only retrieve their own profile through this endpoint.
- Sensitive information such as password hashes is never returned.
"""

GET_MY_PROFILE_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        "description": ("User profile retrieved successfully."),
    },
    401: {
        "description": ("Authentication credentials were not provided or are invalid."),
    },
    404: {
        "description": ("User profile not found."),
    },
}
