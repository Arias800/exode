sous_menu = {
    "movie": {
    "Populaires": "popular",
    "Mieux notes": "top_rated",
    "En salles": "now_playing",
    "Recemment" : "latest",
    "A venir" : "upcoming" },
    "tv": {
    "Populaires": "popular",
    "Mieux notes" : "top_rated",
    "Diffusees 7 jours" : "on_the_air",
    "Recemment" : "latest",
    "Diffusees ce jour": "airing_today" }
}

menu = {
    "Films": 'movie',
    "Series tv": 'tvshow',
    "test2": 'Autre', 
    'Parametre': 'pref'}


#print menu.viewvalues()
#print menu.viewkeys()

#print menu.get('Films')

#print sous_menu.get('tv').viewkeys()

#print sous_menu.get('tv').get('Populaires')

tube = {
  "adult": False,
  "backdrop_path": "/aHcth2AXzZSjhX7JYh7ie73YVNc.jpg",
  "belongs_to_collection": {
    "id": 87096,
    "name": "Avatar - Saga",
    "poster_path": "/nslJVsO58Etqkk17oXMuVK4gNOF.jpg",
    "backdrop_path": "/9s4BM48NweGFrIRE6haIul0YJ9f.jpg"
  },
  "budget": 237000000,
  "genres": [
    {
      "id": 28,
      "name": "Action"
    },
    {
      "id": 12,
      "name": "Aventure"
    },
    {
      "id": 14,
      "name": "Fantastique"
    },
    {
      "id": 878,
      "name": "Science-Fiction"
    }
  ],
  "homepage": "http://www.avatarmovie.com/index.html",
  "id": 19995,
  "imdb_id": "tt0499549"}



for genre in tube['genres']:
      genres = genre['name'] + ' '

print genres