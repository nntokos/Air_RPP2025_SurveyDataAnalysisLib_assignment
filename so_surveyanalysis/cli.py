import argparse
from tabulate import tabulate
from .loader import SurveyDataLoader
from .queries import SurveyAnalyzer


def display_survey_structure(loader):
    """Display the survey structure (list of questions)."""
    questions = loader.get_questions()
    print("Survey Questions:")
    for idx, question in enumerate(questions, 1):
        print(f"{idx}. {question}")


def search_question_or_option(loader, search_term):
    """Search for specific question or option."""
    print(f"Searching for '{search_term}'...")
    matching_questions = loader.search_questions(search_term)
    matching_options = loader.search_options(search_term)

    if matching_questions:
        print("\nMatching Questions:")
        for question in matching_questions:
            print(f"- {question}")
    else:
        print("\nNo matching questions found.")

    if matching_options:
        print("\nMatching Options:")
        for question, options in matching_options.items():
            print(f"- {question}: {', '.join(options)}")
    else:
        print("\nNo matching options found.")


def make_respondent_subset(loader, base_question, base_option):
    """Create a subset of respondents based on a question and option."""
    try:
        subset = loader.get_respondent_subset(base_question, base_option)
        print(f"Subset created with {len(subset)} respondents who selected '{base_option}' for '{base_question}'.")
    except ValueError as e:
        print(f"Error: {e}")


def display_answer_distribution(analyzer, question):
    """Display the distribution of answers for a question."""
    try:
        distribution = analyzer.get_answer_distribution(question)
        print(f"Answer Distribution for '{question}':")
        print(f"Total Respondents: {distribution['total_respondents']}")
        print(f"Valid Responses: {distribution['valid_responses']}")
        print(f"Missing Responses: {distribution['missing_responses']}")
        print("\nDistribution:")
        table = [
            [answer, stats['count'], f"{stats['percentage']:.2f}%"]
            for answer, stats in distribution['distribution'].items()
        ]
        print(tabulate(table, headers=["Answer", "Count", "Percentage"]))
    except ValueError as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Stack Overflow Survey Data Analysis CLI")
    parser.add_argument("file", help="Path to the survey data XLSX file")
    parser.add_argument("--structure", action="store_true", help="Display the survey structure (list of questions)")
    parser.add_argument("--search", type=str, help="Search for a specific question or option")
    parser.add_argument("--subset", nargs=2, metavar=("QUESTION", "OPTION"),
                        help="Create a subset of respondents based on a question and option")
    parser.add_argument("--distribution", type=str, help="Display the distribution of answers for a question")

    args = parser.parse_args()

    # Load survey data
    try:
        loader = SurveyDataLoader(args.file)
        analyzer = SurveyAnalyzer(loader)
    except Exception as e:
        print(f"Failed to load survey data: {e}")
        return

    # Handle CLI options
    if args.structure:
        display_survey_structure(loader)
    if args.search:
        search_question_or_option(loader, args.search)
    if args.subset:
        base_question, base_option = args.subset
        make_respondent_subset(loader, base_question, base_option)
    if args.distribution:
        display_answer_distribution(analyzer, args.distribution)


if __name__ == "__main__":
    main()