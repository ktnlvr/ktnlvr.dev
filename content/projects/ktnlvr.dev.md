+++
title = "ktnlvr.dev"
brief = "the website you are looking at right now, very meta" 
draft = true
+++

## `<noscript/>`

I don't see the purpose of JavaScript for a blog. The content here is static by nature and is intended to be read more often than edited

Understandably, this philosophy is impossible apply all over the web. A website of a bank or an electronic judge with no dynamic actions is absurd to think about. My blog isn't a bank or an ejudge. Some of my projects include a link or an `<iframe/>`[^iframe] with the demo, which would be impossible to do if it wasn't for JS, but generally everything is static.

The only place that actually has JavaScript is the [404 page](/this-page-does-not-exist). If you are going to a non-existent page you really need a search bar.

## Bells And Whistles

### MathML

Some features might undergo unnoticed unless pointed out specifically.

Getting maths to work with hugo was a difficult feat, but I did it:

\[f(a) = \dfrac{1}{2\pi i}\oint_\gamma \dfrac{f(z)}{z - a} dz\]

This features introduces a custom step in the build pipeline. Hugo produces a `./public` directory, where all the statically generated pages are. The math embedding `./mathml.py` script is then executed by the Github Action CI/CD pipeline. It looks for `<p>[` and `]</p>`, extracts everything inbetween and then substitutes the contents into `$$`, which is then passed into `pandoc`. Finally, the result from `pandoc` is substituted back into the webpage with square braces removed, producing MathML.

This approach has several minor disadvantagees. Firstly, it limits by ability to start a paragraph with a `[`, since it will be interpreted as a start of a mathematical expression. This is not a great loss, but might hurt be down the road.

Secondly... TODO

Thirdly, the maths is not visible in the dev environment. When running a hot-reload build with `hugo -D` it uses in-memory pages, which means they are not accessible to any scripts.

[^iframe]: For instance, [batteleships](/projects/battleships).
