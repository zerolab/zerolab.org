new:
	hugo new posts/`date +%Y-%m-%d`-new-draft.md

build:
	rm -rf public && hugo --gc --minify

serve:
	open http://localhost:1313/ && hugo serve --buildDrafts --gc