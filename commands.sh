#!/bin/bash
#/etc/init.d/nginx start
#nohup conda run -n Sprint bash -c 'uwsgi uwsgi_config.ini > /dev/tty 2>&1'
conda run -n Sprint bash -c 'uwsgi --http :80 --wsgi-file Sprint/wsgi.py --enable-threads --static-map /static=/app/staticfiles --threads 10 --harakiri 1200 > /dev/tty 2>&1'