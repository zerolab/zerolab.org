.DEFAULT_GOAL := help

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: help post til build serve sync deploy

help:  ## ⁉️   - Display help comments for each make command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_\-\.]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

post:  ## 🆕  - Create a new draft post with a Y-m-d prefix
	hugo new posts/`date +%Y-%m-%d`-new-draft.md

til:  ## 🆕  - Create a new draft TIL
	hugo new til/new-draft.md

build:  ## 🍄  - Generate site
	rm -rf public && hugo --gc --minify

serve:  ## 🍦  - Serve locally with drafts
	open http://localhost:1313/ && hugo serve --buildDrafts --gc

sync:  ## 🔄  - Sync to server
	@echo "Syncing to $(HOST):$(PUBLIC_DIR)"
    rsync -avz --delete -e ssh public/ $(USER)@$(HOST):$(PUBLIC_DIR)

deploy: build sync  ## 🚀  - Build and deploy
