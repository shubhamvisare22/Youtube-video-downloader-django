from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from .downloader import YouTubeDownloader
from django.views import View
import os
import json
from django.conf import settings


def home(request):
    return render(request, "home.html")


class DownloadView(View):
    def post(self, request):
        try:
            yt_obj = YouTubeDownloader()
            
            links = request.POST.get("link")
            resolution = request.POST.get("resolution")
            links = eval(links)
            if len(links) > 1:
                result = yt_obj.download_multiple_videos(links, resolution)
                if result.get("status"):
                    zip_file_path = result.get("zip_file_path")
                    zip_file_name = os.path.basename(zip_file_path)
                    return JsonResponse({"status": True, "zip_file_name": zip_file_name, "file_type":1})
                return JsonResponse({"status": False, "msg": result.get("msg")})
            else:
                result = yt_obj.download_single_video(links[0], resolution)                
                if result.get("status"):
                    file_path = result.get("file_path")
                    file_name = os.path.basename(file_path)
                    return JsonResponse({"status": True, "file_name": file_name, "file_type":0})
                return JsonResponse({"status": False, "msg": result.get("msg")})
                
        except Exception as e:
            print(e)
            return JsonResponse({"status": False, "msg": str(e)})
    

class DownloadFileView(View):
    def post(self, request):
        try:
            filename = json.loads(request.body).get('filename')
            
            if not filename:
                return JsonResponse({"status": False, "msg": "Filename not provided."}, status=400)

            if filename.endswith(".zip"):
                file_path = os.path.join(settings.BASE_DIR, "downloaded_videos/zip_file", filename)
            else:
                file_path = os.path.join(settings.BASE_DIR, "downloaded_videos/single_videos", filename)

            if not os.path.exists(file_path):
                return JsonResponse({"status": False, "msg": "File not found."}, status=404)

            file_ = open(file_path, 'rb')
            os.remove(file_path)
            return FileResponse(file_, as_attachment=True, filename=filename)
            
        except Exception as e:
            return JsonResponse({"status": False, "msg": str(e)}, status=500)
    