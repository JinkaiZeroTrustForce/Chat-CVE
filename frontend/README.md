# Chat-CVE

## backend
### 起動方法（Dockerを使わない）
```
$ cd backend/
$ pip install -r requirements.txt
$ echo "OPEN_API_KEY=あなたのAPI_KEY" > .env
$ uvicorn main:app --port 3000
```
