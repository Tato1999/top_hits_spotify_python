from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do u want to travel to? Type the date in this format YYYY-MM-DD \n")

spotify_end_id = "*******************"
spotify_end_key = "****************"

link = f"https://www.billboard.com/charts/hot-100/{date}"
print(link)

resp = requests.get(link)
page = resp.text



soup = BeautifulSoup(page,"lxml")
song_name = []
uris = []
# chart = soup.select(".o-chart-results-list-row-container .o-chart-results-list-row span")
chart = soup.select(".chart-results-list .o-chart-results-list-row-container .lrv-u-width-100p .lrv-a-unstyle-list #title-of-a-story")

for i in chart:
    music_name = i.getText()
    music_name = music_name.translate({ord("\n"): None})
    music_name = music_name.translate({ord("\t"): None})
    song_name.append(music_name)
   
    
sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="spotify_end_id",
        client_secret="spotify_end_key",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()

print(user_id["id"])
playlist = sp.user_playlist_create(user=user_id['id'], name=f"{date} Billboard 100", public=False)
for i in song_name:

    result = sp.search(q=f"track: {i}", type="track")
    items = result["tracks"]["items"][0]['uri']
    uris.append(items)

print(uris)
sp.playlist_add_items(playlist_id=playlist["id"], items=uris)

