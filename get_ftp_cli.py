#!/usr/bin/env python

from __future__ import print_function

import optparse
import re
from bs4 import BeautifulSoup

def main():
  """Executes program and handles options"""

  p = optparse.OptionParser(
    description='Parses MS Azure PublishSettings file and eturns properly formatted CLI for use with Unix ftp command',
    prog='get_ftp_cli',
    version='%prog 1.0.0',
    usage='%prog [path/to/*.PublishSettings]')

  options, arguments = p.parse_args()
  
  if len(arguments) == 1:
    infile = open(arguments[0], 'r')
    contents = infile.read()

    soup = BeautifulSoup(contents, 'html.parser')

    profiles = soup.find_all('publishprofile')
    ftp_profile = [profile for profile in profiles if profile['publishmethod'] == 'FTP'][0]

    matches = re.search('ftp://(.+)/site/wwwroot', ftp_profile['publishurl'])

    ftp_host = matches.group(1) if matches else ''

    ftp_username = ftp_profile['username'].replace("\\$", "%5C%24")
    ftp_password = ftp_profile['userpwd']

    print('Execute the following command to connect to the Azure FTP:')
    print("==========================================================")
    print('ftp ftp://{}:{}@{}'.format(ftp_username, ftp_password, ftp_host))
    print("==========================================================")
  else:
    p.print_help()

if __name__ == '__main__':
  main()
