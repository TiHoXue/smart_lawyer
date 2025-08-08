import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Create the FastAPI app instance
app = FastAPI()

# Define the directory to save uploaded files
UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(parents=True,
                       exist_ok=True)  # Create the directory if it doesn't exist


# --- The Upload Endpoint ---
# This function will be called when a POST request is made to /upload
# The `files: List[UploadFile]` part tells FastAPI to expect a list of uploaded files
# from a form field named "files".
@app.post("/upload")
async def create_upload_files(files: List[UploadFile] = File(...)):
    """
    Receives and saves a list of files sent from the client.
    """
    uploaded_filenames = []

    for file in files:
        # Define the destination path for the file
        destination_path = UPLOAD_DIRECTORY / file.filename
        uploaded_filenames.append(file.filename)

        try:
            # Save the file to the destination path by copying its contents
            with open(destination_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        finally:
            # Always close the file handle
            file.file.close()

    print(f"Files received: {uploaded_filenames}")

    # Send a success response back to the client
    return JSONResponse(
        status_code=200,
        content={
            "message": f"{len(uploaded_filenames)} files uploaded successfully!",
            "filenames": uploaded_filenames,
        },
    )


# --- Serve the Frontend ---
# This mounts a directory named 'static' to serve static files like index.html and upload.js
# The name 'static' in mount_path is what you'll use in the URL (e.g., /static/index.html)
# We will serve index.html at the root for convenience.
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse('index.html')
