from subprocess import call
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import request


def download_playlist():
    file1 = open('./playlists.txt', 'r')
    lines = file1.readlines()

    count = 0
    for line in lines:
        count += 1
        url = line.strip()
        print("Processing playlist nr{}: {}".format(count, url))
        call(["youtube-dl", url, "--audio-format", "mp3", "-x", "--yes-playlist", "--download-archive", "records.txt",
              "-o", "/music/%(playlist)s/%(title)s.%(ext)s"])


sched = BackgroundScheduler()
sched.add_job(download_playlist, 'cron', month='*', day='*', hour='04', minute='*', max_instances=1)
sched.start()

app = Flask(__name__)


@app.route('/download/')
def download():
    url = request.args.get('url', default=1, type=str)
    print(str(url))
    call(["youtube-dl", url, "--audio-format", "mp3", "-x", "--yes-playlist", "--download-archive", "records.txt",
          "-o", "/music/%(playlist)s/%(title)s.%(ext)s"])

    return 'starting...'


if __name__ == "__main__":
    app.run()
