import requests
import json
import os

class JiraClient:
    def __init__(self, url, email, api_token):
        self.url = url.rstrip('/') if url.startswith('http') else 'https://' + url.rstrip('/')
        self.email = email
        self.api_token = api_token

    def fetch_ticket(self, ticket_id):
        """
        Fetches the title, description, and raw JSON of a Jira ticket.
        """
        endpoint = f"{self.url}/rest/api/2/issue/{ticket_id}"
        
        try:
            response = requests.get(
                endpoint,
                auth=(self.email, self.api_token),
                headers={"Accept": "application/json"},
                timeout=15
            )
            
            if response.status_code != 200:
                return {
                    "error": True,
                    "message": f"Jira API error {response.status_code}: {response.text}"
                }
            
            data = response.json()
            fields = data.get('fields', {})
            
            summary = fields.get('summary', 'No Title')
            
            # Simple description extraction (ADF format check)
            desc_field = fields.get('description')
            description = "No Description"
            if isinstance(desc_field, dict) and desc_field.get('type') == 'doc':
                # Quick parse of Atlassian Document Format
                texts = []
                for v in desc_field.get('content', []):
                    for c in v.get('content', []):
                        if c.get('type') == 'text':
                            texts.append(c.get('text', ''))
                description = " ".join(texts)
            elif isinstance(desc_field, str):
                description = desc_field
                
            return {
                "error": False,
                "ticket_id": ticket_id,
                "title": summary,
                "description": description,
                "raw_acceptance_criteria": fields.get('customfield_10000', '') # Example generic fallback
            }
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Exception occurred: {str(e)}"
            }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--ticket", required=True)
    args = parser.parse_args()
    
    client = JiraClient(args.url, args.email, args.token)
    print(json.dumps(client.fetch_ticket(args.ticket), indent=2))
