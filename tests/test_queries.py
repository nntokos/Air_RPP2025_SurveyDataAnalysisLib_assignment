import pytest
import pandas as pd
from so_surveyanalysis.queries import SurveyAnalyzer
from so_surveyanalysis.loader import SurveyDataLoader


@pytest.fixture
def sample_data(tmp_path):
    """Fixture to create a sample XLSX file for testing."""
    data = {
        "Question 1": ["Option A", "Option B", "Option A", None],
        "Question 2": ["A;B", "B;C", None, "A;C"],
        "Question 3": [1, 2, 3, 4],
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "sample_survey.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


@pytest.fixture
def analyzer(sample_data):
    """Fixture to initialize the SurveyAnalyzer."""
    loader = SurveyDataLoader(sample_data)
    return SurveyAnalyzer(loader)


def test_get_answer_distribution(analyzer):
    """Test the distribution of answers for a question."""
    dist_q1 = analyzer.get_answer_distribution("Question 1")
    assert dist_q1["total_respondents"] == 4
    assert dist_q1["valid_responses"] == 3
    assert dist_q1["missing_responses"] == 1
    assert dist_q1["distribution"]["Option A"]["count"] == 2
    assert dist_q1["distribution"]["Option B"]["count"] == 1

    dist_q2 = analyzer.get_answer_distribution("Question 2")
    assert dist_q2["total_respondents"] == 4
    assert dist_q2["valid_responses"] == 3
    assert dist_q2["missing_responses"] == 1
    assert dist_q2["distribution"]["A"]["count"] == 2
    assert dist_q2["distribution"]["B"]["count"] == 2
    assert dist_q2["distribution"]["C"]["count"] == 2


def test_compare_distributions(analyzer):
    """Test comparison of distributions between two questions."""
    comparison = analyzer.compare_distributions("Question 1", "Question 2")
    assert comparison["question1"]["total_respondents"] == 4
    assert comparison["question2"]["total_respondents"] == 4
    assert comparison["comparison"]["q1_valid_rate"] == 0.75
    assert comparison["comparison"]["q2_valid_rate"] == 0.75
    assert comparison["comparison"]["q1_most_common"][0] == "Option A"
    assert comparison["comparison"]["q2_most_common"][0] in ["A", "B", "C"]


def test_get_cross_tabulation(analyzer):
    """Test cross-tabulation between two single-choice questions."""
    # Add a new SC question for testing
    analyzer.loader.data["Question 4"] = ["X", "Y", "X", "Z"]
    analyzer.loader.questions.append("Question 4")
    analyzer.loader._classify_questions()
    # Update the analyzer's data reference
    analyzer.data = analyzer.loader.get_data()

    cross_tab = analyzer.get_cross_tabulation("Question 1", "Question 4")
    assert cross_tab.loc["Option A", "X"] == 2
    assert cross_tab.loc["Option B", "Y"] == 1
    assert cross_tab.loc["All", "All"] == 3


def test_get_subset_distribution(analyzer):
    """Test distribution of a target question within a subset."""
    subset_dist = analyzer.get_subset_distribution("Question 1", "Option A", "Question 2")
    assert subset_dist["subset_info"]["base_question"] == "Question 1"
    assert subset_dist["subset_info"]["base_option"] == "Option A"
    assert subset_dist["subset_info"]["subset_size"] == 2
    assert subset_dist["distribution"]["A"]["count"] == 1
    assert subset_dist["distribution"]["B"]["count"] == 1


def test_get_question_completeness(analyzer):
    """Test completeness statistics for all questions."""
    completeness = analyzer.get_question_completeness()
    assert len(completeness) == 3
    assert completeness[0]["question"] == "Question 3"  # Highest completion rate
    assert completeness[-1]["question"] == "Question 2"  # Lowest completion rate


def test_get_summary_statistics(analyzer):
    """Test overall summary statistics for the survey."""
    summary = analyzer.get_summary_statistics()
    assert summary["total_respondents"] == 4
    assert summary["total_questions"] == 3
    assert summary["average_completion_rate"] > 0.5
    assert summary["highest_completion"]["question"] == "Question 3"
    assert summary["lowest_completion"]["question"] == "Question 1"