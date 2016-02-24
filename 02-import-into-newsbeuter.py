
import sys
import sqlite3
import json

liferea_db = json.loads(open("items.json").read())

try:
    with sqlite3.connect("cache.db") as con:
        cur = con.cursor()

    for item in liferea_db:
        guid = item['guid']
        if not guid:
            guid = item['url']

        query = "select * from rss_item where guid is \"" + guid + "\""

        cur.execute(query)

        rows = cur.fetchall()

        if len(rows) > 0:
            print item['guid'], "already in newsbeuter db"
        else:
            # CREATE TABLE rss_item (
            #             id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            #             guid VARCHAR(64) NOT NULL,
            #             title VARCHAR(1024) NOT NULL,
            #             author VARCHAR(1024) NOT NULL,
            #             url VARCHAR(1024) NOT NULL,
            #             feedurl VARCHAR(1024) NOT NULL,
            #             pubDate INTEGER NOT NULL,
            #             content VARCHAR(65535) NOT NULL,
            #             unread INTEGER(1) NOT NULL,
            #             enclosure_url VARCHAR(1024),
            #             enclosure_type VARCHAR(1024),
            #             enqueued INTEGER(1) NOT NULL DEFAULT 0,
            #             flags VARCHAR(52),
            #             deleted INTEGER(1) NOT NULL DEFAULT 0,
            #             base VARCHAR(128) NOT NULL DEFAULT "");

            # http://stackoverflow.com/questions/6514274/how-do-you-escape-strings-for-sqlite-table-column-names-in-python#6701665
            def add_string(q, i):
                if i is not None:
                    i = i.replace("\"", "\"\"")
                    i = i.encode("utf-8", "strict").decode("utf-8")
                    return q + "\"" + i + "\""
                else:
                    return q + "\"\""

            def add_number(q, i):
                return q + "%d" % (i)

            query  = "insert into rss_item "
            query += "(guid, title, author, url, feedurl, pubDate, "
            query += "content, unread, enclosure_url, enclosure_type, "
            query += "enqueued, flags, deleted, base)"
            query += " values ("
            query  = add_string(query, guid) + ", "
            query  = add_string(query, item['title']) + ", "
            query  = add_string(query, item['author']) + ", "
            query  = add_string(query, item['url']) + ", "
            query  = add_string(query, item['feedurl']) + ", "
            query  = add_number(query, item['pubDate']) + ", "
            query  = add_string(query, item['content']) + ", "
            query  = add_number(query, item['unread']) + ", "
            query  = add_string(query, item['enclosure_url']) + ", "
            query  = add_string(query, item['enclosure_type']) + ", "
            query  = add_number(query, item['enqueued']) + ", "
            query  = add_string(query, item['flags']) + ", "
            query  = add_number(query, item['deleted']) + ", "
            query  = add_string(query, item['base']) + ")"

            print query.encode('utf-8')
            cur.execute(query)
            con.commit()

except sqlite3.Error, e:
    print "Error %s" % (e.args[0])
    sys.exit(1)

