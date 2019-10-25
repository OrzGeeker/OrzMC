
# !/usr/bin/env bash
# -*- coding: utf-8 -*-

# if [ "`git status -s`" ]
# then
#     echo "The working directory is dirty. Please commit any pending changes."
#     exit 1;
# fi

SITE_ROOT="website"
SITE_PUB_DIR="${SITE_ROOT}/public"
SITE_CONTENT_DIR="${SITE_ROOT}/content"
SITE_THEME_DIR="${SITE_ROOT}/themes"

echo "Deleting old publication"
rm -rf ${SITE_PUB_DIR}
mkdir ${SITE_PUB_DIR}
git worktree prune
rm -rf .git/worktrees/${SITE_PUB_DIR}

echo "Checking out gh-pages branch into public"
git worktree add -B gh-pages ${SITE_PUB_DIR} origin/gh-pages

echo "Removing existing files"
rm -rf ${SITE_PUB_DIR}/*

echo "Generating site"
hugo -s "${SITE_ROOT}" -c content -t OrzAnanke -e production

echo "Updating gh-pages branch"
cd ${SITE_PUB_DIR} && git add --all && git commit -m "Publishing to gh-pages (publish.sh)"

#echo "Pushing to github"
#git push --all