Session Recording
=================

Brome use the package `CastroRedux <https://github.com/brome-hq/CastroRedux>`_ to record the session. CastroRedux record the session using vnc.

Configuration
-------------

Hub configuration
+++++++++++++++++

The only thing you need to configure on the hub machine is the vnc password file::

    $ echo "$VNCPASSWD" >> ~/.vnc/passwd

Node configuration
++++++++++++++++++

You need to start vnc on your node machine. See this `post <http://brome-hq.logdown.com/posts/306522-selenium-ec2-grid-node-installation>`_ and this `post <http://brome-hq.logdown.com/posts/305608-selenium-ubuntu-node-configuration-on-virtualbox>`_ for some inspiration.

Watch
-----

First you need to enable the config `SHOW_VIDEO_CAPTURE` in your brome.yml::

    #/path/to/project/config/brome.yml
    [...]
    webserver:
      SHOW_VIDEO_CAPTURE: true
    [...]

Launch the webserver (`./bro webserver`), navigate to a specific test batch and click on the `Video recordings` button.
