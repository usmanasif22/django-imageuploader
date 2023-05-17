from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from .models import Image
import os
from django.conf import settings
import uuid


def upload(request):
    if request.method == 'POST' and request.FILES.get("image"):
        image = request.FILES["image"]
        filename = f"{request.POST.get('caption')}"
        file_path = default_storage.save(f"images/{filename}.png", image)
        image_obj = Image()
        image_obj.image_url = file_path
        image_obj.caption = filename
        image_obj.save()
        return JsonResponse({"status":'success',"id":image_obj.id,"file_path": file_path})
    else:
        return JsonResponse({"status":'error',"messgae": "No file Attached"})

def get_image(request):
    try:
        image_obj = Image.objects.get(caption=request.GET.get('name'))
        if image_obj:
            image_path = image_obj.image_url
            # image_path = f"images/{request.GET.get('name')}.png"
            if os.path.exists(image_path):
                with open(image_path,'rb') as file:
                    image = file.read()
                return HttpResponse(image, content_type='image/png')
        else:
            return HttpResponse("Image Not found",status=404)
    except Exception as exc:
        return HttpResponse(f"Image Not Found | {exc}")