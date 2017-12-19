# Current status

This application is no longer active development. This service was refactored and published to Google Action applications using  https://github.com/jesseward/songexplorer . The 'musicdiscovery-assist' code will continue to exist here as-is.

# musicdiscovery-assist

Google Home assistant for music recommendations, built with Python , Redis &amp; Flask. Using Google Home and API.ai

In a nutshell this service consists of the following

* a very light weight flask app (https://github.com/jesseward/musicdiscovery-assist) 
* An agent created at api.ai
* All api.ai intents, with the exception of the 'help' intent  are answered by the musicdiscovery-assist webhook (this flask app).
* A self hosted Flask app. Its sole purpose is to massage communication between api.api and the last.fm API. Calls that result in a memcache miss, pass through to the last.fm API.

# Example Google Home invocations 

* OK Google, let me talk to song explorer
* OK Google, ask song explorer about artist Nightmares on Wax
* OK Google, ask song explorer what artists are similar to Underground Resistance
* OK Google, ask song explorer what are the popular songs by Boards of Canada
* OK Google, ask song explorer what songs are similar to Caught Up by Metro Area
* OK Google, ask song explorer what can i do
