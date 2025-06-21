import pytest
import pandas as pd
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
def loader(sample_data):
    """Fixture to initialize the SurveyDataLoader."""
    return SurveyDataLoader(sample_data)


def test_load_data(loader):
    """Test if data is loaded correctly."""
    assert loader.get_data().shape == (4, 3)
    assert len(loader.get_questions()) == 3


def test_question_classification(loader):
    """Test if questions are classified correctly."""
    assert loader.get_question_type("Question 1") == "SC"
    assert loader.get_question_type("Question 2") == "MC"
    assert loader.get_question_type("Question 3") == "SC"


def test_get_question_options(loader):
    """Test retrieving unique options for questions."""
    options_q1 = loader.get_question_options("Question 1")
    assert options_q1 == {"Option A", "Option B"}

    options_q2 = loader.get_question_options("Question 2")
    assert options_q2 == {"A", "B", "C"}


def test_search_questions(loader):
    """Test searching for questions by term."""
    results = loader.search_questions("Question")
    assert len(results) == 3
    assert "Question 1" in results

    results = loader.search_questions("1")
    assert results == ["Question 1"]


def test_search_options(loader):
    """Test searching for options by term."""
    results = loader.search_options("Option")
    assert "Question 1" in results
    assert results["Question 1"] == {"Option A", "Option B"}

    results = loader.search_options("A")
    assert "Question 1" in results
    assert "Question 2" in results
    assert results["Question 1"] == {"Option A"}
    assert results["Question 2"] == {"A"}


def test_get_respondent_subset(loader):
    """Test creating subsets of respondents."""
    subset_q1 = loader.get_respondent_subset("Question 1", "Option A")
    assert subset_q1.shape[0] == 2

    subset_q2 = loader.get_respondent_subset("Question 2", "A")
    assert subset_q2.shape[0] == 2


def test_get_survey_info(loader):
    """Test retrieving survey summary information."""
    info = loader.get_survey_info()
    assert info["total_respondents"] == 4
    assert info["total_questions"] == 3
    assert info["single_choice_questions"] == 2
    assert info["multiple_choice_questions"] == 1
    assert "Question 1" in info["sc_questions"]
    assert "Question 2" in info["mc_questions"]