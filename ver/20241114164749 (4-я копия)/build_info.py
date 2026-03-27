from dataclasses import dataclass


@dataclass
class build_info:
    BUILD_TAG: str = '20260210123520'
    BUILD_VERSION: str = 'source'
    APPS_BUILT = ['gcs_ap_manager', 'gcs_anemometer_manager', 'gcs_time_server', 'gcs_broadcaster', 'gcs_udp_api', 'gcs_monitoring_system', 'gcs_rtklora_manager', 'gcs_dispatch', 'gcs_frontend', 'gcs_drone_manager', 'gcs_broker_lorartk', 'gcs_license_manager', 'updater', ]
    GIT_RELEASE_HASH: str = 'c3d719af15de091b654bd730c4a535bdf361177d'
    GIT_RELEASE_TAG: str = 'v0.11.2'
    GIT_RELEASE_DATETIME: str = '2026-02-10 14:28:56'
    GIT_BRANCH: str = '0.11'

