#!/bin/bash

mkdir /media/raw
mkdir /media/prew
mkdir /media/mp4
mkdir /media/webm

# TODO change to mount vith correct uid in manifests
chmod 777 /media/* -R

apt-get update
apt-get install -y ffmpeg
celery -A stepik worker -l info --uid=nobody
#celery -A stepik worker -l info
