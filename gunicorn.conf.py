import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "workers.ConfigurableUvicornWorker"
timeout = 120

accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "debug")
