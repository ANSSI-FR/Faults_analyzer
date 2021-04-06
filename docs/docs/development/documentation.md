---
layout: home
title: Documentation
permalink: /dev/doc/
nav_order: 0
parent: Development
---

# Developing the documentation
{: .no_toc}

This page presents how to update this documentation.

- TOC
{:toc}

## Requirements
- ruby ([https://www.ruby-lang.org](https://www.ruby-lang.org))
- jekyll ([https://jekyllrb.com/](https://jekyllrb.com/))
- bundler ([https://bundler.io/](https://bundler.io/))

It is suggested to install ruby using your distribution packages but jekyll and
bundler using the `gem` package manager (as suggested
[here](https://jekyllrb.com/)).
{: .info}

## Template documentation
This documentation use the
[Just-the-Docs](https://pmarsceill.github.io/just-the-docs/) template.

## Plugins
Some plugins are used to have some interesting features, they are already
embedded in the project and no more installation is needed.
- Absolute path plugin: [https://github.com/tnhu/jekyll-include-absolute-plugin](https://github.com/tnhu/jekyll-include-absolute-plugin)
- Callouts
  - issue: [https://github.com/pmarsceill/just-the-docs/issues/171](https://github.com/pmarsceill/just-the-docs/issues/171) (this is implemented currently)
  - pull request: [https://github.com/pmarsceill/just-the-docs/pull/466](https://github.com/pmarsceill/just-the-docs/pull/466) (not merged in just-the-docs yet, check regularly)

## Building the documentation
### Using the `Makefile`
```sh
make build
```

### Using `jekyll`
```sh
bundle exec jekyll build
```

The website will be built in the `_site` directory.

The statically built project cannot be used without a server. The reason is that
the links are relative to the server root. Therefore, the links are not
correctly resolved if the `index.html` is simply opened in a browser.
{: .warn}

## Live test
### Using the `Makefile`
```sh
make server
```
With this command the website is available at `http://localhost:4000`.

### Using `jekyll`
```sh
bundle exec jekyll serve
```
With this command the website is available at `http://localhost:4000`.

## Live test using `Python3` (if Jekyll is not installed)
```sh
make show
```
This should open your internet browser on the documentation which is available at `http://localhost:8000`.

## Adding a page

This section describe how to add a page to the documentation. Knowing how
`jekyll` work is important to fully understand it. However, the following points
are enough to understand how to add a simple page.

- `jekyll` able to build an HTML/CSS/JavaScript based website.
- The meta-data are defined in the `_config.yml` file (both information for
  `jekyll` and `Just-the-Docs` are present in it). This file can be used to add plugins, change the template, set the files to ignore during the website build, _etc_.
- When `jekyll` build the website, it will use all the files in the root
  directory expected the ones starting with an underscore `"_"`, the ones
  mentioned in the `_config.yml` to be ignored and the `ruby` configuration
  files (`Gemfile`, `Gemfile.lock`).
- The files describing the pages can be either in markdown or in HTML. The will
  be converted in HTML in the end.
- `jekyll` can interpret [`liquid`](https://jekyllrb.com/docs/liquid/) scripting
  for creating pages.

### Directory organization
- `404.html`: this is the "page not found" page.
- `_config.yml`: the configuration file of the website.
- `Gemfile` and `Gemfile.lock`: the files managing the `ruby` packages.
- `index.md`: this is the index page of our website.
- `Makefile`: the Makefile (I should not describe this one).
- `readme.md`: you should read this.
- `assets/`: this directory contains all the public files available from the
  website (`css` and `js` files, images, `pdf` files, _etc_)
- `docs/`: this directory contains all the documentation pages that are the
  content of this documentation. This directory is organized with various
  categories which correspond to the different documented projects.
- `_plugins`: this directory contains the plugins that are not in the official
  `ruby` packages and that were added "by hand".
- `_sass`: this directory contains the custom `css` styles used by the website.
- `_site`: this directory is created when building the documentation and
  contains the website itself. To put the documentation online, the server must
  be set with this directory as root.
  
### Creating a new page
A new page can be created at any location in the directory. However, it is
recommended to store all the pages in the `docs/` directory.

The page can be either in HTML or in markdown, but, in both cases, a header is
needed by `Jekyll` and `Just-the-Docs` to work properly.

For instance, the header of this page is:
```sh
---
layout: home
title: Documentation
permalink: /dev/doc/
nav_order: 0
parent: Development
has_children: false
---
```

These attributes are the most important to give. More can be find in the
[`Jekyll`](https://jekyllrb.com/) and
[`Just-the-Docs`](https://pmarsceill.github.io/just-the-docs/) documentations.
Here are their purpose:
- `layout`: this attributes gives the layout where to integrate the page. The
  `home` layout contains the sidebar, the search field and all the inclusions
  for the page to render correctly.
- `title`: this attributes is the title of the page (used in the web browser
  typically) but also an (not necessary unique) identifier of the page.
- `permalink`: this is the suffix of the URL of this page. The complete URL will
  be `{{ site.url }}/{{ site.baseurl }}/{{ permalink }}` where `url` and
  `baseurl` are defined in the `_config.yml`. For instance, on the test version,
  the complete URL of this page is `http://localhost:4000/dev/doc/`
- `nav_order`: is the index of the page in the sidebar navigation menu. The higher
  the number, the lower the page is in the navigation menu. If two pages have
  the same `nav_order` they are sort in the alphabetical way.
- `parent`: this attributes refers to the parent of the page in the navigation
  menu. The references must match the `title` attribute of the parent. In the
  case of children of children, the `grand_parent` attribute must also be set.
- `has_children`: this attributes describes if the current page can have
  children in the navigation menu.

### Page content
For the content, it depends if you work on a HTML or a Markdown file. However, I
will only describe the markdown content specificities of this site.

- [Markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
- [Jekyll cheatsheet](https://devhints.io/jekyll)
- [Just-the-Docs documentation](https://pmarsceill.github.io/just-the-docs/)
- Absolute path plugin usage: `{{ "{% include_absolute 'path/to/the/file' " }}%}`
- Callouts:
  ```sh
  This is an informative callout.
  {: .info}
  ```
  
  This is an informative callout.
  {: .info}

  ```sh
  This is a warning callout.
  {: .warn}
  ```
  
  This is a warning callout.
  {: .warn}
  
  ```sh
  This is a danger callout.
  {: .danger}
  ```

  This is a danger callout.
  {: .danger}

- Reference to another page:
  ```sh
  [Link text]({{ "{{ site.baseurl " }}}}/{{ "{{ page.permalink " }}}})
  ```
  For instance:
  ```sh
  [Create an experiment from scratch]({{ "{{ site.baseurl " }}}}/scratch/)
  ```
  [Create an experiment from scratch]({{site.baseurl}}/scratch/)

## Images
The way to include images in a markdown file is described in the [Markdown
cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).
However, as we store them in the `assets/` directory, we must append their
location to the `site.baseurl` attribute to have it render properly in HTML,
such as:
```sh
![Image text]({{ "{{ site.baseurl " }}}}/assets/path/to/image)
```

### The `drawio` directory
In the `assets/` directory, there is the `drawio/` directory. This directory
store the file describing some diagrams used in this documentation. To edit
them, one must use the [draw.io website](https://app.diagrams.net/).
