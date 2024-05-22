# :rainbow::rainbow::rainbow: MULTICAST-CHECKER :rainbow::rainbow::rainbow:

> YOUR USAGE OF THE SCRIPTS IS AT YOUR OWN RISK
## Installing / Getting started

Script is python3 compatible and use [FFprobe](https://ffmpeg.org/ffprobe.html) and [FFmpeg](https://www.ffmpeg.org/ffmpeg.html)

Please install before use: 

1. https://www.python.org/downloads/
2. https://www.ffmpeg.org/download.html

You can simply run the following examples to see how it works:

### **multicast-checker.py:**
```shell
python3 multicast-checker.py --playlist playlist.m3u
```
where *playlist.m3u* is a [M3U](https://en.wikipedia.org/wiki/M3U) file where all the UDP channels are listed

M3U file example:
```
#EXTM3U
#EXTINF:2,Info channel #1
udp://@233.99.65.1:1234
#EXTINF:2,Info channel #2
udp://@233.99.65.2:5500
#EXTINF:2,Info channel #3
udp://@233.99.65.3:1234
#EXTINF:2,Info channel #4
udp://@233.99.65.4:5500
```

The script will scan all the schannels in the playlist.m3u using multithreading and return the results
The service_name metadata field from the UDP stream will be captured in advance.

Output example:
```
Channel: Info channel #1 - UDP link udp://@233.99.65.1:1234 failed: Timeout. Make sure the server is running and reachable.
Channel: Info channel #2 - UDP link udp://@233.99.65.2:5500 is working.
Channel: Info channel #3 - UDP link udp://@233.99.65.3:1234 is working.
Channel: Info channel #4 - UDP link udp://@233.99.65.4:5500 is working.


[*] Finished in 7.0 second(s)
```

Scripts were tested on Windows (Windows 10 pro)


### Initial Configuration

You can find all the parameters of the scripts using the following:

```
python3 multicast-checker.py -h

--playlist         "Playlist *.m3u file with UDP streams"             required: True
```

```

## Features

* checking the availability of the UDP channels;


## Contributing

The **multicast_checker.py** project was created as a tool to monitor the ISP IPTV network and sent the alerts in case of channels outages.

Please feel free to comment/blame/suggest the further development

## Links

- Project homepage: https://github.com/kideas11/Udp_playlist_checker
- Issue tracker: https://github.com/kideas11/Udp_playlist_checker/issues

Data used:
- FFmpeg/FFprobe: https://github.com/FFmpeg/FFmpeg
- UDP Multicast: https://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml
- Subnets division: https://www.davidc.net/sites/default/subnets/subnets.html

## Licensing

The code in this project is licensed under  GPL-3.0 license
