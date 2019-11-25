
# Based on the python script by Laurens Houben
#   Example response for blup@blup.com:
#   [{"Title":"Adobe","Name":"Adobe","Domain":"adobe.com","BreachDate":"2013-10-04","AddedDate":"2013-12-04T00:00:00Z","PwnCount":152445165,"Description":"In October 2013, 153 million Adobe accounts were breached with each containing an internal ID, username, email, <em>encrypted</em> password and a password hint in plain text. The password cryptography was poorly done and <a href=\"http://stricture-group.com/files/adobe-top100.txt\" target=\"_blank\" rel=\"noopener\">many were quickly resolved back to plain text</a>. The unencrypted hints also <a href=\"http://www.troyhunt.com/2013/11/adobe-credentials-and-serious.html\" target=\"_blank\" rel=\"noopener\">disclosed much about the passwords</a> adding further to the risk that hundreds of millions of Adobe customers already faced.","DataClasses":["Email addresses","Password hints","Passwords","Usernames"],"IsVerified":true,"IsSensitive":false,"IsActive":true,"IsRetired":false,"IsSpamList":false,"LogoType":"svg"},{"Title":"Xbox-Scene","Name":"Xbox-Scene","Domain":"xboxscene.com","BreachDate":"2015-02-01","AddedDate":"2016-02-07T20:26:56Z","PwnCount":432552,"Description":"In approximately February 2015, the Xbox forum known as <a href=\"http://xboxscene.com/\" target=\"_blank\" rel=\"noopener\">Xbox-Scene</a> was hacked and more than 432k accounts were exposed. The IP.Board forum included IP addresses and passwords stored as salted hashes using a weak implementation enabling many to be rapidly cracked.","DataClasses":["Email addresses","IP addresses","Passwords","Usernames"],"IsVerified":true,"IsSensitive":false,"IsActive":true,"IsRetired":false,"IsSpamList":false,"LogoType":"png"}]
# -

import requests
import time
import argparse

parser = argparse.ArgumentParser(description="Verify if email address has been pwned")
parser.add_argument("-a", dest="address",
                  help="Single email address to be checked")
parser.add_argument("-f", dest="filename",
                  help="File to be checked with one email addresses per line")
args = parser.parse_args()

rate = 1.3                            # 1.3 seconds is a safe value that in most cases does not trigger rate limiting
server = "haveibeenpwned.com"         # Website to contact
sslVerify = True                      # Verify server certificate (set to False when you use a debugging proxy like BurpSuite)
proxies = {                           # Proxy to use (debugging)
#  'http': 'http://127.0.0.1:8080',    # Uncomment when needed
#  'https': 'http://127.0.0.1:8080',   # Uncomment when needed
}

# Set terminal ANSI code colors
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAILRED = '\033[91m'
ENDC = '\033[0m'

address = str(args.address)
filename = str(args.filename)
lstEmail = ["info@example.com","example@example.com"]

def main():
    if address != "None":
        checkAddress(address)
    elif filename != "None":
        email = [line.rstrip('\n') for line in open(filename)] # strip the newlines
        for email in email:
            checkAddress(email)
    else:
        for email in lstEmail:
            checkAddress(email)

def checkAddress(email):
    sleep = rate # Reset default acceptable rate
    # API request here
    # Now the API must be paid, unlucky but at least we have the script, add the key if you want, paiddude
    check = requests.get("https://haveibeenpwned.com/api/v3/" + email + "/" +"?includeUnverified=true",
                 proxies = proxies,
                 verify = sslVerify)
    if str(check.status_code) == "404":
        print check.status_code
        print OKGREEN + "[i] " + email + " has not been breached." + ENDC
        time.sleep(sleep)
        return False
    elif str(check.status_code) == "200":
        print FAILRED + "[!] " + email + " has been breached!" + ENDC
        time.sleep(sleep)
        return True
    elif str(check.status_code) == "429":
        print WARNING + "[!] Rate limit exceeded, server instructed us to retry after " + check.headers['Retry-After'] + " seconds" + ENDC
        print WARNING + "    Refer to acceptable use of API: https://haveibeenpwned.com/API/v2#AcceptableUse" + ENDC
        sleep = float(check.headers['Retry-After'])
        time.sleep(sleep)
        checkAddress(email)
    else:
        print str(check.status_code)
        print WARNING + "[!] Something went wrong while checking " + email + ENDC
        time.sleep(sleep)
        return True

if __name__ == "__main__":
    main()
