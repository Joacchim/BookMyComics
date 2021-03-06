class SupportBase:
    name = None

    def __init__(self, wrapped_driver, *args, **kwargs):
        self._wrapper = wrapped_driver
        self._driver = wrapped_driver.driver

    def load_random(self):
        pass

    def prev_page(self):
        pass

    def next_page(self):
        pass

from .mangahere import MangaHereDriver
from .mangafox import FanFoxDriver
from .mangakakalot import MangaKakalotDriver
from .manganelo import MangaNeloDriver
from .isekaiscan import IsekaiScanDriver

drivers = {
    MangaHereDriver.name: MangaHereDriver,
    FanFoxDriver.name: FanFoxDriver,
    MangaKakalotDriver.name: MangaKakalotDriver,
    MangaNeloDriver.name: MangaNeloDriver,
    IsekaiScanDriver.name: IsekaiScanDriver,
}
