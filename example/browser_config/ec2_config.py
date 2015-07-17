test_config = {}
test_config['amiid'] = 'ami-86f2aaee'
test_config['browserName'] = 'PhantomJS'
test_config['username'] = 'ubuntu'
test_config['ssh_key_path'] = '/home/ubuntu/.ssh/worker9-nvirginia.pem'
test_config['hub_ip'] = 'localhost'
test_config['platform'] = 'LINUX'
test_config['launch'] = True
test_config['region'] = "us-east-1"
test_config['terminate'] = True
test_config['available_in_webserver'] = True
test_config['nb_instance'] = 3
test_config['nb_browser_by_instance'] = 1
test_config['max_number_of_instance'] = 20
test_config['ec2_region'] = 'us-east-1'
test_config['security_group_ids'] = ['sg-00487c65']
test_config['instance_type'] = 't2.micro'
test_config['selenium_command'] = "DISPLAY=:0 nohup java -jar selenium-server.jar -role node -hub http://{hub_ip}:4444/grid/register -browser browserName={browserName},maxInstances={nb_browser_by_instance},platform={platform} > node.log 2>&1 &"

chrome_config = {}
chrome_config['amiid'] = 'ami-86f2aaee'
chrome_config['browserName'] = 'Chrome'
chrome_config['username'] = 'ubuntu'
chrome_config['ssh_key_path'] = '/home/ubuntu/.ssh/worker9-nvirginia.pem'
chrome_config['hub_ip'] = 'localhost'
chrome_config['platform'] = 'LINUX'
chrome_config['launch'] = True
chrome_config['terminate'] = True
chrome_config['available_in_webserver'] = True
chrome_config['nb_instance'] = 3
chrome_config['nb_browser_by_instance'] = 1
chrome_config['max_number_of_instance'] = 20
chrome_config['ec2_region'] = 'us-east-1'
chrome_config['security_group_ids'] = ['sg-00487c65']
chrome_config['instance_type'] = 't2.micro'
chrome_config['selenium_command'] = "DISPLAY=:0 nohup java -jar selenium-server.jar -role node -hub http://{hub_ip}:4444/grid/register -browser browserName={browserName},maxInstances={nb_browser_by_instance},platform={platform} > node.log 2>&1 &"
internet_explorer_config = {}
internet_explorer_config['amiid'] = 'ami-86f2aaee'
internet_explorer_config['browserName'] = 'internet explorer'
internet_explorer_config['username'] = 'Administrator'
internet_explorer_config['hub_ip'] = 'localhost'
internet_explorer_config['platform'] = 'WINDOWS'
internet_explorer_config['launch'] = True
internet_explorer_config['terminate'] = True
internet_explorer_config['available_in_webserver'] = True
internet_explorer_config['nb_instance'] = 3
internet_explorer_config['nb_browser_by_instance'] = 1
internet_explorer_config['ec2_region'] = 'us-east-1'
internet_explorer_config['security_group_ids'] = ['sg-00487c65']
internet_explorer_config['instance_type'] = 't2.micro'
internet_explorer_config['password'] = '1111'
internet_explorer_config['selenium_command'] = "xvfb-run -a --server-args='-screen 0, 1024x768x24' rdesktop -u {username} -p {password} {instance_ip_address}:3389 &"

ec2_config_dict = {}
ec2_config_dict['test'] = test_config
