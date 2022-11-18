A quick script to find/replace all the instances of my template string

```python
import os
from git import Repo

def renameFiles(repo, find, rep):
    for entry in repo.commit().tree.traverse():
        if not os.path.isfile(entry.abspath):
            continue
        fld, name = os.path.split(entry.path)
        newname = name.replace(find, rep)
        if name != newname:
            repo.index.move([os.path.join(fld, name), os.path.join(fld, newname)])

    for entry in repo.commit().tree.traverse():
        if not os.path.isdir(entry.abspath):
            continue
        fld, name = os.path.split(entry.path)
        newname = name.replace(find, rep)
        if name != newname:
            repo.index.move([os.path.join(fld, name), os.path.join(fld, newname)])

def replaceText(repo, find, rep):
    for entry in repo.commit().tree.traverse():
        if not os.path.isfile(entry.abspath):
            continue
        path = entry.abspath
        with open(path, 'r') as f:
            text = f.read()
        newText = text.replace(find, rep)
        with open(path, 'w') as f:
            f.write(newText)

find = 'GITHUB_PROJECT_NAME'
rep = 'newProjectName'
repo = Repo(r'C:\path\to\repo\folder')
replaceText(repo, find, rep)
renameFiles(repo, find, rep)
```



