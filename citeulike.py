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
    refs = json.loads(jsontext)
    return citeULikeKeys(refs)

def getCiteULikeBibTeX(user='user', cookie=None):
    """
    Retrieves the BibTeX file from CiteULike and returns a
    string with the contents. Does not require a cookie.
        getCiteULikeBibTeX(user='user') -> string
    """
    url = 'http://www.citeulike.org/bibtex/'+user
    if cookie==None:
        cookie = getCiteULikeCookie()
    bibText = downloadFile(url, cookie)
    return bibText


