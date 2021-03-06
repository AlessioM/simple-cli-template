import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
    face_history: int = 30
    blur_amount: int = 31


# pydantic raises an error if secrets dir does not exist
# see: https://github.com/samuelcolvin/pydantic/issues/2175
DOCKER_SECRETS = "/run/secrets"
_settings_args = {}

if os.path.isdir(DOCKER_SECRETS):
    _settings_args["_secrets_dir"] = DOCKER_SECRETS

cfg = Settings(**_settings_args)
