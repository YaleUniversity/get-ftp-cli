#!/usr/bin/env python

from __future__ import print_function

import optparse
import re
from bs4 import BeautifulSoup

def ftp_profile(publish_settings):
  """Takes PublishSettings, extracts ftp user, password, and host"""
  soup = BeautifulSoup(publish_settings, 'html.parser')

  profiles = soup.find_all('publishprofile')
  ftp_profile = [profile for profile in profiles if profile['publishmethod'] == 'FTP'][0]

  matches = re.search('ftp://(.+)/site/wwwroot', ftp_profile['publishurl'])

  host = matches.group(1) if matches else ''

  username = ftp_profile['username'].replace("\\$", "%5C%24")
  password = ftp_profile['userpwd']
  return host, username, password, ftp_profile['publishurl']

def default_db_connection(publish_settings):
  """"Takes PublishSettings looks for Azure default db connection, returns default db connection string for local environment and SQL to add user to local db"""
  
  username, password = '', ''
  soup = BeautifulSoup(publish_settings, 'html.parser')
  connections = soup.find_all('add')
  regex = 'Database=(.+);Data Source=(.+);User Id=(.+);Password=(.+)'
  db_connection = [conn for conn in connections if conn['name'] == 'defaultConnection'][0]
  matches = re.search(regex, db_connection['connectionstring'])
  if matches:
    username = matches.group(3)
    password = matches.group(4)
  return username, password

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
    db_user, db_passwd = default_db_connection(contents)
    print('')
    print('Execute the following command to connect to the Azure FTP:')
    print('----------------------------------------------------------')
    print('ftp ftp://{}:{}@{}'.format(ftp_username, ftp_password, ftp_host))
    print('')
    print('Execute the following command to put the contents of a directory to the Azure website:')
    print('----------------------------------------------------------')
    print('wput $HOME/Sites/[appdir]/* ftp://{}:{}@{}/'.format(ftp_username, ftp_password, publish_url))
    print('')
    print('Append the following line to `./httpd.conf`. (Substitute correct [Local_DB_Name]:')
    print('----------------------------------------------------------')
    print(
      '''SetEnv MYSQLCONNSTR_defaultConnection "Database=[Local_DB_Name];Data Source=localhost;User Id={};Password={}"'''.format(db_user, db_passwd))
    print('')
    print('Execute the following command to add the user to the local MySQL database:')
    print('----------------------------------------------------------')
    print(
      '''mysql -u root -p -e "GRANT ALL PRIVILEGES ON *.* TO '{}'@'localhost' IDENTIFIED BY '{}';"'''.format(db_user, db_passwd))
    print('')
  else:
    p.print_help()

if __name__ == '__main__':
  main()
