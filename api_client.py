import requests

url = "https://fretzlimos.onrender.com/campus-events"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    print("CAMPUS EVENTS")
    print("========================")

    for event in data["events"]:
        print("Event ID:", event["event_id"])
        print("Event Name:", event["event_name"])
        print("Date:", event["date"])
        print("Venue:", event["venue"])
        print("Status:", event["status"])
        print("------------------------")

else:
    print("Request failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)