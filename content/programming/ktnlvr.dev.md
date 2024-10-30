---
title: ktnlvr.dev
url: /kldd
draft: true

unlisted: true
brief: the website you are looking at right now, very meta
---

## Why this style?

The style is heavily inspired by [motherfucking website](https://motherfuckingwebsite.com/), [better motherfucking website](http://bettermotherfuckingwebsite.com/) and [the best motherfucking website](https://thebestmotherfucking.website/). I don't enjoy writing media queries, so the website doesn't use any fancy styling. Animations are also not a thing, they can distract from the writing.

## Does it perform?

This is a static website with a single CSS and no JS files. Can probably run using IPoAC [RFC1149](https://datatracker.ietf.org/doc/html/rfc1149) just fine.[^page-speed-insights]

## Bells And Whistles

### MathML

Some features might go unnoticed unless pointed out specifically.

Getting maths to work with hugo was a difficult feat, but I did it:

\[f(a) = \dfrac{1}{2\pi i}\oint_\gamma \dfrac{f(z)}{z - a} dz\]

This features introduces a custom step in the build pipeline. Hugo produces a `./public` directory, where all the statically generated pages are. The math embedding `./mathml.py` script is then executed by the Github Action CI/CD pipeline. It looks for `<p>[` and `]</p>`, extracts everything inbetween and then substitutes the contents into `$$`, which is then passed into `pandoc`. Finally, the result from `pandoc` is substituted back into the webpage with square braces removed, producing MathML.

This approach has several minor disadvantagees. Firstly, it limits by ability to start a paragraph with a `[`, since it will be interpreted as a start of a mathematical expression. This is not a great loss, but might hurt be down the road.

Secondly... TODO

Thirdly, the maths is not visible in the dev environment. When running a hot-reload build with `hugo -D` it uses in-memory pages, which means they are not accessible to any scripts.

On the other hand, getting LaTeX to work on a hugo website *statically* is troublesome. Humble brag? Defo.[^hugo-maths-official]

### Short links

All the posts have a slug consisting of the first letters making up the title of the post. This is done to ease recall and make links look less visually overwhelming, while keeping them sensible.

### `<noscript/>`

I don't see the purpose of JavaScript for a blog. The content here is static by nature and is intended to be read more often than edited

Understandably, this philosophy is impossible apply all over the web. A website of a bank or an electronic judge with no dynamic actions is absurd to think about. My blog isn't a bank or an ejudge. Some of my projects include a link or an `<iframe/>`[^iframe] with the demo, which would be impossible to do if it wasn't for JS, but generally everything is static.

The only place that actually has JavaScript is the [404 page](/this-page-does-not-exist). If you are going to a non-existent page you really need a search bar.

[^iframe]: For instance, [batteleships](/programming/battleships).
[^page-speed-insights]: [What does PageSpeed Insights have to say?](https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fktnlvr.dev%2Fprogramming%2Fktnlvr.dev). You can also scan it using [Unlighthouse](https://next.unlighthouse.dev/). Last time I checked, everything was in the green.
[^hugo-maths-official]: [Hugo's docs](https://gohugo.io/content-management/mathematics/) suggest using a `<script>` tag, we can't have that.