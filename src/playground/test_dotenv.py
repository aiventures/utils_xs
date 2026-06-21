import os
from dotenv import load_dotenv, dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
print(dict(config))

load_dotenv()
for k, v in config.items():
    print(f"{k}: {os.environ.get(k)}")
