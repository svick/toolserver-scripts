#!/usr/bin/env python2.5

import wikitools
import settings
import re
 
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)

params = {
    'action': 'query',
    'list': 'categorymembers',
    'cmtitle': 'Category:Stub message boxes needing attention',
    'cmprop': 'ids|sortkeyprefix',
    'cmnamespace': '10',
    'cmlimit': 'max'
  }
request = wikitools.APIRequest(wiki, params, False, False)
result = request.query()['query']['categorymembers']
result = filter(lambda p: p['sortkeyprefix'][0] == 'E', result)

limit = float('inf')
i = 0;

for pageinfo in result:
  pageid = pageinfo['pageid']
  page = wikitools.Page(wiki, pageid=pageid)
  title = page.title
  text = page.getWikiText()
  newText = re.sub(r'^(\s*\|\s*name\s*=\s*).*$', r'\1' + title, text, flags=re.MULTILINE)
  page.edit(newText, summary='Fixing name', bot=1)
  i += 1
  if i >= limit:
    break
