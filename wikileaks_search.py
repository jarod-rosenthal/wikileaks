import requests
import sys
import tempfile
import subprocess
from urllib.parse import urlencode

def search_wikileaks(query, exact_phrase, any_of, exclude_words, document_date_start, document_date_end, released_date_start, released_date_end):
    # Construct the query parameters
    params = {
        'query': query,
        'exact_phrase': exact_phrase,
        'any_of': any_of,
        'exclude_words': exclude_words,
        'document_date_start': document_date_start,
        'document_date_end': document_date_end,
        'released_date_start': released_date_start,
        'released_date_end': released_date_end,
        'new_search': 'True'
    }

    # URL encode the parameters
    encoded_params = urlencode(params)

    # Construct the URL
    url = f"https://search.wikileaks.org/?{encoded_params}"

    # Send the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return "Error: Unable to fetch data"

# Check if enough arguments are provided
if len(sys.argv) < 9:
    print("Usage: python wikileaks_search.py <query> <exact_phrase> <any_of> <exclude_words> <document_date_start> <document_date_end> <released_date_start> <released_date_end>")
    sys.exit(1)

# Unpack arguments
_, query, exact_phrase, any_of, exclude_words, document_date_start, document_date_end, released_date_start, released_date_end = sys.argv

# Call the function with CLI arguments
result = search_wikileaks(query, exact_phrase, any_of, exclude_words, document_date_start, document_date_end, released_date_start, released_date_end)

# Save result to a temporary file
with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.html') as tmp_file:
    tmp_file.write(result)
    tmp_file_path = tmp_file.name

# Open the temporary file in lynx
subprocess.run(['lynx', tmp_file_path])

