import pandas as pd

class SurveyQueryEngine:
    def __init__(self, data, question_types):
        """
        Parameters:
            data (pd.DataFrame): The survey responses
            question_types (dict): Mapping of question to "SC" or "MC"
        """
        self.data = data
        self.question_types = question_types

    def search_questions(self, keyword):
        """Return list of questions where keyword is found in question ID or any response."""
        keyword = keyword.lower()
        matches = []

        for col in self.data.columns:
            if keyword in col.lower():
                matches.append(col)
                continue
            series = self.data[col].dropna().astype(str)
            if series.str.lower().str.contains(keyword).any():
                matches.append(col)

        return matches

    def subset_respondents(self, question, option):
        """Return DataFrame of respondents who selected the given option."""
        if question not in self.data.columns:
            raise ValueError(f"Question '{question}' not found.")

        question_type = self.question_types.get(question, "SC")
        column = self.data[question].dropna().astype(str)

        if question_type == "MC":
            mask = column.str.contains(rf"\b{option}\b", case=False, na=False)
        else:
            mask = column.str.lower() == option.lower()

        return self.data[mask]

    def get_distribution(self, question, normalize=True):
        """Return distribution (value counts) of answers for a question."""
        if question not in self.data.columns:
            raise ValueError(f"Question '{question}' not found.")

        question_type = self.question_types.get(question, "SC")
        column = self.data[question].dropna().astype(str)

        if question_type == "MC":
            exploded = column.str.split(';').explode().str.strip()
            counts = exploded.value_counts(normalize=normalize)
        else:
            counts = column.value_counts(normalize=normalize)

        return counts