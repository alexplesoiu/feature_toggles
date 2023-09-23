import json
from typing import Dict, Any, Optional
from rollout import is_rolled_out
import datetime


class FeatureManager:
    _instance: Optional["FeatureManager"] = None
    _error_counts: Dict[str, int] = {}


    def __new__(cls) -> "FeatureManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance


    def initialize(self) -> None:
        with open('features_config.json', 'r') as file:
            self.features: Dict[str, Any] = json.load(file)


    def disable(self, feature_name: str) -> None:
        self.features[feature_name]["active"] = False
        self._save()


    def _save(self) -> None:
        with open('features_config.json', 'w') as file:
            json.dump(self.features, file, indent=4)
    
    def get_feature_metadata(self, feature_name: str) -> Dict[str, Any]:
        return self.features.get(feature_name, {}).get("metadata", {})
    

    def is_enabled(self, feature_name: str, user_context: Dict[str, Any]) -> bool:
        feature_config = self.features.get(feature_name, {})

        # Global Activation Check
        if not feature_config.get("active"):
            return False
        
        # If no other fields are set, and "active" is True, the feature is enabled for everyone.
        if len(feature_config) == 1:  # Only 'active' field is present
            return True
        
        # Check for scheduled activation
        if "activation_date" in feature_config:
            activation_date = datetime.datetime.fromisoformat(feature_config["activation_date"])
            if datetime.datetime.now() < activation_date:
                return False

        # Check for error limit
        if self._error_counts.get(feature_name, 0) > feature_config.get("error_threshold", float("inf")):
            return False

        # Check feature dependencies (we check reccursive)
        # Be careful for infinite dependency loop 
        if "depends_on" in feature_config:
            for dependency in feature_config["depends_on"]:
                if not self.is_enabled(dependency, user_context):
                    return False

        # If no user context is provided and the feature is active, we return True
        if user_context == {}:
            return True

        # User Specific Check
        if "users" in feature_config and user_context["user_id"] in feature_config["users"]:
            return True

        # Region Specific Check
        region_enabled = "regions" not in feature_config or user_context["region"] in feature_config["regions"]
        
        # Account Type and Beta Program Checks
        account_type_enabled = "account_types" not in feature_config or user_context["account_type"] in feature_config["account_types"]

        beta_program_enabled = not feature_config.get("beta_program") or user_context["beta_program"]

        # If both account type and beta program conditions are met, then check for regions.
        if account_type_enabled and beta_program_enabled and region_enabled:
            if "percentage_rollout" in feature_config:

                # Check for percentage rollout
                if is_rolled_out(
                    user_id=user_context["user_id"], 
                    percentage=feature_config["percentage_rollout"],
                    salt=feature_name
                ):
                    return True
            else:
                return True

        return False
    
    def report_error(self, feature_name: str) -> None:
        self._error_counts[feature_name] = self._error_counts.get(feature_name, 0) + 1
