import os
import time
import hvac

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://vault:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_SECRET_PATH = os.getenv("VAULT_SECRET_PATH", "secret/data/db")


def get_database_url(retries: int = 15, delay: int = 3) -> str:
    """Получает DATABASE_URL из Vault с повторными попытками."""
    if not VAULT_TOKEN:
        raise RuntimeError("VAULT_TOKEN is not set")

    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            if not client.is_authenticated():
                raise RuntimeError("Vault authentication failed")

            response = client.secrets.kv.v2.read_secret_version(
                path="db",
                mount_point="secret",
            )
            secret = response["data"]["data"]

            database_url = (
                f"postgresql://{secret['user']}:{secret['password']}"
                f"@{secret['host']}:{secret['port']}/{secret['dbname']}"
            )
            print(f"[Vault] Retrieved DATABASE_URL (host={secret['host']}, db={secret['dbname']})")
            return database_url

        except Exception as e:
            last_error = e
            print(f"[Vault] Attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)

    raise RuntimeError(f"Could not retrieve secrets from Vault: {last_error}")
def get_kafka_config(retries: int = 15, delay: int = 3) -> dict:
    """Получает Kafka-конфигурацию из Vault."""
    if not VAULT_TOKEN:
        raise RuntimeError("VAULT_TOKEN is not set")

    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            if not client.is_authenticated():
                raise RuntimeError("Vault authentication failed")

            response = client.secrets.kv.v2.read_secret_version(
                path="kafka",
                mount_point="secret",
            )
            secret = response["data"]["data"]

            config = {
                "bootstrap_servers": secret["bootstrap_servers"],
                "topic": secret["topic"],
            }
            print(f"[Vault] Retrieved Kafka config: {config}")
            return config

        except Exception as e:
            last_error = e
            print(f"[Vault] Kafka config attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)

    raise RuntimeError(f"Could not retrieve Kafka config from Vault: {last_error}")