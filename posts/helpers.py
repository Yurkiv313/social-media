import pathlib
import uuid
from django.utils.text import slugify


def post_image_path(instance, filename) -> pathlib.Path:
    filename = (
        f"{slugify(instance.author.email)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/post/") / pathlib.Path(filename)
