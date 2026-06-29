import sys
from worker.config import settings
from worker.image_providers.mock import MockProvider
from worker.storage.local import LocalStorage
from worker.backend.client import BackendClient

def main() -> None:
    # Resolve image provider name
    if settings.image_provider == "mock":
        image_provider = MockProvider()
        image_provider_name = image_provider.get_name()
    else:
        image_provider_name = settings.image_provider

    # Resolve storage provider name
    if settings.storage_provider == "local":
        storage_provider = LocalStorage()
        storage_provider_name = storage_provider.get_name()
    else:
        storage_provider_name = settings.storage_provider

    # Print initialization details
    print("AI Studio Worker")
    print(f"Version: {settings.worker_version}")
    print(f"Worker Name: {settings.worker_name}")
    print(f"Backend URL: {settings.backend_url}")
    print(f"Selected Image Provider: {image_provider_name}")
    print(f"Selected Storage Provider: {storage_provider_name}")

    print("Checking backend...")
    client = BackendClient()
    if client.check_connection():
        print("Backend Connected")
        print("Worker Status READY")
    else:
        print("Backend Offline")
        print("Worker Status ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()
