#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""動画ファイルから音声だけを抜き出す

準備:

1. Python3.6以降を用意
2. ffmpegをinstall
    sudo apt-get install ffmpeg


使い方:

1. このスクリプトを動画ファイルを含むディレクトリに置く
2. このスクリプト中の変数SUFFIXESに処理の対象としたい動画ファイルの拡張子を指定
2. このスクリプト中の変数OUTPUT_DIRに抜き出した音声の出力先を指定
    (既定だとこのpyファイルのあるディレクトリにoutputというディレクトリが作られ、そこに出力される)
4. このスクリプトを実行
    python3 ./extract_audio.py
"""

import subprocess
from pathlib import Path

PARENT_DIR = Path(__file__).parent.absolute()
OUTPUT_DIR = PARENT_DIR / 'output'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SUFFIXES = ('.mp4', '.mkv', 'webm', )


def extract_audio(*, inpath, outpath):
    command = (
        'ffmpeg', 
        '-i', str(inpath),
        '-acodec', 'copy', '-map',  '0:1',
        str(outpath),
    )
    with subprocess.Popen(command) as process:
        process.wait()
        print('ffmpeg return code :', process.returncode)


def find_entries(dirpath, *, recursive):
    for entry in dirpath.iterdir():
        if entry.is_dir():
            if recursive:
                yield from find_entries(entry, recursive=recursive)
        elif entry.suffix in SUFFIXES:
            yield entry


def extract_all_audio(dirpath, *, recursive):
    for path in find_entries(dirpath, recursive=recursive):
        print(path)
        extract_audio(inpath=path, outpath=OUTPUT_DIR / path.name)


if __name__ == '__main__':
    extract_all_audio(Path(), recursive=True)
