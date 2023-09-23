from feature_manager import FeatureManager


def main():
    feature_manager = FeatureManager()

    if feature_manager.is_enabled("new_ui"):
        print("-> Displaying the new UI")
    
    if feature_manager.is_enabled("advanced_search"):
        print("-> Using Advanced Search")


    '''
    You can use Feature Toggles to control which algorithm to use
    '''
    if feature_manager.is_enabled("new_display_algorithm"):
        print("-> Displaying items using the new algorithm")
    else:
        print("-> Displaying items using the old algorithm")


if __name__ == "__main__":
    main()