

## Planned API List

### Auth-service

```
POST   /api/v1/authors/           -> Onboard a user as an officially recognized Author
GET    /api/v1/authors/           -> List and search authors with pagination filters
GET    /api/v1/authors/{id}       -> Fetch specific author profile and dynamic engagement metrics
PUT    /api/v1/authors/{id}       -> Update professional biography, website links, or settings
GET    /api/v1/authors/{id}/stats -> Aggregate service endpoint tracking reader analytics/views

POST   POST /api/v1/authors/{id}/follow   -> Follow an Author/User
POST    POST /api/v1/authors/{id}/unfollow  -> Unfollow an Author/User
GET    /api/v1/social/authors/{id}/followers -> Get list of User IDs following this author
GET    /api/v1/social/users/{id}/following   -> Get list of Author/User IDs this user follows
```

### Blog Service

```
POST   /api/v1/posts/             -> Create a new blog post entry (Draft or Published)
GET    /api/v1/posts/             -> Read a public chronological timeline feed of posts
GET    /api/v1/posts/{id}         -> Fetch an individual blog post payload by ID
PUT    /api/v1/posts/{id}         -> Modify post text content, update tags, or change draft status
DELETE /api/v1/posts/{id}         -> Delete a post record
GET    /api/v1/posts/author/{id}  -> Fetch all blog entries published by a target author


POST   /api/v1/posts/{id}/rate     -> Submit or update a rating (Guarded by is_authenticated)
DELETE /api/v1/posts/{id}/rate     -> Remove the current user's rating (Guarded by is_authenticated)


POST   /api/v1/posts/{post_id}/comments        -> Leave a top-level comment (Guarded by is_authenticated)
POST   /api/v1/posts/{post_id}/comments/{id}   -> Reply to a specific comment (Guarded by is_authenticated, passes parent_id)
GET    /api/v1/posts/{post_id}/comments        -> Fetch the entire threaded comment tree for a post
DELETE /api/v1/comments/{id}                   -> Delete a comment (Cascades down to delete its replies)
```

### User Service

```text
POST   /api/v1/users/         -> Create/Register a new user account
POST   /api/v1/users/login    -> Authenticate credentials (upsert user on-the-fly, returns JWT token)
GET    /api/v1/users/me       -> Retrieve current authenticated user profile (via authheader)
GET    /api/v1/users/{id}     -> Fetch a public user profile by unique ID
PUT    /api/v1/users/{id}     -> Update profile fields or upload a new profile image
DELETE /api/v1/users/{id}     -> Soft-delete/Archive an account

POST   /api/v1/users/me/addresses     -> Add a new address
GET    /api/v1/users/me/addresses     -> List all addresses for the current user
PUT    /api/v1/users/me/addresses/{id} -> Update a specific address entry
DELETE /api/v1/users/me/addresses/{id} -> Remove an address entry


GET    /api/v1/authors/{id}         -> Public profile view (returns the profile details along with the socials JSON object)
PUT    /api/v1/authors/me/socials   -> Update social links payload (guarded by is_authenticated)
```
