#CHROME EC2
chrome_ec2 = {}
chrome_ec2['amiid'] = 'ami-86f2aaee'
chrome_ec2['browserName'] = 'Chrome'
chrome_ec2['username'] = 'ubuntu'
chrome_ec2['ssh_key_path'] = '/home/ubuntu/.ssh/worker9-nvirginia.pem'
chrome_ec2['hub_ip'] = 'localhost'
chrome_ec2['platform'] = 'LINUX'
chrome_ec2['launch'] = True
chrome_ec2['terminate'] = True
chrome_ec2['available_in_webserver'] = True
chrome_ec2['nb_instance'] = 3
chrome_ec2['nb_browser_by_instance'] = 1
chrome_ec2['max_number_of_instance'] = 20
chrome_ec2['region'] = 'us-east-1'
chrome_ec2['security_group_ids'] = ['sg-00487c65']
chrome_ec2['instance_type'] = 't2.micro'
chrome_ec2['selenium_command'] = "DISPLAY=:0 nohup java -jar selenium-server.jar -role node -hub http://{hub_ip}:4444/grid/register -browser browserName={browserName},maxInstances={nb_browser_by_instance},platform={platform} > node.log 2>&1 &"

#INTERNET EXPLORER EC2
internet_explorer_ec2 = {}
internet_explorer_ec2['amiid'] = 'ami-86f2aaee'
internet_explorer_ec2['browserName'] = 'internet explorer'
internet_explorer_ec2['username'] = 'Administrator'
internet_explorer_ec2['hub_ip'] = 'localhost'
internet_explorer_ec2['platform'] = 'WINDOWS'
internet_explorer_ec2['launch'] = True
internet_explorer_ec2['terminate'] = True
internet_explorer_ec2['available_in_webserver'] = True
internet_explorer_ec2['nb_instance'] = 3
internet_explorer_ec2['nb_browser_by_instance'] = 1
internet_explorer_ec2['ec2_region'] = 'us-east-1'
internet_explorer_ec2['security_group_ids'] = ['sg-00487c65']
internet_explorer_ec2['instance_type'] = 't2.micro'
internet_explorer_ec2['password'] = '1111'
internet_explorer_ec2['selenium_command'] = "xvfb-run -a --server-args='-screen 0, 1024x768x24' rdesktop -u {username} -p {password} {instance_ip_address}:3389 &"

#LOCALHOST FIREFOX
firefox_localhost = {}
firefox_localhost['browserName'] = 'Firefox'
firefox_localhost['highlight:use_highlight']= False
firefox_localhost['browser:window_width'] = 200
firefox_localhost['browser:window_height'] = 200
firefox_localhost['available_in_webserver'] = True

#LOCALHOST CHROME
chrome_localhost = {}
chrome_localhost['browserName'] = 'Chrome'
chrome_localhost['available_in_webserver'] = True

#LOCALHOST PHANTOMJS
phantomjs_localhost = {}
phantomjs_localhost['browserName'] = 'PhantomJS'
phantomjs_localhost['max_number_of_instance'] = 1
phantomjs_localhost['available_in_webserver'] = True

phantomjs_localhost2 = {}
phantomjs_localhost2['browserName'] = 'PhantomJS'
phantomjs_localhost2['max_number_of_instance'] = 3
phantomjs_localhost2['available_in_webserver'] = True

#MAIN CONFIG
browsers_config = {}
browsers_config['lfirefox'] = firefox_localhost
browsers_config['lf'] = firefox_localhost
browsers_config['lchrome'] = chrome_localhost
browsers_config['lphantomjs'] = phantomjs_localhost
browsers_config['lphantomjs2'] = phantomjs_localhost2
browsers_config['internet_explorer_ec2'] = internet_explorer_ec2
browsers_config['chrome_ec2'] = chrome_ec2
