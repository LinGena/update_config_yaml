import schedule
from parse.parse import Parse
from parse.update_yaml import update_config
import subprocess


def main():
    tokens = Parse().run()
    if tokens:     
        try:
            update_config(tokens)
            subprocess.run(["sudo", "systemctl", "restart", "tenderduty"], check=True)
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    # main()
    # schedule.every(3).seconds.do(main)
    # while True:
    #     schedule.run_pending()
    import random
    nodes = [
            {"url": "https://story-testnet-rpc.itrocket.net:443", "alert_if_down": False},
            {"url": "https://odyssey.storyrpc.io:443", "alert_if_down": False},
            {"url": "https://story-testnet-rpc.contributiondao.com:443", "alert_if_down": False},
            {"url": "https://story-testnet.rpc.kjnodes.com:443", "alert_if_down": False}
        ]
    print(nodes)
    random.shuffle(nodes)
    print(nodes)