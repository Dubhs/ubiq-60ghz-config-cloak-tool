from read_write_60ghz_config import (
    extract_wave_config,
    overwrite_wave_backup,
    write_wave_config,
    load_wave_config
)
import tarfile
import json
import argparse

def extract(gzip_file_path):
    """
    Extracts the config.json file from the given gzipped tar file and prints it in a pretty-printed format.
    
    Parameters:
    gzip_file_path (str): The path to the gzipped tar file containing the config.json.
    """
    with tarfile.open(gzip_file_path, 'r:gz') as config_tar_file:
        config = extract_wave_config(config_tar_file)
        if config is not None:
            config_dict = json.dumps(json.loads(config), indent=2)
            print(config_dict)
            write_wave_config(config, "extracted_config.json")
    
def overwrite(template, backup):
    """
    Overwrites the config.json file in the backup gzipped tar file with the contents of the template config file.
    
    Parameters:
    template (str): The path to the template config file.
    backup (str): The path to the backup gzipped tar file.
    """
    config = load_wave_config(template)
    overwrite_wave_backup(backup, config)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Edit a 60GHz config file. Usage:\n\n"
            "extract: Extract and pretty-print the config.json from the given backup file.\n"
            "   Example: overwrite --config config_path --backup backup_path\n\n"
            "overwrite: Overwrite the config.json in the backup file with the contents of the template file.\n"
            "   Example: extract --backup backup_path",
        formatter_class=argparse.RawTextHelpFormatter
    )
    argparser.add_argument(
        "command", 
        choices=["extract", "overwrite"]
    )
    argparser.add_argument(
        "--config", 
        help="Path to the template config file (required for 'overwrite' command)."
    )
    argparser.add_argument(
        "--backup", 
        help="Path to the backup gzipped tar file (required for both 'extract' and 'overwrite' commands)."
    )

    args = argparser.parse_args()
    
    if args.command == "extract":
        if args.backup is None:
            print("Error: --backup is required for the 'extract' command.")
        else:
            extract(args.backup)
    elif args.command == "overwrite":
        if args.config is None or args.backup is None:
            print("Error: Both --config and --backup are required for the 'overwrite' command.")
        else:
            overwrite(args.config, args.backup)
