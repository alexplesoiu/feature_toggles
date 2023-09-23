from feature_manager import FeatureManager


class ErrorReporter:
    def __init__(self, toggle_manager: FeatureManager) -> None:
        self.toggle_manager = toggle_manager

    def report(self, feature_name: str) -> None:
        self.toggle_manager.report_error(feature_name)