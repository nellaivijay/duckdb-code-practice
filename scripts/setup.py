#!/usr/bin/env python3
"""
Setup script for DuckDB Practice Environment

Validates environment and helps users get started with the DuckDB practice environment.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    print("Checking Python version...")
    version = sys.version_info
    if version >= (3, 8):
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} detected (requires 3.8+)")
        return False


def check_pip():
    """Check if pip is available"""
    print("Checking pip availability...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("✓ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("✗ pip is not available")
        return False


def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking required dependencies...")
    
    required_packages = ['duckdb', 'pandas', 'jupyter']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True


def check_directory_structure():
    """Check if required directories exist"""
    print("Checking directory structure...")
    
    required_dirs = ['data', 'docs', 'labs', 'notebooks', 'scripts', 'solutions', 'wiki']
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"✗ {dir_name}/ directory missing")
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"\nMissing directories: {', '.join(missing_dirs)}")
        return False
    
    return True


def check_sample_data():
    """Check if sample data exists"""
    print("Checking sample data...")
    
    sample_dir = Path('data/sample')
    if sample_dir.exists():
        files = list(sample_dir.glob('*.csv')) + list(sample_dir.glob('*.parquet'))
        if files:
            print(f"✓ Sample data found ({len(files)} files)")
            return True
        else:
            print("✗ Sample data directory exists but is empty")
            return False
    else:
        print("✗ Sample data directory does not exist")
        return False


def generate_sample_data():
    """Generate sample data"""
    print("\nGenerating sample data...")
    try:
        subprocess.run([sys.executable, "scripts/generate_sample_data.py"], check=True)
        print("✓ Sample data generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to generate sample data: {e}")
        return False


def load_sample_data():
    """Load sample data into database"""
    print("\nLoading sample data into database...")
    try:
        subprocess.run([sys.executable, "scripts/load_sample_data.py"], check=True)
        print("✓ Sample data loaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to load sample data: {e}")
        return False


def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    print("Checking environment configuration...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists():
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✓ Created .env file from .env.example")
            print("  You can edit .env to customize your configuration")
            return True
        else:
            print("✗ .env.example file not found")
            return False
    else:
        print("✓ .env file already exists")
        return True


def print_setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS")
    print("="*60)
    print("\n1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Configure environment (optional):")
    print("   cp .env.example .env")
    print("   # Edit .env with your preferences")
    print("\n3. Generate sample data:")
    print("   python3 scripts/generate_sample_data.py")
    print("\n4. Load sample data:")
    print("   python3 scripts/load_sample_data.py")
    print("\n5. Start Jupyter notebook:")
    print("   jupyter notebook")
    print("\nOr use Docker:")
    print("   docker-compose up -d")
    print("\n" + "="*60)


def main():
    print("="*60)
    print("DuckDB Practice Environment - Setup Check")
    print("="*60 + "\n")
    
    all_checks_passed = True
    
    # Run checks
    all_checks_passed &= check_python_version()
    all_checks_passed &= check_pip()
    all_checks_passed &= check_directory_structure()
    all_checks_passed &= create_env_file()
    
    if not all_checks_passed:
        print("\n❌ Some setup checks failed. Please fix the issues above.")
        print_setup_instructions()
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠️  Dependencies not installed. Install with: pip install -r requirements.txt")
        response = input("Would you like to install dependencies now? (y/n): ")
        if response.lower() == 'y':
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              check=True)
                print("✓ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install dependencies: {e}")
                sys.exit(1)
        else:
            print_setup_instructions()
            sys.exit(1)
    
    # Check sample data
    if not check_sample_data():
        print("\n⚠️  Sample data not found.")
        response = input("Would you like to generate and load sample data now? (y/n): ")
        if response.lower() == 'y':
            if not generate_sample_data():
                sys.exit(1)
            if not load_sample_data():
                sys.exit(1)
        else:
            print("You can generate sample data later with:")
            print("  python3 scripts/generate_sample_data.py")
            print("  python3 scripts/load_sample_data.py")
    
    print("\n" + "="*60)
    print("✅ Setup check completed successfully!")
    print("="*60)
    print("\nYour DuckDB practice environment is ready to use.")
    print("\nNext steps:")
    print("1. Start Jupyter: jupyter notebook")
    print("2. Or use Docker: docker-compose up -d")
    print("3. Begin with Lab 1: labs/lab-01-setup.md")
    print("\nHappy learning! 🚀")


if __name__ == '__main__':
    main()