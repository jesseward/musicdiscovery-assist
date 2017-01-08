# musicdiscovery-assist

Google Home assistant for music recommendations, built with Python &amp; Flask. Using Google Home, Google Cloud Platform and API.ai

In a nutshell this service consists of the following

* a very light weight flask app (https://github.com/jesseward/musicdiscovery-assist) 
* An agent created at api.ai
* All api.ai intents, with the exception of the 'help' intent  are answered by the musicdiscovery-assist webhook (this flask app).
* Flask app is hosted on GAE. Its sole purpose is to massage communication between api.api and the last.fm API. Calls that result in a memcache miss, pass through to the last.fm API.

# Example Google Home invocations 

* OK Google, let me talk to music recommendations
* OK Google, ask music discovery about artist Nightmares on Wax
* OK Google, ask music discovery what artists are similar to Underground Resistance
* OK Google, ask music discovery what are the popular songs by Boards of Canada
* OK Google, ask music discovery what songs are similar to Caught Up by Metro Area
* OK Google, ask music discovery what can i do
