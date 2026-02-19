import requests
import time
import uuid

US_IP = "34.121.182.32"
EU_IP = "35.241.187.167"


def run_latency_test(name, url, method):
    global user_count

    latencies = []
    print(f"---------Taking Latency Measurements on {name}---------\n")

    for _ in range(10):
        start_time = time.time()

        if method == "post":
            requests.post(url, json={"username": str(uuid.uuid4())})

        else:
            requests.get(url)

        end_time = time.time()
        duration = (end_time - start_time) * 1000

        latencies.append(duration)

    avg_latency = sum(latencies) / len(latencies)
    print("Average Latency: \n", avg_latency)

    return avg_latency


def run_consistency_test():
    print("---------Observing Eventual Consistency---------\n")
    misses = 0

    for _ in range(100):
        unique_username = str(uuid.uuid4())

        requests.post(
            f"http://{US_IP}:8080/register", json={"username": unique_username}
        )

        data = requests.get(f"http://{EU_IP}:8080/list").json()
        users = data.get("users")

        if users is None or unique_username not in users:
            misses += 1

    print("Misses: \n", misses)
    return misses


us_reg = run_latency_test("US /register", f"http://{US_IP}:8080/register", "post")
eu_reg = run_latency_test("EU /register", f"http://{EU_IP}:8080/register", "post")
us_list = run_latency_test("US /list", f"http://{US_IP}:8080/list", "get")
eu_list = run_latency_test("EU /list", f"http://{EU_IP}:8080/list", "get")

consistency_misses = run_consistency_test()
