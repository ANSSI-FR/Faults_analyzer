# Fault Analyzer documentation

## Requirements
- jekyll ([https://jekyllrb.com/](https://jekyllrb.com/))
- bundler ([https://bundler.io/](https://bundler.io/))

## See the documentation
```sh
make show
```

## Development
### Plugins
- Absolute path plugin [https://github.com/tnhu/jekyll-include-absolute-plugin](https://github.com/tnhu/jekyll-include-absolute-plugin)
- Callouts 
  - issue: [https://github.com/pmarsceill/just-the-docs/issues/171](https://github.com/pmarsceill/just-the-docs/issues/171) (this is implemented currently)
  - pull request: [https://github.com/pmarsceill/just-the-docs/pull/466](https://github.com/pmarsceill/just-the-docs/pull/466) (not merged in just-the-docs yet, check regularly)

### Live test
```sh
make server
```
Then go to http://localhost:4000 on a web browser. 
Also, the documentation website is available in the `_site` folder and can be shared anywhere.

### Build
```sh
make build
```
The documentation website is available in the `_site` folder and can be shared anywhere.

### Images
The images are created via the [draw.io](https://app.diagrams.net/)
([https://app.diagrams.net/](https://app.diagrams.net/)) website. The diagram
are stored in `assets/drawio/` and the images in `assets/img/`.
