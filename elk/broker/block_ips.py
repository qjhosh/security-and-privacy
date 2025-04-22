from elasticsearch import Elasticsearch
import subprocess
import time

ES_HOST = "http://localhost:9200"
INDEX_NAME = "alert_logs"
BLOCKED_FILE = "tmp/blocked_ips.txt"

es = Elasticsearch(ES_HOST)

def get_blocked_ips():
    try:
        with open(BLOCKED_FILE, 'r') as f:
            return set(f.read().splitlines())
    except:
        return set()

def save_blocked_ip(ip):
    with open(BLOCKED_FILE, 'a') as f:
        f.write(ip + "\n")

def block_ip(ip):
    print(f"Blocking IP: {ip}")
    # Windows 命令格式（例子），请根据实际情况测试:
    # 添加入站规则封锁攻击 IP
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockIP_"+ip, "dir=in", "action=block", f"remoteip={ip}"], check=True)
    save_blocked_ip(ip)


def main():
    print("Starting IP blocker loop...")
    while True:
        blocked = get_blocked_ips()
        query = {
            "size": 10,
            "sort": [{"@timestamp": "desc"}],
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": "now-1m"
                    }
                }
            }
        }

        try:
            res = es.search(index=INDEX_NAME, body=query)
            for hit in res["hits"]["hits"]:
                ip = hit["_source"].get("source_ip")
                if ip and ip not in blocked:
                    # 阈值可在告警中控制，这里假设一旦有告警，就封锁 IP
                    block_ip(ip)
        except Exception as e:
            print(f"Error querying Elasticsearch: {e}")

        time.sleep(60)

if __name__ == "__main__":
    main()
