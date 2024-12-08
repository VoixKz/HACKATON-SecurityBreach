from celery import shared_task
from .parsing import main

# @shared_task
def scheduled_task():
    print('Im in tasks')
    main()