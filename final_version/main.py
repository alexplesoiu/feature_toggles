from feature_manager import FeatureManager
from performance_monitor import PerformanceMonitor
from traffic_monitor import TrafficMonitor
from error_reporter import ErrorReporter
from user_context import UserContext
from typing import Dict, Union
import threading
import time


def traffic_monitoring_job(toggle_manager: FeatureManager) -> None:
    """Job to run the traffic monitoring in a loop."""

    traffic_monitor = TrafficMonitor(toggle_manager)

    # Simulating traffic data
    while True:
        # Here, you would normally fetch real-time traffic data.
        # For simplicity, we'll simulate it.
        simulated_traffic_data: Dict[str, Union[int, float]] = {"drop": 25 + (10 * time.time() % 10)}
        
        traffic_monitor.monitor("new_ui", simulated_traffic_data)
        time.sleep(10)  # Check every 10 seconds


def refresh_configuration() -> None:
    """ Dynamic Configuration Reload """

    while True:
        # Since this is a singleton class, 
        # it will automatically reload the toggles everywhere
        FeatureManager().load_config()
        time.sleep(5)  # Reload Every 5 seconds


def main() -> None:
    feature_manager = FeatureManager()
    
    user_context = UserContext(
        user_id=123,
        region="US",
        account_type="premium",
        beta_program=True
    )

    environment = "production"


    if feature_manager.is_enabled("new_ui", vars(user_context), environment):
        print("New UI Active for this user!")
    
    if feature_manager.is_enabled("advanced_search", vars(user_context), environment):
        print("Advanced Search is Active for this user!")
        performance_monitor = PerformanceMonitor(feature_manager)

        try:
            result = performance_monitor.monitor("advanced_search", lambda: {
                # The code for our Advanced search that can also raise some Exceptions
                print("Advanced Search: No results found")
            })
            
            pass
        except Exception as e:
            error_reporter = ErrorReporter(feature_manager)
            error_reporter.report("advanced_search")
            print(f"Error occurred: {e}")

    # Start the traffic monitor in a separate thread
    traffic_thread = threading.Thread(target=traffic_monitoring_job, args=(feature_manager,))
    traffic_thread.daemon = True  # So that the thread will close when the main program closes
    traffic_thread.start()

    # Add Support for Dynamic Configuration Reload
    hot_reload_thread = threading.Thread(target=refresh_configuration, args=())
    hot_reload_thread.daemon = True
    hot_reload_thread.start()


    # Keeping the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting main program...")


if __name__ == "__main__":
    main()
