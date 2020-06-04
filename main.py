# Traceroute Collector
#
# This code packages the methodology for my Environmental Technology MSc
# thesis at Imperial College London so that the required traceroute data
# can be collected from volunteers as easily as possible.
#
# Copyright (C) 2020 David Mytton <david@davidmytton.co.uk>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# System
from urllib.parse import urlparse
from urllib.request import urlopen
import argparse
import fileinput
import json
import os
import socket
import ssl
import subprocess

# 3rd party
import youtube_dl

# scamper needs root
if os.geteuid() != 0:
    exit('You must run this with sudo')

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('--connection',
                    help='Specify connected over wifi or 4g',
                    required=True)
parser.add_argument('--ipinfo_key', help='No longer used')
args = parser.parse_args()

if args.connection == 'wifi':
    connection = 'wifi'
elif args.connection == '4g':
    connection = '4g'
else:
    exit('You must specify a value for --connection as either wifi or 4g')


def runTest(video_url):
    video_url_parsed = urlparse(video_url)

    filename = '%s-%s' % (video_url_parsed.netloc, connection)
    print('---')
    print(filename)
    print('---')
    print('Discovering CDN URL...', end='', flush=True)

    # Get the CDN URL using youtube-dl in simulation mode
    ydl = youtube_dl.YoutubeDL({'quiet': True,
                                'nocheckcertificate': True})  # Older macOS don't have up to date certs

    with ydl:
        result = ydl.extract_info(
            video_url,
            download=False  # We just want to extract the info
        )
    video = result

    # Parse the URL from the response
    if video_url_parsed.netloc == 'www.youtube.com':
        cdn_url = urlparse(video['formats'][0]['url'])
    elif video_url_parsed.netloc == 'www.instagram.com':
        cdn_url = urlparse(video['entries'][0]['url'])
    else:
        print(video)
        exit('Unknown content type')

    print('done:', (cdn_url.netloc))

    # Look up the IP from the hostname
    print('Looking up CDN IP...', end='', flush=True)
    cdn_ip = socket.getaddrinfo(cdn_url.netloc,
                                443,
                                proto=socket.IPPROTO_TCP)

    # Extract the IP with a list comprehension
    cdn_ip = [x[4] for x in cdn_ip]
    cdn_ip = [x[0] for x in cdn_ip]
    cdn_ip = cdn_ip[0]
    print('done:', (cdn_ip))

    # Run scamper
    print('Running scamper trace (may take a few minutes)...',
          end='',
          flush=True)
    scamper_filename = 'scamper-%s.json' % (filename)
    subprocess.run(['./scamper',
                    '-O', 'json',
                    '-o', scamper_filename,
                    '-i', cdn_ip],
                   stdout=subprocess.PIPE)
    print('done')

    # scamper will dump a json object per line
    # We're only interested in the trace line, so skip the others
    for line in fileinput.input([scamper_filename]):
        try:
            json_line = json.loads(line)
            if json_line['type'] == 'trace':
                trace = json_line
            else:
                pass
        except Exception:
            pass

    # Get my public IP so it can be redacted from the trace
    print('Redacting source IPs...', end='', flush=True)

    # Opt out of cert verification
    # Some participants have very old macOS versions which error when trying
    # to verify HTTPS certs. Disable the check.
    # https://www.python.org/dev/peps/pep-0476/
    context = ssl._create_unverified_context()
    # Source: https://stackoverflow.com/a/9481595
    # jsonip.com is the only one that properly provides the IPv4/IPv6 address
    my_ip = json.load(urlopen('https://jsonip.com', context=context))['ip']

    # Redact source IP from JSON
    if trace['src'] == my_ip:
        trace['src'] = 'REDACTED'

    # Loop through each hop and ensure the source IP is redacted if necessary
    for index, hop in enumerate(trace['hops']):
        if hop['addr'] == my_ip:
            hop['addr'] = 'REDACTED'
            trace['hops'][index]['addr'] = 'REDACTED'

    # Save the results trace
    results_filename = 'results-%s.json' % (filename)
    with open(results_filename, 'w', encoding='utf-8') as f:
        json.dump(trace, f, ensure_ascii=False, indent=4)

    # Remove the original results file
    try:
        os.remove(scamper_filename)
    except OSError:
        pass

    print('done')

    print('Finished test')


runTest('https://www.youtube.com/watch?v=kJQP7kiw5Fk')
runTest('https://www.instagram.com/p/B5vhf4innBN/')
