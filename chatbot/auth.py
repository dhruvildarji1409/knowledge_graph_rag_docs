#!/usr/bin/env python3

import os
import time
import json
import sys
import base64
import re
from pathlib import Path

# Handle import errors gracefully
try:
    import requests
    from openai import AzureOpenAI
    DEPENDENCIES_INSTALLED = True
except ImportError:
    DEPENDENCIES_INSTALLED = False
    print("Warning: Required dependencies not installed. Using simulated responses only.", file=sys.stderr)
    print("To install dependencies: pip install requests openai", file=sys.stderr)


def basic_auth(p_client_id, p_client_secret):
    """Create Basic Auth header value."""
    token = base64.b64encode(f"{p_client_id}:{p_client_secret}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

def get_oauth_token(p_token_url, p_client_id, p_client_secret, p_scope):
    """Get OAuth token from server or cache."""
    if not DEPENDENCIES_INSTALLED:
        return None
        
    file_name = "py_llm_oauth_token.json"
    try:
        base_path = Path(__file__).parent
        file_path = Path.joinpath(base_path, file_name)
    except Exception as e:
        print(f"Error occurred while setting file path: {e}", file=sys.stderr)
        return None

    try:
        # Check if the token is cached
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                token = json.load(f)
                
                # Check if the token is expired
                if "expires_in" in token and "created_at" in token:
                    expiry_time = token["created_at"] + token["expires_in"]
                    if time.time() < expiry_time:
                        return token["access_token"]
        
        # Get a new token from the OAuth server
        payload = "grant_type=client_credentials&scope=" + p_scope
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": basic_auth(p_client_id, p_client_secret)
        }
        
        response = requests.request("POST", p_token_url, headers=headers, data=payload)
        token = response.json()
        
        # Add creation timestamp
        token["created_at"] = time.time()
        
        with open(file_path, "w") as f:
            json.dump(token, f)
            
        return token["access_token"]
    except Exception as e:
        print(f"Error occurred while getting OAuth token: {e}", file=sys.stderr)
        return None

def get_azure_client():
    """Get authenticated Azure OpenAI client."""
    if not DEPENDENCIES_INSTALLED:
        return None
        
    try:
        # Azure OpenAI credentials
        client_id = "nvssa-prd-_lwo4JYj0iZDQaQhmQE64W5gl25gqmvjnBjvY-6YSuU"
        client_secret = "ssap-ryqWx5WbHYNulr9TPcA"
        token_url = "https://5kbfxgaqc3xgz8nhid1x1r8cfestoypn-trofuum-oc.ssa.nvidia.com/token"
        scope = "azureopenai-readwrite"

        token = get_oauth_token(token_url, client_id, client_secret, scope)
        if not token:
            return None
            
        api_base = "https://prod.api.nvidia.com/llm/v1/azure/openai"
        api_version = "2023-12-01-preview"

        client = AzureOpenAI(api_key=token, api_version=api_version, base_url=api_base)
        return client
    except Exception as e:
        print(f"Error creating Azure OpenAI client: {e}", file=sys.stderr)
        return None



def client_llm(messages):
    """Get response from LLM, falling back to simulated responses if unavailable."""
    print("Getting LLM response...")
    if DEPENDENCIES_INSTALLED:
        try:
            # Get the Azure OpenAI client
            client = get_azure_client()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000
            )
            return response.choices[0].message.content
            # print(client)
            # if client:
            #     # Add user prompt
            #     messages = [{"role": "user", "content": "What is the capital of the moon?"}]
            #     # Call the OpenAI Chat Completion
            #     completion = client.chat.completions.create(
            #         model="gpt-4o",
            #         messages=messages,
            #         max_tokens=1000
            #     )
            #     print(completion)
            # return completion.choices[0].message.content
        
        except Exception as e:
            print(f"Error calling LLM API: {e}", file=sys.stderr)
    return client

if __name__ == "__main__":
    # This script can be called from command line with arguments:
    # arg1: user prompt
    # arg2 (optional): context

    client = client_llm()
    print(client)