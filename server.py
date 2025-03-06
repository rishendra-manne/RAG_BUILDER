import os
import uuid
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from src.pipelines.training_pipeline import Pipeline
from src.pipelines.prediction_pipeline import PredictPipeline
from src.exception import CustomException
from src.logger import logging
import time

app = FastAPI()
pipeline=Pipeline()
prediction_pipe=PredictPipeline()


@app.post("/create_pipeline/{pipeline_id}")
async def create_pipeline(pipeline_id: str, file: UploadFile = File(...)):
    if not pipeline_id.strip():
        raise HTTPException(status_code=400, detail="Pipeline ID cannot be empty")
    pipeline.create_pipeline(pipeline_id,file)
    return JSONResponse(content="Pipeline created successfully",status_code=200)


@app.post("/query_pipeline/{pipeline_id}")
async def query_pipeline(pipeline_id: str, query: str):
    response = prediction_pipe.query_pipeline(pipeline_id, query)
    return JSONResponse(content=response, status_code=200)

@app.delete("/delete_pipeline/{pipeline_id}")
async def delete_pipeline(pipeline_id: str):
    """
    Endpoint to delete a specific pipeline.
    
    Args:
        pipeline_id (str): Unique pipeline identifier
    
    Returns:
        JSONResponse with deletion status
    """
    result = pipeline.delete_pipeline(pipeline_id)
    return JSONResponse(content=result, status_code=200)