
import requests

url = "https://YOUR-CLASSMATES-RENDER-URL.onrender.com/books"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("\nCLASSMATE'S API DATA")
    print("========================")

    print(data)

else:
    print("Request failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
