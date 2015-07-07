class TestResult(object):
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.result = kwargs.get('result')
        self.timestamp = kwargs.get('timestamp')
        self.test_id = kwarg.get('test_id')
        self.test_instance_id = kwargs.get('test_instance_id')
        self.test_batch_id = kwargs.get('test_batch_id')
        self.browser_id = kwargs.get('browser_id')
        self.screenshot_path = kwargs.get('screenshot_path')
        self.videocapture_path = kwargs.get('video_capture_path')
        self.extra_data = kwargs.get('extra_data')
