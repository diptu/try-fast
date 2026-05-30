"""
Documentation for user deletion endpoints.
"""

DELETE_USER_DESCRIPTION = """
Soft-delete (archive) a user account.

Authorization
-------------
Allowed roles:

- admin
- superadmin

Notes
-----
The user record remains stored in the database and is marked as
archived instead of being permanently deleted.
"""

DELETE_USER_SUMMARY = "Soft-delete a user account"
