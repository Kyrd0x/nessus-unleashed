import subprocess
import requests
import random
import string
import re

# Constants
stop_script = 'scripts/stop.sh'
install_script = 'scripts/install.sh'
saving_folder = 'nessus_reports'

proxies_list = 'https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt'

# Step 1 : SAVE -    download all *.nessus reports
# Step 2 : STOP -    stop daemon and rm -rf /opt/nessus
# Step 3 : INSTALL - re install from .deb (download if wrong checksum) and start daemon
# Step 4 : SET -     generate trial code, activate and set eveyrthing
# Step 5 : RESTORE - restore all *.nessus reports

def get_proxy():
    all_proxies = requests.get(proxies_list).json()
    proxy_info = random.choice(all_proxies)
    proxy_url = f"{proxy_info['type']}://{proxy_info['ip']}:{proxy_info['port']}"
    return proxy_url

def save():
    print("Saving Nessus reports")
    try:
        # todo
        pass
    except subprocess.CalledProcessError as e:
        print("Erreur :", e.stderr)
        exit(1)

def stop():
    print("Stopping Nessus daemon")
    try:
        result = subprocess.run(['sudo', 'bash', stop_script], check=True, capture_output=True, text=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Erreur :", e.stderr)
        exit(1)

def install():

    url = "https://www.tenable.com/downloads/api/v2/pages/nessus/files/Nessus-10.8.3-ubuntu1604_amd64.deb"
    output_file = "Nessus.deb"

    print("Downloading Nessus")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded to : {output_file}")
    else:
        print(f"Error during download : {response.status_code}")
        exit(1)

    # check if ok, maybe delete it once install is over

    print("Installing Nessus")
    try:
        result = subprocess.run(['sudo', 'bash', install_script], check=True, capture_output=True, text=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Erreur :", e.stderr)
        exit(1)

def get_new_code(proxy):
    random_first_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    random_last_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(4, 8)))
    random_phone = ''.join(random.choice(string.digits) for _ in range(10))
    random_company = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(7, 14)))
    email =  ''.join(random.choice(string.ascii_letters) for _ in range(15)) + "@" + random_company + random.choice([".com", ".in", ".co", ".org", ".net"])
    
    data = {
        "skipContactLookup": "true",
        "product": "expert",
        "first_name": random_first_name,
        "last_name": random_last_name,
        "email": email,
        "partnerId": "",
        "phone": random_phone,
        "title": "Test",
        "company": random_company,
        "companySize": "10-49",
        "pid": "",
        "utm_source": "",
        "utm_campaign": "",
        "utm_medium": "",
        "utm_content": "",
        "utm_promoter": "",
        "utm_term": "",
        "alert_email": "",
        "_mkto_trk": "",
        "mkt_tok": "",
        "lookbook": "",
        "gclid": "",
        "country": "US",
        "region": "",
        "zip": "",
        "apps": "expert",
        "tempProductInterest": "Tenable Nessus Expert",
        "gtm": {"category": "Nessus Expert"},
        "queryParameters": "",
        "referrer": ""
    }

    url = 'https://www.tenable.com/evaluations/api/v2/trials'
    response = requests.post(url, proxies=proxy, json=data)

    if response.status_code == 200:
        try:
            # Adjusted regex to correctly extract the activation code
            regex = r"\"code\":\"([A-Z0-9-]+)\""
            matches = re.search(regex, response.text)
            activation_code = matches.group(1)
            return activation_code
        except AttributeError:
            print("Failed to retrieve Nessus Activation Code. Response:", response.text)
    else:
        print("Request failed. Status code:", response.status_code)
        print("Response text:", response.text)




def main():
    proxy = get_proxy()
    stop()
    # save

    new_code = get_new_code(proxy)

    # reinstall

    # re upload reports

if __name__ == '__main__':
    main()