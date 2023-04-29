import itertools
import sys
import time

from threading import Event, Thread

ANIMATION_FRAME_SECONDS = 0.04
DEFAULT_LOADING_MESSAGE = 'Loading...'

FRAMES = [
    "|==========>                    |",
    " |==========>                   |",
    "  |==========>                  |",
    "   |==========>                 |",
    "    |==========>                |",
    "     |==========>               |",
    "      |==========>              |",
    "       |==========>             |",
    "        |==========>            |",
    "         |==========>           |",
    "          |==========>          |",
    "           |==========>         |",
    "            |==========>        |",
    "             |==========>       |",
    "              |==========>      |",
    "               |==========>     |",
    "                |==========>    |",
    "                 |==========>   |",
    "                  |==========>  |",
    "                   |==========> |",
    "                    |==========>|",
    "                     |==========|",
    "                      |=========|",
    "                       |========|",
    "                        |=======|",
    "                         |======|",
    "                          |=====|",
    "                           |====|",
    "                            |===|",
    "                             |==|",
    "                              |=|",
    "                               ||",
    "                               ||",
    "                               ||",
    "                               ||",
    "                               ||",
    "                               ||",
    ">                               |",
    "=>                              |",
    "==>                             |",
    "===>                            |",
    "====>                           |",
    "=====>                          |",
    "======>                         |",
    "=======>                        |",
    "========>                       |",
    "=========>                      |",
    "==========>                     |",
]


def loadable(func, loading_message):
    '''
    This decorator is used to display a loading animation
    while a function is running.

    :param func: The function to be decorated
    :param loading_message: The message to be displayed before the animation
    '''
    def wrapper(*args, **kwargs):
        # Start a thread to display the loading animation
        stop_loading = Event()
        loader_thread = Thread(target=_loading, args=(
            stop_loading, loading_message,))
        loader_thread.start()

        result = func(*args, **kwargs)

        # Stop the loading animation thread once the response is received
        stop_loading.set()
        loader_thread.join()

        return result

    return wrapper


def _loading(stop_loading, loading_message):
    while not stop_loading.is_set():
        _display_loader(stop_loading, loading_message)


def _display_loader(stop_loading, prefix=DEFAULT_LOADING_MESSAGE):
    spinner = itertools.cycle(FRAMES)
    while not stop_loading.is_set():
        sys.stdout.write(f"{prefix}{next(spinner)}")
        sys.stdout.flush()
        time.sleep(ANIMATION_FRAME_SECONDS)
        sys.stdout.write('\r')
    sys.stdout.write('\n')
