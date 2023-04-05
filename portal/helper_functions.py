def create_va(payload, org_id, api_key):
    url = "https://app.moderntreasury.com/api/virtual_accounts"
    try:
        resp = requests.post(url=url, auth=(org_id, api_key), json=payload)
        return resp
    except Exception as e:
        print(e)
        return "Call failed."

def dollars_to_cents(dollars):
    cents = float(dollars) * 100

    return int(cents)