# team_e

動かし方。

まず、TwitterとDocomoの言語解析APIのAPIキーを取得して、local/local_settings.py に貼ってください。

そして、次のコマンドでDBを初期化してください。

```
python manage.py shell
>>> import politician_updater
>>> politician_updater.main()
```

ちょっと時間がかかります。


ローカルで遊ぶなら
```
python manage.py runserver
```

サーバーにデプロイするならuWSGIで呼んでください。

