#!/usr/bin/env python 
# encoding: utf-8
#====================================================================
# Name        :  citeulike.py
# Version    :  0.1a
# Author      :  Lampros Mountrakis (L.Mountrakis hosted-at gmail.com )
# Date        : 
# Description : 
#====================================================================
import os
import sys
import json
import urllib2

""" 
downloadFile(url, cookie=cookie) -> DataInBinaryString
    Downloads the contents of the given url

getCiteULikeCookie() -> CookieString
    Gets the cookie from firefox  

getCiteULikeJSON(user='user') -> DICTrefs
    Retrieves the JSON list from CiteULike and returns dict structure 
    based on the citation key. Does not require a cookie.
"""

def downloadFile(url, cookie=None):
    """ 
    Downloads the contents of the given url
        downloadFile(url, cookie=cookie) -> DataInBinaryString
    """
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    if cookie:
        opener.addheaders.append(('Cookie', cookie))
    return opener.open(url).read()

def getCiteULikeCookie():
    """   
    Gets the cookie from firefox  
        getCiteULikeCookie() -> CookieString
    """
    if sys.platform=='darwin':
        cookies='~/Library/Application\ Support/Firefox/Profiles/*.default/cookies.sqlite'
    else:
        cookies="~/.mozilla/firefox/*.default/cookies.sqlite"
    cmd="""echo ".mode tabs
    select host, case when host glob '.*' then 'TRUE' else 'FALSE' end, path,
    case when isSecure then 'TRUE' else 'FALSE' end, expiry, name, value
    from moz_cookies;" | sqlite3 """ + cookies + """ | grep -i citeulike | grep 'login' | grep -v 'login_perm' | awk '{print $7, $8, $9}'"""
    cookie = "login="+os.popen(cmd).read()[:-1]
    return cookie

def citeULikeKeys(refs):
    """ 
    Retrieves json output and returns a dict structure based on the citation key
        citeULikeKeys(JSONrefs) -> DICTrefs
    """
    cul_dict = {}
    for ref in refs:
        refKey = ref['citation_keys'][-1]
        if refKey == None:
            refKey = ref['citation_keys'][-2]
        cul_dict[refKey] = ref
    return cul_dict

def getCiteULikeJSON(user='user', cookie=None):
    """
    Retrieves the JSON list from CiteULike and returns dict structure 
    based on the citation key. Does not require a cookie.
        getCiteULikeJSON(user='user') -> DICTrefs
    """
    url = 'http://www.citeulike.org/json/user/'+user
    if cookie==None:
        cookie = getCiteULikeCookie()
    jsontext = downloadFile(url, cookie)
    return json.loads(jsontext)

def getCiteULikeDictionary(user='user', cookie=None):
    """
    Retrieves the JSON list from CiteULike and returns dict structure 
    based on the citation key. Does not require a cookie.
        getCiteULikeDictionary(user='user') -> DICTrefs
    """
    return citeULikeKeys(getCiteULikeJSON(user, cookie))

def getCiteULikeBibTeX(user='user', cookie=None):
    """
    Retrieves the BibTeX file from CiteULike and returns a
    string with the contents. Does not require a cookie.
        getCiteULikeBibTeX(user='user') -> string
    """
    url = 'http://www.citeulike.org/bibtex/'+user
    if cookie==None:
        cookie = getCiteULikeCookie()
    return downloadFile(url, cookie)

def getCiteULikeJSONFile(user='user', cookie=None):
    """
    Retrieves the JSON file from CiteULike and returns a
    string with the contents. Does not require a cookie.
        getCiteULikeJSONFile(user='user') -> string
    """
    url = 'http://www.citeulike.org/json/user/'+user
    if cookie==None:
        cookie = getCiteULikeCookie()
    return downloadFile(url, cookie)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Simple CiteULike operations. Access granded through Firefox cookies.')
    parser.add_argument('-u', '--user', dest='user', required=True, \
                type=str, help='CiteULike username [required]')

    parser.add_argument('-j', '--json', action='store_true', 
        default=False, \
        help='Save CiteULike JSON file [default:./${user}.json]')

    parser.add_argument('-b', '--bibtex', action='store_true', 
        default=False, \
        help='Save CiteULike JSON file [default:./${user}.json]')

    parser.add_argument('-o', '--output', dest='output', default=None, \
                help='Path to save CiteULike BibTeX/JSON file [default:./${user}.{json,bib}]')

    # Read and curate argument
    args = parser.parse_args()
    user, bibtexDL, jsonDL, output = args.user, args.bibtex, args.json, args.output
    if not (bibtexDL or jsonDL):
        print "No action defined."
    if output == None:
        output = './'+user
    elif output[-5:].split('.')[-1] in ('json', 'bib'):
        output = output[:-5] + output[-5:].replace('.bib', '').replace('.json', '')

    try:
        if jsonDL:
            text_file = open(output + '.json', "w")
            text_file.write(getCiteULikeJSONFile(user))
            text_file.close()
            print 'JSON file saved to', output + '.json'
        if bibtexDL:
            text_file = open(output + '.bib', "w")
            text_file.write(getCiteULikeBibTeX(user))
            text_file.close()
            print 'BibTeX file saved to', output + '.bib'
    except urllib2.HTTPError as e:
        print e
    except Exception as e:
        print 'Something went terribly wrong.. ', e
    except:
        print 'Something went terribly wrong.. '


