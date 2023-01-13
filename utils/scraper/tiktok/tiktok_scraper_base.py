from abc import ABC, abstractmethod
import yaml


class TiktokScraperBase(ABC):

    def _load_header_from_yaml(self, yaml_path: str) -> dict:
        with open(yaml_path, 'r') as f:
            headers = yaml.load(f, yaml.Loader)
        return headers

    @abstractmethod
    def process_response(self, response: dict) -> list[dict]:
        pass

    @abstractmethod
    def scrape_lazyload(self, **kwargs):
        pass

    @abstractmethod
    def scrape(self, **kwargs):
        pass