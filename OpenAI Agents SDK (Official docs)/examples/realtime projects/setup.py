"""
Setup script for Future Trading Bot
Run this script to set up the environment and install dependencies
"""

import os
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True

def setup_config():
    """Set up configuration file"""
    config_template = Path('config_template.py')
    config_file = Path('config.py')
    
    if not config_file.exists():
        if config_template.exists():
            # Copy template to config.py
            with open(config_template, 'r') as template:
                content = template.read()
            
            with open(config_file, 'w') as config:
                config.write(content)
            
            print("✓ Configuration file created (config.py)")
            print("⚠️  Please update config.py with your OpenAI API key and other settings")
        else:
            print("✗ Configuration template not found")
            return False
    else:
        print("✓ Configuration file already exists")
    
    return True

def check_openai_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✓ OpenAI API key found in environment variables")
        return True
    else:
        print("⚠️  OpenAI API key not found in environment variables")
        print("   You can set it by running: set OPENAI_API_KEY=your_key_here")
        print("   Or update the config.py file")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory created: {directory}")

def main():
    """Main setup function"""
    print("Future Trading Bot Setup")
    print("=" * 40)
    
    success = True
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Setup configuration
    if not setup_config():
        success = False
    
    # Check OpenAI API key
    check_openai_key()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Set your OpenAI API key in environment variables or config.py")
        print("2. Review and update config.py with your preferred settings")
        print("3. Run the bot with: python bot.py")
    else:
        print("✗ Setup completed with errors")
        print("Please resolve the errors above before running the bot")

if __name__ == "__main__":
    main()
