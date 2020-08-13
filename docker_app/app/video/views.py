from django.shortcuts import render
from .forms import UploadFileForm
from .models import Video
import os
import random
import string
from django.conf import settings
from .tasks import generate_thumbnail, generate_mp4, generate_webm, download_file


def handle_uploaded_files(files):
    for file in files:
        title, ext = os.path.splitext(file.name)
        mix = ''
        while True:
            try:
                rec = Video(title=title, mix=mix)
                rec.save()
            except:
                mix = '-' + ''.join(random.choice(string.ascii_letters) for _ in range(6))
            else:
                break
        filename = settings.RAW_STORAGE.save(''.join((title, mix, ext)), file)
        print(f'filename: {filename}, title: {title}, mix: {mix}')
        generate_thumbnail.delay(rec.id, filename)
        generate_mp4.delay(rec.id, filename)
        generate_webm.delay(rec.id, filename)


def main_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                handle_uploaded_files(request.FILES.getlist('files'))
            if form.cleaned_data.get('url'):
                download_file.delay(form.cleaned_data.get('url'))
    form = UploadFileForm()

    context = {
        'videos': Video.objects.all().order_by('-id'),
        'form': form,
    }
    return render(request, 'video/index.html', context)
