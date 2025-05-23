from drf_spectacular.utils import OpenApiParameter
from user.serializers import (
    UserCreateSerializer,
    UserReadSerializer,
    FollowingListSerializer,
    FollowersListSerializer,
)

register_schema = {
    "summary": "Register a new user",
    "description": "Creates a new user using email and password.",
    "request": UserCreateSerializer,
    "responses": {201: UserReadSerializer},
    "tags": ["auth"],
}

logout_schema = {
    "summary": "Logout user (blacklist refresh token)",
    "description": (
        "Accepts a refresh token and blacklists it, "
        "effectively logging the user out.\n\n"
        "📥 **Request Body**:\n"
        "```json\n"
        '{ "refresh": "<refresh_token>" }\n'
        "```\n"
        "🔁 **Response**:\n"
        "- 205 No Content — success\n"
        "- 400 Bad Request — if token is invalid or missing"
    ),
    "tags": ["auth"],
    "request": {
        "type": "object", "properties": {"refresh": {"type": "string"}}
    },
    "responses": {
        205: None,
        400: {"type": "object", "example": {"detail": "Invalid token."}},
    },
}

user_list_schema = {
    "summary": "Search users",
    "description": "Returns a list of users. "
    "Supports search by email, first name, or last name.",
    "parameters": [
        OpenApiParameter(
            "search", str, OpenApiParameter.QUERY, description="Search query"
        )
    ],
    "responses": UserReadSerializer(many=True),
    "tags": ["users"],
}

follow_schema = {
    "summary": "Follow or unfollow user",
    "description": "Send POST to follow a user and DELETE to unfollow."
    " Can't follow yourself.",
    "tags": ["follows"],
    "responses": {
        201: None,
        204: None,
        400: {"type": "object", "example": {"detail": "Already following."}},
    },
}

following_list_schema = {
    "summary": "List users you are following",
    "description": "Returns a list of users the current user is following.",
    "responses": FollowingListSerializer(many=True),
    "tags": ["follows"],
}

followers_list_schema = {
    "summary": "List your followers",
    "description": "Returns a list of users that are "
                   "following the current user.",
    "responses": FollowersListSerializer(many=True),
    "tags": ["follows"],
}
