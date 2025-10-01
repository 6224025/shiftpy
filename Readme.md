# シフト管理API
## !CAUTION
これはあくまで仮のコードです。全体像を把握後、Golangでの実装を予定しています。また、デプロイは行いません。


## 起動方法
```bash
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```
http://localhost:8000/docs でAPIドキュメントを確認可能。


```bash
uv pip freeze > requirements.txt
```