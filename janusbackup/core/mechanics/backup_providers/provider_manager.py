from typing import Optional, Type

from janusbackup.core.mechanics.backup_providers import BaseBackupProvider


class BackupProviderManager:
    @classmethod
    def get_provider_by_type(cls, db_type: str) -> Optional[Type[BaseBackupProvider]]:
        for provider in BaseBackupProvider.__subclasses__():
            if provider.db_type == db_type:
                return provider
