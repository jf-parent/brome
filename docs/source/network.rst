Network Capture
===============

Brome use the mitm proxy to gather the network data. It support chrome and firefox on localhost.

Below are the step to follow in order to capture the network data.

Install Mitmproxy
-----------------

Follow the steps found here: https://mitmproxy.org/doc/install.html

Browser config
--------------

Add the `enable_proxy` config to your browser config::

    #/path/to/project/config/browsers_config.yml
    firefox:
      browserName: 'Firefox'
      enable_proxy: True
    chrome:
      browserName: 'Chrome'
      enable_proxy: True

Brome config
------------

Add the following config to your brome yaml::

    #/path/to/project/config/brome.yml
    mitmproxy:
      path: '/path/to/proxy/mitmdump'
      filter: "~m post" #optional this filter will only gather post requests
    webserver:
      SHOW_NETWORK_CAPTURE: true
      analyse_network_capture_func: 'model.network_analysis'

Network capture data
--------------------

The network capture data will be stored in the test results folder under the network_capture folder of the specific test batch. For example: `/path/to/project/test_results/tb_1/network_capture/test.data`

You can analyse the data manually with this code::

    #!/usr/bin/env python
    import pprint
    import sys

    from libmproxy import flow

    with open(sys.argv[1], "rb") as logfile:
        freader = flow.FlowReader(logfile)
        pp = pprint.PrettyPrinter(indent=4)
        try:
            for f in freader.stream():
                print(f)
                print(f.request.host)
                pp.pprint(f.get_state())
                print("")
        except flow.FlowReadError as v:
            print "Flow file corrupted. Stopped loading."

Analysis in the webserver
-------------------------

The webserver can automatically analyse the network captured data for you if you provided a method. Here is an example::

    #/path/to/project/model/network_analysis.py
    import json

    from libmproxy import flow

    def analyse(network_capture_path):
        with open(network_capture_path, "rb") as logfile:
            freader = flow.FlowReader(logfile)

            nb_success = 0
            nb_failure = 0
            try:
                for f in freader.stream():
                    try:
                        result = json.loads(f.response.get_decoded_content())
                        if result['success']:
                            nb_success += 1
                        else:
                            nb_failure += 1
                    except:
                        pass

                return "<p>Nb success: %s</p><p>Nb failure: %s</p>"%(nb_success, nb_failure)
            except flow.FlowReadError as v:
                return "<p>Flow file corrupted. Stopped loading.</p>"
