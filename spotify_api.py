import requests
import time


def get_recently_played_tracks(token,days):
    curr_time = time.time() # Time since epoch
    tiempo = curr_time - (86400 * days)
    tiempo_ml = int(tiempo * 1000)
    params = {'limit': 10, 'before': tiempo_ml}
    headers = {'Authorization': 'Bearer {}'.format(token)}
    endpoint = 'https://api.spotify.com/v1/me/player/recently-played'
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()


if __name__ == '__main__':
	token = ''
	music_played = get_recently_played_tracks(token,days)
	print(music_played)