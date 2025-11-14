#!/usr/bin/env python3
"""
Test script to verify Anthropic API key and available models
"""

import json
import anthropic

def test_api_key():
    """Test if the Anthropic API key works"""

    print("🔍 Testing Anthropic API Configuration...\n")

    # Load config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found!")
        return

    api_key = config.get('anthropic_api_key')

    if not api_key or api_key == "YOUR_ANTHROPIC_API_KEY_HERE":
        print("❌ No valid API key found in config.json")
        print("   Please add your Anthropic API key to config.json")
        return

    print(f"✓ API key found: {api_key[:10]}...{api_key[-4:]}\n")

    # Test different models
    models_to_test = [
        "claude-3-sonnet-20240229",
        "claude-3-5-sonnet-20240620",
        "claude-3-haiku-20240307",
        "claude-3-opus-20240229",
    ]

    client = anthropic.Anthropic(api_key=api_key)

    print("Testing models:\n")

    for model_name in models_to_test:
        try:
            print(f"Testing {model_name}...", end=" ")

            message = client.messages.create(
                model=model_name,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )

            print(f"✅ WORKS")

        except anthropic.NotFoundError:
            print(f"❌ NOT FOUND (model not available)")
        except anthropic.PermissionDeniedError:
            print(f"❌ PERMISSION DENIED (upgrade plan needed)")
        except anthropic.AuthenticationError:
            print(f"❌ AUTHENTICATION ERROR (invalid API key)")
        except Exception as e:
            print(f"❌ ERROR: {e}")

    print("\n✅ Test complete!")
    print("\nRecommendation:")
    print("- Use the first model that shows '✅ WORKS'")
    print("- Update that model name in research_engine.py, email_generator.py, and setup.py")

if __name__ == '__main__':
    test_api_key()
