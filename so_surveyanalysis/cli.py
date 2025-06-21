import cmd
from so_surveyanalysis.loader import SurveyDataLoader
from so_surveyanalysis.queries import SurveyQueryEngine
from tabulate import tabulate


class SurveyShell(cmd.Cmd):
    intro = "Welcome to the Stack Overflow Survey CLI. Type 'help' or '?' to list commands.\n"
    prompt = "(survey) "

    def __init__(self, file_path):
        super().__init__()
        self.loader = SurveyDataLoader(file_path)
        self.engine = SurveyQueryEngine(self.loader.get_raw_data(), self.loader.question_types)

    def do_list(self, arg):
        """List all questions"""
        for q in self.loader.list_questions():
            print(q)

    def do_show(self, question):
        """Show metadata and answer type for a question: show <question>"""
        if question not in self.loader.questions:
            print("Question not found.")
            return
        print(f"Question: {question}")
        print(f"Type: {self.loader.get_question_type(question)}")
        responses = self.loader.data[question].dropna().unique()[:10]
        print("Sample responses:", responses)

    def do_search(self, keyword):
        """Search for questions/options containing keyword: search <keyword>"""
        if not keyword:
            print("Provide a keyword.")
            return
        matches = self.engine.search_questions(keyword)
        print(f"Found {len(matches)} matches:")
        for m in matches:
            print(" -", m)

    def do_subset(self, arg):
        """Filter respondents by question and option: subset <question> <option>"""
        try:
            q, opt = arg.split(" ", 1)
        except ValueError:
            print("Usage: subset <question> <option>")
            return
        try:
            subset = self.engine.subset_respondents(q, opt)
            print(f"{len(subset)} respondents matched.")
        except Exception as e:
            print("Error:", e)

    def do_dist(self, question):
        """Show answer distribution for question: dist <question>"""
        try:
            dist = self.engine.get_distribution(question)
            print(tabulate(dist.reset_index().values, headers=["Answer", "Share"], tablefmt="github"))
        except Exception as e:
            print("Error:", e)

    def do_exit(self, _):
        """Exit the program"""
        print("Goodbye.")
        return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Stack Overflow Survey CLI")
    parser.add_argument("file", help="Path to the XLSX survey file")

    subparsers = parser.add_subparsers(dest="command", required=False)

    # repl
    subparsers.add_parser("repl", help="Launch interactive shell")

    # list
    subparsers.add_parser("list", help="List all questions")

    # show
    show_parser = subparsers.add_parser("show", help="Show metadata for a question")
    show_parser.add_argument("question")

    # search
    search_parser = subparsers.add_parser("search", help="Search for questions/options")
    search_parser.add_argument("keyword")

    # subset
    subset_parser = subparsers.add_parser("subset", help="Filter respondents by question and option")
    subset_parser.add_argument("question")
    subset_parser.add_argument("option")

    # dist
    dist_parser = subparsers.add_parser("dist", help="Show answer distribution")
    dist_parser.add_argument("question")

    args = parser.parse_args()

    # Load the dataset
    loader = SurveyDataLoader(args.file)
    engine = SurveyQueryEngine(loader.get_raw_data(), loader.question_types)

    # Handle subcommands
    if args.command == "repl" or args.command is None:
        SurveyShell(args.file).cmdloop()

    elif args.command == "list":
        for q in loader.list_questions():
            print(q)

    elif args.command == "show":
        q = args.question
        if q not in loader.questions:
            print("Question not found.")
        else:
            print(f"Question: {q}")
            print(f"Type: {loader.get_question_type(q)}")
            responses = loader.data[q].dropna().unique()[:10]
            print("Sample responses:", responses)

    elif args.command == "search":
        matches = engine.search_questions(args.keyword)
        for m in matches:
            print(m)

    elif args.command == "subset":
        subset = engine.subset_respondents(args.question, args.option)
        print(f"{len(subset)} respondents matched.")

    elif args.command == "dist":
        dist = engine.get_distribution(args.question)
        print(tabulate(dist.reset_index().values, headers=["Answer", "Share"], tablefmt="github"))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()