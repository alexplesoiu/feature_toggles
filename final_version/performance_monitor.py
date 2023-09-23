from feature_manager import FeatureManager
from typing import Callable, Any
import time


class PerformanceMonitor:
    def __init__(self, toggle_manager: FeatureManager) -> None:
        self.toggle_manager = toggle_manager


    def monitor(self, feature_name: str, code_block: Callable[[], Any]) -> Any:
        start_time = time.time()
        result = code_block()
        end_time = time.time()

        self.toggle_manager.report_performance(feature_name, end_time - start_time)

        return result
