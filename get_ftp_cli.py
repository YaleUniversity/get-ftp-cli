#!/usr/bin/env python

from __future__ import print_function

import optparse
import re
from bs4 import BeautifulSoup

def ftp_profile(publish_settings):
  """Takes PublishSettings, extracts ftp user and password, returns ftp command"""
  soup = BeautifulSoup(publish_settings, 'html.parser')

  profiles = soup.find_all('publishprofile')
  ftp_profile = [profile for profile in profiles if profile['publishmethod'] == 'FTP'][0]

  matches = re.search('ftp://(.+)/site/wwwroot', ftp_profile['publishurl'])

  host = matches.group(1) if matches else ''

  username = ftp_profile['username'].replace("\\$", "%5C%24")
  password = ftp_profile['userpwd']
  return host, username, password, ftp_profile['publishurl']

def main():
  """Executes program and handles options"""

  p = optparse.OptionParser(
    description='Parses MS Azure PublishSettings file and eturns properly formatted CLI for use with Unix ftp command',
    prog='get_ftp_cli',
    version='%prog 1.0.1',
    usage='%prog [path/to/*.PublishSettings]')

  options, arguments = p.parse_args()
  
  if len(arguments) == 1:
    infile = open(arguments[0], 'r')
    contents = infile.read()

    ftp_host, ftp_username, ftp_password, publish_url = ftp_profile(contents)
    print("")
    print('Execute the following command to connect to the Azure FTP:')
    print("")
    print('ftp ftp://{}:{}@{}'.format(ftp_username, ftp_password, ftp_host))
    print("")
    print('Execute the following command to put the contents of a directory to the Azure website:')
    print("")
    print('wput $HOME/Sites/[appdir]/* ftp://{}:{}@{}/'.format(ftp_username, ftp_password, publish_url))
    print("")
  else:
    p.print_help()

if __name__ == '__main__':
  main()
