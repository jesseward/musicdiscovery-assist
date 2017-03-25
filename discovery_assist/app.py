import logging
import urllib

from logging.handlers import SysLogHandler

from cache import cached_result
from config import cfg
from flask import Flask, jsonify, abort, request

app = Flask(__name__)

API_MOUNTPOINT = '/api'
API_VERSION = 'v1'

handler = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_USER)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("music-discovery - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger('music-discovery')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def api_url(url):
    url = url[1:] if url.startswith('/') else url
    a = '/'.join([x for x in [API_MOUNTPOINT, API_VERSION, url]])
    return a


# @app.route(api_url('/artist/bio'), methods=['POST'])
def artist_bio(req):
    """Fetches the artist biography summary text from last.fm

    Expects JSON paramater 'artist'"""

    artist = req.get('result').get('parameters').get('artist')
    logger.info('received {0} request for artist="{1}"'.format('artist_bio', artist))
    bio = cached_result('get_artist_info', [artist], {})
    speech = 'Unable to locate biography for {artist}'.format(artist=artist)

    if bio and len(bio) > 0:
        speech = bio

    return jsonify(
        {'speech': speech,
         'displayText': speech,
         'source': 'last-assist'})


# @app.route(api_url('/artist/toptracks'), methods=['POST'])
def artist_top_tracks(req):
    """Fetches top tracks for artist from last.fm

    Expects JSON paramater 'artist'"""

    artist = req.get('result').get('parameters').get('artist')
    logger.info('received {0} request for artist="{1}"'.format('artist_top_tracks', artist))
    top_tracks = cached_result('get_artist_top_tracks', [artist], {})
    speech = 'Unable to locate top tracks for {artist}'.format(artist=artist)

    if top_tracks is not None:
        speech = 'The most popular songs for {artist} are'.format(artist=artist)
        for track in top_tracks:
            speech += '. ' + track

    return jsonify(
        {'speech': speech,
         'displayText': speech,
         'source': 'last-assist'})


# @app.route(api_url('/artist/similar'), methods=['POST'])
def artist_similar(req):
    """Fetches artists that are similar to the given artist

    Expects JSON paramater 'artist'"""

    artist = req.get('result').get('parameters').get('artist')
    logger.info('received {0} request for artist="{1}"'.format('artist_similar', artist))
    sim_artists = cached_result('get_similar_artists', [artist], {})
    speech = 'Unable to locate similar artists for {artist}'.format(artist=artist)

    if sim_artists and len(sim_artists) > 0:
        speech = 'The following artists are similar to {artist}'.format(
            artist=artist)
        for art in sim_artists:
            speech += u'. {artist}'.format(artist=art)

    return jsonify(
        {'speech': speech,
         'displayText': speech,
         'source': 'last-assist'})


# @app.route(api_url('/track/similar'), methods=['POST'])
def track_similar(req):
    """Given a song title and artist, this will retrieve like or similar songs.

    Expects JSON paramater 'artist' and 'track'"""

    artist = req.get('result').get('parameters').get('artist')
    track = req.get('result').get('parameters').get('track')
    logger.info('received {0} request for artist="{1}", track="{2}"'.format('track_similar', artist, track))
    sim_tracks = cached_result('get_similar_tracks', [artist, track], {})
    speech = 'Unable to locate similar tracks for song {track} by {artist}'.format(
        track=track, artist=artist)

    if sim_tracks and len(sim_tracks) > 0:
        speech = 'The following songs are similar to {track} by {artist}'.format(
            track=track, artist=artist)
        for track in sim_tracks:
            speech += '. ' + track[0] + ' by ' + track[1]

    return jsonify(
        {'speech': speech,
         'displayText': speech,
         'source': 'last-assist'}
    )


@app.route(api_url('/apiai-hook'), methods=['POST'])
def apiai_hook():
    """A single entry point into the web hook. Request is then dispersed
    to the appropriate method based on the 'action' passed from API.ai.
    API.ai allows only a single fullfillment endpoint per agent."""

    route = {
        'artist_bio': artist_bio,
        'artist_top_tracks': artist_top_tracks,
        'artist_similar': artist_similar,
        'track_similar': track_similar,
    }

    req = request.get_json(silent=True, force=True)
    response = {}
    try:
        response = route[req.get('result').get('action')](req)
    except (KeyError, AttributeError) as e:
        logger.error('Invalid action specified, error="{0}".'.format(e))
        return jsonify(response)

    return response


@app.errorhandler(500)
def server_error(e):
    logger.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.run(debug=False)
