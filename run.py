import requests
import bs4
import yt_dlp
import multiprocessing
import os

VAVRUSKA_SYLABUS_URL = 'https://www.vavruska.info/video-sylabus/?action=login'
PASSWORD_FILE = 'passwords'
OUTPUT_FOLDER = 'videos'


class VavruskaDownloader:
    """Download Vavruska YT videos."""

    def __init__(self, passwords_filename: str, output_folder: str):
        self.passwords_filename = passwords_filename
        self.output_folder = output_folder

        self.passwords: list[str] = []
        self._load_passwords()

    def _load_passwords(self) -> None:
        with open(self.passwords_filename) as file:
            for line in file.readlines():
                line = line.strip()
                self.passwords.append(line)

    def download(self) -> None:
        """Download all YT videos from syllabus."""
        youtube_links_to_download = []

        for password in self.passwords:
            youtube_links_to_download.extend(self._get_links(password))

        with multiprocessing.Pool(os.cpu_count()) as pool:
            pool.map(self._download_videos, youtube_links_to_download)

    def _get_links(self, password: str) -> list[str]:
        session = requests.sessions.Session()
        response = session.post(
            VAVRUSKA_SYLABUS_URL,
            data={'password': password}
        )

        parsed_page = bs4.BeautifulSoup(response.text, 'html.parser')
        youtube_links_to_download = []

        for iframe in parsed_page.find_all('iframe'):  # YT videos are iframes
            youtube_link = iframe.get('src')

            youtube_links_to_download.append(youtube_link)

        return youtube_links_to_download

    def _download_videos(self, youtube_links: list[str]) -> None:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{OUTPUT_FOLDER}/%(title)s.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(youtube_links)


vd = VavruskaDownloader(PASSWORD_FILE, OUTPUT_FOLDER)
vd.download()
