from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import Response
from starlette.requests import Request
import logging
import os
from datetime import datetime

app = FastAPI()

# Configure logging
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.get("/list")
async def read_file_names(path: str = "official", language: str = "en"):
    response = ""  # Initialize the response variable

    # Check if the path parameter is "unofficial" and construct the full folder path based on language
    folder_path = os.path.join("official", language) if path == "official" else os.path.join("unofficial", language)

    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail=f"The folder '{folder_path}' does not exist")

    file_names = [entry.name for entry in os.scandir(folder_path) if entry.is_file()]
    response = "\n".join([
        "Name | Type | Description | Size | Last Modified",
        "------- | -------- | -------- | -------- | --------",
    ])
    for f in file_names:
        base_name, extension = os.path.splitext(f)  # Unpack the tuple
        file_type = extension.lstrip(".").title()  # Access the extension part
        file_size = os.path.getsize(os.path.join(folder_path, f))
        last_updated = datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, f))).strftime("%Y-%m-%d %H:%M:%S")
        description = ""  # Get description from desc.txt if available
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
    # Restrictions on file name and type
    allowed_extensions = {".md", ".txt"}
    file_name, file_extension = os.path.splitext(file.filename)

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .md or .txt files are allowed.")

    # Restrictions on file size
    max_file_size = 10 * 1024 * 1024  # 10 MB (or any other desired limit)
    file_size = 0

    # Read the file content and get its size
    while chunk := file.file.read(8192):  # Read in blocks of 8 KB (you can adjust the block size according to your needs)
        file_size += len(chunk)
        if file_size > max_file_size:
            raise HTTPException(status_code=400, detail="The file size exceeds the maximum limit of 10 MB.")

    # Check if the file already exists
    allowed_path = "unofficial"
    # Save the file in the language-specific folder
    file_path = os.path.join("unofficial", language, file.filename)  # Example using "unofficial"

    if os.path.isfile(file_path):
        raise HTTPException(status_code=400, detail="A file with this name already exists. Please choose a different name.")

    # Write the file to the allowed path
    with open(file_path, "wb") as f:
        file.file.seek(0)  # Rewind the file pointer before writing
        content = file.file.read()
        f.write(content)

    return {"filename": file.filename}

@app.post("/file/{folder}")
async def read_file_content(folder: str, file_name: str, language: str, request: Request):
    # Check if the route is allowed
    allowed_paths = {"official", "unofficial"}
    if folder not in allowed_paths:
        raise HTTPException(status_code=400, detail="Invalid folder. Choose 'official' or 'unofficial'.")

    # Construct the full file path and construct the full file path based on language
    file_path = os.path.join(folder, language, file_name)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"The file '{file_name}' in folder '{folder}' does not exist")

    with open(file_path, "rb") as f:
        content = f.read().decode()

    return Response(content=content, media_type="text/plain")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    client_ip = request.client.host
    request_method = request.method
    request_url = request.url.path
    status_code = response.status_code
    user = request.headers.get("User")
    logging.info(f"{client_ip} - {request_method} {request_url} - {status_code} - {process_time:.2f}s - {user}")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
