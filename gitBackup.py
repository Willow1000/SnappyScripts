import os
import subprocess
import shutil

def git_push(repo_path=None, commit_message=None, readmeText=None, email=None, username=None, repo_link=None, files_to_ignore=None, branch=None):
    """
    Automatically stages, commits, and pushes files to GitHub.

    Args:
        repo_path (str): The path to the local Git repository.
        commit_message (str): The commit message to use.
    """
    try:
        # Change directory to the repository path
        os.chdir(repo_path)

        if not os.path.exists('.git'):
            try:
                # Initialize a new Git repository
                subprocess.run(['git', 'init'], check=True)

                # Add files to .gitignore
                with open('.gitignore', 'a+') as f:
                    for i in files_to_ignore:
                        f.write(i + '\n')

                # Create README.md with provided text
                with open('README.md', 'a+') as f:
                    for i in readmeText:
                        f.write(i+"\n")

                # Configure Git user information
                subprocess.run(['git', 'config', '--global', 'user.name', username], check=True)
                subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)

                # Set default branch to main (or provided)
                subprocess.run(['git', 'config', '--global', 'init.defaultBranch', 'main'], check=True)

                # Add remote origin
                subprocess.run(['git', 'remote', 'add', 'origin', repo_link], check=True)

                # Add all files to staging
                subprocess.run(['git', 'add', '.'], check=True)

                # Commit changes
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)

                # Push to the remote repository
                subprocess.run(['git', 'push', '--set-upstream', 'origin', branch], check=True)

            except subprocess.CalledProcessError as e:
                print(f'An error occurred while initializing the repo or pushing: {e}')
                shutil.rmtree('.git')  # Clean up if something goes wrong
        else:
            # Check if the directory is already a Git repository
            subprocess.run(["git", "status"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Add all changes to staging
            subprocess.run(["git", "add", "-A"], check=True)

            with open('README.md', 'a+') as f:
                for i in readmeText:
                    f.write(i+"\n")

            # Commit the changes
            subprocess.run(["git", "commit", "-m", commit_message], check=True)

            # Push the changes to the remote repository
            subprocess.run(["git", "push", "-u", "origin", branch], check=True)

            print("Changes pushed to GitHub successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Git commands: {e}")

if __name__ == "__main__":
    # Path to your Git repository (change this to your repository path)
    repo_path = input("Enter the path to your local Git repository: ").strip()
    # Commit message
    commit_message = input("Enter your commit message: ").strip()
    
    # Branch
    branch = input('Enter the branch to push changes to: ').strip()

    # Additional info to README.md
    readmeText = input('Enter additional information for the README file(separate with ,): ').strip().split(',')
    if not os.path.exists(repo_path):
        email = input('Enter your email: ')
        username = input('Enter your GitHub username: ')
        
        
        # For existing repositories, ask for files to ignore
        files_to_ignore = input('Enter files to be ignored by git (separate with spaces): ').strip().split(' ')
        repo_link = input('Enter the link to your GitHub repository (e.g., https://github.com/username/repo.git): ')
        
        # Push changes to GitHub
        git_push(repo_path, commit_message, readmeText, email, username, repo_link, files_to_ignore, branch)
    else:
        git_push(commit_message=commit_message,branch=branch,repo_path=repo_path,readmeText=readmeText)
        print(f"The specified repository path does not exist: {repo_path}")
