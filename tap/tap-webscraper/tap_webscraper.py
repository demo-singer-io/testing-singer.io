import requests
import html2text
import singer
import urllib.request
from datetime import datetime, timezone
import io
import os
import sys
import json

logger = singer.get_logger()


def main():
    url='https://www.singer.io/tap/github'

    html_content = requests.get(url)
    rendered_content = html2text.html2text(html_content.text)

    now = datetime.now(timezone.utc).isoformat()
    schema = {
        'properties':   {
            'stream': {'type': 'string'},
            'timestamp': {'type': 'string', 'format': 'date-time'},
        },
    }

    singer.write_schema('webscraper', schema, 'timestamp')
    singer.write_records('webscraper', [{'timestamp': now, 'stream': rendered_content}])
    #singer.write_records('webscraper', [{'timestamp': now, 'stream': 'rendered_content'}])


    #file = open('file_text1.txt', 'w', encoding="utf-8")
    #try:
    #	file.write(rendered_content)
    #except Exception as e:
    #	print(e)
    #file.close()


if __name__ == '__main__':
    main()