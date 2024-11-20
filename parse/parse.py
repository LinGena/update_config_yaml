import requests
from utils.db import Db
import urllib.parse


class Parse(Db):
    def __init__(self):
        super().__init__()
        self.address_links = [
            'https://api-story-testnet.itrocket.net/cosmos/slashing/v1beta1/signing_infos',
            'https://api-story-testnet.trusted-point.com/cosmos/slashing/v1beta1/signing_infos'
            ]
        self.moniker_links = [
            'https://api-story-testnet.itrocket.net/cosmos/staking/v1beta1/validators?status=BOND_STATUS_BONDED',
            'https://api-story-testnet.trusted-point.com/cosmos/staking/v1beta1/validators?status=BOND_STATUS_BONDED'
            ]
    
    def run(self) -> list:
        try:
            rpc_datas = self.get_rpcs()
            addresses = self.get_address(rpc_datas)
            moniker_datas = self.get_apis()
            result = self.get_result_list(addresses, moniker_datas)
            # result = self.get_db_result(parse_result)
            self._logger.info(f'Received {len(result)} new address and moniker tokens.')
            return result
        except Exception as ex:
            self._logger.error(ex)

    def get_db_result(self, parse_result: list) -> list:
        result = []
        for data in parse_result:
            if not self.does_record_exist(f"rpc = '{data['rpc']}'"):
                self.insert(data)
                result.append(data)
        return result

    def get_result_list(self, addresses: list, moniker_datas: list) -> list:
        result = []
        filtered_data = [
            {"moniker": entry["description"]["moniker"], "key": entry["operator_address"]}
            for entry in moniker_datas
            if "description" in entry and "moniker" in entry["description"] and "operator_address" in entry
        ]
        for address in addresses:
            
            moniker = self.get_moniker(address['address'], filtered_data)
            if moniker:
                res = {
                    'rpc': address['address'],
                    'moniker': moniker
                }
                result.append(res)
        if result:
            return result
        raise Exception("In the obtained RPC and API lists, there are no matching linking keys.")

    def get_moniker(self, rpc_value: str, moniker_datas: list) -> str:
        key_to_moniker = {entry['key'][:30]: entry['moniker'] for entry in moniker_datas}
        key_equivalent = rpc_value.replace('storyvalcons', 'storyvaloper')[:30]
        return key_to_moniker.get(key_equivalent, None)

    def get_address(self, datas: list) -> list:
        result = [
            {"address": entry["address"]}
            for entry in datas
            if "address" in entry
        ]
        if result:
            return result
        raise Exception("In the resulting list, there is no address and value.")

    def get_rpcs(self) -> list:
        for link in self.address_links:
            result = self.get_next(link)
            if result:
                return result
        raise Exception("Failed to retrieve address data from the specified links.")
    

    def get_next(self, url: str, result_nex: list = []) -> dict:
        result = self.get_respose(url)
        if result:
            if 'info' in result and result['info']:
                result_nex.extend(result['info']) 
                if 'pagination' in result and result['pagination']:
                    url = url.split('?')[0]
                    encoded_next_key = encoded_next_key = urllib.parse.quote(result['pagination']['next_key'])
                    link = url + f"?pagination.key={encoded_next_key}"
                    return self.get_next(link, result_nex)                    
        return result_nex

    
    def get_apis(self) -> list:
        for link in self.moniker_links:
            result = self.get_next_moniker(link)
            if result:
                return result
        raise Exception("Failed to retrieve validators data from the specified links.")
    
    def get_next_moniker(self, url: str, result_nex: list = []) -> dict:
        result = self.get_respose(url)
        if result:
            if 'validators' in result and result['validators']:
                result_nex.extend(result['validators']) 
                if 'pagination' in result and result['pagination']:
                    url = url.split('?')[0]
                    encoded_next_key = encoded_next_key = urllib.parse.quote(result['pagination']['next_key'])
                    link = url + f"?status=BOND_STATUS_BONDED&pagination.key={encoded_next_key}"
                    return self.get_next_moniker(link, result_nex)                    
        return result_nex

    def get_respose(self, link: str) -> dict:
        try:
            response = requests.get(url=link, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as ex:
            self._logger.error(ex)
        return None