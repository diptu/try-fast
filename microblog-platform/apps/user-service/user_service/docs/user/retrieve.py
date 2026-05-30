"""
User profile retrieval endpoint documentation.
"""

from typing import Any

GET_USER_PROFILE_SUMMARY = "Retrieve a user profile"

GET_USER_PROFILE_DESCRIPTION = """
Retrieve a user profile by its unique identifier.

Endpoint
--------
GET /{id}

Parameters
----------
id : str
    Unique identifier of the user.

Returns
-------
UserRead
    User profile information.

Authentication
--------------
No authentication required.

Notes
-----
- Returns the user profile associated with the supplied identifier.
- Sensitive information such as password hashes is excluded.
"""

GET_USER_PROFILE_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        "description": ("User profile retrieved successfully."),
    },
    404: {
        "description": ("User profile not found."),
    },
}
