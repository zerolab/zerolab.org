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

purge:  ## 🗑  - Clean up built files
	rm -rf public
	
serve:  ## 🍦  - Serve locally with drafts
	open http://localhost:1313/ && hugo server --buildDrafts --watch --gc

view:  ## 🔎  - Run server
	hugo server --watch

build:  ## 🍄  - Generate site
	@make purge
	hugo --gc --minify

sync:  ## 🔄  - Sync to server
	rsync -avz --delete -e ssh public/ $(USER)@$(HOST):$(PUBLIC_DIR)

publish: ## 🚀  - Build and deploy
	@make build
	@make sync
