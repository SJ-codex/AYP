# AYP

YouTubeのURLからサムネイル画像を取得するためのシンプルなCLIツールです。

## 使い方

1. 必要に応じて実行権限を付与します。

   ```bash
   chmod +x youtube_thumbnail_fetcher.py
   ```

2. YouTubeのURL、または動画IDを指定して実行します。

   ```bash
   ./youtube_thumbnail_fetcher.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```

   `maxresdefault`（最高解像度）のサムネイルが取得できない場合は、`--resolution`で
   `sddefault`・`hqdefault`・`mqdefault`・`default`のいずれかを指定して再実行してください。

   ```bash
   ./youtube_thumbnail_fetcher.py "https://youtu.be/dQw4w9WgXcQ" \
       --resolution hqdefault --output ./thumbnails/sample.jpg
   ```

サムネイル画像は指定したパスにJPEG形式で保存されます。
