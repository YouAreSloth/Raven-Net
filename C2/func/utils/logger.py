import logging
from datetime import datetime

# Configure the logging
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(message)s')

def log(self, input: str, type: str):
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_message = f"{timestamp} [{type}] {input}"

    match type:
        case "generic":
            self.stdout.write(f"\033[94m{input}\033[0m")
        case "error":
            self.stdout.write(f"\033[91m{input}\033[0m")
        case "debug":
            self.stdout.write(f"\033[92m{input}\033[0m")
        case _:
            print("Unknown type")

    logging.debug(log_message)