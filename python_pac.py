import requests
import json

r_crt_txt = requests.get("https://raw.githubusercontent.com/leapcode/bitmask-vpn/main/providers/riseup/riseup-ca.crt").content
print("Riseup's CA Certificate is ...")
print(r_crt_txt)
with open("./riseup-ca.crt","wb") as f_crt:
    f_crt.write(r_crt_txt)

r_pem_txt = requests.get("https://api.black.riseup.net/3/cert",verify="./riseup-ca.crt").content
print("Riseup's User Certificate and Private Key is ...")
print(r_crt_txt)

r_eip_service_json = requests.get("https://api.black.riseup.net/3/config/eip-service.json",verify="./riseup-ca.crt").json()
print("Riseup's valid Server List is ...")
print(r_eip_service_json)




