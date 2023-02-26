ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: help new serve build deploy sync

help:  ## ⁉️  - Display help comments for each make command
	@grep -E '^[0-9a-zA-Z_-]+:.*? .*$$'  \
		$(MAKEFILE_LIST)  \
		| awk 'BEGIN { FS=":.*?## " }; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'  \
		| sort

new:  ## 🆕  - Create a new draft post with a Y-m-d prefix
	hugo new posts/`date +%Y-%m-%d`-new-draft.md

build:  ## 🍄  - Generate site
	rm -rf public && hugo --gc --minify

serve:  ## 🍦  - Serve locally with drafts
	open http://localhost:1313/ && hugo serve --buildDrafts --gc

sync:  ## 🔄  - Sync to server
    rsync -avz --delete public/ ${USER}@${HOST}:${PUBLIC_DIR}

deploy: build sync  ## 🚀  - Build and deploy
