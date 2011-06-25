#!/usr/bin/env python2.5
 
# Copyright 2009-2010 bjweeks, MZMcBride, svick
 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
import wikitools
import settings
 
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)

request = wikitools.APIRequest(wiki, {'action': 'query', 'list': 'allpages', 'apnamespace': '4', 'apprefix': 'WikiProject_Mathematics:List_of_mathematics_articles_', 'aplimit': 'max'}, False, False)
result = request.query()['query']['allpages']

for pageinfo in result:
  pageid = pageinfo['pageid']
  page = wikitools.Page(wiki, pageid=pageid)
  oldtitle = page.title
  newtitle = oldtitle.replace(':WikiProject Mathematics:', ':WikiProject Mathematics/')
  print page.move(newtitle, 'should be subpage of project', True)
