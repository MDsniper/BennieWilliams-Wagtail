#!/usr/bin/env python3
"""
Deploy Wagtail site to Coolify
This script automates the deployment of the new Wagtail site to Coolify
"""

import os
import sys
import time
import secrets
import string
from playwright.sync_api import sync_playwright

def generate_secret_key():
    """Generate a secure Django secret key"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(50))

def deploy_to_coolify():
    """Deploy the Wagtail application to Coolify"""

    # Get credentials from environment or prompt
    coolify_url = os.environ.get('COOLIFY_URL') or input('Enter Coolify URL (e.g., https://coolify.yourdomain.com): ')
    coolify_email = os.environ.get('COOLIFY_EMAIL') or input('Enter Coolify email: ')
    coolify_password = os.environ.get('COOLIFY_PASSWORD') or input('Enter Coolify password: ')

    # Generate a secure secret key
    secret_key = generate_secret_key()
    print(f"Generated SECRET_KEY: {secret_key[:10]}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        context = browser.new_context()
        page = context.new_page()

        try:
            print(f"Navigating to Coolify at {coolify_url}")
            page.goto(coolify_url)

            # Login to Coolify
            print("Logging in to Coolify...")
            page.fill('input[type="email"]', coolify_email)
            page.fill('input[type="password"]', coolify_password)
            page.click('button[type="submit"]')

            # Wait for dashboard to load
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Navigate to projects/applications
            print("Navigating to applications...")
            page.click('text="Projects"')
            time.sleep(1)

            # Look for existing benniewilliams app
            if page.locator('text="benniewilliams"').count() > 0:
                print("Found existing benniewilliams deployment")
                page.click('text="benniewilliams"')
                time.sleep(1)

                # Stop the current deployment
                if page.locator('button:has-text("Stop")').count() > 0:
                    print("Stopping current deployment...")
                    page.click('button:has-text("Stop")')
                    time.sleep(5)

            # Create new application
            print("Creating new application...")
            page.click('button:has-text("New")')
            time.sleep(1)
            page.click('text="Application"')
            time.sleep(1)

            # Select GitHub as source
            print("Selecting GitHub as source...")
            page.click('text="GitHub"')
            time.sleep(1)

            # Enter repository URL
            print("Configuring GitHub repository...")
            page.fill('input[placeholder*="github.com"]', 'https://github.com/MDsniper/benniewilliams-wagtail')
            page.fill('input[placeholder*="branch"]', 'main')

            # Select Dockerfile build pack
            page.click('text="Dockerfile"')

            # Configure application settings
            print("Configuring application settings...")
            page.fill('input[placeholder*="name"]', 'benniewilliams-wagtail')
            page.fill('input[placeholder*="port"]', '8000')

            # Add environment variables
            print("Adding environment variables...")
            page.click('text="Environment Variables"')
            time.sleep(1)

            # Add SECRET_KEY
            page.click('button:has-text("Add")')
            page.fill('input[placeholder="Key"]', 'SECRET_KEY')
            page.fill('input[placeholder="Value"]', secret_key)

            # Add ALLOWED_HOSTS
            page.click('button:has-text("Add")')
            page.fill('input[placeholder="Key"]', 'ALLOWED_HOSTS')
            page.fill('input[placeholder="Value"]', 'benniewilliams.com,www.benniewilliams.com,localhost')

            # Add Django settings module
            page.click('button:has-text("Add")')
            page.fill('input[placeholder="Key"]', 'DJANGO_SETTINGS_MODULE')
            page.fill('input[placeholder="Value"]', 'benniewilliams.settings.production')

            # Configure domains
            print("Configuring domains...")
            page.click('text="Domains"')
            time.sleep(1)
            page.fill('input[placeholder*="domain"]', 'benniewilliams.com')
            page.click('button:has-text("Add")')
            page.fill('input[placeholder*="domain"]', 'www.benniewilliams.com')
            page.click('button:has-text("Add")')

            # Enable SSL
            page.check('text="Enable SSL"')
            page.check('text="Force HTTPS"')

            # Deploy the application
            print("Starting deployment...")
            page.click('button:has-text("Deploy")')

            # Wait for deployment to start
            time.sleep(5)

            # Monitor deployment logs
            print("Monitoring deployment logs...")
            page.click('text="Logs"')

            # Wait for deployment to complete (timeout after 10 minutes)
            max_wait = 600  # 10 minutes
            start_time = time.time()

            while time.time() - start_time < max_wait:
                # Check if deployment is successful
                if page.locator('text="Deployment successful"').count() > 0:
                    print("✅ Deployment successful!")
                    break

                # Check for errors
                if page.locator('text="Deployment failed"').count() > 0:
                    print("❌ Deployment failed. Check logs for details.")
                    break

                time.sleep(5)

            print("\nDeployment complete!")
            print(f"Site should be available at: https://benniewilliams.com")
            print(f"Admin panel at: https://benniewilliams.com/admin")
            print(f"\nSecret key saved - keep this secure!")

        except Exception as e:
            print(f"Error during deployment: {str(e)}")
            return False

        finally:
            browser.close()

    return True

def main():
    """Main entry point"""
    print("=== Coolify Wagtail Deployment Script ===\n")

    # Check if playwright is installed
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Installing...")
        os.system("pip install playwright")
        os.system("playwright install chromium")
        print("Please run the script again.")
        sys.exit(1)

    # Run deployment
    if deploy_to_coolify():
        print("\n✅ Deployment completed successfully!")
    else:
        print("\n❌ Deployment failed. Please check the logs and try manually.")

if __name__ == "__main__":
    main()