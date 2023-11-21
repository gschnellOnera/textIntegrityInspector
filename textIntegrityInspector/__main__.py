import argparse
import logging
from textIntegrityInspector.validator import TextIntegrityChar

def parse_arguments(args=None):
    parser = argparse.ArgumentParser(description="Text Integrity Inspector - Validate UTF-8 characters in specified language text files.")

    parser.add_argument("roots", nargs="*", default=["."], help="Root directories for analysis (default: current directory)")
    parser.add_argument("--extensions", nargs="+", default=[], help="List of file extensions to include in the analysis (default: None -> all extention) (example:--extensions txt py])")
    parser.add_argument("--exclude-dirs", nargs="+", default=[], help="List of directories to exclude from analysis with gitignore syntaxe")
    parser.add_argument("--exclude-files", nargs="+", default=[], help="List of files to exclude from analysis")
    parser.add_argument("--language", choices=["fr", "de", "en"], default=None, help="Language code for character validation (default: None)")
    parser.add_argument("--additional-chars", default="", help="Additional characters accepted in addition to the language-specific ones")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode (INFO level)")

    return parser.parse_args(args)

def main_args(args): 
    
    textIntegrityChar = TextIntegrityChar()
    # Call the validator with the provided arguments
    for root in args.roots :
       textIntegrityChar.validate_directory(
            root=root,
            extensions=args.extensions,
            exclude_dirs=args.exclude_dirs,
            exclude_files=args.exclude_files,
            language=args.language,
            additional_chars=args.additional_chars)
    textIntegrityChar.print_lErrors()
    textIntegrityChar.print_speCar()

def configure_logging(verbose):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s', stream=sys.stderr)

def main():  # pragma: no cover
    args = parse_arguments()
    configure_logging(args.verbose)
    main_args(args)


if __name__ == "__main__":  # pragma: no cover
    import sys
    
    sys.argv.append('--language') 
    sys.argv.append('fr') 
    sys.argv.append('--exclude-dirs') 
    sys.argv.append('.venv') 
    sys.argv.append('.git') 
    sys.argv.append('**\\dist') 
    sys.argv.append('**\\target') 
    sys.argv.append('.pytest_cache') 
    sys.argv.append('**\\FitnesseSikuli') 
    sys.argv.append('**\\win32-64') 
   
    sys.argv.append('--extensions') 
    sys.argv.append('py',) 
    sys.argv.append('java')
    sys.argv.append('txt')
    sys.argv.append('--') 
    sys.argv.append('D:\gschnell\Development_SATIS\workspace\Satis')
    
    
    #sys.argv.append('--exclude-dirs=.git')
    main()
