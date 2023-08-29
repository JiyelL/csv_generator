from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import csv

app = FastAPI()

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