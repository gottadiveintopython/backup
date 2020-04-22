#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""youtubeの動画を落とすためのScript

準備:

1. Python3.6以降を用意
2. youtube-dlをinstall又はupdate
    python3 -m pip install youtube-dl
    python3 -m pip install youtube-dl --upgrade


使い方:

1. このスクリプトを動画を落としたいディレクトリに置く
2. このスクリプト中の変数URLに落としたい動画のURLを書き込む。(コマンドライン引数で
   URLを渡す場合は不要)

    単一の動画の場合:
        https://www.youtube.com/watch?v=xxxxxxxxx
    Playlistの場合:
        https://www.youtube.com/playlist?list=xxxxxxxx
    Channelの場合:
        https://www.youtube.com/channel/xxxxxxxx
    Userの動画を全部落としたい場合
        https://www.youtube.com/user/xxxxxxxx

3. このスクリプト中の変数command内のyoutube-dlへ渡す引数を自分好みに変更
4. このスクリプトを実行
    python3 ./youtube-dl-helper.py
    または
    python3 ./youtube-dl-helper.py https://www.youtube.com/xxxxxxxxxxx
"""


import subprocess
from pathlib import Path


URL = r'https://www.youtube.com/watch?v=a1-ina4tKVg'


def download(*, url):
    PARENT_DIR = Path(__file__).parent.absolute()

    command = (
        'youtube-dl',

        # 落とす動画を2017/01/01より後に限定
        # '--dateafter', '20170101',

        # 落とす動画を2018/01/01より前に限定
        # '--datebefore', '20180101',

        # 字幕ファイルも落とす
        # '--write-sub',

        # 落とす字幕ファイルの言語を指定
        # この例だと 英語,繁体中國語,日本語,韓國語
        # '--sub-lang', 'en,zh-Hant,zh-TW,zh-HK,ja,ko',

        # 落とす動画の品質を指定
        # 特に指定しなければ自動的に最高品質が落とされる。この例だと360p
        # '--format', '18',

        # '--format', '137+140', '--merge-output-format', 'mkv',

        # 既定では動画は新しい物から落とされるが、この引数を与える事で古い物から落
        # とせる
        '--playlist-reverse',

        # 動画を実際には落とさずにどの動画が落とされるのか確認したい時に使う引数
        # '--get-filename',

        # 落とす動画のサイズに上限を設ける
        # この例だと 1000 mega bytes
        '--max-filesize', '1000m',

        # 最大Download件数
        '--max-downloads', '20',

        '--output', str(PARENT_DIR / r'%(upload_date)s.%(title)s.%(ext)s'),
        '--download-archive', str(PARENT_DIR / 'history.txt'),
        url,
    )
    with subprocess.Popen(command) as process:
        process.wait()
        print('youtube-dl return code :', process.returncode)


if __name__ == '__main__':
    from sys import argv
    download(url=URL if len(argv) == 1 else argv[1])
