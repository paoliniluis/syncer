import argparse
import json
import sys
import ssl

import urllib.request
import urllib.error

def main():
    parser = argparse.ArgumentParser(description="Notify Metabase about DB schema changes.")
    parser.add_argument("db_id", type=int, help="The ID of the database in Metabase.")
    parser.add_argument("--table-id", type=int, required=True, help="The ID of the table.")
    parser.add_argument("--table-name", type=str, required=True, help="The name of the table.")
    parser.add_argument("--metabase-host", type=str, required=True, help="Metabase hostname (e.g., http://localhost:3000).")
    parser.add_argument("--api-key", type=str, required=True, help="Metabase API key.")
    parser.add_argument("--scan", type=str, default="full", help="Scan type (default: full).")

    args = parser.parse_args()

    # Validate inputs
    if args.table_id <= 0:
        print("Error: --table-id must be greater than zero.", file=sys.stderr)
        sys.exit(1)
    if not args.table_name.strip():
        print("Error: --table-name must not be blank.", file=sys.stderr)
        sys.exit(1)
    if not args.metabase_host.startswith(('http://', 'https://')):
         print("Warning: --metabase-host should start with http:// or https://", file=sys.stderr)


    # Construct URL and data
    url = f"{args.metabase_host.rstrip('/')}/api/notify/db/{args.db_id}"
    data = {
        "scan": args.scan,
        "table_id": args.table_id,
        "table_name": args.table_name,
    }
    json_data = json.dumps(data).encode('utf-8')

    # Construct headers
    headers = {
        "Content-Type": "application/json",
        "X-METABASE-APIKEY": args.api_key,
    }

    # Create and send request
    req = urllib.request.Request(url, data=json_data, headers=headers, method='POST')

    # Create an unverified SSL context (use with caution)
    context = ssl._create_unverified_context()

    try:
        print(f"Sending POST request to {url}")
        print(f"Body: {data}")
        # Pass the unverified context to urlopen
        with urllib.request.urlopen(req, context=context) as response:
            response_body = response.read().decode('utf-8')
            print(f"Response Status: {response.status}")
            print(f"Response Body: {response_body}")
            if response.status >= 400:
                 sys.exit(1) # Exit with error if status indicates failure

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error Body: {error_body}", file=sys.stderr)
        except Exception:
            print("Could not read error body.", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
