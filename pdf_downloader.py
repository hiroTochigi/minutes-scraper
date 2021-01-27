import requests

response = requests.get(f"http://cambridgema.iqm2.com/Citizens/FileOpen.aspx?Type=12&ID=2147&Inline=True")
if response.status_code == 200:
    with open("download.pdf", "wb") as w:
        w.write(response.content)
