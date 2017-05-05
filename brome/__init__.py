import pickle
import hashlib
import shutil
import os
import argparse
import re
from glob import glob


from brome.core.utils import (
    update_test,
    delete_database,
    DbSessionContext
)
from brome.webserver.server.app import run_app
from brome.core.grep import grep_files
from brome.runner.local_runner import LocalRunner
from brome.runner.grid_runner import GridRunner
from brome.core.settings import BROME_CONFIG
from brome.core.configurator import (
    generate_brome_config
)

__version__ = "1.2.0"


class Brome(object):
    def __init__(self, **kwargs):
        self.configure(**kwargs)

    def configure(self, **kwargs):
        brome_config = kwargs.get('config', dict())
        selector_dict = kwargs.get('selector_dict', dict())
        test_dict = kwargs.get('test_dict', dict())
        browsers_config = kwargs.get('browsers_config', dict())
        self.tests = kwargs.get('tests', list())

        if 'project' in brome_config:
            absolute_path = kwargs.get('absolute_path')
            brome_config['project']['absolute_path'] = absolute_path
            if not absolute_path:
                print('[Warning] absolute_path not provided in the brome.configure()')  # noqa

        BROME_CONFIG.update(generate_brome_config())
        for key in iter(BROME_CONFIG):
            if key in brome_config:
                BROME_CONFIG[key].update(brome_config[key])

        for key in iter(brome_config):
            if key not in BROME_CONFIG:
                BROME_CONFIG[key] = brome_config[key]

        BROME_CONFIG['selector_dict'] = selector_dict
        BROME_CONFIG['browsers_config'] = browsers_config
        BROME_CONFIG['test_dict'] = test_dict

    def print_usage(self):
        print('$ ./bro admin | run | webserver | list | find | webadmin')
        exit(1)

    def execute(self, args):
        if len(args) < 2:
            self.print_usage()

        if args[1] == 'run':
            self.run(args[2:])
        elif args[1] == 'admin':
            self.admin(args[2:])
        elif args[1] == 'find':
            self.find(args[2:])
        elif args[1] == 'list':
            self.list_(args[2:])
        elif args[1] == 'webserver':
            self.webserver(args[2:])
        elif args[1] == 'webadmin':
            self.webadmin(args[2:])
        else:
            self.print_usage()

    def run(self, args):
        parser = argparse.ArgumentParser(description='Brome runner')

        # TEST SEARCH QUERY
        parser.add_argument(
                            '--search',
                            '-s',
                            dest='test_search_query',
                            default='*',
                            help='The search query used to activate tests'
        )
        # TEST NAME
        parser.add_argument(
                            '--name',
                            '-n',
                            dest='test_name',
                            help='The test name to be executed'
        )

        # TEST FILE
        parser.add_argument(
            '--test-file',
            dest='test_file',
            default=False,
            help='The file containing the tests name'
        )

        # LOCALHOST RUNNER
        parser.add_argument(
                            '--localhost',
                            '-l',
                            dest='localhost_runner',
                            help='Launch a browser from localhost'
        )

        # REMOTE RUNNER
        parser.add_argument(
                            '-r',
                            '--remote',
                            dest='remote_runner',
                            default=False,
                            help='Launch a browser on a remote'
        )

        def test_config_string(value):
            try:
                re.match("([^=]+=[^,]+,?)+", value).group(0)
                return value
            except AttributeError:
                print("--test-config '%s' does not match required format (key=value,key1:value1)" % (value))  # noqa
                exit(1)

        # TEST CONFIG KWARGS
        parser.add_argument(
                            '--test-config',
                            type=test_config_string,
                            dest='test_config',
                            help='The config that will be pass to the test. ex: "key=value,key1=value1"'  # noqa
        )

        parsed_args = parser.parse_args(args)
        run_args = vars(parsed_args)
        BROME_CONFIG['runner_args'] = run_args

        if BROME_CONFIG['test_dict']:
            self.auto_update_test()

        if run_args['localhost_runner']:
            browsers_id = [run_args['localhost_runner']]
        elif run_args['remote_runner']:
            browsers_id = run_args['remote_runner'].split(',')
        else:
            raise Exception('Please select -r or -l')

        for browser_id in browsers_id:
            if browser_id not in BROME_CONFIG['browsers_config'].keys():
                raise Exception("""
                    This browser id is not available
                    in the provided browsers config\n
                    Supported browser(s) are: {browsers}
                """.format(
                    browsers=BROME_CONFIG['browsers_config'].keys()
                ))

        # LOCALHOST RUNNER
        if run_args['localhost_runner']:
            LocalRunner(self).execute()

        # REMOTE RUNNER
        elif run_args['remote_runner']:
            GridRunner(self).execute()

        # ERROR
        else:
            raise Exception(
                'Select either -l "{browser_id}" or -r "{browser_id}"'
            )

    def webserver(self, args):
        run_app()

    def webadmin(self, args):
        from brome.admin.app import app as admin_app
        admin_config = BROME_CONFIG['webserver']['admin']
        admin_app.run(
            host=admin_config['host'],
            port=admin_config['port'],
            debug=admin_config.get('debug', False)
        )

    def list_(self, args):
        query = os.path.join(
                        BROME_CONFIG['project']['absolute_path'],
                        BROME_CONFIG['brome']['script_folder_name'],
                        "%s*.py" %
                        BROME_CONFIG['brome']['script_test_prefix']
                    )

        tests = glob(query)
        print("[index]\t|test name|")
        for index, test in enumerate(tests):
            test_name = test.split(os.sep)[-1][5:-3]
            print("[%s]\t%s" % (index, test_name))

    def admin(self, args):
        parser = argparse.ArgumentParser(description='Brome admin')

        parser.add_argument(
                            '--reset',
                            dest='reset',
                            action='store_true',
                            help='delete the database + delete the test batch results + update the test collection'  # noqa
        )

        parser.add_argument(
                            '--delete-test-states',
                            dest='delete_test_states',
                            action='store_true',
                            help='Delete all the test states'
        )

        parser.add_argument(
                            '--delete-test-results',
                            dest='delete_test_result',
                            action='store_true',
                            help='Delete all the test batch results'
        )

        parser.add_argument(
                            '--delete-database',
                            dest='delete_database',
                            action='store_true',
                            help='Delete the project database'
        )

        parser.add_argument(
                            '--update-test',
                            dest='update_test',
                            action='store_true',
                            help='Update the test in the database'
        )

        parsed_args = parser.parse_args(args)

        def delete_test_states():
            states_dir = os.path.join(
                BROME_CONFIG["project"]["absolute_path"],
                BROME_CONFIG["brome"]["script_folder_name"],
                "states"
            )
            try:
                shutil.rmtree(states_dir)
            except OSError:
                pass

            try:
                os.makedirs(states_dir)
            except OSError:
                pass

            print('States deleted')

        def delete_test_batch_result():
            tb_results_path = os.path.join(
                BROME_CONFIG['project']['test_batch_result_path'],
                'tb_results'
            )
            if os.path.exists(tb_results_path):
                shutil.rmtree(tb_results_path)
                print('Test batch result (%s) deleted!' % tb_results_path)
            else:
                print('Nothing to delete')

        if parsed_args.reset:
            delete_database(BROME_CONFIG['database']['mongo_database_name'])
            delete_test_batch_result()
            if BROME_CONFIG['test_dict']:
                self.update_test()
        elif parsed_args.delete_test_result:
            delete_test_batch_result()
        elif parsed_args.delete_test_states:
            delete_test_states()
        elif parsed_args.delete_database:
            delete_database(BROME_CONFIG['database']['mongo_database_name'])
        elif parsed_args.update_test:
            self.update_test()

    def find(self, args):
        parser = argparse.ArgumentParser(description='Brome find')

        parser.add_argument(
                            '--test-id',
                            dest='test_id',
                            help='Find a test_id in model and test directory'
        )

        parser.add_argument(
                            '--unused-test-id',
                            dest='unused_test_id',
                            action='store_true',
                            help='Find all unused test id in model and test directory'  # noqa
        )

        parser.add_argument(
                            '--selector',
                            dest='selector',
                            help='Find a selector in model and test directory'
        )

        parser.add_argument(
                            '--unused-selector',
                            dest='unused_selector',
                            action='store_true',
                            help='Find all unused selector variable in model and test directory'  # noqa
        )

        parsed_args = parser.parse_args(args)

        test_id_regex = "[\'\"]+(%s){1}[\'\"]+"
        selector_regex = "\..*\(+[\'\"]+.*(%s)+.*[\'\"]+"
        if parsed_args.test_id:
            pattern = test_id_regex % parsed_args.test_id
        elif parsed_args.selector:
            pattern = selector_regex % parsed_args.selector

        paths = [
            os.path.join(
                BROME_CONFIG['project']['absolute_path'],
                BROME_CONFIG['brome']['script_folder_name']
            ),
            os.path.join(
                BROME_CONFIG['project']['absolute_path'],
                "model"
            ),
        ]

        if parsed_args.test_id or parsed_args.selector:
            result = grep_files(paths, pattern, True)
        else:
            if parsed_args.unused_selector:
                print('Unused selector variable:')
                dict_ = BROME_CONFIG['selector_dict']
                regex_ = selector_regex

            elif parsed_args.unused_test_id:
                print('Unused test id:')
                dict_ = BROME_CONFIG['test_dict']
                regex_ = test_id_regex

            try:
                for key in dict_:
                    pattern = regex_ % key
                    result = grep_files(paths, pattern, True, return_list=True)
                    if not result:
                        print(key)

            except KeyboardInterrupt:
                pass

    def update_test(self):
            if BROME_CONFIG['test_dict']:
                with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                    update_test(session, BROME_CONFIG['test_dict'])
            else:
                raise Exception("No test dictionary provided")

    def auto_update_test(self):
        brome_memory_pickle_path = os.path.join(
            BROME_CONFIG['project']['absolute_path'],
            ".brome.pkl"
        )

        new_hash = hashlib.sha1(
            BROME_CONFIG['test_dict'].__repr__().encode('utf')
        ).hexdigest()

        if os.path.isfile(brome_memory_pickle_path):
            with open(brome_memory_pickle_path, "rb") as fd:
                data = pickle.load(fd)

            if 'test_dict_hash' in data:
                if data['test_dict_hash'] != new_hash:
                    self.update_test()

                    data['test_dict_hash'] = new_hash
                    with open(brome_memory_pickle_path, "wb") as fd:
                        pickle.dump(data, fd)
        else:
            data = {}
            data['test_dict_hash'] = new_hash

            with open(brome_memory_pickle_path, "wb") as fd:
                pickle.dump(data, fd)
            self.update_test()
