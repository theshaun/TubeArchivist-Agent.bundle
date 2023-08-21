# TubeArchivist-Agent.bundle: Plex TV Series library agent

This is a simple Plex Agent for showing videos downloaded via Tube Archivist in Plex.
It expects folders and file names to be the default format from Tube Archivist (raw identifiers)

Issues:
 - Currently it only supports channels, playlists may be added later.
 - Episode ordering is all over the place

Installation
============

The plugin code needs to be put into `Plex Media Server/Plug-ins` folder:
- https://support.plex.tv/articles/201187656-how-do-i-manually-install-a-plugin/

Here is how to find the Plug-in folder location:
- https://support.plex.tv/articles/201106098-how-do-i-find-the-plug-ins-folder/

Plex main folder location could be one of:

    * '%LOCALAPPDATA%\Plex Media Server\'                                        # Windows Vista/7/8
    * '%USERPROFILE%\Local Settings\Application Data\Plex Media Server\'         # Windows XP, 2003, Home Server
    * '$HOME/Library/Application Support/Plex Media Server/'                     # Mac OS
    * '$PLEX_HOME/Library/Application Support/Plex Media Server/',               # Linux
    * '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/', # Debian,Fedora,CentOS,Ubuntu
    * '/usr/local/plexdata/Plex Media Server/',                                  # FreeBSD
    * '/usr/pbi/plexmediaserver-amd64/plexdata/Plex Media Server/',              # FreeNAS
    * '${JAIL_ROOT}/var/db/plexdata/Plex Media Server/',                         # FreeNAS
    * '/c/.plex/Library/Application Support/Plex Media Server/',                 # ReadyNAS
    * '/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/',        # QNAP
    * '/volume1/Plex/Library/Application Support/Plex Media Server/',            # Synology, Asustor
    * '/raid0/data/module/Plex/sys/Plex Media Server/',                          # Thecus
    * '/raid0/data/PLEX_CONFIG/Plex Media Server/'                               # Thecus Plex community

To obtain the code:
1. Download the Zip file: https://github.com/theshaun/TubeArchivist-Agent.bundle/archive/refs/heads/master.zip
1. Unpack the downloaded Zip and rename the contents as `TubeArchivist-Agent.bundle` (remove `-master`)
1. Place it inside `Plug-ins` folder
1. Restart Plex Media Server to make sure that the new plugin will be loaded.

To enable for Library:
1. Create a new (or update an existing) library
2. Choose `Manage Library` -> `Edit`
3. Click on the `Advanced` tab, select the scanner `Plex Series Scanner` and then select the Agent: `Tube Archivist Series`
4. Fill in your Tube Archivist details
5. Select Hide on Seasons to hide the Seasons folder

History
=======

Based code structure from [@ZeroQI]'s `YouTube-Agent.bundle` agent.
