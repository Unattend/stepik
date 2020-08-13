import os
import random
import string
import logging
from django.conf import settings
import requests
from stepik.celery import app
from .models import Video
import ffmpeg


@app.task
def generate_thumbnail(id, filename):
    print(id)
    record = Video.objects.get(id=id)
    input = settings.RAW_STORAGE.path(filename)
    output = os.path.join(settings.PREW_STORAGE.location, ''.join((record.title, record.mix, '.jpg')))
    logging.info(f'ffmpeg create preview:{output} for {record.title}')
    try:
        (
            ffmpeg.input(input, ss=5)
                .filter('scale', 640, 360)
                .output(output, vframes=1)
                .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        logging.exception(e.stderr)
    else:
        Video.objects.filter(title=record.title, mix=record.mix).update(has_prew=True)

    if all([record.has_prew, record.has_mp4, record.has_webm]):
        settings.RAW_STORAGE.delete(filename)


@app.task
def generate_mp4(id, filename):
    record = Video.objects.get(id=id)
    input = settings.RAW_STORAGE.path(filename)
    output = os.path.join(settings.MP4_STORAGE.location, ''.join((record.title, record.mix, '.mp4')))
    logging.info(f'ffmpeg create mp4: {output} for: {record.title}')
    try:
        (
            ffmpeg.input(input)
                .filter('scale', 640, 360)
                .output(output)
                .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        logging.exception(e.stderr)
    else:
        Video.objects.filter(title=record.title, mix=record.mix).update(has_mp4=True)

    if all([record.has_prew, record.has_mp4, record.has_webm]):
        settings.RAW_STORAGE.delete(filename)


@app.task
def generate_webm(id, filename):
    record = Video.objects.get(id=id)
    input = settings.RAW_STORAGE.path(filename)
    output = os.path.join(settings.WEBM_STORAGE.location, ''.join((record.title, record.mix, '.webm')))
    logging.info(f'ffmpeg create webm: {output} for: {record.title}')
    try:
        (
            ffmpeg.input(input)
                .filter('scale', 640, 360)
                .output(output)
                .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        logging.exception(e.stderr)
    else:
        Video.objects.filter(title=record.title, mix=record.mix).update(has_webm=True)

    if all([record.has_prew, record.has_mp4, record.has_webm]):
        settings.RAW_STORAGE.delete(filename)


@app.task
def download_file(url):
    filename = url.split('/')[-1]
    title, ext = os.path.splitext(filename)
    mix = ''
    while True:
        try:
            rec = Video(title=title, mix=mix)
            rec.save()
        except:
            mix = '-' + ''.join(random.choice(string.ascii_letters) for _ in range(6))
        else:
            break
    filename = ''.join((title, mix, ext))
    output = os.path.join(settings.RAW_STORAGE.location, filename)

    logging.info(f'downloading from: {url} to: {output}')
    with requests.get(url, stream=True) as r:
        try:
            r.raise_for_status()
            with open(output, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        except:
            rec.delete()
            logging.exception(f'error in downloading {url}')
        else:
            print(f'filename:{filename}')
            generate_thumbnail.delay(rec.id, filename)
            generate_mp4.delay(rec.id, filename)
            generate_webm.delay(rec.id, filename)
