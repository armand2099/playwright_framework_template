import json
from pathlib import Path


def open_json(self, file_name: str, mode = 'r'):
            '''
            Open JSON file
            '''
            json_path = Path(file_name).resolve()
    
            with open(json_path, mode, encoding="utf-8") as file:
                self.log(f"Json file {file_name} opened")
    
            return file


def get_key_from_json(self, file_name: str, key: str) -> list:
        '''
        Get the list of keys in the AI generated JSON file
        '''
        data = json.load(self.open_json(file_name))
        json_list = []

        for item in data:
            json_list.append(item[key])

        return json_list


def write_to_json(self, file_name: str, primary_key: str, pk_value: str, update_key: str, uk_value: str):
        '''
        Updates JSON data
        '''
        found = False
        file = self.open_json(file_name, "w")
        data = json.load(file)

        for item in data:
            if item[primary_key] == pk_value:
                item[update_key] = uk_value
                found = True
                break

        if not found:
            self.log(f"Key {primary_key} not found")
            raise ValueError(f"Key {primary_key} not found")

        with open("PODS.json", "w", encoding="utf-8") as file:
            self.log(f"Value of Key {update_key} updated to: {uk_value}")
            json.dump(data, file, indent=2)    