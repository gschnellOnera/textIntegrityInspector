import os
import sys
import argparse
import toml
import yaml
import logging
from textIntegrityInspector.validator import TextIntegrityChar

def parse_arguments(args=None):
    parser = argparse.ArgumentParser(description="Text Integrity Inspector - Validate UTF-8 characters in specified language text files.")

    parser.add_argument("roots", nargs="*", help="Root directories for analysis (default: current directory)")
    parser.add_argument("--config-file", default=".textIntegrityInspector.yaml", help="Path to the config file (yaml, toml format accepted)")
    parser.add_argument("--extensions", nargs="+", default=[], help="List of file extensions to include in the analysis (default: None -> all extention) (example:--extensions txt py])")
    parser.add_argument("--exclude-dirs", nargs="+", default=[], help="List of directories to exclude from analysis with gitignore syntaxe")
    parser.add_argument("--exclude-files", nargs="+", default=[], help="List of files to exclude from analysis")
    parser.add_argument("--language", choices=["fr", "de", "en"], default=None, help="Language code for character validation (default: None)")
    parser.add_argument("--additional-chars", default="", help="Additional characters accepted in addition to the language-specific ones")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode (INFO level)")

    args = parser.parse_args(args)

    config = {}
    if args.config_file:
        if os.path.isfile(args.config_file) :
            extension = args.config_file.split('.')[-1]
            logging.info(f"Load configuration file {args.config_file}.")
            with open(args.config_file, 'r') as config_file:
                if extension in ['yml', 'yaml', 'YML', 'YAML'] :
                    config = yaml.safe_load(config_file)
                elif extension in ['toml', 'TOML'] :
                    config = toml.load(config_file)
                else : 
                   logging.error(f"The configurtaion file {args.config_file} must be in toml or yaml format") 
    # Add configuration file to configuration by arguments 
    
    if not args.roots:  args.roots=config.get('roots', ['.']) 
    args.extensions += config.get('extensions', [])
    args.exclude_dirs += config.get('exclude-dirs', [])
    args.exclude_files += config.get('exclude-files', [])
    args.language = config.get('language', args.language)
    args.additional_chars += config.get('additional-chars', '')
    args.verbose = config.get('verbose', args.verbose)
    
    return args

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
    logging.info(f"Configuration applied: \n{toml.dumps(vars(args))}")
    main_args(args)


if __name__ == "__main__":  # pragma: no cover
    main()
