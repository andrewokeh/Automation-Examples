import os
import requests
from getpass import getpass


# Work in progress...
# Plan on turning all the functions into methods in a class to reduce the amount of repeated code

# class NsAPI:
#     def __init__(self, domain: str, access_token: str) -> None:
#         self.domain = domain
#         self.token = access_token

def get_access_token(username: str, password: str) -> str:
    """
    Generate access token with subscriber credentials
    """
    endpoint = "https://phones.californiatelecom.com/ns-api/oauth2/token/"
    client_id = "andrew_api"
    client_secret = os.getenv("CLIENTSECRET")
    username = username
    password = password

    parameters = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password
    }

    response = requests.get(endpoint, params=parameters)
    response.raise_for_status()
    data = response.json()
    return data["access_token"]


def get_call_queues(domain: str, access_token: str) -> list:
    url = f"https://phones.californiatelecom.com/ns-api/v2/domains/{domain}/callqueues"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data


def read_agents_in_queue(domain: str, callqueue: str, access_token: str) -> list:
    url = f"https://phones.californiatelecom.com/ns-api/v2/domains/{domain}/callqueues/{callqueue}/agents"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    # print(response.text)
    return data


def update_agent_in_queue(domain: str, callqueue: str, agent_id: str, access_token: str) -> list:
    url = f"https://phones.californiatelecom.com/ns-api/v2/domains/{domain}/callqueues/{callqueue}/agents/{agent_id}"

    payload = {
        "callqueue-agent-wrap-up-allowance-seconds": 10,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(response.text)
    return data


def update_call_queue(domain: str, callqueue: str, access_token: str) -> list:
    url = f"https://phones.californiatelecom.com/ns-api/v2/domains/{domain}/callqueues/{callqueue}"

    payload = {
        "callqueue-max-current-callers-to-accept-new-callers": 15
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(response.text)
    return data


def add_agent_to_call_queue(domain: str, callqueue: str, user: str, access_token: str) -> list:
    url = f"https://phones.californiatelecom.com/ns-api/v2/domains/{domain}/callqueues/{callqueue}/agents"

    payload = {
        "synchronous": "no",
        "callqueue-agent-wrap-up-allowance-seconds": 0,
        "auto-answer-enabled": "no",
        "callqueue-agent-answer-confirmation-enabled": "no",
        "callqueue-agent-id": f"sip:{user}@{domain}",
        "callqueue-agent-dispatch-queue-priority-ordinal": 10
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(response.text)
    return data


def add_answer_rule(domain: str, user: str, access_token: str) -> list:
    url = f"https://phones.californiatelecom.com/ns-api/v2/domains/{domain}/users/{user}/answerrules"

    payload = {
        "synchronous": "no",
        "time-frame": "Holiday Forwarding",
        "enabled": "yes",
        "forward-always": {
            "enabled": "yes",
            "parameters": [""]
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(response.text)
    return data


def update_answer_rule(domain: str, user: str, access_token: str) -> list:
    url = f"https://phones.californiatelecom.com/ns-api/v2/domains/{domain}/users/{user}/answerrules/*"

    payload = {
        "enabled": "yes",
        "forward-on-busy": {
            "enabled": "yes",
            "parameters": [f"vmail_{user}"]
        },
        "forward-when-unregistered": {
            "enabled": "yes",
            "parameters": [f"vmail_{user}"]
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(response.text)
    return data


def get_domains(access_token: str) -> list:
    url = "https://phones.californiatelecom.com/ns-api/v2/domains"
    headers = {
        "accept": "application/json",
        f"authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data


def update_domain(domain: str, access_token: str) -> list:
    url = f"https://phones.californiatelecom.com/ns-api/v2/domains/{domain}"

    payload = {
        "email-send-from-address": ""
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data


def main():
    access_token = get_access_token(input("Username: "), getpass("Password: "))
    print(access_token)
    call_queues = get_call_queues("", access_token)
    call_queue_exts = set()
    for queue in call_queues:
        call_queue_exts.add(queue["callqueue"])

    for queue in call_queue_exts:
        print(queue)
        agents = read_agents_in_queue("", queue, access_token)
        for agent in agents:
            print(agent["callqueue-agent-id"])
            update_agent_in_queue("", queue, agent["callqueue-agent-id"], access_token)


if __name__ == "__main__":
    main()
