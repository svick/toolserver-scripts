#!/usr/bin/env python2.5

import wikitools
import settings
 
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)

params = {
    'action': 'query',
    'list': 'allpages',
    'apnamespace': '0',
    'apprefix': 'List of asteroids/',
    'apfilterredir': 'nonredirects',
    'aplimit': 'max'
  }
request = wikitools.APIRequest(wiki, params, False, False)
result = request.query()['query']['allpages']

limit = float('inf')
i = 0;

for pageinfo in result:
  pageid = pageinfo['pageid']
  page = wikitools.Page(wiki, pageid=pageid)
  oldtitle = page.title
  newtitle = oldtitle.replace('List of asteroids/', 'List of minor planets/')
  print page.move(newtitle, 'moving to reflect move of parent', True)
  i += 1
  if i > limit:
    break
