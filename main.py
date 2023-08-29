from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://x.thunkable.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create_csv/")
async def create_csv(file: UploadFile = File(...)):
    data = await file.read()
    # Convert the data to a list of dictionaries
    data_list = [dict(row) for row in csv.DictReader(data.decode().splitlines())]
    # Create a temporary CSV file
    with open('temp.csv', mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data_list[0].keys())
        writer.writeheader()
        writer.writerows(data_list)
    # Return the CSV file as a response
    return FileResponse('temp.csv', media_type='text/csv', filename='data.csv')