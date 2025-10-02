# Chat-CVE


## Dockerを使った起動場合の起動方法
```
各自でDockerをインストールする
$ echo "OPEN_API_KEY=あなたのAPI_KEY" > backend/.env
$ docker-compose up --build
コンソール画面に出てくるfrontendのリンクをウェブブラウザに貼り付ける
```

## Dockerを使わない場合の起動方法
### backend
```
$ cd backend/
$ pip install -r requirements.txt
$ echo "OPEN_API_KEY=あなたのAPI_KEY" > .env
$ uvicorn main:app --port 5173
```

### frontend
```
$ cd frontend/
$ pip install -r requirements.txt
$ python postlang.py
```
