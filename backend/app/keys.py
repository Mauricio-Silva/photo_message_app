import json, uuid, os


class Keys:
    PATH = "app/static/key-pairs.json"
    REPOSITORY = {}


    @classmethod
    def init(cls):
        if not os.path.exists(cls.PATH):
            with open(cls.PATH, "x"):
                pass
        else:
            with open(cls.PATH) as file:
                print(file.name)
                print(file.read())
                print(json.loads(file.read()))
                cls.REPOSITORY = dict(json.load(file))


    @classmethod
    def clean_keys(cls, user1_key: str) -> None:
        del cls.REPOSITORY[user1_key]
        cls.save()


    @classmethod
    def find_all(cls) -> dict:
        return cls.REPOSITORY.copy()


    @classmethod
    def generate(cls) -> str:
        pairs = cls.find_all()
        keys = list(pairs.keys())
        values = list(pairs.values())
        keys.extend(values)
        while True:  
            key = str(uuid.uuid4()).upper()[:5]
            if keys.count(key) == 0:
                return key


    @classmethod
    def register_user1(cls, user1_key: str) -> None:
        cls.REPOSITORY.update({user1_key: ""})
        # cls.save()


    @classmethod
    def register_user2(cls, user1_key: str, user2_key: str) -> None:
        cls.REPOSITORY[user1_key] = user2_key
        # cls.save()


    @classmethod
    def save(cls) -> None:
        with open(cls.PATH, "w") as file:
            file.write(json.dumps(cls.REPOSITORY, indent=2))
            

    @classmethod
    def check_connection(cls, user1_key: str) -> bool:
        if cls.REPOSITORY.get(user1_key) is None:
            return False
        return True


    @classmethod
    def get_key(cls, user_key: str) -> str:
        if cls.REPOSITORY.get(user_key) is not None:
            return cls.REPOSITORY.get(user_key)
        for key in cls.REPOSITORY:
            if cls.REPOSITORY[key] == user_key:
                return key




