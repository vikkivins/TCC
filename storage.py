import oci

# Configurar o cliente Oracle Cloud Object Storage
config = oci.config.from_file("C:\\Users\\victo\\.oci\\config")  # Carrega as credenciais da Oracle Cloud
object_storage_client = oci.object_storage.ObjectStorageClient(config)
namespace = object_storage_client.get_namespace().data  # Namespace único da sua conta Oracle
bucket_name = "sparkle-images"  # Nome do bucket criado
