# services.py

import oci
from storage import object_storage_client, config
from datetime import datetime

def generate_par_url(filename, object_storage_client, namespace, bucket_name):
    par_request = oci.object_storage.models.CreatePreauthenticatedRequestDetails(
        name=filename,
        object_name=filename,
        bucket_name=bucket_name,
        access_type="ObjectRead",
        time_expires=datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expira em 1 hora
    )

    par = object_storage_client.create_preauthenticated_request(
        namespace, bucket_name, par_request
    ).data

    return f"https://objectstorage.{config['region']}.oraclecloud.com{par.access_uri}"