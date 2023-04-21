from pprint import pprint
import time

def log(fn):
    from main import exec_args

    if not exec_args.debbuger:
        return fn
    
    def wrapper(*args, **kwargs):
        print("\n--- DEBBUGER ---\n")
        print(f"> Function: {fn.__name__}")
        print(f"> Arguments:")
        arguments = get_args_dict(fn, *args, **kwargs)
        for name, value in arguments.items():
            print(f">> {name} = [{value}]")

        start_time = time.time()
        result = fn(*args, **kwargs)
        print(f"\n[DEBUG] Result: {result}")
        print(f"[DEBUG] Time spent: {round(time.time() - start_time, 3)}s\n")
        print("----------------\n")
        return result

    return wrapper

def get_args_dict(fn, *args, **kwargs):
    args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    return {**dict(zip(args_names, args)), **kwargs}
