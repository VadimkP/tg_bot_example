# tg_bot

```bash
docker build -t tg_bot . --no-cache
```


```bash
docker run -d -v handlers/:/scripts/handlers/ -v keyboards/:/scripts/keyboards/ -v db/:/scripts/db/ -v sqlite/:/scripts/sqlite/ --name tg_bot tg_bot
```
