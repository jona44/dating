# Dating App API Documentation

This API is built using Django REST Framework to support the React Native mobile application.

## 🔐 Authentication

The API uses **JWT (JSON Web Token)** for authentication.

### Login
*   **URL:** `/api/auth/login/`
*   **Method:** `POST`
*   **Payload:** `{"email": "user@example.com", "password": "password"}`
*   **Response:**
    ```json
    {
        "refresh": "TOKEN_STRING",
        "access": "TOKEN_STRING"
    }
    ```

### Register
*   **URL:** `/api/auth/register/`
*   **Method:** `POST`
*   **Payload:** `{"email": "user@example.com", "password": "password123", "password2": "password123"}`

---

## 📱 Core Endpoints

### Discovery
*   **URL:** `/api/profiles/discovery/`
*   **Method:** `GET` (Authenticated)
*   **Description:** Get a list of profiles based on your preferences, excluding people you've already liked or skipped.

### Likes & Matches
*   **URL:** `/api/likes/`
*   **Method:** `POST`
*   **Payload:** `{"to_profile_id": "UUID"}`
*   **Description:** Like a profile. If they've already liked you, the response will include `is_match: true` and match details.

### Messaging
*   **URL:** `/api/conversations/`
*   **Method:** `GET`
*   **Description:** List all your conversations with last message preview and unread count.

---

## 📘 Documentation Tools

When the server is running, you can access interactive documentation:

*   **Swagger UI:** [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)
*   **Redoc:** [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)
*   **Schema (JSON):** [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

## 🛠 React Native Integration Tips

1.  **Base URL:** Set your base URL to your server address (e.g., `http://10.0.2.2:8000/api/` for Android Emulator).
2.  **Headers:** All authenticated requests must include the header:
    `Authorization: Bearer <access_token>`
3.  **Token Refresh:** If you receive a `401 Unauthorized`, use the refresh token at `/api/auth/token/refresh/` to get a new access token.
