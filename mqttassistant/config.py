import yaml
from pathlib import Path
from typing import (
    Optional,
    Type,List
)
from pydantic import (
    BaseModel,
    Extra,
)
from .component import ComponentConfig
from .auth import Auth, User
from .log import get_logger


logger = get_logger('Config')


class Config(BaseModel):
    component: Optional[ComponentConfig] = ComponentConfig()
    auth: Optional[Auth] = Auth()
    users: Optional[List[User]] = []

    class Config:
        extra = Extra.forbid

    @classmethod
    def parse_config_path(cls: Type['Config'], path: Path) -> 'Config':
        config = dict()
        files = []
        if path.is_file():
            files = [path]
        if path.is_dir():
            files = list(path.glob('*.yaml'))
        if files:
            for file in files:
                logger.info('Parsing {}'.format(file.absolute()))
                with file.open(mode='r') as f:
                    file_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
                    config.update(file_config)
        else:
            logger.warning('No config files found in {}'.format(path.absolute()))
        return Config.parse_obj(config)
