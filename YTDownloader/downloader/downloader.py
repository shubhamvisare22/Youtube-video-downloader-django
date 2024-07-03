from pytube import YouTube
import os
import zipfile
from pytube.exceptions import VideoUnavailable, PytubeError


class YouTubeDownloader:
    SINGLE_DOWNLOAD_PATH = "./downloaded_videos/single_videos"
    ZIP_DOWNLOAD_PATH = "./downloaded_videos/zip_file"

    def __init__(self):
        os.makedirs(self.SINGLE_DOWNLOAD_PATH, exist_ok=True)
        os.makedirs(self.ZIP_DOWNLOAD_PATH, exist_ok=True)

    def _download_video(self, link, resolution, output_path):
        try:
            yt_obj = YouTube(link)
        except VideoUnavailable:
            return {"status": False, "msg": "Video is not available"}
        except PytubeError as e:
            return {"status": False, "msg": str(e)}
        except Exception as e:
            return {"status": False, "msg": str(e)}

        stream_list = yt_obj.streams.filter(file_extension='mp4')
        try:
            for stream in stream_list:
                if stream.resolution == resolution:
                    file_path = stream.download(output_path=output_path)
                    return {"status": True, "msg": "Video downloaded.", "file_path": file_path}
            return {"status": False, "msg": "Video is not available for the given resolution."}

        except Exception as e:
            return {"status": False, "msg": "Something went wrong. " + str(e)}

    def download_single_video(self, link, resolution):
        return self._download_video(link, resolution, self.SINGLE_DOWNLOAD_PATH)

    def download_multiple_videos(self, links, resolution):
        downloaded_files = []
        for link in links:
            result = self._download_video(link, resolution, self.SINGLE_DOWNLOAD_PATH)
            if result.get("status"):
                downloaded_files.append(result.get("file_path"))
            else:
                return {"status": False, "msg": result.get("msg")}

        if downloaded_files:
            zip_file_path = os.path.join(self.ZIP_DOWNLOAD_PATH, "output_videos.zip")
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for file in downloaded_files:
                    zipf.write(file, os.path.basename(file))
                    os.remove(file)
            return {"status": True, "msg": "Videos downloaded and zipped.", "zip_file_path": zip_file_path}
        return {"status": False, "msg": "Something went wrong."}
