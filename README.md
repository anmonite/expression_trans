# expression_trans
このPythonパッケージは、日本語テキストを形態素解析モジュール"[SudachiPy](https://github.com/WorksApplications/SudachiPy)"を利用して解析し、指定した変換モデルに従って口調変換するものです。

標準の口調変換モデルは、アニメ「狼と香辛料」の"ホロ"の花魁風言葉ですw

オリジナル(Java)の"Sudachi"について詳細はQiitaの[Elasticsearchのための新しい形態素解析器 「Sudachi」](https://qiita.com/sorami/items/99604ef105f13d2d472b)をご覧下さい。

開発の経緯はQiitaに投稿した「[雑談ボットの応答テキストを「狼と香辛料」のホロの花魁言葉っぽい口調にした](https://qiita.com/anmorenight/items/3be08333d85648faad43)」をご覧ください。

## 機能
日本語テキストを"SudachiPy"で形態素解析し、口調変換モデルのパターンファイル(json)の定義に従って文言を置換して口調を変換します。

- カスタムモデル
    + 新たなjsonパターンファイルを作成することで他の口調モデルを選択できます。
      (例、他のアニメキャラクターや方言など)
- 確認用に、"SudachiPy"による形態素解析結果だけを返すこともできます。

## 動作確認環境

- AWS t2.maicro Linux (mem:1GB swap:2GB)にて開発・動作確認
- Python3.6+ (Python 3.0系なら問題ないと思います)

## インストール

```
$ git clone git@github.com:anmonite/expression_trans.git
$ cd expression_trans
$ pip install -e .
```

## 使い方
- command line:
```
    $ python3 expression_trans.py
    INPUT TEXT (exit = n) > 私が惚れたら困ります。
    
    Original text:
    -----
    私が惚れたら困ります。
    -----
    Processing log:
    -----
    Translate honorific words:
    -----
    Nothing to translate in text.
    -----
    
    Translate specific words:
    -----
    Nothing to translate in text.
    -----
    
    Morphological analisis after replacement:
    -----
    > 私    代名詞,*,*,*,*,*        私      私      ワタクシ
    > が    助詞,格助詞,*,*,*,*     が      が      ガ
    > 惚れ  動詞,一般,*,*,下一段-ラ行,連用形-一般   惚れる  惚れる  ホレ
    > たら  助動詞,*,*,*,助動詞-タ,仮定形-一般      た      た      タラ
    > 困り  動詞,一般,*,*,五段-ラ行,連用形-一般     困る    困る    コマリ
    > ます  助動詞,*,*,*,助動詞-マス,終止形-一般    ます    ます    マス
    > 。    補助記号,句点,*,*,*,*   。      。      キゴウ
    
    -----
    0: 私   代名詞,*,*,*,*,*        私      私      ワタクシ
    Found keyword: "私"
    Translated: わっち
    Translate noun token: 私 > わっち
    
    1: が   助詞,格助詞,*,*,*,*     が      が      ガ
    Nothing to translate: が > が
    
    2: 惚れ 動詞,一般,*,*,下一段-ラ行,連用形-一般   惚れる  惚れる  ホレ
    Translate (last)verb token: 惚れ > 惚れ
    
    3: たら 助動詞,*,*,*,助動詞-タ,仮定形-一般      た      た      タラ
    Nothing to translate: たら > たら
    
    4: 困り 動詞,一般,*,*,五段-ラ行,連用形-一般     困る    困る    コマリ
    Found keyword: "困り"
    Translated: 困りんす
    Translate (last)verb token: 困り > 困りんす
    
    6: 。   補助記号,句点,*,*,*,*   。      。      キゴウ
    Nothing to translate: 。 > 。
    
    -----
    Translated text:
    -----
    わっちが惚れたら困りんす。
    -----
    INPUT TEXT (exit = n) > 
```
- command line option
  - -v : 変換中の詳細ログを出力

- code:
```
>>> import json
>>> from sudachipy import config
>>> from sudachipy import dictionary
>>> from expression_trans import expressionTranslate
>>> with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
...     sudachi_settings = json.load(f)
...
>>> dict = dictionary.Dictionary(sudachi_settings)
>>> sudachi_instance = dict.create()
>>> input_text = '私が惚れたら困ります。'
>>> ex_trans = expressionTranslate(False, 'holo', sudachi_instance)
>>> translated_text = ex_trans.translateText(input_text).translated_text
>>> print(translated_text)
わっちが惚れたら困りんす。
```

-----
# expression_trans
This Python package is to translate Japanese text along the expression converting model with using "[SudachiPy](https://github.com/WorksApplications/SudachiPy)" as a morphological tokenizer.

The default converting model is a heroine of "Spice and Wolf" in a Japanese anime named "Holo" with its speaking tone like an geisha girl. :)

To see more information about original Java based "Sudachi", please find out [Elasticsearchのための新しい形態素解析器 「Sudachi」](https://qiita.com/sorami/items/99604ef105f13d2d472b) on "Qiita".

Please refer to the article "[雑談ボットの応答テキストを「狼と香辛料」のホロの花魁言葉っぽい口調にした](https://qiita.com/anmorenight/items/3be08333d85648faad43)]" posted on Qiita for the background of development.


## Features
Morphologically analyze Japanese text with "SudachiPy" and convert the tone by replacing the words according to the definition of the pattern file (json) of the tone conversion model.

- Custom model
    + You can choice the other convering model if you(or someone) create additional json pattern files.
      (ex. other anime characters or local dialect and so on)

- For confirmation, it is possible to return only the morphological analysis result by "SudachiPy".

## Environment

- development on AWS t2.maicro Linux (mem:1GB swap:2GB)
- expression_trans requires Python3.6+. (maybe 3.0+ is avarable)

## Instruction

```
$ git clone git@github.com:anmonite/expression_trans.git
$ cd expression_trans
$ pip install -e .
```

## Usage
- command:
```
    $ python3 expression_trans.py
    INPUT TEXT (exit = n) > 私が惚れたら困ります。
    
    Original text:
    -----
    私が惚れたら困ります。
    -----
    Processing log:
    -----
    Translate honorific words:
    -----
    Nothing to translate in text.
    -----
    
    Translate specific words:
    -----
    Nothing to translate in text.
    -----
    
    Morphological analisis after replacement:
    -----
    > 私    代名詞,*,*,*,*,*        私      私      ワタクシ
    > が    助詞,格助詞,*,*,*,*     が      が      ガ
    > 惚れ  動詞,一般,*,*,下一段-ラ行,連用形-一般   惚れる  惚れる  ホレ
    > たら  助動詞,*,*,*,助動詞-タ,仮定形-一般      た      た      タラ
    > 困り  動詞,一般,*,*,五段-ラ行,連用形-一般     困る    困る    コマリ
    > ます  助動詞,*,*,*,助動詞-マス,終止形-一般    ます    ます    マス
    > 。    補助記号,句点,*,*,*,*   。      。      キゴウ
    
    -----
    0: 私   代名詞,*,*,*,*,*        私      私      ワタクシ
    Found keyword: "私"
    Translated: わっち
    Translate noun token: 私 > わっち
    
    1: が   助詞,格助詞,*,*,*,*     が      が      ガ
    Nothing to translate: が > が
    
    2: 惚れ 動詞,一般,*,*,下一段-ラ行,連用形-一般   惚れる  惚れる  ホレ
    Translate (last)verb token: 惚れ > 惚れ
    
    3: たら 助動詞,*,*,*,助動詞-タ,仮定形-一般      た      た      タラ
    Nothing to translate: たら > たら
    
    4: 困り 動詞,一般,*,*,五段-ラ行,連用形-一般     困る    困る    コマリ
    Found keyword: "困り"
    Translated: 困りんす
    Translate (last)verb token: 困り > 困りんす
    
    6: 。   補助記号,句点,*,*,*,*   。      。      キゴウ
    Nothing to translate: 。 > 。
    
    -----
    Translated text:
    -----
    わっちが惚れたら困りんす。
    -----
    INPUT TEXT (exit = n) > 
```
- command line option
  - -v : output vorbose log when in processing

- code:
```
>>> import json
>>> from sudachipy import config
>>> from sudachipy import dictionary
>>> from expression_trans import expressionTranslate
>>> with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
...     sudachi_settings = json.load(f)
...
>>> dict = dictionary.Dictionary(sudachi_settings)
>>> sudachi_instance = dict.create()
>>> input_text = '私が惚れたら困ります。'
>>> ex_trans = expressionTranslate(False, 'holo', sudachi_instance)
>>> translated_text = ex_trans.translateText(input_text).translated_text
>>> print(translated_text)
わっちが惚れたら困りんす。
```

