from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import shutil
import os
import json
from pathvalidate import sanitize_filepath

# Elasticsearch login credentials. Default username is 'elastic'
ELASTIC_USERNAME = ''
ELASTIC_PASSWORD = ''

# Your TubeArchivist library and appdata folders. No trailing slashes.
TA_LIBRARY = ''
TA_APPDATA = ''

# Folder you want the exported videos in. No trailing slashes.
EXPORT_FOLDER = ''

# Shouldn't need to change anything here unless you're running Elasticsearch on a port other than the default.
# Note that this script much be run locally on the machine that is hosting TubeArchivist and Elasticsearch.
client = Elasticsearch('http://localhost:9200', basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD))

# Creates the base export folder set by user.
os.makedirs(EXPORT_FOLDER, exist_ok=True)

# Checks if there is already an archive file present and reads from it if there is.
# Archive file is a record of any videos which have already been exported. These are skipped to save time.
if os.path.isfile('./archive.txt'):
    with open('./archive.txt', 'r') as file:
        archive = file.readlines()
else:
    archive = ''

# Loads all video results into a list to prevent Elasticsearch timeouts while doing large copy operations.
videos_list = []
for vid in scan(client, index='ta_video'):
    videos_list.append(vid)

# Main loop that handles all the video, thumbnail, info and subtitle files.
for a in videos_list:
    sourcevid = '{}/{}'.format(TA_LIBRARY, a['_source']['media_url'])
    sourcethumb = '{}/videos/{}/{}.jpg'.format(TA_APPDATA, a['_source']['youtube_id'][0].lower(), a['_source']['youtube_id'])
    
    destfolder = sanitize_filepath(f"{a['_source']['channel']['channel_name']} [{a['_source']['channel']['channel_id']}]/{a['_source']['published']} {a['_source']['title'].replace('/', '').replace(':', '')}")
    destvid = sanitize_filepath(f"{a['_source']['title'].replace('/', '').replace(':', '')} [{a['_source']['youtube_id']}].mp4")
    destthumb = sanitize_filepath(f"{a['_source']['title'].replace('/', '').replace(':', '')} [{a['_source']['youtube_id']}]-thumb.jpg")
    destjson = sanitize_filepath(f"{a['_source']['title'].replace('/', '').replace(':', '')} [{a['_source']['youtube_id']}].info.json")
    destsub = sanitize_filepath(f"{a['_source']['title'].replace('/', '').replace(':', '')} [{a['_source']['youtube_id']}].en.vtt")
    json_data = a['_source']

    os.makedirs(f'{EXPORT_FOLDER}/{destfolder}', exist_ok=True)
    
    # Checks if id of current video is in the archive and skips if it is.
    if a['_source']['youtube_id']+'\n' not in archive:
        shutil.copyfile(sourcevid, f'{EXPORT_FOLDER}/{destfolder}/{destvid}')
        shutil.copyfile(sourcethumb, f'{EXPORT_FOLDER}/{destfolder}/{destthumb}')
        
        with open(f'{EXPORT_FOLDER}/{destfolder}/{destjson}', 'w') as jfile:
            json.dump(json_data, jfile)    
            
        if 'subtitles' in a['_source'] and a['_source']['subtitles'] != []:
            sourcesub = '{}/{}'.format(TA_LIBRARY, a['_source']['subtitles'][0]['media_url'])
            shutil.copyfile(sourcesub, f'{EXPORT_FOLDER}/{destfolder}/{destsub}')
            
        with open('archive.txt', 'a') as file:
            file.write(a['_source']['youtube_id']+'\n')
            
        print(f"{a['_source']['youtube_id']} exported and recorded in archive.")
    else:
        print(f"{a['_source']['youtube_id']} already exported, skipping...")
