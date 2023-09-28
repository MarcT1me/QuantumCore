
# other
from loguru import logger

# import Engine config
from QuantumCore.data import config
# engine elements import
from QuantumCore.scene import Location, Builder

# core elements
from gamedata import settings


class TestScene(Location):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.builder = Builder(target=rf"{config.__APPLICATION_FOLDER__}/{settings.SAVES_path}/dev.xml")

    def build(self, app, add) -> None:
        
        self.builder.read_tpt()
        self.builder.read_sav(app, add)
        self.builder.read_custom_tags(app, add)
        
        logger.debug('TestScene - load\n\n')
        