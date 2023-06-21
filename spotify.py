import spotipy  # package for spotify api.
import spotipy.oauth2
import requests
import os
# from pprint import pprint


class Spotify:

    def __init__(self, date, list_track):
        self.date = date
        self.list_track = list_track
        self.client_id = os.environ["client_id"]
        self.client_sc = os.environ["client_sc"]
        self.redirect_url = "http://example.com"
        self.sp_user_token = None
        self.sp_user_id = None
        self.sp_playlist_id = None
        self.sp_uris = []
        self.auth()
        self.make_uri()

    def auth(self):
        sp_auth = spotipy.oauth2.SpotifyOAuth(client_id=self.client_id, client_secret=self.client_sc,
                                              redirect_uri=self.redirect_url, scope="playlist-modify-private")
        self.sp_user_token = sp_auth.get_cached_token()["access_token"]
        sp = spotipy.client.Spotify(auth=self.sp_user_token)
        self.sp_user_id = sp.me()["id"]

    def make_uri(self):
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=self.client_id,
                                                                             client_secret=self.client_sc)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth=self.sp_user_token)
        sp.set_auth(self.sp_user_token)
        for song in self.list_track:
            try:
                result = sp.search(q=f'track: {song["track"]} artist: {song["artist"]}', limit=1)
                self.sp_uris.append(f"spotify:track:{result['tracks']['items'][0]['id']}")
            except:
                pass
        self.create_playlist()

    def create_playlist(self):
        playlist_endpoint = f"https://api.spotify.com/v1/users/{self.sp_user_id}/playlists"
        body = {
            "name": f"{self.date} Billboard TOP 100",
            "description": f"Chart of Billboard TOP 100 songs in {self.date}.",
            "public": False
        }
        response = requests.post(url=playlist_endpoint, json=body,
                                 headers={"Authorization": f"Bearer {self.sp_user_token}"})
        self.sp_playlist_id = response.json()["id"]
        self.add_playlist()

    def add_playlist(self):
        playlist_endpoint = f"https://api.spotify.com/v1/playlists/{self.sp_playlist_id}/tracks"
        requests.post(url=playlist_endpoint, json=self.sp_uris,
                      headers={"Authorization": f"Bearer {self.sp_user_token}"})
