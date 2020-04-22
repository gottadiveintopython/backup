# Markdownで書いた文書をkindleに持っていくまで

ここに書かれた手順に従うことでmarkdownから

- 埋め込んだソースコードが色付けされて
- 論理目次付きで
- kindle storeにupload可能な

epub3形式の文書を作れる。  

### pandocをinstall

```
$ sudo apt-get install pandoc
```

pipにもpandocというパッケージがありますが、それをinstallしたからといって`pandoc`コマンドが使えるようにはならないので`apt-get`で入れたほうが良いと思う。

### 書いたmarkdown文書をpandoc向けに修正

##### 文書のmetadata(主題、副題、著者、制作者などの情報)を書く

書いたmarkdownの先頭に以下の物を書き加える。

```yaml
---
title:
- type: main
  text: ここに本の主題を書く
- type: subtitle
  text: ここに本の副題を書く
creator:
- role: author
  text: ここに制作者の名前を書く
rights: ここに著者の名前を書く
lang: ja
...
```

pandocは独自拡張したmarkdown形式を扱えるようになっていて、これがそれを利用したmetadataの書き方。他にもコマンドラインオプション(`--epub-metadata`)からmetadataを渡す方法もあるようである。

##### 色付け不要な場合は"default"

````
```
これ
```
````

或いは

````
```text
これ
```
````

のような色付け不要な成形済み文字列は

````
```default
こんな風に
```
````

defaultを指定してあげれば、色付けのthemeにそった背景色が付けられる。背景色が不要ならしなくていい。

### 埋め込んだソースコードの色付けのtheme

```
$ pandoc --list-highlight-styles
```

と打つと

```
pygments
tango
espresso
zenburn
kate
monochrome
breezedark
haddock
```

出てくる。これらが色付けのtheme。この中から好きなthemeを選んで

```
$ pandoc --highlight-style espresso 略
```

のように指定してあげる。既存のthemeを元に独自のthemeを作りたい場合は、元にしたいthemeの定義fileを以下のように出力して

```
$ pandoc --print-highlight-style espresso > ./custom_espresso.theme
```

出てきた[custom_espresso.theme](custom_espresso.theme)を自分好みに弄った後、

```
$ pandoc --highlight-style espresso 略
```

に代えて

```
$ pandoc --highlight-style ./custom_espresso.theme 略
```

と指定してあげればいい。ここでfileの拡張子は`.theme`でないといけないのが注意点。

### 表の罫線

既定ではmarkdownで書いた表に全く線が引かれない。これを変えたいなら例えばこのような[cssファイル](custom.css)を書いてコマンドライン引数(`--css`)で教える必要がある。

### 最終的なコマンド

以上の事を踏まえて最終的なコマンドは

```
$ pandoc --highlight-style <好きなtheme> --css <cssファイル名> -t epub3 -o <出力先file名> <入力file名(複数可)>
```

となる。尚コマンドを実行する時は入力fileのあるdirectoryをカレントディレクトリにした方が良い。(じゃないと画像fileがうまくepubに詰め込まれなかった)。
