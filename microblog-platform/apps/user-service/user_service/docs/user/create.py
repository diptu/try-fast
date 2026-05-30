"""
User creation endpoint documentation.
"""

from typing import Any

CREATE_USER_SUMMARY = "Create a user account"

CREATE_USER_DESCRIPTION = """
Create a new user account.

This endpoint registers a new user and persists the account in the
system. Passwords are securely hashed before storage.

Endpoint
--------
POST /

Request Content Type
--------------------
multipart/form-data

Parameters
----------
name : str
    User's full name.

email : EmailStr
    Unique email address.

password : str
    Plain-text password. The password is hashed before being stored.

role : str, default="customer"
    Role assigned to the user.

    Supported values include:

    - customer
    - admin
    - superadmin

status_value : str, default="active"
    Initial account status.

    Common values include:

    - active
    - inactive
    - suspended

is_email_verified : bool, default=False
    Indicates whether the user's email address has already been
    verified.

image : UploadFile, optional
    Optional profile image associated with the user account.

Returns
-------
UserRead
    The newly created user resource.

Authentication
--------------
No authentication is required.

Notes
-----
- Email addresses must be unique.
- Passwords are never stored in plain text.
- User roles and statuses are validated by the service layer.
- Profile images are optional.
- The response excludes sensitive information such as password hashes.

Examples
--------
Create a customer account:

- role = customer
- status_value = active
- is_email_verified = false
"""

CREATE_USER_RESPONSES: dict[int | str, dict[str, Any]] = {
    201: {
        "description": ("User account created successfully."),
    },
    400: {
        "description": ("Invalid request data."),
    },
    409: {
        "description": ("A user with the provided email address already exists."),
    },
    422: {
        "description": ("Validation error."),
    },
    500: {
        "description": ("Unexpected server error while creating the user."),
    },
}
