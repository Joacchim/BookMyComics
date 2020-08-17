import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from . import SupportBase
from .. import RetriableError, retry

class MangaNeloDriver(SupportBase):
    name = "manganelo"

    def __init__(self, *args, **kwargs):
        super(MangaNeloDriver, self).__init__(*args, **kwargs)

    def _get_mangas(self):
        # First, go to the website
        self._driver.get('https://manganelo.com/')
        # Retrieve the generated random link, which is generated after loading the page
        return self._driver.find_elements(by=By.CLASS_NAME, value='content-homepage-item')

    @retry(abort=True)
    def load_random(self, predicate=None):
        to_ignore = []

        mangas = self._get_mangas()
        while len(mangas) > 0:
            manga = mangas.pop(random.randrange(len(mangas)))
            chapters = manga.find_elements(by=By.CSS_SELECTOR, value='.item-chapter>a')
            if len(chapters) < 3:
                continue
            href = chapters[1].get_attribute('href')
            if '://manganelo.com/' not in href or href in to_ignore:
                continue
            self._driver.get(href)
            # Validate predicate if specified
            if predicate and not predicate(self):
                to_ignore.append(href)
                mangas = self._get_mangas()
                continue
            return

        raise "No manga with enough chapters nor with link on manganelo"

    def prev_page(self):
        # In case you wonder, yes, button with "next" class is actually to go to the previous
        # chapter, because why not!
        btn = self._driver.find_element(
            by=By.CSS_SELECTOR,
            value='.navi-change-chapter-btn>.navi-change-chapter-btn-prev')
        btn.click()

    def next_page(self):
        # In case you wonder, yes, button with "back" class is actually to go to the next
        # chapter, because why not!
        btn = self._driver.find_element(
            by=By.CSS_SELECTOR,
            value='.navi-change-chapter-btn>.navi-change-chapter-btn-next')
        btn.click()

    def get_comic_name(self):
        """
            Extracts the comic name from the current URL
        """
        url = self._driver.current_url
        if 'manganelo.com' not in url:
            return None
        parts = self._driver.find_elements(
            by=By.CSS_SELECTOR,
            value=".panel-breadcrumb > .a-h")
        if len(parts) < 2:
            return None
        return parts[1].inner_text