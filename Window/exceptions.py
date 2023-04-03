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
        print("\033[1;32m Trace doesn't contain noise \033[00m")
        return False





def find_nth_value(x,n):
    print('start')
    try:
        result = x[n]
    except IndexError as err:
        print(err)
    else:
        print("Your answer is ", result)

def ex(signal_rates: list, noise_rates: list):
    try:
        stabilizing_coef = 0
        x = 1/0
    except Exception:
        # print("\033[1;32m Signal is pure. There is no noise \033[00m")
        raise Warning("\033[1;32m Signal is pure. There is no noise \033[00m")
        print("aero")
    except TypeError:
        print("type")
    return 14