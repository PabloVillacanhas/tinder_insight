#!/bin/sh

gunicorn -w 1 run:gunicorn_app