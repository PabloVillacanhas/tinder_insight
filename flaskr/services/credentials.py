import logging
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()

secrets = None


def load():
    global secrets
    if secrets is None:
        project_id = '670663813881'
        secret_ids = ['API_TINDER', 'MONGO_PASS_TINDER']
        version_id = '1'

        my_secrets = {'MONGO_PASS_TINDER': None, 'API_TINDER': None}

        for secret_id in secret_ids:
            name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

            # Access the secret version.
            response = client.access_secret_version(request={"name": name})
            payload = response.payload.data.decode("UTF-8")
            my_secrets[secret_id] = payload

        secrets = my_secrets
    return secrets
