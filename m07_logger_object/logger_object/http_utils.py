import logging
import requests

# Используем родительский логгер "utils"
logger = logging.getLogger("utils.http")

GET_IP_URL = "https://api.ipify.org?format=json"

def get_ip_address():
    logger.debug("Start working: requesting IP")
    try:
        response = requests.get(GET_IP_URL)
        response.raise_for_status()
        ip = response.json().get("ip")
        logger.info(f"IP Address: {ip}")
        return ip
    except Exception as e:
        logger.exception("Error retrieving IP")
        return None