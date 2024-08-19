

# MULTICAST-CHECKER


## Overview

The **MULTICAST-CHECKER** is a Python3-compatible script designed to monitor the availability of UDP and RTP channels listed in an M3U playlist. The script leverages [FFmpeg](https://www.ffmpeg.org/ffmpeg.html) and [FFprobe](https://ffmpeg.org/ffprobe.html) for handling media streams and generates detailed reports on channel status.

## Prerequisites

Before using the script, ensure the following are installed:

1. [Python 3.x](https://www.python.org/downloads/)
2. [FFmpeg/FFprobe](https://www.ffmpeg.org/download.html)

## Getting Started

### Testing a Playlist

You can run the **MULTICAST-CHECKER** script to test all channels in a playlist using the following command:

```shell
python3 multicast-checker.py --playlist playlist.m3u --report report.csv
```

Where `playlist.m3u` is an [M3U](https://en.wikipedia.org/wiki/M3U) file containing the UDP/RTP channels you want to check, and `report.csv` is the output report file.

### Testing a Single UDP Link

To test a single UDP link, use:

```shell
python3 multicast-checker.py --link udp://@233.99.65.1:1234 --report report.csv
```

### Testing a Single RTP Link

To test a single RTP link, use:

```shell
python3 multicast-checker.py --rtp_link rtp://@233.99.65.1:1234 --report report.csv
```

### Sending a Report via Email

You can automatically send the report to an email address:

```shell
python3 multicast-checker.py --playlist playlist.m3u --report report.csv --email recipient@example.com --email_sender your_email@example.com --email_password your_email_password
```

### Command-Line Arguments

- `--playlist`: Path to M3U playlist file containing UDP streams.
- `--rtp_playlist`: Path to M3U playlist file containing RTP streams.
- `--link`: A single UDP link to test.
- `--rtp_link`: A single RTP link to test.
- `--all`: Test all URLs in the specified M3U playlist file.
- `--report`: Generate a CSV report.
- `--email`: Send the generated report to the specified email address.
- `--email_sender`: Email address to send the report from (required if sending via email).
- `--email_password`: Password for the sender's email address (required if sending via email).
- `--info`: Contact information.

### Example of an M3U File

```plaintext
#EXTM3U
#EXTINF:2,Info channel #1
udp://@233.99.65.1:1234
#EXTINF:2,Info channel #2
rtp://@233.99.65.2:5500
```



### Report Example

The script can generate a CSV report with the following fields:

- **timestamp**: Date and time when the link was tested.
- **channel_name**: Name of the channel as specified in the M3U file.
- **link**: The tested UDP/RTP link.
- **protocol**: The protocol used (UDP/RTP).
- **status**: Result of the test (Working/Failed).
- **error_message**: Description of any errors encountered.

### Initial Configuration

You can display all the available parameters for the script using:

```shell
python3 multicast-checker.py -h
```

## Features

- **Multicast Monitoring**: Check the availability of UDP and RTP channels listed in an M3U playlist.
- **Multithreaded Execution**: The script scans channels using multithreading to ensure faster results.
- **Email Integration**: Automatically send the test report to a specified email address.
- **Service Name Metadata Capture**: Retrieves the service_name metadata field from the UDP/RTP stream.

## Contributing

The **MULTICAST-CHECKER** project was initially developed to monitor an ISP's IPTV network and send alerts in case of channel outages. Contributions, suggestions, and feedback are welcome to help improve the tool further.

## Links

- **Project Homepage**: [MULTICAST-CHECKER GitHub Repository](https://github.com/kideas11/Udp_playlist_checker)
- **Issue Tracker**: [Report Issues](https://github.com/kideas11/Udp_playlist_checker/issues)

### References

- [FFmpeg/FFprobe](https://github.com/FFmpeg/FFmpeg)
- [UDP Multicast Addresses](https://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml)
- [Subnet Calculator](https://www.davidc.net/sites/default/subnets/subnets.html)

## Licensing

This project is licensed under the GPL-3.0 license.

