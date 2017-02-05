import re
import requests

# cleans HTML entities that may be present in the artist
# bio/summary field.
clean_re = re.compile('<.*?>')


class LastFM(object):
    """Wraps the bare minimum last.fm endpoints that we're targeting.
    The current active list of endpoints we're using is:
        artist.getInfo
        artist.getSimilar
        artist.getTopTracks
        track.getSimilar

    For documentation of last.fm API see -> http://www.last.fm/api .
    API account creation actioned at http://www.last.fm/api/account/create"""

    def __init__(self, api_key=None):
        self.api_key = api_key

    @staticmethod
    def get_deep_dict(pth, mtx):
        for level in pth:
            mtx = mtx.get(level, None)
            if mtx is None:
                break
        return mtx

    def _clean_string(self, raw):
        return re.sub(clean_re, '', raw)

    def _fetch(self, uri='http://ws.audioscrobbler.com/2.0/', params={}):
        """Issues a requests.get call to last.fm ws URI

        :param uri: AS/LastFM API endpoint.
        :param params: Dictionary containing key->value pairs for the webservice call.
        :return: Returns a requests dict from the converted JSON response object."""

        params['format'] = 'json'
        params['api_key'] = self.api_key

        res = requests.get(uri, params=params).json()

        if res.get('error'):
            raise LookupError(res.get('message'))

        return res

    def get_similar_tracks(self, artist, track_name, method='track.getSimilar', limit=10):
        """Retrieves similar tracks to an artist and trackname

        :param artist: Artist name (string) of the track we're in search of
        :param track_name: Song name (string) in which to search
        :param method: The LastFM webservice method we're calling ('artist.getinfo')
        :return: A dictionary"""

        resp = self._fetch(params={'method': method, 'limit': limit,
                                   'artist': artist, 'track': track_name})
        results = []
        for track in resp['similartracks']['track']:
            artist = track['artist']['name']
            song = track['name']
            results.append([song,  artist])
        return results

    def get_artist_info(self, artist, method='artist.getinfo'):
        """Retrieves artist/band biography summary text.

        :param artist: Artist name (string) in which we wish to retrieve artist information.
        :param method: The LastFM webservice method we're calling ('artist.getinfo')
        :return: A dictionary."""

        resp = self._fetch(params={'method': method, 'artist': artist})
        summary = resp['artist']['bio']['content']
        return self._clean_string(summary)

    def get_similar_artists(self, artist, method='artist.getsimilar', limit=10):
        """Invokes the artist.getsimilar call to last.fm

        :param artist: Target band/artist to search
        :param method: LastFM webservice to query
        :return: A list of strings containing related artists."""

        resp = self._fetch(params={'method': method, 'limit': limit,
                                   'artist': artist})
        results = []
        for artist in resp['similarartists']['artist']:
            results.append(artist['name'])

        return results

    def get_artist_top_tracks(self, artist, method='artist.getTopTracks', limit=10):
        """Fetches the top X tracks via artist.getTopTracks

        :param artist: Target artist/band to search (string)
        :param method: The LastFM webservice method to invoke (artist.getTopTracks)
        :return: A list of song names."""

        resp = self._fetch(params={'method': method, 'limit': limit,
                                   'artist': artist})

        results = []
        for track in resp['toptracks']['track']:
            results.append(track['name'])

        return results
