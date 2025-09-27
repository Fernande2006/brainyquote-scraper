from supabase_client import supabase

data = {
    "quote": "Test de citation",
    "author": "Moi",
    "link": "https://example.com"
}

res = supabase.table("quotes").insert(data).execute()
print(res)