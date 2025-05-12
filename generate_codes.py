import argparse
import requests
import random
import string
import time
import sys
import re

from stem import Signal
from stem.control import Controller

# Delay after each Tor renewing
TOR_DELAY = 10

def renew_tor_identity_and_get_session():
    print("[INFO] Renewing Tor identity...")
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        time.sleep(TOR_DELAY)  # Wait for new circuit to be established

    # Create a new Tor session
    session = requests.session()
    session.proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    # Fetch IP
    try:
        ip = session.get('https://icanhazip.com', timeout=10).text.strip()
        print(f"[INFO] New TOR IP: {ip}")
    except Exception as e:
        print(f"[ERROR] Failed to fetch IP: {e}")

    return session, ip

def generate_random_string(length, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_phone():
    return ''.join(random.choice(string.digits) for _ in range(10))

def generate_random_company_name():
    return generate_random_string(random.randint(5, 10))

def get_mail():
    company = generate_random_company_name()
    return generate_random_string(15) + "@" + company + random.choice([".com", ".in", ".co", ".org", ".net", ".info", ".biz", ".me", ".io", ".ai"])

def generate_nessus_key(app_type, session):
    random_first_name = generate_random_string(random.randint(5, 10))
    random_last_name = generate_random_string(random.randint(4, 8))
    random_phone = generate_random_phone()
    random_company = generate_random_company_name()
    email = get_mail()
    product_map = {
        "essentials": ("Tenable Nessus Essentials", "Nessus Essentials Eval"),
        "pro": ("Tenable Nessus Professional", "Nessus Pro Eval"),
        "expert": ("Tenable Nessus Expert", "Nessus Expert Eval")
    }

    try:
        tempProductInterest, gtm_category = product_map[app_type]
    except KeyError:
        print(f"[ERROR] Invalid Nessus type: {app_type}")
        return None

    data = {
        "skipContactLookup": "true",
        "product": app_type,
        "first_name": random_first_name,
        "last_name": random_last_name,
        "email": email,
        "partnerId": "",
        "phone": random_phone,
        "title": "IT Security",
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
        "apps": [app_type],
        "tempProductInterest": tempProductInterest,
        "gtm": {"category": gtm_category},
        "queryParameters": "",
        "referrer": ""
    }

    url = 'https://www.tenable.com/evaluations/api/v2/trials'
    response = session.post(url, json=data)

    if response.status_code == 200:
        try:
            # Adjusted regex to correctly extract the activation code
            regex = r"\"code\":\"([A-Z0-9-]+)\""
            matches = re.search(regex, response.text)
            activation_code = matches.group(1)
            return activation_code
        except AttributeError:
            print("Failed to retrieve Nessus Activation Code. Response:", response.text)
            return None
    else:
        print("Request failed. Status code:", response.status_code)
        print("Response text:", response.text)
        return None

def parse_args():
    parser = argparse.ArgumentParser(
        add_help=True,
        description=(
            "This script allows you to generate Nessus License codes.\n\n"
            "Example :\n"
            "  python3 generate_codes.py -q 10 -t pro -o pro_codes.txt"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-q", "--quantity", type=int, dest="quantity", default=5, help="Quantity to generate. (default: 5).")
    parser.add_argument("-t", "--type", type=str, dest="type", choices=['essentials', 'pro', 'expert'], default="essentials", help="Nessus License Type. [essentials, pro, expert] (default: Essential).")
    parser.add_argument("-o", "--output", type=str, dest="output_file", default="codes.txt", help="Output TXT file. (default: codes.txt).")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    pretty_type=args.type[0].upper() + args.type[1:]

    print(f"Generating {args.quantity} Nessus {pretty_type} activation codes into '{args.output_file}'...")

    try:
        session, public_ip = renew_tor_identity_and_get_session()
    except Exception as e:
        print(f"[ERROR] Could not renew Tor identity: {e}")
        sys.exit(1)

    try:
        with open(args.output_file, "w") as f:
            for i in range(args.quantity):
                if i > 0 and i % 3 == 0: # Nessus rate limit
                    session, public_ip = renew_tor_identity_and_get_session()

                generated=False
                while not generated:
                    code = generate_nessus_key(args.type, session)
                    if code:
                        generated=True
                        f.write(code + "\n")
                        print(f"[{i+1}/{args.quantity}] Nessus {pretty_type} Code generated: {code}")
                        time.sleep(2)
                    else:
                        print(f"[INFO] Rate limit exceeded or error occurred. Renewing Tor identity...")
                        session, public_ip = renew_tor_identity_and_get_session()
                        print(f"[INFO] New IP: {public_ip}")
    except IOError as e:
        print(f"[ERROR] Could not write to file '{args.output_file}': {e}")
        sys.exit(1)

    print("Generation complete")
    print(f"Codes saved to '{args.output_file}'")  