#! /usr/bin/env python

import os

import yaml
from boto import s3

from brome.core.utils import DbSessionContext
from brome.model.testinstancde import Testinstance

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(HERE, '..')

brome_config_path = os.path.join(ROOT, "configs", "brome.yml")
with open(brome_config_path) as fd:
    config = yaml.load(fd)

DB_NAME = config['database']['mongo_database_name']
BUCKET_NAME = config['database']['s3_bucket_name']


with DbSessionContext(DB_NAME) as session:
    # fetch test instance that has their video in local
    test_instance_list = session.query(Testinstance)\
        .filter(Testinstance.video_location == 'local')\
        .filter(Testinstance.video_capture_path != '')\
        .all()

    for test_instance in test_instance_list:
        # upload the video to s3
        s3.meta.client.upload_file(
            test_instance.video_capture_path,
            BUCKET_NAME,
            test_instance.video_capture_path
        )

        remote_file_name = \
            'https://s3-us-west-2.amazonaws.com/{bucket}/{path}' \
            .format(
                bucket=BUCKET_NAME,
                path=test_instance.video_capture_path
            )

        # set the video_location to s3
        test_instance.video_location = 's3'
        test_instance.remote_file_name = remote_file_name
        session.save(test_instance, safe=True)

print('Done')
