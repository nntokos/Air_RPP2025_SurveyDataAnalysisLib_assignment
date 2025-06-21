"""
Data loader module for Stack Overflow Survey Analysis Library.
Handles loading and parsing of survey data from XLSX files.
"""

import pandas as pd
from typing import Dict, List, Set, Optional
import re


class SurveyDataLoader:
    """
    Loads and manages Stack Overflow survey data.
    
    Handles both single-choice (SC) and multiple-choice (MC) questions,
    automatically detecting question types based on the presence of
    semicolon-separated values.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the loader with survey data file.
        
        Args:
            file_path: Path to the XLSX survey data file
        """
        self.file_path = file_path
        self.data: Optional[pd.DataFrame] = None
        self.questions: Optional[List[str]] = None
        self.question_types: Optional[Dict[str, str]] = None
        self._load_data()
    
    def _load_data(self):
        """Load survey data from XLSX file."""
        try:
            self.data = pd.read_excel(self.file_path)
            self.questions = list(self.data.columns)
            self._classify_questions()
            print(f"Loaded survey data: {self.data.shape[0]} respondents, {self.data.shape[1]} questions")
        except Exception as e:
            raise Exception(f"Failed to load data from {self.file_path}: {str(e)}")
    
    def _classify_questions(self):
        """
        Classify questions as Single Choice (SC) or Multiple Choice (MC).
        
        MC questions are identified by the presence of semicolon-separated values.
        """
        self.question_types = {}
        
        for question in self.questions:
            # Sample non-null values to detect multiple choice patterns
            sample_values = self.data[question].dropna().head(100)
            
            # Check if any values contain semicolons (indicating multiple choices)
            has_semicolons = sample_values.astype(str).str.contains(';', na=False).any()
            
            if has_semicolons:
                self.question_types[question] = 'MC'  # Multiple Choice
            else:
                self.question_types[question] = 'SC'  # Single Choice
    
    def get_questions(self) -> List[str]:
        """Get list of all survey questions."""
        return self.questions.copy()
    
    def get_question_type(self, question: str) -> str:
        """
        Get the type of a specific question.
        
        Args:
            question: Question name
            
        Returns:
            'SC' for Single Choice, 'MC' for Multiple Choice
            
        Raises:
            ValueError: If question doesn't exist
        """
        if question not in self.question_types:
            raise ValueError(f"Question '{question}' not found in survey data")
        return self.question_types[question]
    
    def get_question_options(self, question: str) -> Set[str]:
        """
        Get all unique options/answers for a specific question.
        
        For MC questions, extracts individual options from semicolon-separated values.
        For SC questions, returns unique values directly.
        
        Args:
            question: Question name
            
        Returns:
            Set of unique options for the question
        """
        if question not in self.questions:
            raise ValueError(f"Question '{question}' not found in survey data")
        
        question_type = self.get_question_type(question)
        values = self.data[question].dropna()
        
        if question_type == 'MC':
            # For multiple choice, split by semicolon and collect all unique options
            all_options = set()
            for value in values:
                if pd.notna(value):
                    options = [opt.strip() for opt in str(value).split(';')]
                    all_options.update(options)
            return all_options
        else:
            # For single choice, return unique values
            return set(values.unique())
    
    def search_questions(self, search_term: str) -> List[str]:
        """
        Search for questions containing the search term.
        
        Args:
            search_term: Term to search for in question names
            
        Returns:
            List of matching question names
        """
        search_term = search_term.lower()
        return [q for q in self.questions if search_term in q.lower()]
    
    def search_options(self, search_term: str) -> Dict[str, Set[str]]:
        """
        Search for options containing the search term across all questions.
        
        Args:
            search_term: Term to search for in option values
            
        Returns:
            Dictionary mapping question names to matching options
        """
        search_term = search_term.lower()
        results = {}
        
        for question in self.questions:
            try:
                options = self.get_question_options(question)
                matching_options = {opt for opt in options if search_term in opt.lower()}
                if matching_options:
                    results[question] = matching_options
            except Exception:
                # Skip questions that cause errors (e.g., completely empty columns)
                continue
        
        return results
    
    def get_respondent_subset(self, question: str, option: str) -> pd.DataFrame:
        """
        Get subset of respondents who selected a specific option for a question.
        
        Args:
            question: Question name
            option: Option/answer to filter by
            
        Returns:
            DataFrame containing only respondents who selected the specified option
        """
        if question not in self.questions:
            raise ValueError(f"Question '{question}' not found in survey data")
        
        question_type = self.get_question_type(question)
        
        if question_type == 'MC':
            # For multiple choice, check if option is present in semicolon-separated values
            # First filter out NaN values, then check for option presence
            non_null_mask = self.data[question].notna()
            option_mask = self.data[question].astype(str).str.contains(
                re.escape(option), case=False, na=False
            )
            mask = non_null_mask & option_mask
        else:
            # For single choice, exact match (case-insensitive)
            # First filter out NaN values, then check for exact match
            non_null_mask = self.data[question].notna()
            match_mask = self.data[question].astype(str).str.lower() == option.lower()
            mask = non_null_mask & match_mask
        
        return self.data[mask].copy()
    
    def get_data(self) -> pd.DataFrame:
        """Get the complete survey data."""
        return self.data.copy()
    
    def get_survey_info(self) -> Dict[str, any]:
        """
        Get summary information about the survey.
        
        Returns:
            Dictionary with survey statistics
        """
        sc_questions = [q for q, t in self.question_types.items() if t == 'SC']
        mc_questions = [q for q, t in self.question_types.items() if t == 'MC']
        
        return {
            'total_respondents': len(self.data),
            'total_questions': len(self.questions),
            'single_choice_questions': len(sc_questions),
            'multiple_choice_questions': len(mc_questions),
            'sc_questions': sc_questions,
            'mc_questions': mc_questions
        }