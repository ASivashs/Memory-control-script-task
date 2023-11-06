import requests
import click

from sys import platform
from subprocess import check_output
from time import sleep
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("memory_control.log")
    ]
)

logger = logging.getLogger(__name__)


def get_memory_usage() -> float:
    """
    Retrieves the memory usage of the system.

    This function determines the memory usage of the system by executing a 
    platform-specific command 'free -m' to obtain information about the total 
    and used memory. It specifically targets Linux systems. The function 
    calculates the usage percentage by dividing the used memory by the total 
    memory and multiplying by 100.

    :return: (float) The memory usage percentage of the system.
    """
    if platform.startswith("linux"):
        total_memory, used_memory = \
            check_output(["free", "-m"]).decode("utf-8").split('\n')[1].split()[1:3]
        usage_percentage = int(used_memory) / int(total_memory) * 100
        return usage_percentage


def send_request(used_memory: int, url: str) -> int | None:
    """
    Sends an HTTP POST request to a specified URL with information about 
    the used memory.
    
    This function constructs a request message that includes the used memory 
    value and an optional message. It then attempts to send the request using 
    the `requests.post()` method. The request is sent with a timeout of 5 seconds.
    
    :param used_memory: (int) Represent used memory percentage of system.
    :param url: (str) Specify alarm http request to api.
    :return: (int or None) Return status code of http response or nothing.
    """
    used_memory = "{:.2f}".format(used_memory)
    request_message = {
        "memory_usage": used_memory,
        "message": f"Memory is {used_memory}% full.",
    }
    timeout = 5
    
    try:
        response = requests.post(url, timeout=timeout, json=request_message)
        response.raise_for_status()
        logger.info("Request sent successfully. %s", request_message)
        
    except requests.Timeout as err:
        logger.error("Timeout: %s.", err)
        
    except requests.exceptions.RequestException as err:
        logger.error("Request exception: %s.", err)
        
    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        logger.error("Http exception: %s. Status code: %i.", err, status_code)
        
    except Exception as err:
        logger.error("Exception: %s.", err)
    
    else:
        return response.status_code
    return


@click.command()
@click.option(
    "-m", 
    "--memory-usage", 
    type=float, 
    default=80., 
    help="System memory usage in percent"
    )
@click.option(
    "-r", 
    "--request-url", 
    type=str, 
    default="http://127.0.0.1:5000/alarm", 
    help="URL of http request to api"
    )
def check(memory_usage: int, request_url: str):
    """
    Monitor system memory consumption every second and generate an alarm when 
    memory usage exceeds a certain threshold.
    """
    while True:
        current_memory = get_memory_usage()
        if current_memory >= memory_usage:
            send_request(get_memory_usage(), request_url)
            sleep(1)
            

if __name__ == "__main__":
    check()
    