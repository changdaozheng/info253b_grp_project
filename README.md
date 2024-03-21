### …or create a new repository on the command line
```bash
echo "# group-project-team-1" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/UCB-INFO-BACKEND-WEBARCH/group-project-team-1.git
git push -u origin main
```

### …or push an existing repository from the command line
```bash
git remote add origin https://github.com/UCB-INFO-BACKEND-WEBARCH/group-project-team-1.git
git branch -M main
git push -u origin main
```

### …or import code from another repository
You can initialize this repository with code from a Subversion, Mercurial, or TFS project.