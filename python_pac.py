import requests
import json

ovpn_txt_temp = """
remote {} {}
proto tcp-client

dev tun0
auth SHA1
cipher AES-128-CBC
tls-cipher DHE-RSA-AES128-SHA
keepalive 10 30
float

persist-tun
persist-key
resolv-retry infinite

tls-client

<ca>
{}
</ca>

<cert>
{}
</cert>

<key>
{}
</key>"""

def json_parser(dict):
    cand_list = []
    # ip, port, host, location, type

    for i in dict["gateways"]:
        # print("{} - {} : {}".format(i["ip_address"],i["host"],i["location"]))
        for j in i["capabilities"]["transport"]:
        #     print("{} - {} - {}".format(j["type"],", ".join(j["protocols"]),",".join(j["ports"])))
            if j["type"] == "openvpn" and "tcp" in j["protocols"]:
                cand_list.append({"ip":i["ip_address"],"port":j["ports"][0],"host":i["host"],"location":i["location"],"type":j["type"]})

    return cand_list

def main():
    r_crt_txt = requests.get("https://raw.githubusercontent.com/leapcode/bitmask-vpn/main/providers/riseup/riseup-ca.crt").content.decode("utf-8")
    print("Riseup's CA Certificate is ...")
    print(r_crt_txt)
    with open("./riseup-ca.crt","w") as f_crt:
        f_crt.write(r_crt_txt)

    r_pem_txt = requests.get("https://api.black.riseup.net/3/cert",verify="./riseup-ca.crt").content.decode("utf-8")
    print("Riseup's User Certificate and Private Key is ...")
    print(r_crt_txt)

    r_eip_service_json = requests.get("https://api.black.riseup.net/3/config/eip-service.json",verify="./riseup-ca.crt").json()
    cand_list = json_parser(r_eip_service_json)

    print("Riseup's Valid Server List is...")
    for i in cand_list:
        print(i)

    print("Creating OVPN config file...")
    r_ca = r_crt_txt.split("-----END CERTIFICATE-----")[1] + "-----END CERTIFICATE-----"
    r_cert = r_pem_txt.split("-----END RSA PRIVATE KEY-----")[1]
    r_key = r_pem_txt.split("-----END RSA PRIVATE KEY-----")[0] + "-----END RSA PRIVATE KEY-----"

    print("Outputting config file...")
    for index, cand in enumerate(cand_list):
        ovpn =  ovpn_txt_temp.format(cand["ip"], cand["port"], r_ca, r_cert, r_key)

        with open("./ovpn/ovpn_{}_{}_{}.ovpn".format(index, cand["host"], cand["location"]), "w") as f:
            f.write(ovpn)
    
    print("All have done!!")

    
if __name__ == '__main__':
        main()



