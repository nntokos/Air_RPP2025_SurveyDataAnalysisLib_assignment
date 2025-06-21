# tests/test_loader.py

import pytest
import pandas as pd
from so_surveyanalysis.loader import SurveyDataLoader

def test_loader_reads_data(tmp_path):
    # Prepare test data
    df = pd.DataFrame({
        "MainBranch": ["Employed full-time", "Freelancer", None],
        "LanguageWorkedWith": ["Python;JavaScript", "C++;Python", "Java"],
    })
    file_path = tmp_path / "sample_survey.xlsx"
    df.to_excel(file_path, index=False)

    # Load data
    loader = SurveyDataLoader(file_path)

    assert loader.data.shape[0] == 3
    assert "MainBranch" in loader.questions
    assert loader.get_question_type("LanguageWorkedWith") == "MC"
    assert loader.get_question_type("MainBranch") == "SC"