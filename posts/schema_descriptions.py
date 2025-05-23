from drf_spectacular.utils import OpenApiParameter
from posts.serializers import PostListSerializer, PostRetrieveSerializer

post_list_schema = {
    "summary": "List posts",
    "description": (
        "Returns posts created by the current user and by users they follow.\n\n"
        "Optionally filters posts by hashtag using the `hashtag` query parameter."
    ),
    "parameters": [
        OpenApiParameter(
            name="hashtag",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter posts by hashtag substring (case-insensitive)"
        )
    ],
    "responses": PostListSerializer(many=True),
    "tags": ["posts"]
}

post_create_schema = {
    "summary": "Create a new post",
    "description": (
        "Create a new post with optional image and hashtags. "
        "Only authenticated users can create posts."
    ),
    "request": PostRetrieveSerializer,
    "responses": {201: PostRetrieveSerializer},
    "tags": ["posts"]
}

post_detail_schema = {
    "summary": "Retrieve, update or delete a post",
    "description": (
        "Full CRUD operations on a post. Only the author can update or delete the post."
    ),
    "responses": {
        200: PostRetrieveSerializer,
        403: {"description": "You are not the author of this post"},
        404: {"description": "Post not found"},
    },
    "tags": ["posts"]
}
