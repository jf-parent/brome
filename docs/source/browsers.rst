Browsers
========

Browser config
--------------

The brome object need a browser config (yaml). You provide it in the bro executable::

    brome = Brome(
        config_path = os.path.join(HERE, "config", "brome.yml"),
        selector_dict = selector_dict,
        test_dict = test_dict,
        browsers_config_path = os.path.join(HERE, "config", "browsers_config.yml"), # <-- this file
        absolute_path = HERE
    )

The browser config look something like this::
    
    firefox:
      browserName: 'Firefox'

    c:
      browserName: 'Chrome'

So when you want to run a test using firefox you specify it to the bro executable::
    
    $./bro run -l 'firefox'

    $./bro run -l 'c'

You can add brome config in the browser config also::
    
    firefox:
      browserName: 'Firefox'
      "highlight:use_highlight": false
      maximize_window: true
      "runner:embed_on_test_crash": true

    c:
      browserName: 'Chrome'
      window_height: 950
      window_width: 1550
      "runner:embed_on_test_crash": false

You can override a brome config for a specific browser, for example if the config `runner:embed_on_test_crash` is set to True in the brome.yml and you wish to not embed_on_test_crash in chrome then you can set `"runner:embed_on_test_crash"` to false in the browser_config under the chrome section.

Init driver
-----------

If you want to change the way the browser is initiliazed then you can do the following::

    #/path/to/project/model/basetest.py
    from selenium import webdriver

    from brome.core.model.basetest import BaseTest as BromeBaseTest
    from brome.core.model.proxy_driver import ProxyDriver

    class BaseTest(BromeBaseTest):
        
        def init_driver(self, *args, **kwargs):
            #DO WHATEVER YOU WANT
            driver = Firefox()

            #Make sure that you wrap the selenium driver in the ProxyDriver tho
            return ProxyDriver(
                driver = driver,
                test_instance = self,
                runner = self._runner
            )

    #/path/to/project/tests/test_scenario.py
    #Make sure that your test inherit from your BaseTest
    from model.basetest import BaseTest

    class Test(BaseTest):
        pass

You can look at how the brome basetest implement the init_driver (https://github.com/brome-hq/brome/search?utf8=%E2%9C%93&q=init_driver)
      
Examples
--------

Localhost
~~~~~~~~~

Chrome
******

::

    chrome:
      browserName: 'Chrome'

IE
**

::

    ie:
      browserName: 'internet explorer'

Firefox
******

::

    firefox:
      browserName: 'Firefox'

Safari
******

::

    safari:
      browserName: 'Safari'

PhantomJS
*********

::
    
    phantomjs:
      browserName: 'PhantomJS'

IOS Simulator
*************

::

    iphone:
      appium: true
      deviceName: 'iPhone 5'
      platformName: 'iOS'
      platformVersion: '9.0'
      browserName: 'Safari'
      nativeWebTap: true
      "proxy_element:use_touch_instead_of_click": true
      udid: ''

Android
*******

::

    android:
      appium: true
      "proxy_element:use_touch_instead_of_click": true
      deviceName: 'Android'
      platformName: 'Android'
      version: '4.2.2'
      browserName: 'chrome'

Remote
~~~~~~

EC2
***

::

    chrome_ec2:
      amiid: ''
      browserName: 'chrome'
      available_in_webserver: True
      hub_ip: '127.0.0.1'
      platform: 'LINUX'
      launch: True
      ssh_key_path: '/path/to/identity.pem'
      terminate: True
      nb_browser_by_instance: 1
      max_number_of_instance: 30
      username: 'ubuntu'
      window_height: 950
      window_width: 1550
      region: 'us-east-1'
      security_group_ids: ['sg-xxxxxxx']
      instance_type: 't2.micro'
      selenium_command: "DISPLAY=:0 nohup java -jar selenium-server.jar -role node -hub http://{hub_ip}:4444/grid/register -browser browserName={browserName},maxInstances={nb_browser_by_instance},platform={platform} > node.log 2>&1 &"

Virtual Box
***********

::

    firefox_vbox:
      browserName: 'firefox'
      available_in_webserver: true
      hub_ip: 'localhost'
      password: ''
      platform: 'LINUX'
      launch: true
      terminate: true
      username: ''
      vbname: 'ubuntu-firefox'
      vbox_type: 'gui' #'headless'
      version: '31.0'

Sauce Labs
**********

::

    chrome_saucelabs:
      saucelabs: True
      platform: "Mac OS X 10.9"
      browserName: "chrome"
      version: "31"

Browserstack
************

::

    ie_browserstack:
      browserstack: True
      os: 'Windows'
      os_version: 'xp'
      browser: 'IE'
      browser_version: '7.0'

