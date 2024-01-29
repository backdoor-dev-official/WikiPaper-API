# Import the required libraries
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import Response
from starlette.requests import Request
import os
from datetime import datetime
from pycloudflared import try_cloudflare

app = FastAPI()

@app.get("/list")
async def list_files(path: str = "official"):
    """List all files in a given directory"""
    response = ""  # Initialize the response variable

    # Check if the path parameter is "unofficial"
    if path == "unofficial":
        folder_path = "unofficial"
    else:
        folder_path = "official"

    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail="The folder '{}' does not exist".format(folder_path))

    file_names = [entry.name for entry in os.scandir(folder_path) if entry.is_file()]
    response = "\n".join([
        "Name | Type | Description | Size | Last Modified",
        "------- | -------- | -------- | -------- | --------",
    ])
    for f in file_names:
        base_name, extension = os.path.splitext(f)  # Unpack the tuple
        file_type = extension.lstrip(".").title()  # Access the extension part
        file_size = os.path.getsize(os.path.join(folder_path, f))
        last_modified = datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, f))).strftime("%Y-%m-%d %H:%M:%S")
        description = ""  # Get description from desc.txt if available
        desc_file_path = os.path.join(folder_path, "desc.txt")
        if os.path.isfile(desc_file_path):
            with open(desc_file_path, "r") as f_desc:
                for line in f_desc:
                    file_name_in_desc, desc = line.rsplit("-", 1)
                    if file_name_in_desc.strip() == f:
                        description = desc.strip()
        response += f"\n{base_name} | {file_type} | {description} | {file_size:,} KB | {last_modified}"
    return Response(content=response, media_type="text/plain")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a new file to the server"""
    # Set restrictions on filename and file type
    allowed_extensions = {".md", ".txt"}
    file_name, file_extension = os.path.splitext(file.filename)
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .md or .txt files are allowed.")

    # Set restriction on file size
    max_file_size = 10 * 1024 * 1024  # 10 MB (or any other desired limit)
    file_size = 0

    # Read the file content and get its size
    while chunk := file.file.read(8192):  # Read in chunks of 8 KB (adjustable according to your needs)
        file_size += len(chunk)
        if file_size > max_file_size:
            raise HTTPException(status_code=400, detail="The file size exceeds the maximum limit of 10 MB.")

    # Check if the file already exists
    allowed_path = "unofficial"
    file_path = os.path.join(allowed_path, file.filename)

    if os.path.isfile(file_path):
        raise HTTPException(status_code=400, detail="A file with this name already exists. Please choose a different name.")

    # Save the file to the allowed path
    with open(file_path, "wb") as f:
        file.file.seek(0)  # Reset the pointer position before writing
        content = file.file.read()
        f.write(content)

    return {"filename": file.filename}

@app.post("/file/{folder}")
async def read_file_content(folder: str, file_name: str, request: Request):
    """Read the contents of an existing file"""
    # Check if the route is allowed
    allowed_paths = {"official", "unofficial"}
    if folder not in allowed_paths:
        raise HTTPException(status_code=400, detail="Invalid folder. Choose 'official' or 'unofficial'.")

    # Construct the full file path
    file_path = os.path.join(folder, file_name)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"The file '{file_name}' in folder '{folder}' does not exist")

    with open(file_path, "rb") as f:
        content = f.read().decode()

    return Response(content=content, media_type="text/plain")

try_cloudflare(port=5000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
