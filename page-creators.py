#! /usr/bin/env python
# -*- coding: utf-8 -*-
#Written by MZMcBride and Svick

#$ -l sql-s1-user=1
#$ -j y

debug = False

"""
CREATE DATABASE u_svick_enwiki_page_creators_p;
CREATE TABLE creator (
c_page_id INT UNSIGNED NOT NULL PRIMARY KEY,
c_user_id INT UNSIGNED NOT NULL,
c_timestamp VARBINARY(14) NOT NULL
);
CREATE INDEX c_creator ON creator (c_user_id);
"""

import MySQLdb, MySQLdb.cursors

conn1 = MySQLdb.connect(host='sql-s1', db='enwiki_p', read_default_file='~/.my.cnf')
cursor1 = conn1.cursor()
# Get the max(page_id)
cursor1.execute('SELECT MAX(page_id) FROM page;')
real_max_page_id = cursor1.fetchone()[0]

conn2 = MySQLdb.connect(host='sql-s1-user', db='u_svick_enwiki_page_creators_p', read_default_file='~/.my.cnf')
cursor2 = conn2.cursor()
# Get the max(page_id)
cursor2.execute('SELECT MAX(c_page_id) FROM creator;')
stored_max_page_id = cursor2.fetchone()[0]
if stored_max_page_id is None:
    stored_max_page_id = 0
else:
    stored_max_page_id = stored_max_page_id

all_page_ids = set()
limit = 100000
cursor1.execute('''
/* page-creators.py SLOW_OK */
SELECT
  page_id
FROM page
WHERE page_id > %s
ORDER BY page_id ASC
LIMIT %s;
''' , (stored_max_page_id, limit))

for row in cursor1.fetchall():
    page_id = row[0]
    all_page_ids.add(page_id)

if debug:
    print len(all_page_ids)

if debug:
    print len(range(stored_max_page_id+1, real_max_page_id+1))

for integer in range(stored_max_page_id+1, real_max_page_id+1):
    if integer in all_page_ids:
        try:
            cursor1.execute('''
            /* page-creators.py SLOW_OK */
            SELECT
              rev_user, rev_timestamp
            FROM revision
            WHERE rev_timestamp = (SELECT
                                     MIN(rev_timestamp)
                                   FROM revision AS last
                                   WHERE last.rev_page = %s)
            AND rev_page = %s;
            ''' , (integer, integer))
            page_revision = cursor1.fetchone()
            page_creator = page_revision[0]
            page_created = page_revision[1]
            if debug:
                print integer, page_creator
            elif not debug:
                cursor2.execute('INSERT INTO creator VALUES (%s, %s, %s);' , (integer, page_creator, page_created))
        except TypeError:
            continue

conn2.commit()
cursor1.close()
conn1.close()
cursor2.close()
conn2.close()

