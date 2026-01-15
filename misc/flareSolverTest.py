import os
import requests
from rich import print
from requests.cookies import cookiejar_from_dict
from typing import Dict

base_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "referer": "https://www.controller.com/listings/for-sale/cirrus/aircraft",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # We'll set 'x-xsrf-token' dynamically (if found in cookies)
    # "x-xsrf-token": "some_value",
}

def get_cookies(url):
    flare_url = "http://127.0.0.1:8191/v1"
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000,
        "returnOnlyCookies": True,
        # "proxy": os.getenv("stickyproxy"),
    }
    response = requests.post(flare_url, headers=headers, json=data)
    if "solution" in response.json() and "cookies" in response.json()["solution"]:
        return response.json()["solution"]["cookies"]
    else:
        raise ValueError(f"Unexpected response format: {response.json()}")

def load_cookies(session: requests.Session, cookies_dict: Dict):
    cookie = {}
    for elem in cookies_dict:
        cookie[elem["name"]] = elem["value"]
    session.cookies = cookiejar_from_dict(cookie)
    return session

def build_cookie_header(cookies_list: dict) -> str:
    cookie_pairs = []
    for c in cookies_list:
        name, value = c["name"], c["value"]
        cookie_pairs.append(f"{name}={value}")
    return "; ".join(cookie_pairs)


def main():
    session = requests.Session()
    # proxy = os.getenv("stickyproxy")
    # if proxy is not None:
    #     session.proxies = {
    #         "http": proxy,
    #         "https": proxy,
    #     }

    cookie_url = "https://www.controller.com/"
    cookies = get_cookies(cookie_url)
    # load_cookies(session, cookies)

    # urls = ["https://httpbin.org/cookies", "https://httpbin.org/ip"]
    # for url in urls:
    #     resp = session.get(url)
    #     print(resp.json())
    
    print(cookies)
    for cookie in cookies:
        if cookie["name"] == "__XSRF-TOKEN":
            base_headers["x-xsrf-token"] = cookie["value"]
            break

    cookie_header_str = build_cookie_header(cookies)
    base_headers["Cookie"] = cookie_header_str
    print(base_headers)
    target_url = "https://www.controller.com/ajax/listings/ajaxsearch?Manufacturer=CIRRUS&sort=1&page=2&lang=en-US"
    response = session.get(target_url, headers=base_headers)
    
    # Print the response content
    print(response.text)

if __name__ == "__main__":
    main()