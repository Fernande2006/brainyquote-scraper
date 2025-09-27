 Documentation : BrainyQuote Scraper

Informations de la base Supabase 

username : brainyquote
password : AZERTY12345@

 Installation
  Prérequis :- Python 3.10+ installé- Node.js + npm installés- Git installé (optionnel)- Un compte Supabase avec :- Une table `quotes` dans la base de données- (Optionnel) Un bucket Supabase Storage pour les images
  Étapes backend (Python) :
 1. Clone ou télécharge le projet dans un dossier :
 
 git clone https://github.com/votre-nom/brainyquote-scraper.git
 cd brainyquote-scraper

 2. Crée un environnement virtuel et active-le :

 python -m venv venv
 . env\Scripts ctivate  (Windows)
 source venv/bin/activate  (Linux / macOS)
 
 3. Installe les dépendances Python :

 pip install -r requirements.txt 

 4. Crée un fichier `.env` à la racine avec :
 
 SUPABASE_URL=...
 SUPABASE_KEY=...
 
 5. Lance le scraper manuellement :
 
 python scraper.py
 
 
 Frontend (Nuxt.js)
  Installation :
 
 cd frontend
 npm install

  Démarrage local :
 
 npm run dev
 
 Puis ouvre [http://localhost:3000](http://localhost:3000) dans ton navigateur.--
 
 Utilisation
 1. Dans l’interface Nuxt, entre un sujet de citations (`motivational`, `success`, `love`, etc).
 2. Clique sur “Lancer le scraper”.
 3. Attends que les données soient extraites.
 4. Clique sur “Télécharger CSV” ou “Télécharger JSON” si tu veux exporter.--

 
 Déploiement
  Backend (Python)- Héberge `scraper.py` dans un serveur ou sur [Render](https://render.com),
 [Railway](https://railway.app), etc