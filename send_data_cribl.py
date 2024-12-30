import logging
from splunk_data_sender import SplunkSender


splunk_conf = {
    'endpoint': 'default.main.confident-gilbert-b0v5dbx.cribl.cloud',
    'port': '8088',
    'token': '39444963-6f62-756a-7551-534c4d654177',
    'index': 'main',
    'channel': '79e6e39a-eb92-4de5-94a0-37844a3b20a3', # GUID
    'api_version': '1.0',
    # 'hostname': 'hostname',  # manually set a hostname parameter, defaults to socket.gethostname()
    # 'source': 'source',  # manually set a source, defaults to the log record.pathname
    # 'source_type': '_json',  # manually set a source_type, defaults to 'generic_single_line'
    # 'allow_overrides': True,  # Whether to look for one of the Splunk built-in parameters(index, host, ecc)
    'verify': False,  # turn SSL verification on or off, defaults to True
    # 'timeout': 60,  # timeout for waiting on a 200 OK from Splunk server, defaults to 60s
    # 'retry_count': 5,  # Number of retry attempts on a failed/erroring connection, defaults to 5
    # 'retry_backoff': 2.0,  # Backoff factor, default options will retry for 1 min, defaults to 2.0
    'enable_debug': True  # turn on debug mode; prints module activity to stdout, defaults to False
}

splunk = SplunkSender(**splunk_conf)

is_alive = splunk.get_health()
logging.info(is_alive)
if not is_alive:
    raise Exception("HEC not alive")

# The first payload is a quote to the italian theme song of Hello!Spank
txt_record = "Hello! Splunk resta con me, Hello! Splunk non te ne andare, Caro Splunk! gioca con me, siamo amici io e te."
json_record = { # this record will be parsed as normal text due to default "sourcetype" conf param
        "source": "spacecraft Discovery 1",
        "host": "HAL9000",
        # "sourcetype": "_json",  # source type without underscore to allow the override of this built-in parameter
        "index": "main",
        "event": {"message": "I am afraid I can't do that Dave.", "severity": "ERROR"},
        "rack": "42",
        "os": "Linux, obvious",
        "arch": "x64"
    }
payloads = [txt_record, json_record]

splunk_res = splunk.send_data(payloads)
logging.info(splunk_res)

ack_id = splunk_res.get('ackId')
splunk_ack_res = splunk.send_acks(ack_id)
logging.info(splunk_ack_res)