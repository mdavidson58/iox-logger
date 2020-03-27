# iox-logger
App to store syslog and SNMP Traps from IR 8x9 devices permanent to USB flash.  Also can remotely configure remote syslog server and syslog via MQTT.  The default config can be used with the following advanced template.


The following package_config.ini file controls aspects of this application:

[mqtt] mqtt_enable = 0 # enabled = 1 disabled = 0
mqtt_server = 10.0.0.144. # IP address of northbound MQTT server
mqtt_port = 1883 # port of northbound MQTT Server
mqtt_client_id = ir8x9 # client id of MQTT client
mqtt_username = mark #mqtt user name
mqtt_password = mark # mqtt password
mqtt_topic = RAMA # TOPIC used to store logging data

[logs]
rotate_days = 1 # Number of days before rotating logs to a new log file
num_logs = 5 # number of logs to store on the USB Flash drive
syslog_server2 = # IP address if sending logs to a remote syslog server. Blank if no other syslog server

The following lines must be set in the GMM advanced template

snmp-server host ${gw.ip_prefix}.${gw.ip_suffix?number + 1} public udp-port 3162
logging host ${gw.ip_prefix}.${gw.ip_suffix?number + 1} protocol udp port 3514
snmp-server community public RO

The docker with the pre-built application is here:

docker pull mdavidson58/iox_logger:2.5
