import requests

res = requests.get("http://127.0.0.1:3000/api/main")# отправляем гет запрос  сервер локальный
print(res.json())
