import pandas as pd

class SurveyDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.questions = []
        self.question_types = {}  # SC or MC
        self._load_data()

    def _load_data(self):
        """Load survey data from XLSX file."""
        try:
            self.data = pd.read_excel(self.file_path, engine="openpyxl")
            self.questions = list(self.data.columns)
            self._classify_questions()
            print(f"Loaded survey data: {self.data.shape[0]} respondents, {self.data.shape[1]} questions")
        except Exception as e:
            raise Exception(f"Failed to load data from {self.file_path}: {str(e)}")

    def _classify_questions(self):
        """Classify each question as SC (Single Choice) or MC (Multiple Choice)."""
        for col in self.questions:
            sample = self.data[col].dropna().astype(str)
            if sample.str.contains(";").any():
                self.question_types[col] = "MC"
            else:
                self.question_types[col] = "SC"

    def list_questions(self):
        """Return list of all questions (column names)."""
        return self.questions

    def get_question_type(self, question):
        """Return 'SC' or 'MC' for a given question."""
        return self.question_types.get(question, None)

    def get_raw_data(self):
        """Return the full DataFrame."""
        return self.data