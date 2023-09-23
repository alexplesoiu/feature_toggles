import json


class FeatureManager:
    def __init__(self, config_file: str = 'features_config.json') -> None:
        self.config_file = config_file

        with open(self.config_file, 'r') as file:
            self.features = json.load(file)

    def is_enabled(self, feature_name: str) -> bool:
        return self.features.get(feature_name, False)

    def enable(self, feature_name: str) -> None:
        self.features[feature_name] = True
        self._save()

    def disable(self, feature_name: str) -> None:
        self.features[feature_name] = False
        self._save()

    def _save(self) -> None:
        with open(self.config_file, 'w') as file:
            json.dump(self.features, file, indent=4)
