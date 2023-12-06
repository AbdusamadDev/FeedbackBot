import requests

for i in range(100):
    request = requests.post(
        url="http://localhost:8000/api/questions/",
        json={
            "text": f"question {i}",
            "status": False,
            "category": {1, 2}.pop(),
            "user": {15, 16, 22, 23}.pop(),
        },
    )
    print(request.json())
