from supabase_client import supabase
from playwright.sync_api import sync_playwright
import time
import requests
import uuid

def scrape_quotes(topic="motivational"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        })

        url = f"https://www.brainyquote.com/topics/{topic}-quotes"
        print(f"🔍 Ouverture de : {url}")
        page.goto(url, timeout=60000)

        # attend les citations
        page.wait_for_selector(".b-qt")

        quotes = page.locator(".b-qt")
        authors = page.locator(".bq-aut")
        images = page.locator(".bqPhoto")  # peut ne rien trouver

        total = quotes.count()
        print(f"\n== {total} citations trouvées ==\n")

        for i in range(total):
            quote = quotes.nth(i).inner_text()
            author = authors.nth(i).inner_text()
            storage_url = None

            # On récupère l'image seulement si elle existe
            if i < images.count():
                try:
                    image_attr = images.nth(i).get_attribute("data-img-url") or images.nth(i).get_attribute("src")
                    if image_attr:
                        image_url_full = f"https://www.brainyquote.com{image_attr}"
                        img_data = requests.get(image_url_full).content
                        filename = f"{uuid.uuid4()}.jpg"
                        supabase.storage.from_("quotes-images").upload(filename, img_data)
                        storage_url = supabase.storage.from_("quotes-images").get_public_url(filename)["publicUrl"]
                except Exception as e:
                    print(f"⚠️ Erreur téléchargement image: {e}")

            data = {
                "quote": quote,
                "author": author,
                "link": url,
                "image_url": storage_url
            }

            supabase.table("quotes").insert(data).execute()
            print(f"{i+1}. \"{quote}\" — {author}")
            time.sleep(0.1)

        browser.close()
        print("✅ Scraping terminé !")

if __name__ == "__main__":
    scrape_quotes("motivational")
