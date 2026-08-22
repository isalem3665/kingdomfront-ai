from src.planner_stage import PlannerStageClassifier


class TestPlannerStageClassifier:

    def test_local_stage(self):
        context = {
            "city": "riyadh",
            "available_days": 1
        }

        classifier = PlannerStageClassifier(context)
        actual_result = classifier.detect_stage()
        expected_result = "local"

        assert actual_result == expected_result

    def test_travel_stage(self):
        context = {
            "city": "jeddah",
            "available_days": 2
        }

        classifier = PlannerStageClassifier(context)
        actual_result = classifier.detect_stage()
        expected_result = "travel"

        assert actual_result == expected_result

    def test_family_stage(self):
        context = {
            "city": "riyadh",
            "available_days": 2,
            "has_kids": 1
        }

        classifier = PlannerStageClassifier(context)
        actual_result = classifier.detect_stage()
        expected_result = "family"

        assert actual_result == expected_result