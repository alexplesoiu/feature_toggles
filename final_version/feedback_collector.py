from typing import List, Dict


class FeedbackCollector:
    def __init__(self) -> None:
        self._feedbacks: Dict[str, str] = {}


    def collect(self, feature_name: str, feedback: str) -> None:
        if feature_name not in self._feedbacks:
            self._feedbacks[feature_name] = []
        self._feedbacks[feature_name].append(feedback)


    def get_feedback(self, feature_name: str) -> List[str]:
        return self._feedbacks.get(feature_name, [])
