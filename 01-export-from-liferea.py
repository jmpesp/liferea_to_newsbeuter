
import sys
import sqlite3
import json

def dictionary_from_query(cur, query):
    cur.execute(query)

    items = []

    for data in cur.fetchall():
        columns = [x[0] for x in cur.description]
        output = {}
        for entry in zip(columns, data):
            output[entry[0]] = entry[1]
        items.append(output)

    return items

try:
    with sqlite3.connect("liferea.db") as con:
        cur = con.cursor()

        items = dictionary_from_query(cur, "select * from items")
        subscription = dictionary_from_query(cur, "select * from subscription")
        metadata = dictionary_from_query(cur, "select * from metadata")

        newsbeuter_items = []

        for item in items:
            newsbeuter_item = {}

            feedurl = [x['source'] for x in subscription if x['node_id'] == item['node_id']]
            if len(feedurl) == 0:
                feedurl = ""
            else:
                feedurl = feedurl[0]

            author = [x['value'] for x in metadata if x['item_id'] == item['item_id'] and x['key'] == "author"]
            if len(author) == 0:
                author = ""
            else:
                author = author[0]

            newsbeuter_item['feedurl'] = feedurl
            newsbeuter_item['unread'] = not item['read']
            newsbeuter_item['pubDate'] = item['date']
            newsbeuter_item['author'] = author
            newsbeuter_item['url'] = item['source']
            newsbeuter_item['title'] = item['title']
            newsbeuter_item['content'] = item['description']
            newsbeuter_item['guid'] = item['source_id']

            newsbeuter_item['enqueued'] = 0
            newsbeuter_item['enclosure_type'] = ""
            newsbeuter_item['enclosure_url'] = ""
            newsbeuter_item['flags'] = ""
            newsbeuter_item['base'] = ""
            newsbeuter_item['deleted'] = 0

            newsbeuter_items.append(newsbeuter_item)

        print json.dumps(newsbeuter_items, indent=2)

except sqlite3.Error, e:
    print "Error %s" % (e.args[0])
    sys.exit(1)

