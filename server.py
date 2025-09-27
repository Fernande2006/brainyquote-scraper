from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from scraper import scrape_quotes
from supabase_client import supabase
import threading
import csv
from io import StringIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

threads = {}

@app.post("/scrape")
def start_scraper(topic: str):
    if topic in threads and threads[topic].is_alive():
        return {"message": "Scraper déjà en cours pour ce sujet."}
    
    thread = threading.Thread(target=scrape_quotes, args=(topic,))
    thread.start()
    threads[topic] = thread
    return {"message": f"Scraping pour le sujet '{topic}' lancé."}

@app.get("/quotes/csv")
def download_csv():
    data = supabase.table("quotes").select("*").execute().data
    if not data:
        return {"message": "Pas de données"}

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["quote", "author", "link", "image_url"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=quotes.csv"})

@app.get("/quotes/json")
def download_json():
    data = supabase.table("quotes").select("*").execute().data
    return JSONResponse(content=data)