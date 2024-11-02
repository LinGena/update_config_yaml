import subprocess
import yaml

def load_config_with_sudo():
    try:
        result = subprocess.run(
            "sudo -u tenderduty bash -c 'cd && cat config.yml'",
            check=True,
            capture_output=True,
            text=True,
            shell=True
        )
        config = yaml.safe_load(result.stdout)
        return config
    except subprocess.CalledProcessError as e:
        print("Error reading the configuration file:", e)
        return None

def save_config_with_sudo(config):
    config_yaml = yaml.safe_dump(config)
    print(config_yaml)
    # try:
    #     subprocess.run(
    #         ["sudo", "-u", "tenderduty", "tee", config_path],
    #         input=config_yaml,
    #         check=True,
    #         text=True
    #     )
    #     print("Configuration successfully saved.")
    # except subprocess.CalledProcessError as e:
    #     print("Error saving the configuration file:", e)

def update_config(new_entries):
    config = load_config_with_sudo()

    if config is None:
        return

    if "chains" not in config:
        config["chains"] = {}

    for entry in new_entries:
        chain_name = entry['moniker']
        address = entry['rpc']

        config["chains"][chain_name] = {
            "chain_id": "odyssey-0",
            "valoper_address": address,
            "public_fallback": True,
            "nodes": [
                {"url": "https://story-testnet-rpc.itrocket.net:443", "alert_if_down": False},
                {"url": "https://odyssey.storyrpc.io:443", "alert_if_down": False},
                {"url": "https://story-testnet-rpc.contributiondao.com:443", "alert_if_down": False},
                {"url": "https://story-testnet.rpc.kjnodes.com:443", "alert_if_down": False}
            ]
        }
    print('----------------')
    print(config)
    print('----------------')
    save_config_with_sudo(config)
