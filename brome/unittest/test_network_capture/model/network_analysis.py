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
