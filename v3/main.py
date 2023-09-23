from feature_manager import FeatureManager
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


def main() -> None:
    feature_manager = FeatureManager()
    
    user_context = UserContext(
        user_id=123,
        region="US",
        account_type="premium",
        beta_program=True
    )


    if feature_manager.is_enabled("new_ui", vars(user_context)):
        print("New UI Active for this user!")
    
    if feature_manager.is_enabled("advanced_search", vars(user_context)):
        print("Advanced Search is Active for this user!")

        try:
            # The code for our Advanced search that can raise some Exceptions
            pass
        except Exception as e:
            error_reporter = ErrorReporter(feature_manager)
            error_reporter.report("advanced_search")
            print(f"Error occurred: {e}")

    # Start the traffic monitor in a separate thread
    traffic_thread = threading.Thread(target=traffic_monitoring_job, args=(feature_manager,))
    traffic_thread.daemon = True  # So that the thread will close when the main program closes
    traffic_thread.start()


    # Keeping the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting main program...")


if __name__ == "__main__":
    main()
