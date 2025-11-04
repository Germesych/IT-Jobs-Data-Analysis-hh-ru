import time
import psutil
import os
from datetime import timedelta
import functools
import asyncio


def timeit(func):
    """
    Декоратор для измерения времени выполнения, пикового CPU и памяти.
    Работает с синхронными и асинхронными функциями.
    Возвращает кортеж: (результат_функции, stats), где stats — словарь с метриками.
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        start_time = time.perf_counter()
        start_mem = process.memory_info().rss / 1024 / 1024  # MB
        start_cpu = process.cpu_percent(interval=0.1)

        result = await func(*args, **kwargs)

        end_time = time.perf_counter()
        end_mem = process.memory_info().rss / 1024 / 1024  # MB
        end_cpu = process.cpu_percent(interval=0.1)

        duration = timedelta(seconds=end_time - start_time)
        formatted_duration = str(duration).split('.')[0]
        peak_mem = max(start_mem, end_mem)
        peak_cpu = max(start_cpu, end_cpu)

        stats = {
            "duration": formatted_duration,
            "peak_mem_mb": peak_mem,
            "peak_cpu_percent": peak_cpu,
        }

        print(f"Сбор данных выполнился за {formatted_duration}")
        print(f"Пиковое потребление памяти: {peak_mem:.2f} MB")
        print(f"Пиковое использование CPU: {peak_cpu:.1f}%")

        return result, stats

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        start_time = time.perf_counter()
        start_mem = process.memory_info().rss / 1024 / 1024  # MB
        start_cpu = process.cpu_percent(interval=0.1)

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        end_mem = process.memory_info().rss / 1024 / 1024  # MB
        end_cpu = process.cpu_percent(interval=0.1)

        duration = timedelta(seconds=end_time - start_time)
        formatted_duration = str(duration).split('.')[0]
        peak_mem = max(start_mem, end_mem)
        peak_cpu = max(start_cpu, end_cpu)

        stats = {
            "duration": formatted_duration,
            "peak_mem_mb": peak_mem,
            "peak_cpu_percent": peak_cpu,
        }

        print(f"Сбор данных выполнился за {formatted_duration}")
        print(f"Пиковое потребление памяти: {peak_mem:.2f} MB")
        print(f"Пиковое использование CPU: {peak_cpu:.1f}%")

        return result, stats

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
