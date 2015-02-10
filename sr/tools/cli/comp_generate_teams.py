from __future__ import print_function
import argparse
import sys
import json
import yaml

from six.moves.urllib.parse import urljoin
from six.moves.urllib.request import urlopen

def command(args):
    root_uri = urljoin(args.server, 'teams-data.php')
    team_data = json.load(urlopen(root_uri))
    output_database = {}
    for tla, data in team_data.items():
        if u'team_name' in data:
            name = data[u'team_name']
        else:
            name = data[u'college'][u'name']
        output_database[tla.encode('utf-8')] = {'name': name.encode('utf-8')}
    yaml.dump({'teams': output_database},
              args.output,
              default_flow_style=False)

def add_subparser(subparsers):
    parser = subparsers.add_parser('comp-generate-teams',
                                   help='Generate teams.yaml from srweb')
    parser.add_argument('--server',
                        type=str,
                        default='https://www.studentrobotics.org/',
                        help='srweb root from which to load data')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='teams.yaml file to write to')
    parser.set_defaults(func=command)

