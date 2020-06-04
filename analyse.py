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
import argparse
import csv
import json
import os

# 3rd party
import ipinfo

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('--results_dir',
                    help='Directory containing Scamper results JSON files',
                    required=True)
parser.add_argument('--ipinfo_key',
                    help='API key for ipinfo.io',
                    required=True)
args = parser.parse_args()

fieldnames = ['Participant ID',
              'Participant City',
              'Participant Country',
              'Connection',
              'Destination',
              'Destination IP',
              'Destination Hostname',
              'Destination ASN',
              'Destination City',
              'Destination Country',
              'Trace Hop Count',
              'Hop 1 IP', 'Hop 1 Hostname', 'Hop 1 RTT', 'Hop 1 ASN', 'Hop 1 City', 'Hop 1 Country',
              'Hop 2 IP', 'Hop 2 Hostname', 'Hop 2 RTT', 'Hop 2 ASN', 'Hop 2 City', 'Hop 2 Country',
              'Hop 3 IP', 'Hop 3 Hostname', 'Hop 3 RTT', 'Hop 3 ASN', 'Hop 3 City', 'Hop 3 Country',
              'Hop 4 IP', 'Hop 4 Hostname', 'Hop 4 RTT', 'Hop 4 ASN', 'Hop 4 City', 'Hop 4 Country',
              'Hop 5 IP', 'Hop 5 Hostname', 'Hop 5 RTT', 'Hop 5 ASN', 'Hop 5 City', 'Hop 5 Country',
              'Hop 6 IP', 'Hop 6 Hostname', 'Hop 6 RTT', 'Hop 6 ASN', 'Hop 6 City', 'Hop 6 Country',
              'Hop 7 IP', 'Hop 7 Hostname', 'Hop 7 RTT', 'Hop 7 ASN', 'Hop 7 City', 'Hop 7 Country',
              'Hop 8 IP', 'Hop 8 Hostname', 'Hop 8 RTT', 'Hop 8 ASN', 'Hop 8 City', 'Hop 8 Country',
              'Hop 9 IP', 'Hop 9 Hostname', 'Hop 9 RTT', 'Hop 9 ASN', 'Hop 9 City', 'Hop 9 Country',
              'Hop 10 IP', 'Hop 10 Hostname', 'Hop 10 RTT', 'Hop 10 ASN', 'Hop 10 City', 'Hop 10 Country',
              'Hop 11 IP', 'Hop 11 Hostname', 'Hop 11 RTT', 'Hop 11 ASN', 'Hop 11 City', 'Hop 11 Country',
              'Hop 12 IP', 'Hop 12 Hostname', 'Hop 12 RTT', 'Hop 12 ASN', 'Hop 12 City', 'Hop 12 Country',
              'Hop 13 IP', 'Hop 13 Hostname', 'Hop 13 RTT', 'Hop 13 ASN', 'Hop 13 City', 'Hop 13 Country',
              'Hop 14 IP', 'Hop 14 Hostname', 'Hop 14 RTT', 'Hop 14 ASN', 'Hop 14 City', 'Hop 14 Country',
              'Hop 15 IP', 'Hop 15 Hostname', 'Hop 15 RTT', 'Hop 15 ASN', 'Hop 15 City', 'Hop 15 Country',
              'Hop 16 IP', 'Hop 16 Hostname', 'Hop 16 RTT', 'Hop 16 ASN', 'Hop 16 City', 'Hop 16 Country',
              'Hop 17 IP', 'Hop 17 Hostname', 'Hop 17 RTT', 'Hop 17 ASN', 'Hop 17 City', 'Hop 17 Country',
              'Hop 18 IP', 'Hop 18 Hostname', 'Hop 18 RTT', 'Hop 18 ASN', 'Hop 18 City', 'Hop 18 Country',
              'Hop 19 IP', 'Hop 19 Hostname', 'Hop 19 RTT', 'Hop 19 ASN', 'Hop 19 City', 'Hop 19 Country']

with open('results.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each of the JSON files, which we assume are Scamper output
    for entry in os.scandir(args.results_dir):
        scamper_filename = entry.path
        print('Processing %s...' % (scamper_filename), end='', flush=True)

        if scamper_filename.endswith('.json'):
            with open(scamper_filename, 'r') as f:
                csv_line = {}
                trace = json.load(f)

                print('filesplit...', end='', flush=True)

                # Parse details from filename
                scamper_filename = scamper_filename.replace(args.results_dir, '')  # Remove directory name
                scamper_filename_split = scamper_filename.split('-')  # Separate components
                # e.g. ['results', 'uk', 'london', '15', 'www.instagram.com', '4g.json']

                csv_line['Participant ID'] = scamper_filename_split[3]
                csv_line['Participant City'] = scamper_filename_split[2]
                csv_line['Participant Country'] = scamper_filename_split[1]
                csv_line['Connection'] = scamper_filename_split[5].replace('.json', '')
                csv_line['Destination'] = scamper_filename_split[4]
                csv_line['Destination IP'] = trace['dst']

                print('destination...', end='', flush=True)

                # Set up ipinfo lookup
                ipinfo_handler = ipinfo.getHandler(args.ipinfo_key)

                # ipinfo lookup: destination IP
                ip_details = ipinfo_handler.getDetails(trace['dst'])

                if hasattr(ip_details, 'hostname'):
                    csv_line['Destination Hostname'] = ip_details.hostname
                else:
                    csv_line['Destination Hostname'] = 'Unknown'

                csv_line['Destination ASN'] = ip_details.org
                csv_line['Destination City'] = ip_details.city
                csv_line['Destination Country'] = ip_details.country_name

                # How many hops?
                hops = trace['hop_count']

                if trace['stop_reason'] == 'GAPLIMIT':
                    hops = hops - 5  # If we hit the gap limit (5), subtract from the total

                csv_line['Trace Hop Count'] = hops

                print('hops...', end='', flush=True)

                # Loop through the hops and query the IP from https://ipinfo.io
                if 'hops' in trace:
                    for hop in trace['hops']:
                        ip_details = ipinfo_handler.getDetails(hop['addr'])
                        hop_number = hop['probe_ttl']

                        csv_line['Hop ' + str(hop_number) + ' IP'] = hop['addr']
                        csv_line['Hop ' + str(hop_number) + ' RTT'] = hop['rtt']

                        if hasattr(ip_details, 'hostname'):
                            csv_line['Hop ' + str(hop_number) + ' Hostname'] = ip_details.hostname
                        else:
                            csv_line['Hop ' + str(hop_number) + ' Hostname'] = 'Unknown'

                        if not hasattr(ip_details, 'bogon'):
                            if hasattr(ip_details, 'org'):
                                csv_line['Hop ' + str(hop_number) + ' ASN'] = ip_details.org
                            if hasattr(ip_details, 'city'):
                                csv_line['Hop ' + str(hop_number) + ' City'] = ip_details.city
                            if hasattr(ip_details, 'country'):
                                csv_line['Hop ' + str(hop_number) + ' Country'] = ip_details.country_name

                writer.writerow(csv_line)
            print ('done')
        else:
            print('skipped')

print('Finished analysis')
