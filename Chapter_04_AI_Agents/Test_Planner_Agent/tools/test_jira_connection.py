import argparse
import requests
import json
import sys

def test_jira_connection(url, email, api_token):
    """
    Test Jira API connection.
    Endpoint: GET /rest/api/3/myself or /rest/api/2/myself
    """
    if not url.startswith("http"):
        url = "https://" + url
    
    endpoint = f"{url.rstrip('/')}/rest/api/2/myself"
    
    try:
        response = requests.get(
            endpoint,
            auth=(email, api_token),
            headers={"Accept": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print(json.dumps({"status": "success", "message": f"Successfully connected to Jira as {response.json().get('displayName')}"}))
            return True
        else:
            print(json.dumps({"status": "error", "message": f"Failed to connect. HTTP {response.status_code}: {response.text}"}))
            return False
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Jira Connection")
    parser.add_argument("--url", required=True, help="Jira Base URL")
    parser.add_argument("--email", required=True, help="Jira Email")
    parser.add_argument("--token", required=True, help="Jira API Token")
    
    args = parser.parse_args()
    success = test_jira_connection(args.url, args.email, args.token)
    if not success:
        sys.exit(1)
