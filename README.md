# Metabase DB Schema Notifier

This script notifies a Metabase instance about potential schema changes for a specific table within a database, triggering a re-scan if necessary.

## Prerequisites

1.  **Python 3**: Ensure you have Python 3 installed.
2.  **Metabase API Key**: You need a Metabase API key with permissions to access the `/api/notify/db/:id` endpoint. This key should be provided via the `--api-key` argument or, ideally, set as an environment variable (though the current script requires it as an argument).

## Usage

To use the main.py script for notifying a Metabase instance about database schema changes, follow these steps:

1. Prerequisites

Ensure you have the following:

- Python 3 installed on your system.
- A valid Metabase API key with permissions to access the /api/notify/db/:id endpoint.
- The database ID, table ID, and table name for the schema you want to notify Metabase about.
- The Metabase hostname (e.g., http://localhost:3000).

2. Running the Script

Run the script from the terminal using the following command format:

```
python3 /path/to/main.py <db_id> --table-id <table_id> --table-name <table_name> --metabase-host <metabase_host> --api-key <api_key> [--scan <scan_type>]
```

3. Arguments

db_id: The ID of the database in Metabase (required positional argument).
--table-id: The ID of the table (required).
--table-name: The name of the table (required).
--metabase-host: The Metabase hostname, including the protocol (e.g., http://localhost:3000) (required).
--api-key: The Metabase API key (required).
--scan: The type of scan to perform. Defaults to "full" (optional).

4. Example Usage

Here’s an example command:
```
python3 /home/luis/Documents/labs/new-labs/postgres/lotsa/syncer/main.py 1 --table-id 123 --table-name "users" --metabase-host "http://localhost:3000" --api-key "your_api_key_here" --scan "full"
```

5. Notes
- Ensure the --metabase-host starts with http:// or https://. Otherwise, a warning will be displayed.
- The script will validate the inputs and exit with an error message if any required argument is invalid.
- The --scan argument can be omitted if you want to use the default "full" scan type.
