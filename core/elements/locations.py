
# other
from loguru import logger

# engine elements import
from QuantumCore.scene import Location


class TestScene(Location):
    def __init__(self, app) -> None:
        super().__init__(app)

    def build(self, app, add) -> None:

        self.builder.read_sav(app, add)
        self.builder.read_tpt()
        
        logger.debug('TestScene - load\n\n')
        