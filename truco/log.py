import inspect
import logging
import time

def log(fn):
    from truco.arguments import exec_args

    if not exec_args.debugger:
        return fn
    
    logger = logging.getLogger()
    logging.basicConfig(format="[%(levelname)s]: %(message)s \n[%(levelname)s] End\n", level=logging.DEBUG)
    def wrapper(*args, **kwargs):
        arguments = get_args_dict(fn, *args, **kwargs)
        log_msg = "{}()\n\n> Arguments: ".format(fn.__name__)
        for name, value in arguments.items():
            log_msg += "\n>> {} : {}".format(name, value)

        start_time = time.perf_counter()
        result = fn(*args, **kwargs)
        log_msg += "\n\n> Return: {}\n\n> Time elapsed: {}\n".format(result, round(time.perf_counter() - start_time, 3))
        logger.debug(log_msg)
        return result

    return wrapper

def get_args_dict(fn, *args, **kwargs):
    args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    return {**dict(zip(args_names, args)), **kwargs}
