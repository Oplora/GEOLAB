from os import path as os_path


def specific_catch(error_message: str, path):
    notification = "⊛---{2}---⊛ \033[1;32m Catched {0} : {1}\033[00m"
    if str(error_message) != "'AxesSubplot' object is not subscriptable":
        raise TypeError(error_message)
    else:
        print(notification.format(type(error_message).__name__, str(error_message), path))
