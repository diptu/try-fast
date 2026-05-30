"""
User profile update endpoint documentation.
"""

UPDATE_USER_PROFILE_SUMMARY = "Update a user profile"

UPDATE_USER_PROFILE_DESCRIPTION = """
Update an existing user profile.

This endpoint allows authenticated users to update their own
account information.

Endpoint
--------
PUT /{id}

Request Content Type
--------------------
multipart/form-data

Parameters
----------
id : str
    Unique identifier of the user.

name : str, optional
    Updated display name.

email : EmailStr, optional
    Updated email address.

password : str, optional
    Updated password.

image : UploadFile, optional
    Updated profile image.

Returns
-------
UserRead
    Updated user profile.

Authentication
--------------
Bearer token required.

Authorization
-------------
Users may only update their own profile.

Notes
-----
- Partial updates are supported.
- Any provided password is securely hashed before storage.
- Updating another user's profile is prohibited.
- Profile image uploads are optional.
- Sensitive information is never returned in the response.
"""

UPDATE_USER_PROFILE_RESPONSES = {
    200: {
        "description": ("User profile updated successfully."),
    },
    401: {
        "description": ("Authentication credentials were not provided or are invalid."),
    },
    403: {
        "description": ("You do not have permission to update this profile."),
    },
    404: {
        "description": ("User profile not found."),
    },
    409: {
        "description": ("A user with the provided email address already exists."),
    },
    422: {
        "description": ("Validation error."),
    },
}
