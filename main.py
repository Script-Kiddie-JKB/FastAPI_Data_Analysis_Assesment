from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Dict
import uuid
import os
from data_handler import DataHandler
from visualizer import Visualizer
from dummy_data_generator import create_dummy_csv

app = FastAPI()

# In-memory storage for uploaded files (in a real-world scenario, will use a database)
file_storage = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_content = await file.read()
    file_storage[file_id] = file_content
    
    return JSONResponse(content={
        "message": "File uploaded successfully",
        "file_id": file_id
    })

@app.get("/summary/{file_id}")
async def get_summary(file_id: str):
    if file_id not in file_storage:
        raise HTTPException(status_code=404, detail="File not found")
    
    data_handler = DataHandler(file_storage[file_id])
    summary = data_handler.get_summary()
    
    return JSONResponse(content={"summary": summary})

class TransformationRequest(BaseModel):
    transformations: Dict[str, Dict[str, List[str]]]

@app.post("/transform/{file_id}")
async def transform_data(file_id: str, request: TransformationRequest):
    if file_id not in file_storage:
        raise HTTPException(status_code=404, detail="File not found")
    
    data_handler = DataHandler(file_storage[file_id])
    transformed_data = data_handler.apply_transformations(request.transformations)
    
    new_file_id = str(uuid.uuid4())
    file_storage[new_file_id] = transformed_data.to_csv().encode()
    
    return JSONResponse(content={
        "message": "Transformations applied successfully",
        "file_id": new_file_id
    })

@app.get("/visualize/{file_id}")
async def visualize_data(
    file_id: str,
    chart_type: str = Query(..., description="Type of chart to generate"),
    columns: List[str] = Query(..., description="Columns to use for visualization")
):
    if file_id not in file_storage:
        raise HTTPException(status_code=404, detail="File not found")
    
    data_handler = DataHandler(file_storage[file_id])
    visualizer = Visualizer(data_handler.get_data())
    
    try:
        image_path = visualizer.create_visualization(chart_type, columns)
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/generate_dummy_data")
async def generate_dummy_csv():
    file_path = create_dummy_csv()
    return FileResponse(file_path, filename="dummy_data.csv")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

