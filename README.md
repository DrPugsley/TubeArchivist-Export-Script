# TubeArchivist-Export-Script
Exports all videos, thumbnails, json info and subtitles from a TubeArchivist instance to a more archive-friendly format\
Must be run locally on the machine that is hosting TubeArchivist and Elasticsearch.

## WARNING: This is a very hacky script that I wrote in a couple of hours.<br>It has worked well for me, but I make no promises that it won't<br> bork your system, sleep with your wife, summon the antichrist, etc.<br>Use at your own risk!

## Usage
1. Set variables in TubeArchivist-Export-Script.py
2. `pip install -r requirements.txt`
3. `python TubeArchivist-Export-Script.py`
4. ???
5. Profit


## Variables
* ELASTIC_USERNAME - Your Elasticsearch username. Default is 'elastic'
* ELASTIC_PASSWORD - Your Elasticsearch password.
* TA_LIBRARY - Your TubeArchivist library folder. No trailing slashes.
* TA_APPDATA - Your TubeArchivist AppData folder. No trailing slashes.
* EXPORT_FOLDER - The folder that you want your exports in. No trailing slashes. Will be created if it doesn't exist.
