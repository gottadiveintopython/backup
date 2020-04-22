# LinuxでAnimeEffectsのbuildに成功した手順のmemo

## 環境

- OS : Ubuntu 16.04 LTS 派生
- CPU : 64bit

## Qt5.7以降をInstall

[ここ](https://download.qt.io/archive/qt/5.12/5.12.0/)より`qt-opensource-linux-x64-5.12.0.run`を落として実行。この時、管理者権限である必要はない。そしてOSには元からQt4が入っているらしいのでそれよりも先に検索されるようにPATHをいじる。

```
$ export PATH=<Qtのinstall先>/5.12.0/gcc_64/bin:$PATH
```

## Anime AnimeEffectsをbuild

[source code](https://github.com/hidefuku/AnimeEffects)を落としたらその中にある`src`というdirectoryの中に入り

```
$ qmake
```

すると`Makefile`が出来上がっているはずなので

```
$ make
```

すると

```
/usr/bin/ld: warning: libicui18n.so.56, needed by <Qtのinstall先>/5.12.0/gcc_64/lib/libQt5Core.so, not found (try using -rpath or -rpath-link)
/usr/bin/ld: warning: libicuuc.so.56, needed by <Qtのinstall先>/5.12.0/gcc_64/lib/libQt5Core.so, not found (try using -rpath or -rpath-link)
/usr/bin/ld: warning: libicudata.so.56, needed by <Qtのinstall先>/5.12.0/gcc_64/lib/libQt5Core.so, not found (try using -rpath or -rpath-link)
<Qtのinstall先>/5.12.0/gcc_64/lib/libQt5Core.so: undefined reference to `u_strToLower_56'
<Qtのinstall先>/5.12.0/gcc_64/lib/libQt5Core.so: undefined reference to `ucnv_getStandardName_56'
<Qtのinstall先>/5.12.0/gcc_64/lib/libQt5Core.so: undefined reference to `ucnv_getAlias_56'
.
.
.
```

と言う風に怒られたので、`AnimeEffects/src/gui/gui.pro`内の以下の部分を

```
gcc:LIBS            += \
    -L"$$OUT_PWD/../ctrl/" -lctrl \
    -L"$$OUT_PWD/../core/" -lcore \
    -L"$$OUT_PWD/../img/"  -limg \
    -L"$$OUT_PWD/../gl/"   -lgl \
    -L"$$OUT_PWD/../cmnd/" -lcmnd \
    -L"$$OUT_PWD/../thr/"  -lthr \
    -L"$$OUT_PWD/../util/" -lutil \
```

以下のように変更。

```
gcc:LIBS            += \
    -L"$$OUT_PWD/../ctrl/" -lctrl \
    -L"$$OUT_PWD/../core/" -lcore \
    -L"$$OUT_PWD/../img/"  -limg \
    -L"$$OUT_PWD/../gl/"   -lgl \
    -L"$$OUT_PWD/../cmnd/" -lcmnd \
    -L"$$OUT_PWD/../thr/"  -lthr \
    -L"$$OUT_PWD/../util/" -lutil \
    -licudata -licuuc -licui18n
```

再度

```
$ make
```

とした所、何とか`AnimeEffects`という実行形式のfileに生成成功。ただしこれを実行する前には

```
$ export LD_LIBRARY_PATH=<Qtのinstall先>/5.12.0/gcc_64/lib
```

という風に共有ライブラリの場所を教えてあげないといけない。なので正しくbuildはできてないのかもしれないが、動くので問題ない。
