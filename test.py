import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes":78, "name":"Harshal", "views":100000},
        {"likes":75, "name":"Niraj", "views":10000},
        {"likes":72, "name":"Omkar", "views":1000}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())


