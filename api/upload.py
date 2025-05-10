from fastapi import APIRouter, BackgroundTasks, File, UploadFile
from uuid import uuid4
import os
import time
import asyncio  # Use asyncio for non-blocking sleep

router = APIRouter()

# Dictionary to simulate an in-memory storage for process status
processing_status = {}


# Endpoint to upload the PDF
@router.post("/upload/")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        # Generate a unique process ID (UUID)
        process_id = str(uuid4())

        # Define a directory to store the uploaded PDFs
        upload_dir = "uploaded_pdfs/"
        os.makedirs(upload_dir, exist_ok=True)  # Create the folder if it doesn't exist

        # Save the PDF file
        file_path = os.path.join(upload_dir, f"{process_id}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Set initial status as "processing"
        processing_status[process_id] = {"status": "processing", "file_path": file_path}

        # Start a background task to process the file
        background_tasks.add_task(process_pdf, process_id)

        return {"message": "File uploaded successfully!", "process_id": process_id}

    except Exception as e:
        return {"error": str(e)}


# Background task to simulate processing
async def process_pdf(process_id: str):
    # Simulate processing (e.g., timer or other processing logic)
    await asyncio.sleep(100)  # Non-blocking sleep for 10 seconds

    # Update the status to "completed"
    if process_id in processing_status:
        processing_status[process_id]["status"] = "processed"


# Endpoint to get the status of a process
@router.get("/status/{process_id}/")
async def get_status(process_id: str):
    if process_id in processing_status:
        status = processing_status[process_id]
        return {"process_id": process_id, "status": status["status"]}
    else:
        return {"error": "Process ID not found"}
