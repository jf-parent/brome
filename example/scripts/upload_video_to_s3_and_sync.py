#! /usr/bin/env python

import os

import boto3
import yaml

from brome.core.utils import DbSessionContext
from brome.model.testinstance import Testinstance

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(HERE, '..')

s3 = boto3.resource('s3')

brome_config_path = os.path.join(ROOT, "config", "brome.yml")
with open(brome_config_path) as fd:
    config = yaml.load(fd)

DB_NAME = config['database']['mongo_database_name']
BUCKET_NAME = config['database']['s3_bucket_name']
ROOT_TB_RESULTS = config['project']['test_batch_result_path']


with DbSessionContext(DB_NAME) as session:
    # fetch test instance that has their video in local
    test_instance_list = session.query(Testinstance)\
        .filter(Testinstance.video_location == 'local')\
        .filter(Testinstance.video_capture_path != '')\
        .all()

    for test_instance in test_instance_list:
        # upload the video to s3
        file_path  = os.path.join(
             ROOT_TB_RESULTS,
             test_instance.video_capture_path
        )
        try:
            data = open(file_path, 'rb')
        except FileNotFoundError:
            print('{file_path} not found'.format(file_path=file_path))
            continue

        print('[*]Uploading {file_path} to s3...'.format(file_path=file_path))
        s3.Bucket(BUCKET_NAME).put_object(Key=test_instance.video_capture_path, Body=data)

        remote_file_name = \
            'https://s3-us-west-2.amazonaws.com/{bucket}/{path}' \
            .format(
                bucket=BUCKET_NAME,
                path=test_instance.video_capture_path
            )

        # set the video_location to s3
        test_instance.video_location = 's3'
        test_instance.video_capture_path = remote_file_name
        session.save(test_instance, safe=True)
        os.remove(file_path)

print('Done')
