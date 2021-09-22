# useful

Odds and ends that I use for my own work, not intended for others but go for it


## figsplit.py

This code is used for animating LaTeX beamer presentations from xfig. xfig and multi-metapost used to do this well but in some upgrade it stopped working and there wasn't an obvious solution. Also my code allows objects to be hidden in subsequent layers

xfig depths can be used to describe multiple layers. The default layer is 50. The higher the layer the sooner it will appear in the animation.

Create your figure in xfig and then save it as a fig. You may also wish to save as PDF for static pictures -- not all dynamic figs may render well of course if you have a very complex animation so think about it. In say lecture notes you may rather want to use on the layers that are produced

In the simplest form you run `figsplit.py` like this:

```figsplit.py  drawing.fig```

This produces a series of PDFs, `drawing-0.pdf`, `drawing-1.pdf`, `drawing-2.pdf`, `drawing-3.pdf` (how many depends on how many layers you have). For the sake of example we assume four layers. Suppose your fig has layers 50, 47, 44, 41 (your layer numbers do not have be consecutive and it's a good idea to leave at least one gap so that if you discover you need a new intermediate later you don't have to go through rounds of mass editing. In this example, `drawing-0` corresponds to layer 50, `drawing-1` corresponds to layer 50 *and* 47, `drawing-2` corresponds to layers 50, 47, 44 and, `drawing-3` has all the objects in the figure.

To include this in your LaTeX you would do this

```
\multiinclude[format=pdf,graphics={width=10cm}]{drawing}
```

(The `graphics` parameter are options that are normally passed to the `\includegraphics` command -- you can omit if you want. Also read up about `multiinclue` for more advanced features). `multiiinclude` will produce (in this case) four separate slides which gives the appearance of animination.

 The above works well for pictures that are builtup from successive layers. Some times you may want to exclude objects that appeared earlier in some later slides. For this you use `--occlude`. Here's an example

``--occlude 47:50``

This says: when you render the PDF for layer 47 for the first time (this would be `drawing-1.pdf` in our example), do not show the layer 50 objects. Note that layer 50 objects will still be shown (in this example) in `drawing-2` and `drawing-3`. If I want to exclude in _all_ subsequent layers I would say `--occlude 47-1:50`.

`--occlude 47:50,44-41:47` says when rendering PDF for layer 47 (in our example this would be `drawing-1`) do now show layer 50 objects, and when rendering PDFs for layers 44 and 41 (`drawing-2` and `drawing-3`) do not show layer 47 objects (but layer 50 objects will appear in these layers because I am only hiding layer 50 in `drawing-1`).

`--occlude 44-41:47.50` says: when showing layers 44 and 41 hide layers 47 and 50.

 



