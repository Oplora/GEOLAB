from os import path as os_path
import numpy as np


def specific_catch(error_message: str, path):
    notification = "⊛---{2}---⊛ \033[1;32m Catched {0} : {1}\033[00m"
    if str(error_message) != "'AxesSubplot' object is not subscriptable":
        raise TypeError(error_message)
    else:
        print(notification.format(type(error_message).__name__, str(error_message), path))
    return


def noise_presence_check(noise_rates: list):
    stabilizing_coef = 0.1 * max(noise_rates)
    if any((noise_rates + stabilizing_coef)):
        return True
    else:
        # print("\033[1;32m Trace doesn't contain noise \033[00m")
        prYellow("Trace doesn't contain noise")
        return False


# COLORFUL PRINT'S
def prCyan(text):
    """SeisImage error"""
    print(f"\033[1;36m {text}\033[00m")


def prYellow(text):
    print("\033[1;32m{}\033[00m".format(text))
