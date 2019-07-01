"""Useful decorators for facilitating logging"""
import functools


def log_call(log):
    """Decorates a function and debug logs a call with arguments representations"""
    def internal_log_call(func):
        @functools.wraps(func)
        def wrapper_log_call(*args, **kwargs):
            args_repr = [repr(x) for x in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            log.debug(f"Calling {func.__name__}({signature})")
            return func(*args, **kwargs)
        return wrapper_log_call
    return internal_log_call
