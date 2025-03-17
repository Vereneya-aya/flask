import logging
import subprocess
import shlex

# Используем родительский логгер "utils"
logger = logging.getLogger("utils.subprocess")

KERNEL_COMMAND = shlex.split("uname -r")

def get_kernel_version():
    logger.debug("Start working: getting kernel version")
    try:
        result = subprocess.run(KERNEL_COMMAND, capture_output=True, text=True, check=True)
        kernel_version = result.stdout.strip()
        logger.info(f"Kernel Version: {kernel_version}")
        return kernel_version
    except Exception as e:
        logger.exception("Error retrieving kernel version")
        return None