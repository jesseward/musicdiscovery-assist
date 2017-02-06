import json
import pytest

from mock import MagicMock

from discovery_assist.liblastfm import LastFM


def test_clean_string():
    fm = LastFM('no api key')
    assert fm._clean_string('<esi>sys64738</esi>') == 'sys64738'


def test_get_similar_tracks():

    with open('lastfm-track.getSimilar.json') as fh:
        data = json.load(fh)

    fm = LastFM('no api key')
    fm._fetch = MagicMock(return_value=data)
    assert len(fm.get_similar_tracks('artist', 'track')) == 99


def test_get_artist_info():

    with open('lastfm-artist.getInfo.json') as fh:
        data = json.load(fh)

    fm = LastFM('fake key for testing')
    fm._fetch = MagicMock(return_value=data)
    assert fm.get_artist_info('mock artist') == fm._clean_string(data['artist']['bio']['content'])


def test_get_similar_artists():

    with open('lastfm-artist.getSimilar.json') as fh:
        data = json.load(fh)

    fm = LastFM('fake key for testing')
    fm._fetch = MagicMock(return_value=data)
    assert len(fm.get_similar_artists('artist')) == 100


def test_get_artist_top_tracks():

    with open('lastfm-artist.getTopTracks.json') as fh:
        data = json.load(fh)

    fm = LastFM('fake key for testing')
    fm._fetch = MagicMock(return_value=data)
    assert len(fm.get_artist_top_tracks('artist')) == 50
