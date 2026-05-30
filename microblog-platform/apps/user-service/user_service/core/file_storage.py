from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool

UPLOAD_DIR = Path("media/users")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def _write_file(filepath: Path, content: bytes) -> None:
    """Helper to write bytes to a file synchronously."""
    with open(filepath, "wb") as buffer:
        buffer.write(content)


async def save_image_file(image: UploadFile | None) -> str | None:
    if image is None or not image.filename:
        return None

    # 1. Validate content type safely
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image type. Allowed types: JPEG, PNG, WEBP.",
        )

    # 2. Extract and sanitize file extension
    extension = Path(image.filename).suffix
    if not extension:
        # Fallback if filename lacks an extension
        extension = ".jpg" if image.content_type == "image/jpeg" else ".png"

    # 3. Generate unique file path
    filename = f"{uuid4()}{extension}"
    filepath = UPLOAD_DIR / filename

    # 4. Read content async and offload blocking write operation to a threadpool
    file_bytes = await image.read()
    await run_in_threadpool(_write_file, filepath, file_bytes)

    # Returns the relative file path as a string (e.g., 'media/users/abc-123.jpg')
    return str(filepath)
