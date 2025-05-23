import pathlib
import uuid
from django.utils.text import slugify


def profile_image_path(instance, filename) -> pathlib.Path:
    filename = (
        f"{slugify(instance.user.email)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/profile/") / pathlib.Path(filename)
