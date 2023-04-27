#!/usr/bin/env python
from argparse import ArgumentParser
import eero
from eero.exception import ClientException
import six
import cookie_store

session = cookie_store.CookieStore('session.yml')
eero = eero.Eero(session)

if __name__ == '__main__':
    if eero.needs_login():
        parser = ArgumentParser()
        parser.add_argument("-l", help="your eero login (email address or phone number)")
        args = parser.parse_args()
        if args.l:
            account_info = args.l
        else:
            account_info = six.moves.input('your eero login (email address or phone number): ')
        try:
            user_token = eero.login(account_info)
            verification_code = six.moves.input('verification key from email or SMS: ')
            eero.login_verify(verification_code, user_token)
            print('Session key stored in session.yml')
        except ClientException as cex:
            print('Error: status {}, message {}'.format(cex.status, cex.error_message))
