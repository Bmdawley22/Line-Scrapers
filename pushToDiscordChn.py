import requests

# https://discord.com/api/v9/channels/1166388909618511894/messages

payload = {
    'content': "testing testing"
}

header = {
    'authorization': "Nzk2MDgxNzg5NTU4NDU2MzUx.GgQdGC.ZCqoFX8tlo7RNB5UgZaLJuuMqh7PvaaX-m1fyo"
}


r = requests.post("https://discord.com/api/v9/channels/1166388909618511894/messages",
                  data={'content': "*insert message here"}, headers=header)
