from abc import ABC, abstractmethod


class SearchService(ABC):

    @abstractmethod
    def search(self, query: str) -> str:
        pass


class OldSearchService(SearchService):
    def search(self, query: str) -> str:
        return f"Searching old way for: {query}"


class NewSearchService(SearchService):
    def search(self, query: str) -> str:
        return f"Searching new way for: {query}"



class FeatureToggle:
    def get_search_service(self) -> SearchService:
        if self._is_new_search_enabled():
            return NewSearchService()
        else:
            return OldSearchService()

    def _is_new_search_enabled(self) -> bool:
        """ 
        Not gonna copy all features configurations
        For now we will just assume that it's enabled
        and it's read from our configuration like we did
        in the past
        """
        return True


class ApplicationController:
    def __init__(self, search_service: SearchService) -> None:
        self.search_service = search_service

    def handle_search(self, query: str) -> str:
        return self.search_service.search(query)


def main() -> None:
    feature_toggle = FeatureToggle()

    # Dependency Injection
    search_service = feature_toggle.get_search_service()
    controller = ApplicationController(search_service)

    print(controller.handle_search("test query"))


if __name__ == "__main__":
    main()