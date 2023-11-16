import argparse
from textIntegrityInspector import validator

def parse_arguments():
    parser = argparse.ArgumentParser(description="Text Integrity Inspector - Validate UTF-8 characters in specified language text files.")

    parser.add_argument("roots", nargs="*", default=["."], help="Root directories for analysis (default: current directory)")
    parser.add_argument("--extensions", nargs="+", default=[], help="List of file extensions to include in the analysis (default: Nome) (example: [txt, py])")
    parser.add_argument("--exclude-dirs", nargs="+", default=[], help="List of directories to exclude from analysis")
    parser.add_argument("--exclude-files", nargs="+", default=[], help="List of files to exclude from analysis")
    parser.add_argument("--language", choices=["fr", "de", "en"], default=None, help="Language code for character validation (default: None)")
    parser.add_argument("--additional-chars", default="", help="Additional characters accepted in addition to the language-specific ones")

    return parser.parse_args()

def main():
    args = parse_arguments()

    # Call the validator with the provided arguments
    validator.validate(
        roots=args.roots,
        extensions=args.extensions,
        exclude_dirs=args.exclude_dirs,
        exclude_files=args.exclude_files,
        language=args.language,
        additional_chars=args.additional_chars
    )

if __name__ == "__main__":
    main()
