# -*- coding: utf-8 -*-

### Imports ###
import sys                  # getdefaultencoding, getfilesystemencoding, platform, argv
import os                   # path.abspath, join, dirname
import re                   #
import inspect              # getfile, currentframe
import urllib2              #


###Mini Functions ###
def natural_sort_key     (s):  return [int(text) if text.isdigit() else text for text in re.split(re.compile('([0-9]+)'), str(s).lower())]  ### Avoid 1, 10, 2, 20... #Usage: list.sort(key=natural_sort_key), sorted(list, key=natural_sort_key)
def sanitize_path        (p):  return p if isinstance(p, unicode) else p.decode(sys.getfilesystemencoding()) ### Make sure the path is unicode, if it is not, decode using OS filesystem's encoding ###

### Get media directory ###
def GetMediaDir (media, movie, file=False):
  if movie:  return os.path.dirname(media.items[0].parts[0].file)
  else:
    for s in media.seasons if media else []: # TV_Show:
      for e in media.seasons[s].episodes:
        Log.Info(media.seasons[s].episodes[e].items[0].parts[0].file)
        return media.seasons[s].episodes[e].items[0].parts[0].file if file else os.path.dirname(media.seasons[s].episodes[e].items[0].parts[0].file)

def SearchTubeArchivist(type, id):
  Log(u"SearchTubeArchivist() - path: {}, key: {}".format(Prefs['TubeArchivist_url']+"/api/"+type+"/"+id, Prefs['TubeArchivist_api_key']))
  request = urllib2.Request(Prefs['TubeArchivist_url']+"/api/"+type+"/"+id, headers={"Authorization" : "Token "+Prefs['TubeArchivist_api_key']})
  contents = urllib2.urlopen(request).read()
  return JSON.ObjectFromString(contents)['data']

def GetTubeArchivistImage(url):
  Log(u"GetTubeArchivistImage() - path: {}, key: {}".format(Prefs['TubeArchivist_url']+"/"+url, Prefs['TubeArchivist_api_key']))
  request = urllib2.Request(Prefs['TubeArchivist_url']+"/"+url, headers={"Authorization" : "Token "+Prefs['TubeArchivist_api_key']})
  return urllib2.urlopen(request).read()

def Start():
  HTTP.CacheTime                  = CACHE_1MONTH
  HTTP.Headers['User-Agent'     ] = 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.54'
  HTTP.Headers['Accept-Language'] = 'en-us'

### Assign unique ID ###
def Search(results, media, lang, manual, movie):  
  filename    = media.filename or media.show
  try:                    filename = sanitize_path(filename)
  except Exception as e:  Log('search() - Exception1: filename: "{}", e: "{}"'.format(filename, e))
  try:                    filename = os.path.basename(filename)
  except Exception as e:  Log('search() - Exception2: filename: "{}", e: "{}"'.format(filename, e))
  try:                    filename = urllib2.unquote(filename)
  except Exception as e:  Log('search() - Exception3: filename: "{}", e: "{}"'.format(filename, e))

  video_id = os.path.basename(filename).rsplit('.', 1)[0]
  video_info = SearchTubeArchivist('video', video_id)

  Log(u"Search() - video_id: {}, title: {}, published: {}".format(video_id, video_info['title'], video_info['published']))
  
  results.Append( MetadataSearchResult( id='tubearchivist|{}'.format(video_id), name=video_info['title'], year=Datetime.ParseDate(video_info['published']).year, score=100, lang=lang ) )
  
  Log(''.ljust(157, '='))


def Update(metadata, media, lang, force, movie):
  dir = sanitize_path(GetMediaDir(media, movie))
    
  folder_name = os.path.basename(dir)
  metadata.studio = 'YouTube'

  if folder_name.startswith('UC') or folder_name.startswith('HC'): 
    for s in sorted(media.seasons, key=natural_sort_key):    
      episodes = 1
      for e in sorted(media.seasons[s].episodes, key=natural_sort_key):
        filename  = os.path.basename(media.seasons[s].episodes[e].items[0].parts[0].file)
        episode   = metadata.seasons[s].episodes[e]
        file_name = os.path.basename(filename).rsplit('.', 1)[0]
        video_info = SearchTubeArchivist('video', file_name)

        if episodes == 1:
          metadata.title = sanitize_path(video_info['channel']['channel_name']);                    Log.Info('[S] title:    "{}"'.format(video_info['channel']['channel_name']))
          metadata.summary = sanitize_path(video_info['channel']['channel_description']);           Log.Info('[S] summary:    "{}"'.format(video_info['channel']['channel_description']))
          metadata.posters["poster"] = Proxy.Media(GetTubeArchivistImage(video_info['channel']['channel_tvart_url']))

        episode.absolute_index          = episodes;   
        episode.index                   = episodes;                                                 Log.Info('[E] index:    "{}"'.format(episodes))
        episode.title                   = sanitize_path(video_info['title']);                       Log.Info('[E] title:    "{}"'.format(video_info['title']))
        episode.summary                 = sanitize_path(video_info['description']);                 Log.Info('[E] summary:  "{}"'.format(video_info['description'].replace('\n', '. ')))
        episode.originally_available_at = Datetime.ParseDate(video_info['published']).date();       Log.Info('[E] date:     "{}"'.format(video_info['published']))
        episode.duration                = video_info['player']['duration']*1000;                    Log.Info('[E] duration:    "{}"'.format(video_info['player']['duration']))
        episode.thumbs["thumbnail"]     = Proxy.Media(GetTubeArchivistImage(video_info['vid_thumb_url']))

        episodes += 1

class TubeArchivistSeries(Agent.TV_Shows):
  name, primary_provider, fallback_agent, contributes_to, accepts_from, languages = 'TubeArchivist Series', True, None, None, ['com.plexapp.agents.localmedia'], [Locale.Language.NoLanguage]
  def search (self, results,  media, lang, manual):  Search (results,  media, lang, manual, False)
  def update (self, metadata, media, lang, force ):  Update (metadata, media, lang, force,  False)

### Variables ###
PluginDir                = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), "..", ".."))
PlexRoot                 = os.path.abspath(os.path.join(PluginDir, "..", ".."))
CachePath                = os.path.join(PlexRoot, "Plug-in Support", "Data", "com.plexapp.agents.tubearchivist", "DataItems")