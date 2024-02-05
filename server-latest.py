from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import Response
from starlette.requests import Request
import logging
import os
from datetime import datetime


app = FastAPI()

def is_desc_txt(file_name: str) -> bool:
    """
    Check if the file name is 'desc.txt'.

    Args:
    file_name (str): The name of the file

    Returns:
    bool: True if the file name is 'desc.txt', False otherwise
    """
    return file_name.lower() == "desc.txt"


@app.get("/list")
async def read_file_names(
    path: str = "official",
    language: str = None,
):
    """
    Retrieves a list of file names in the specified language folder.
    Args:
        path (str): The folder path to be searched.
        language (str): The language for which the file names are to be retrieved.
    Returns:
        Response: A response containing the list of file names.
    Raises:
        HTTPException: If the language is not selected or the folder doesn't exist.
    """
    if not language:
        raise HTTPException(status_code=400, detail="Language not selected")

    response = ""

    folder_path = os.path.join("official", language) if path == "official" else os.path.join("unofficial", language)

    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail=f"Folder '{folder_path}' doesn't exist")

    file_names = [entry.name for entry in os.scandir(folder_path) if entry.is_file() and not is_desc_txt(entry.name)]

    response = "\n".join([
        "Name | Type | Description | Size | Last Modified",
        "------- | -------- | -------- | -------- | --------",
    ])
    for f in file_names:
        base_name, extension = os.path.splitext(f)
        file_type = extension.lstrip(".").title()
        file_size = os.path.getsize(os.path.join(folder_path, f))
        last_updated = datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, f))).strftime("%Y-%m-%d %H:%M:%S")
        description = ""
        desc_file_path = os.path.join(folder_path, "desc.txt")
        if os.path.isfile(desc_file_path):
            with open(desc_file_path, "r") as f_desc:
                for line in f_desc:
                    file_name_in_desc, desc = line.rsplit("-", 1)
                    if file_name_in_desc.strip() == f:
                        description = desc.strip()
        response += f"\n{base_name} | {file_type} | {description} | {file_size:,} KB | {last_updated}"
    return Response(content=response, media_type="text/plain")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), language: str = Form(...)):
    """
    Uploads a file to the server in the specified language directory.
    :param file: The file to be uploaded
    :param language: The language of the file
    :return: The filename of the uploaded file
    """
    # Define allowed file extensions
    allowed_extensions = {".md", ".txt"}

    # Check if file extension is allowed
    file_name, file_extension = os.path.splitext(file.filename)
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only .md or .txt files are allowed.")

    # Check file size
    max_file_size = 10 * 1024 * 1024
    file_size = 0
    while chunk := file.file.read(8192):
        file_size += len(chunk)
        if file_size > max_file_size:
            raise HTTPException(status_code=400, detail="Maximum file size exceeded")

    # Define file path and check if file already exists
    allowed_path = "unofficial"
    file_path = os.path.join("unofficial", language, file.filename)
    if os.path.isfile(file_path):
        raise HTTPException(status_code=400, detail="This file already exists. Choose a different one.")

    # Write file content to the specified path
    with open(file_path, "wb") as f:
        file.file.seek(0)
        content = file.file.read()
        f.write(content)

    return {"filename": file.filename}

@app.get("/file/{folder}/{file_name}")
async def read_file_content(
    folder: str,
    file_name: str,
    language: str = None,
    request: Request = None
):
    """
    Reads the content of a file based on the provided folder, file name, and language.
    Args:
        folder (str): The folder where the file is located.
        file_name (str): The name of the file to be read.
        language (str): The language of the file.
        request (Request): The request object.

    Returns:
        Response: The content of the file as a text/plain response.

    Raises:
        HTTPException: If there's an error accessing the file or if the language or path is invalid.
    """
    try:
        # Check if language is provided
        if not language:
            raise HTTPException(status_code=400, detail="Language not selected")

        # Define allowed paths
        allowed_paths = {"official", "unofficial"}

        # Check if the folder is valid
        if folder not in allowed_paths:
            raise HTTPException(status_code=400, detail="Path invalid. Select official or unofficial only.")

        # Check if the file is a description text
        if is_desc_txt(file_name):
            raise HTTPException(status_code=403, detail=f"Access denied to {file_name}.")

        # Get the current working directory and construct the file path
        current_path = os.getcwd()
        file_path = os.path.join(current_path, folder, language, file_name)

        # Check if the file exists
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail=f"File '{file_name}' in folder '{folder}' doesn't exist")

        # Open and read the file content
        with open(file_path, "rb") as f:
            content = f.read().decode()

        # Return the file content as a text/plain response
        return Response(content=content, media_type="text/plain")

    # Catch HTTPExceptions
    except HTTPException as e:
        raise e
    # Catch any other exceptions and raise a 500 error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log incoming HTTP requests and their processing time.
    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next middleware or endpoint handler.

    Returns:
        Response: The HTTP response to be sent back to the client.
    """
    # Record the start time of the request processing
    start_time = datetime.now()

    # Call the next middleware or endpoint handler to process the request
    response = await call_next(request)

    # Calculate the processing time of the request
    process_time = (datetime.now() - start_time).total_seconds()

    # Extract request details for logging
    client_ip = request.client.host
    request_method = request.method
    request_url = request.url.path
    status_code = response.status_code
    user = request.headers.get("User")

    # Log the request details
    logging.info(f"{client_ip} - {request_method} {request_url} - {status_code} - {process_time:.2f}s - {user}")

    # Return the HTTP response
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
