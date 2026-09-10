#!/bin/sh
set -e

export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN="${VAULT_DEV_ROOT_TOKEN_ID}"

echo "Waiting for Vault to be ready..."
until vault status > /dev/null 2>&1; do
  sleep 1
done

echo "Vault is ready. Enabling KV v2 secrets engine..."
vault secrets enable -path=secret kv-v2 2>/dev/null || true

echo "Writing database secrets to Vault..."
vault kv put secret/db \
  host="db" \
  port="5432" \
  user="${POSTGRES_USER}" \
  password="${POSTGRES_PASSWORD}" \
  dbname="${POSTGRES_DB}"

echo "Writing Kafka secrets to Vault..."
vault kv put secret/kafka \
  bootstrap_servers="${KAFKA_BOOTSTRAP_SERVERS}" \
  topic="${KAFKA_TOPIC}"

echo "Secrets written to Vault successfully."
vault kv get secret/db
vault kv get secret/kafka