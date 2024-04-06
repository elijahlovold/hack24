import json

class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)
    
    @classmethod
    def from_json_file(cls, file_path):
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        return cls.from_json(json_data)

# # Create an instance of MyClass
# obj = MyClass("John", 30)

# # Convert MyClass instance to JSON
# json_data = obj.to_json()
# with open('data.json', 'w') as f:
#     json.dump(json_data, f)


# Load MyClass instance from JSON file
loaded_obj = MyClass.from_json_file('data.json')

# Access loaded object attributes
print("Loaded object:", loaded_obj.name, loaded_obj.age)
