# Guide: How To Use Git And Work On Our Website Project

This is a simple guide I wrote so that anyone joining the project knows exactly how to set things up and contribute without messing things up.

---

# Project File Structure

Below is the structure of the repo. Get familiar with where things go because most issues happen due to wrong paths or wrong placements.

```
C:.
├── assets
│   └── fonts
│   └── images
├───docs
├── src
│   ├── components
│   ├── data
│   │   ├── achievements
│   │   ├── activities
│   │   ├── projects
│   │   └── team
│   ├── pages
│   │   ├── about
│   │   ├── achievements
│   │   ├── activities
│   │   │   └── origo
│   │   ├── contact
│   │   ├── hof
│   │   ├── projects
│   │   └── team
│   ├── scripts
│   └── styles
├── test
└── utils

```

---

# 1. Cloning The Repo

Make sure Git is installed. Then open your terminal and run:

```

git clone https://github.com/spark/SPARK

```

Enter the directory:

```

cd SPARK

```

Open it in VS Code:

```

code .

```

## Forking Instead Of Direct Clone

If you want to fork it first, use this link:

**https://github.com/spark/SPARK/fork**

After forking:

```

git clone <your-fork-link>
cd SPARK
code .

```

---

# 2. Setting Up And Running The Project Locally

Open the terminal in VS Code or your usual terminal inside the repo folder.

## Method 1: Build And Serve

Install dependencies (only once):

```

npm install

```

Build the project whenever you make changes:

```

npm run build

```

After build is done:

```

cd dist
python -m http.server 8000

```

Then open:

```

http://localhost:8000

```

This shows the actual production build.

## Method 2: Live Server (Quick Testing)

Install the Live Server extension in VS Code.  
Right click `index.html` in the left sidebar and select **Open with Live Server**.

Note: Navigation links will not work normally. You must manually append `/src/pages` in the URL because pages live inside `src/pages` but Live Server serves the root.

Example:

Instead of  
`http://127.0.0.1:5500/team/`  
use  
`http://127.0.0.1:5500/src/pages/team/`

### Why this happens

The real deployment uses a GitHub Action that builds the site and deploys from the `dist` folder.  
Local Live Server does not know any of that, so you must help it by adjusting links manually.

---

# 3. Making Changes

## Adding Photos

Rules:

1. Use `.webp` format.
2. Place images in the correct folder under `assets/images/...`
3. If the page uses a json file (team, activities, projects, achievements etc), update the path inside the json.

Example: Adding something to `src/data/achievements/competitions.json`

```

{
"title": "ISRO Robotics Challenge (IRoCU 2025)",
"description": "Made it to the qualification round and secured a place among the top 24 teams across India.",
"photo": "assets/images/achievements/competitions/ISRO.webp"
}

```

Place the image here:

```

assets/images/achievements/competitions/

```

### Important Note
Json files are rendered exactly in the order entries appear, so place your new entry where it belongs.

---

## If You Cannot Find A Photo

Use placeholders but **never leave the name empty**.

Example placeholder entry:

```

{
"name": "ASWIN PK",
"photo": "assets/images/team/b12/logo.webp",
"role": "Team Member",
"socials": [
{
"platform": "linkedin",
"url": ""
}
]
}

```

---

## Changing Layout Or Logic

CSS and JS are inside:

```

src/styles/
src/scripts/

```

If you need to find which file controls what, open the page you want:

```

src/pages/<page>/index.html

```

Check the referenced script and style tags, follow their paths.

### Components Check
Before adding new scripts or HTML blocks, make sure they are not already available as a component under:

```

src/components/

```

If you make a new reusable thing like a footer or navbar, keep it parametrizable and reusable.

---

## If Changes Are Not Showing

Open browser dev tools:

```

Ctrl Shift I

```

Hover over the element. You will see which file controls it. Fix that file.

---

# 4. Contribution Rules

These are strict:

- Work must be professional. If not, it will be rejected.
- Never push directly to `main`. The rules prevent it anyway.
- No unnecessary changes or random experiments.
- Always update json entries properly and check output on local build.
- Maintain clean commit structure and make PRs.

---

# 5. Using Git To Commit And Push Changes

Stage files:

```

git add <path>

```

To stage everything:

```

git add .

```

Check what is staged:

```

git status

```

Commit:

```

git commit -m "feat(contact): added reCAPTCHA verif"

```

### Commit Message Structure

Use prefixes like:

- `feat:` for new feature or new entry
- `fix:` for correcting something broken
- `chore:` for non feature changes like formatting or moving files
- `refactor:` for improving code logic
- `style:` for css only changes
- `docs:` for documentation updates

Describe exactly what you did.  
If you changed many things, write a descriptive message.

Push your branch:

```

git push origin <branch-name>

```

---

# 6. Making A Pull Request Using Commands

Create a new branch first:

```

git checkout -b my-branch

```

After committing and pushing:

```

git push origin my-branch

```

Then open GitHub and it will show **Compare and Pull Request**.

Submit the PR and ask a maintainer to review it.

---

# 7. Other Helpful Commands

These are just additional commands that might help when things break or when you are not sure what happened. Use them when needed.

## Updating Your Local Clone When Repo Got New Changes

If the repo has new commits and your local copy is outdated:

```
git pull origin main
```

If your local branch is not `main`, switch first:

```
git checkout main
git pull origin main
```

## Checking Remotes

To see which remote your repo is connected to:

```
git remote -v
```

If for some reason remote is missing or messed up, add it again:

```
git remote add origin https://github.com/spark/SPARK
```

Set upstream if needed:

```
git branch -u origin/main
```

## Checking What Changed

Show diffs:

```
git diff
```

Show diffs of staged files:

```
git diff --staged
```

View commit history:

```
git log
```

For a cleaner one line history:

```
git log --oneline
```

## Undoing Mistakes

Undo last commit but keep changes in working directory:

```
git reset --soft HEAD~1
```

Fully undo last commit and remove changes:

```
git reset --hard HEAD~1
```

Unstage a file:

```
git reset <file>
```

Restore a deleted or modified file:

```
git checkout -- <file>
```

Revert a commit with a new commit (safe for already pushed commits):

```
git revert <commit-hash>
```

## Switching Branches

List branches:

```
git branch
```

Switch branches:

```
git checkout <branch>
```

Create and switch:

```
git checkout -b <new-branch>
```

## Stashing Changes

If you need to switch branches but have uncommitted changes:

```
git stash
```

Bring them back later:

```
git stash pop
```

---

# Final Notes

This is our website and our club. Keep everything clean and well documented.  
People maintaining this later should have an easy time understanding what you did.

If you need details about deployment or component usage, read the files in:

```

docs/

```

Be responsible and maintain quality.
Do contact [@SlyPredator](https://github.com/SlyPredator) and [@Mummanajagadeesh](https://github.com/Mummanajagadeesh) if you feel anything is not understood or unclear.
