# tests/test_queries.py

import pytest
import pandas as pd
from so_surveyanalysis.queries import SurveyQueryEngine
from so_surveyanalysis.loader import SurveyDataLoader

@pytest.fixture
def sample_engine(tmp_path):
    df = pd.DataFrame({
        "MainBranch": ["Employed full-time", "Freelancer", "Freelancer"],
        "LanguageWorkedWith": ["Python;JavaScript", "C++;Python", "Java"],
    })
    file_path = tmp_path / "sample_survey.xlsx"
    df.to_excel(file_path, index=False)

    loader = SurveyDataLoader(file_path)
    engine = SurveyQueryEngine(loader.get_raw_data(), loader.question_types)
    return engine

def test_search_questions(sample_engine):
    results = sample_engine.search_questions("python")
    assert "LanguageWorkedWith" in results

def test_subset_respondents(sample_engine):
    subset = sample_engine.subset_respondents("LanguageWorkedWith", "Python")
    assert subset.shape[0] == 2

def test_distribution_mc(sample_engine):
    dist = sample_engine.get_distribution("LanguageWorkedWith", normalize=False)
    assert dist["Python"] == 2
    assert dist["JavaScript"] == 1