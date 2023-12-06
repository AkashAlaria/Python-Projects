# importing libraries
from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

client_id = 'c69900443e754f59a83f7d7a1baa8683'
client_secret = 'd256cf44440b4d49af6de1a14d1f71ea'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://localhost:8080',
                                               scope='playlist-modify-private playlist-modify-public'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist = request.form['artist']
        genre = request.form['genre']
        num = request.form['num']
        playlist_name = request.form['playlist_name']

        playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name, public=False)

        results = sp.search(q=f"artist: {artist} genre: {genre}", type='track', limit=num)
        track_uris = [track['uri'] for track in results['tracks']['items']]
        sp.playlist_add_items(playlist['id'], track_uris)

        return "Playlist created!"

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
