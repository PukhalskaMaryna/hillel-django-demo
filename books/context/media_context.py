from django.conf import settings
import os
def media_tree(request):
    root = settings.MEDIA_ROOT
    tree = []
    if os.path.isdir(root):
        for dirpath, dirnames, filenames in os.walk(root):
            rel = os.path.relpath(dirpath, root)
            rel = "" if rel == "." else (rel.replace("\\","/") + "/")
            tree.append((rel, sorted(filenames)))
    return {"MEDIA_URL": settings.MEDIA_URL, "MEDIA_ROOT": str(root), "tree": tree}
