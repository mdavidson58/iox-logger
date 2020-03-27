import configparser
import paho.mqtt.client as mqtt
import time
import sys
import syslog
import logging

from logging.handlers import TimedRotatingFileHandler

# get config files
configfile = ['/data/package_config.ini']
config = configparser.ConfigParser()

if len(config.read(configfile)) != len(configfile):
	sys.stderr.write("Failed to open config file\n")
	sys.exit()

#logrotate Parameters
days = config.get('logs','rotate_days')
numlogs = config.get('logs','num_logs')

#MQTT Parameters
mqtt_enable = int(config.get('mqtt','mqtt_enable'))
mqtt_server = config.get('mqtt','mqtt_server')
mqtt_port = config.get('mqtt','mqtt_port')
mqtt_client_id = config.get('mqtt','mqtt_client_id')
mqtt_username = config.get('mqtt', 'mqtt_username')
mqtt_password = config.get('mqtt', 'mqtt_password')
mqtt_topic = config.get('mqtt', 'mqtt_topic')
gw_name = config.get('_cisco_mqtt_attributes', 'gw.name')

sys.stderr.write('enable = ' + str(mqtt_enable) + ' server = ' + mqtt_server + ' port = ' + mqtt_port + ' client_id = ' + mqtt_client_id + ' user = ' + mqtt_username + ' pass = ' + mqtt_password + ' topic = ' + mqtt_topic + ' name = ' + gw_name +'\n')

#MQTT client
if mqtt_enable == 1:
	syslog.syslog('Opening MQTT socket: %s/%s' % (mqtt_server,mqtt_port))
	mqttclient = mqtt.Client(client_id=mqtt_client_id)
	mqttclient.username_pw_set(mqtt_username,mqtt_password)
	mqttclient.connect(mqtt_server, int(mqtt_port), 60, "")
	if mqttclient:
    		syslog.syslog('Opened MQTT socket: %s/%s' % (mqtt_server,mqtt_port))

	else:
		sys.stderr.write('Could not open MQTT\n')
		sys.exit()

#Open Syslog on ramdisk
try:
	sfile = open("/data/logs/syslog.log","r")

except IOError:
        sys.stderr.write( 'Failed to open /data/logs/syslog.log\n')
	sys.exit()

# Create Logging on USB drive
def create_timed_rotating_log(path):
	""""""
	logger = logging.getLogger('syslogrotator')
	logger.setLevel(logging.INFO)
	fh = TimedRotatingFileHandler(path, when="m", interval=int(days)*12*60, backupCount=int(numlogs) )
#	fh = TimedRotatingFileHandler(path, when="m", interval=1)
	format = logging.Formatter('%(message)s')
	fh.setFormatter(format)
	logger.addHandler(fh)

	while 1:

# is there new data
		where = sfile.tell()
		data = sfile.readline()
		if not data:
			time.sleep(1)
			sfile.seek(where)
    		else:

# send to usb drive
        		logger.info(data)

# send to mqtt
			if mqtt_enable == 1:
		        	mqttclient.publish(mqtt_topic+'/'+gw_name,payload=data,qos=0)

	sfile.close()

#Main 
if __name__ == "__main__":
	create_timed_rotating_log('/mnt/syslog.log')
