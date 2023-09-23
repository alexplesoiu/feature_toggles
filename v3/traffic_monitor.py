from feature_manager import FeatureManager
from typing import Dict, Union


class TrafficMonitor:
    def __init__(
        self,
        toggle_manager: FeatureManager,
        drop_threshold: float = 30.0
    ) -> None:
        
        self.toggle_manager: FeatureManager = toggle_manager
        self.drop_threshold: float = drop_threshold


    def should_deactivate_feature(
        self,
        feature_name: str,
        traffic_data: Dict[str, Union[int, float]]
    ) -> bool:
        """Determine if a feature should be deactivated based on traffic data."""

        is_active = self.toggle_manager.is_enabled(feature_name, {})
        traffic_drop = traffic_data.get("drop", 0)

        return is_active and traffic_drop > self.drop_threshold


    def monitor(
        self,
        feature_name: str,
        traffic_data: Dict[str, Union[int, float]]
    ) -> None:
        """ Monitor a feature """
        
        if self.should_deactivate_feature(feature_name, traffic_data):
            if feature_name in self.toggle_manager.features:
                self.toggle_manager.disable(feature_name)
                
                print(f"Feature '{feature_name}' has been deactivated due to a traffic drop of {traffic_data['drop']}%.")
            else:
                print(f"Feature '{feature_name}' does not exist in the toggle manager.")
