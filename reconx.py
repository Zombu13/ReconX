from intelxapi import intelx
from tabulate import tabulate
import time

# Your IntelX API key
api_key = ""
intelx_client = intelx(api_key)

def simple_search(query):
    try:
        # Perform the search. This returns a search object.
        results_object = intelx_client.search(query)

        if not results_object or not results_object.get('records'):
            print("No results were found.")
            return

        records = results_object['records']
        print(f"Found {len(records)} results for '{query}':\n")

        table_data = []

        for record in records:
            system_id = record.get('systemid', 'N/A')
            bucket = record.get('bucket', 'N/A')
            media_type = record.get('mediah', 'N/A')
            date_found = record.get('date', 'N/A')

            preview = ""
            try:
                if bucket and record.get('storageid'):
                    # Corrected call: Passed positional arguments to FILE_VIEW
                    preview_content_bytes = intelx_client.FILE_VIEW(
                        record.get('type', 0),
                        record.get('media', 0),
                        record.get('storageid'),
                        bucket
                    )

                    preview = preview_content_bytes.decode('utf-8', errors='replace')
                    preview = preview.replace('\n', ' ')[:100] + '...'
                else:
                    preview = "No preview available."

            except Exception as e:
                preview = f"Could not get preview: {e}"

            table_data.append([system_id, bucket, media_type, date_found, preview])

        headers = ["System ID", "Bucket", "Media Type", "Date Found", "Content Preview"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    query = input("Enter an email, domain, or other selector: ")
    simple_search(query)

if __name__ == "__main__":
    main()
