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


def get_memory_usage() -> dict:
    """
    Retrieves the memory usage of the system.

    :return: (dict) The memory usage information with percentage of 
    the system used memory.
    """
    if platform.startswith("linux"):
        total, used, free, shared, cache, available = \
            check_output(["free", "-m"]).decode("utf-8").split('\n')[1].split()[1:7]
        usage_percentage = round((int(used) / int(total) * 100), 2)
        response = {
            "total": total,
            "used": used,
            "used_percentage": usage_percentage,
            "free": free,
            "shared": shared,
            "cache": cache,
        }
        return response


def send_request(message: dict, url: str) -> int | None:
    """
    Sends an HTTP POST request to a specified URL with information about 
    the memory usage.
    
    :param message: (dict) Request message.
    :param url: (str) Specify alarm http request to api.
    :return: (int or None) Return status code of http response or 
    nothing if success.
    """
    timeout = 5
    
    try:
        response = requests.post(url, timeout=timeout, json=message)
        response.raise_for_status()
        logger.info("Request sent successfully. %s", message)
        
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
    default="http://127.0.0.1:8080/reports/", 
    help="URL of http request to api"
    )
def check(memory_usage: int, request_url: str):
    """
    Monitor system memory consumption every second and generate HTTP POST
    request to specific api when memory usage exceeds a certain threshold.
    """
    while True:
        current_memory_info = get_memory_usage()
        current_memory_usage = current_memory_info["used_percentage"]
        if current_memory_usage >= memory_usage:
            send_request(current_memory_info, request_url)
            sleep(1)
            

if __name__ == "__main__":
    check()
    