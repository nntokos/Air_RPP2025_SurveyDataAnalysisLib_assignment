"""
Query and analysis module for Stack Overflow Survey Analysis Library.
Provides functions for analyzing survey data distributions and statistics.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from collections import Counter
import math


class SurveyAnalyzer:
    """
    Analyzes survey data to provide insights and distributions.
    
    Works in conjunction with SurveyDataLoader to perform various
    analytical operations on the survey data.
    """
    
    def __init__(self, loader):
        """
        Initialize analyzer with a data loader.
        
        Args:
            loader: SurveyDataLoader instance
        """
        self.loader = loader
        self.data = loader.get_data()
    
    def get_answer_distribution(self, question: str, 
                              top_n: Optional[int] = None) -> Dict[str, Dict[str, any]]:
        """
        Get the distribution of answers for a specific question.
        
        Args:
            question: Question name
            top_n: Limit results to top N most common answers (None for all)
            
        Returns:
            Dictionary with answer distribution statistics
        """
        if question not in self.loader.get_questions():
            raise ValueError(f"Question '{question}' not found in survey data")
        
        question_type = self.loader.get_question_type(question)
        total_respondents = len(self.data)
        valid_responses = self.data[question].dropna()
        valid_count = len(valid_responses)
        
        if question_type == 'SC':
            # Single choice - direct value counts
            answer_counts = valid_responses.value_counts()
        else:
            # Multiple choice - split and count individual options
            all_answers = []
            for response in valid_responses:
                if pd.notna(response):
                    answers = [ans.strip() for ans in str(response).split(';')]
                    all_answers.extend(answers)
            answer_counts = pd.Series(all_answers).value_counts()
        
        # Apply top_n limit if specified
        if top_n:
            answer_counts = answer_counts.head(top_n)
        
        # Calculate percentages
        distribution = {}
        for answer, count in answer_counts.items():
            if question_type == 'SC':
                # For SC, percentage is out of total valid responses
                percentage = (count / valid_count) * 100
            else:
                # For MC, percentage is out of total respondents (since one can select multiple)
                percentage = (count / total_respondents) * 100
            
            distribution[answer] = {
                'count': count,
                'percentage': percentage
            }
        
        return {
            'question': question,
            'question_type': question_type,
            'total_respondents': total_respondents,
            'valid_responses': valid_count,
            'missing_responses': total_respondents - valid_count,
            'distribution': distribution
        }
    
    def compare_distributions(self, question1: str, question2: str) -> Dict[str, any]:
        """
        Compare distributions between two questions.
        
        Args:
            question1: First question name
            question2: Second question name
            
        Returns:
            Dictionary with comparison statistics
        """
        dist1 = self.get_answer_distribution(question1)
        dist2 = self.get_answer_distribution(question2)
        
        return {
            'question1': dist1,
            'question2': dist2,
            'comparison': {
                'q1_valid_rate': dist1['valid_responses'] / dist1['total_respondents'],
                'q2_valid_rate': dist2['valid_responses'] / dist2['total_respondents'],
                'q1_most_common': max(dist1['distribution'].items(), 
                                    key=lambda x: x[1]['count']) if dist1['distribution'] else None,
                'q2_most_common': max(dist2['distribution'].items(), 
                                    key=lambda x: x[1]['count']) if dist2['distribution'] else None,
            }
        }
    
    def get_cross_tabulation(self, question1: str, question2: str) -> pd.DataFrame:
        """
        Create a cross-tabulation between two single-choice questions.
        
        Args:
            question1: First question name
            question2: Second question name
            
        Returns:
            DataFrame with cross-tabulation results
        """
        # Verify both questions are single choice
        if self.loader.get_question_type(question1) != 'SC':
            raise ValueError(f"Question '{question1}' must be single choice for cross-tabulation")
        if self.loader.get_question_type(question2) != 'SC':
            raise ValueError(f"Question '{question2}' must be single choice for cross-tabulation")
        
        return pd.crosstab(self.data[question1], self.data[question2], margins=True)
    
    def get_subset_distribution(self, base_question: str, base_option: str, 
                               target_question: str, top_n: Optional[int] = None) -> Dict[str, any]:
        """
        Get distribution of a target question within a subset of respondents.
        
        Args:
            base_question: Question to filter by
            base_option: Option value to filter on
            target_question: Question to analyze within the subset
            top_n: Limit results to top N answers
            
        Returns:
            Dictionary with subset distribution statistics
        """
        subset = self.loader.get_respondent_subset(base_question, base_option)
        
        # Create temporary analyzer for the subset
        class SubsetLoader:
            def __init__(self, data, original_loader):
                self.data = data
                self.original_loader = original_loader
            
            def get_questions(self):
                return self.original_loader.get_questions()
            
            def get_question_type(self, question):
                return self.original_loader.get_question_type(question)
            
            def get_data(self):
                return self.data
        
        subset_loader = SubsetLoader(subset, self.loader)
        subset_analyzer = SurveyAnalyzer(subset_loader)
        
        result = subset_analyzer.get_answer_distribution(target_question, top_n)
        result['subset_info'] = {
            'base_question': base_question,
            'base_option': base_option,
            'subset_size': len(subset)
        }
        
        return result
    
    def get_question_completeness(self) -> List[Dict[str, any]]:
        """
        Get completeness statistics for all questions.
        
        Returns:
            List of dictionaries with completeness info for each question
        """
        total_respondents = len(self.data)
        completeness = []
        
        for question in self.loader.get_questions():
            valid_count = self.data[question].count()  # count() excludes NaN
            missing_count = total_respondents - valid_count
            
            completeness.append({
                'question': question,
                'question_type': self.loader.get_question_type(question),
                'valid_responses': valid_count,
                'missing_responses': missing_count,
                'completion_rate': valid_count / total_respondents,
                'missing_rate': missing_count / total_respondents
            })
        
        # Sort by completion rate (descending)
        completeness.sort(key=lambda x: x['completion_rate'], reverse=True)
        return completeness
    
    def get_summary_statistics(self) -> Dict[str, any]:
        """
        Get overall summary statistics for the survey.
        
        Returns:
            Dictionary with comprehensive survey statistics
        """
        info = self.loader.get_survey_info()
        completeness = self.get_question_completeness()
        
        # Calculate average completion rates
        avg_completion = sum(q['completion_rate'] for q in completeness) / len(completeness)
        
        # Find questions with highest/lowest completion rates
        highest_completion = max(completeness, key=lambda x: x['completion_rate'])
        lowest_completion = min(completeness, key=lambda x: x['completion_rate'])
        
        return {
            **info,
            'average_completion_rate': avg_completion,
            'highest_completion': highest_completion,
            'lowest_completion': lowest_completion,
            'questions_above_50_percent': len([q for q in completeness if q['completion_rate'] > 0.5]),
            'questions_above_90_percent': len([q for q in completeness if q['completion_rate'] > 0.9])
        }