from accounts.serializers import PublicProfileSerializer, FullProfileSerializer

own_profile_schema = {
    "summary": "Get or update your profile",
    "description": (
        "Retrieve or update your own profile information.\n\n"
        "You can update your name, bio, location, and profile image."
    ),
    "responses": {
        200: FullProfileSerializer,
        403: {"description": "Permission denied"},
    },
    "tags": ["profile"],
}

public_profile_schema = {
    "summary": "View public profile",
    "description": (
        "Retrieve public profile of another user by their ID.\n\n"
        "Includes email, name, bio, location, and image (read-only)."
    ),
    "responses": {
        200: PublicProfileSerializer,
        404: {"description": "User not found"},
    },
    "tags": ["profile"],
}
