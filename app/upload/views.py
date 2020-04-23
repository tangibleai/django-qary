from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import logging
log = logging.getLogger(__name__)


def image_upload(request):
    log.warn(f"image_upload: {request}")
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        log.warning(f"image_file: {image_file}")
        log.warning(f"vars(image_file): {image_file}")
        if image_file.name.lower().endswith('.md'):
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            image_url = fs.url(filename)
            log.warning(f"django.core.files.storage.FileSystemStorage: {fs}")
            return render(request, "upload.html", {
                "image_url": image_url
            })
    return render(request, "upload.html")
