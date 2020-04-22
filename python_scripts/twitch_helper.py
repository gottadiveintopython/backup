r"""streamlinkを使ってTwitchを見る時のHelperスクリプト

Usage:
    twitch_helper.py auth
    twitch_helper.py live <username> <quality>
    twitch_helper.py chat <username>
    twitch_helper.py past <username> <video_id> <quality>
    twitch_helper.py down <username> <video_id> <quality>
    twitch_helper.py -h | --help

Options:
    -h --help   Show this screen.
    auth        認証KeyをWebBrowserで確めたい時のコマンド
    live        ライブ配信を観たい時のコマンド
    chat        chatを開きたい時のコマンド
    past        過去配信を観たい時のコマンド
    down        過去配信を落としたい時のコマンド
    <username>  配信者のTwitchユーザーID
    <video_id>  動画のID
    <quality>   画質

Requirements:
    pip install docopt streamlink

Description:
    最初にすべき事:
        1. メディアプレイヤーへのパスと渡したいパラメータをこのScriptファイル中の
           変数PLAYERに書き込む
        2. $ twitch_helper.py --auth を実行するとWebBrowserが立ち上がるので、その
           時のURLの access_token=xxxxxx の xxxxxx をこのScriptファイル中の変数
           OAUTH_TOKENに書き込む
        3. 動画の保存先ディレクトリをこのScriptファイル中の変数VIDEO_OUTPUTに書き
           込む
"""

import os
import os.path
import subprocess
import webbrowser

import docopt


PLAYER = 'vlc'
OAUTH_TOKEN = 'your oauth token'
VIDEO_OUTPUT = '/somewhere/output_directory'
URL_PREFIX = 'https://www.twitch.tv/'


def main():
    doargs = docopt.docopt(__doc__)
    for key, value in doargs.items():
        print('{} : {}'.format(key, value))

    if doargs['auth']:
        get_oauth_token()
        return

    username = doargs['<username>']
    quality = doargs['<quality>']

    if doargs['chat']:
        open_chat(url='{}{}/chat?popout='.format(URL_PREFIX, username))
        return

    if doargs['live']:
        watch_video(url=URL_PREFIX + username, quality=quality)
        return

    video_id = doargs['<video_id>']

    if doargs['past']:
        video_url = '{}{}/v/{}'.format(URL_PREFIX, username, video_id)
        watch_video(url=video_url, quality=quality)
        return
    elif doargs['down']:
        down_video(username=username, video_id=video_id, quality=quality)
        return


def down_video(*, username, video_id, quality):
    output_dir = os.path.join(VIDEO_OUTPUT, username)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, video_id) + '.mp4'
    url = '{}{}/v/{}'.format(URL_PREFIX, username, video_id)
    command = [
        "streamlink",
        "--twitch-oauth-token", OAUTH_TOKEN,
        '--output', output_path,
        url,
        quality
    ]
    with subprocess.Popen(command) as process:
        process.wait()
        print("streamlink return code :", process.returncode)


def watch_video(*, url, quality):
    command = [
        "streamlink",
        "--twitch-oauth-token", OAUTH_TOKEN,
        '--player', PLAYER,
        url,
        quality
    ]
    with subprocess.Popen(command) as process:
        process.wait()
        print("streamlink return code :", process.returncode)


def get_oauth_token():
    command = [
        "streamlink",
        "--twitch-oauth-authenticate",
    ]
    with subprocess.Popen(command) as process:
        process.wait()
        print("streamlink return code :", process.returncode)


def open_chat(*, url):
    webbrowser.open(url)


if __name__ == '__main__':
    main()
