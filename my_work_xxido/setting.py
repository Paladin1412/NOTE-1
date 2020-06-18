# -*- coding: utf-8 -*-
"""
@created: 2016/11/10 
"""

import os.path
import time
import logging

log_dir = os.path.join(os.path.dirname(__file__), "log")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

LOG_LEVEL = logging.DEBUG

LOG_FORMATTER = '%(levelname)s-%(asctime)s-%(filename)s->%(funcName)s:%(lineno)d-%(message)s'

LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMATTER
        }
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, "log-%s.log" % time.strftime("%Y-%m-%d", time.localtime())),
            'encoding': 'utf8',
            'maxBytes': 1025*1024*100,
            'backupCount': 1,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': LOG_LEVEL,
        },
    }
}


MONITOR_MERGE_LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMATTER
        }
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, "monitor-merge-%s.log" % time.strftime("%Y-%m-%d", time.localtime())),
            'encoding': 'utf8',
            'maxBytes': 1025*1024*100,
            'backupCount': 1,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': LOG_LEVEL,
        },
    }
}


MONITOR_TASK_LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMATTER
        }
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, "monitor-task-%s.log" % time.strftime("%Y-%m-%d", time.localtime())),
            'encoding': 'utf8',
            'maxBytes': 1025*1024*100,
            'backupCount': 1,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': LOG_LEVEL,
        },
    }
}

WAIT_FOR_ACTIVITY_TIMEOUT = 30
