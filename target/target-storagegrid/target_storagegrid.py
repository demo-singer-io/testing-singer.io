#!/usr/bin/env python3

import argparse
import io
import os
import sys
import json
import threading
import http.client
import urllib
from datetime import datetime
import collections
import pkg_resources
import boto3
import boto3.session
import urllib3
import ssl
import urllib3
urllib3.disable_warnings()
from jsonschema.validators import Draft4Validator
import singer

logger = singer.get_logger()


def write_to_storagegrid(content):
    try:
        filename = 'file8.txt'
        bucketname = 'test-bucket-store1'

        session = boto3.session.Session(profile_name='default')
        endpoint = 'https://113.29.246.178:8082/'
        s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify=False)

        file = s3.Object(bucketname, filename).put(Body=content['stream'])

    except Exception as error:
	    print(error)





def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()

def flatten(d, parent_key='', sep='__'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, str(v) if type(v) is list else v))
    return dict(items)
        
def persist_messages(messages):
    state = None
    validators = {}
    schemas = {}
    for message in messages:
        try:
            o = singer.parse_message(message).asdict()
        except json.decoder.JSONDecodeError:
            logger.error("Unable to parse:\n{}".format(message))
            raise

        message_type = o['type']
        if message_type == 'RECORD':
            if o['stream'] not in schemas:
                raise Exception("A record for stream {} was encountered before a corresponding schema".format(o['stream']))

            validators[o['stream']].validate(o['record'])
            flattened_record = flatten(o['record'])
            write_to_storagegrid(flattened_record)

        elif message_type == 'SCHEMA':
            stream = o['stream']
            schemas[stream] = o['schema']
            validators[stream] = Draft4Validator(o['schema'])

    return state


def send_usage_stats():
    try:
        version = pkg_resources.get_distribution('target-storagegrid').version
        conn = http.client.HTTPConnection('collector.singer.io', timeout=10)
        conn.connect()
        params = {
            'e': 'se',
            'aid': 'singer',
            'se_ca': 'target-storagegrid',
            'se_ac': 'open',
            'se_la': version,
        }
        conn.request('GET', '/i?' + urllib.parse.urlencode(params))
        response = conn.getresponse()
        conn.close()
    except:
        logger.debug('Collection request failed')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as input_json:
            config = json.load(input_json)
    else:
        config = {}

    if not config.get('disable_collection', False):
        logger.info('Sending version information to singer.io. ' +
                    'To disable sending anonymous usage data, set ' +
                    'the config parameter "disable_collection" to true')
        threading.Thread(target=send_usage_stats).start()

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    state = persist_messages(input_messages)

    emit_state(state)
    logger.debug("Exiting normally")


if __name__ == '__main__':
    main()
