# 1. Add to gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore

# 2. Remove all files from git's index
git rm -r --cached .

# 3. Add everything back
git add .

# 4. Commit
git commit -m "Remove __pycache__ files and update .gitignore"

# 5. Push
git push origin main

# 6. Clean local directory
find . -type d -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete