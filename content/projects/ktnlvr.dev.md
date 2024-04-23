+++
title = "ktnlvr.dev"
brief = "the website you are looking at right now, very meta" 
draft = true
+++

## `<noscript/>`

I happen to enjoy not having javascript. Thus, most of the website does not use JavaScript. Sure, minor things might use it, the ones that can't be done with standard HTML. To me it is imperative that my website is mostly static. Even the places that use it have a fallback option if it is disabled.

Understandably, this philosophy is impossible apply all over the web. A website of a bank or an electronic judge with no dynamic actions is absurd to think about. My blog isn't a bank or an ejudge. Some of my projects include a link or an `<iframe/>` with the demo, which would be impossible to do if it wasn't for JS.

The only place that actually has JavaScript is the [404 page](https://ktnlvr.dev/this-page-does-not-exist) (provided the server doesn't override it). If you are going to a page that dose not exist you probably really need a search bar.

## Bells And Whistles

### MathML

Some features might undergo unnoticed unless pointed out specifically.

Getting maths to work with hugo was a difficult feat, but I did it:

\[f(a) = \dfrac{1}{2\pi i}\oint_\gamma \dfrac{f(z)}{z - a} dz\]

This features introduces a custom step in the build pipeline. Hugo produces a `./public` directory, where all the statically generated pages are. The math embedding `./mathml.py` script is then executed by the Github Action CI/CD pipeline. It looks for `<p>[` and `]</p>`, extracts everything inbetween and then substitutes the contents into `$$`, which is then passed into `pandoc`. Finally, the result from `pandoc` is substituted back into the webpage with square braces removed, producing MathML.

This approach has several minor disadvantagees. Firstly, it limits by ability to start a paragraph with a `[`, since it will be interpreted as a start of a mathematical expression. This is not a great loss, but might hurt be down the road.

Secondly... TODO

Thirdly, the maths is not visible in the dev environment. When running a hot-reload build with `hugo -D` it uses in-memory pages, which means they are not accessible to any scripts.
