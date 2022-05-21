from subprocess import call
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask


on = False


def download_playlist():
    global on
    if not on:
        try:
            on = True
            files = open('/data/playlists.txt', 'r')
            lines = files.readlines()

            count = 0
            for line in lines:
                count += 1
                url = line.strip()
                print("Processing playlist nr{}: {}".format(count, url))
                call(["youtube-dl", url, "-f", "bestaudio", "--extract-audio", "--audio-format", "mp3", "-x",
                      "--yes-playlist", "--download-archive", "/data/records.txt", "-o",
                      "/music/%(playlist)s/%(title)s.%(ext)s", "--embed-thumbnail", "--add-metadata",
                      "--postprocessor-args", "-id3v2_version 3"])
                # youtube-dl https://www.youtube.com/playlist?list=PLv3TTBr1W_9tppikBxAE_G6qjWdBljBHJ -f bestaudio --extract-audio --audio-format mp3 -x --yes-playlist --download-archive records.txt -o '/%(playlist)s/%(title)s.%(ext)s' --embed-thumbnail --add-metadata --postprocessor-args '-id3v2_version 3'
                on = False
        except:
            on = False
            download_playlist()
    else:
        print("waiting")

sched = BackgroundScheduler()
sched.add_job(download_playlist, 'cron', month='*', day='*', hour='*', minute='1, 15, 30, 45', max_instances=1)
sched.start()

app = Flask(__name__)


@app.route('/restart')
def download():
    download_playlist()
    return 'restart...'


if __name__ == "__main__":
    app.run()
