.PHONY: server build clean show

show:
	python3 -m http.server -d _site/ &
	xdg-open http://localhost:8000

build:
	bundle exec jekyll build --config _config_local.yml

server:
	bundle exec jekyll serve --config _config_local.yml

clean:
	rm -rf _site
