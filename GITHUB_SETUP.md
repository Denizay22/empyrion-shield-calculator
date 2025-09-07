# GitHub Setup Instructions

Follow these steps to push your code to GitHub and make it available to others:

## 1. Create a GitHub Repository

1. Log in to your GitHub account (or create one if you don't have one)
2. Click the "+" icon in the top right corner and select "New repository"
3. Enter a name for your repository (e.g., "empyrion-shield-calculator")
4. Add a description (optional)
5. Choose whether to make it public (anyone can see) or private (only you and collaborators)
6. DO NOT initialize with README, .gitignore, or license (we already have these files)
7. Click "Create repository"

## 2. Initialize Local Git Repository and Push to GitHub

Run these commands in your terminal (in the project directory):

```bash
# Initialize a new Git repository
git init

# Add all files to the staging area
git add .

# Commit the files
git commit -m "Initial commit"

# Add the GitHub repository as a remote
git remote add origin https://github.com/YourUsername/empyrion-shield-calculator.git

# Push your code to GitHub
git push -u origin main
```

Replace `YourUsername` with your actual GitHub username and `empyrion-shield-calculator` with your repository name if different.

## 3. Making it Easy for Others to Run Your Code

After your code is on GitHub, others can run it by:

1. Cloning your repository:
   ```bash
   git clone https://github.com/YourUsername/empyrion-shield-calculator.git
   cd empyrion-shield-calculator
   ```

2. Installing dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Running the application:
   ```bash
   python shield_calculator.py         # GUI mode (if PyQt6 is installed)
   python shield_calculator.py --cli   # Command-line mode
   ```

4. Alternatively, they can install it as a package:
   ```bash
   pip install .
   shield-calculator
   ```
