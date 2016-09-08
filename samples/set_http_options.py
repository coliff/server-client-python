####
# This script demonstrates how to set http options. It will set the option
# to not verify SSL certificate, and query all workbooks on site.
#
# For more information, refer to the documentation on 'Publish Workbook'
# (https://onlinehelp.tableau.com/current/api/rest_api/en-us/help.htm)
#
# To run the script, you must have installed Python 2.7.9 or later.
####

import tableauserverapi as TSA
import argparse
import getpass
import logging

parser = argparse.ArgumentParser(description='List workbooks on site, with option set to ignore SSL verification.')
parser.add_argument('--server', '-s', required=True, help='server address')
parser.add_argument('--username', '-u', required=True, help='username to sign into server')
parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                    help='desired logging level (set to error by default)')
args = parser.parse_args()

password = getpass.getpass("Password: ")

# Set logging level based on user input, or error by default
logging_level = getattr(logging, args.logging_level.upper())
logging.basicConfig(level=logging_level)

# Step 1: Create required objects for sign in
tableau_auth = TSA.TableauAuth(args.username, password)
server = TSA.Server(args.server)

# Step 2: Set http options to disable verifying SSL
server.add_http_options({'verify': False})

with server.auth.sign_in(tableau_auth):

    # Step 3: Query all workbooks and list them
    pagination_info, all_workbooks = server.workbooks.get()
    print('{0} workbooks found. Showing {1}:'.format(pagination_info.total_available, pagination_info.page_size))
    for workbook in all_workbooks:
        print('\t{0} (ID: {1})'.format(workbook.name, workbook.id))