# My matplotlib theme based on FT style

- inspired by John Burn-Murdoch
- my main plotting library is seaborn

## How to use

```py
plt.style.use("-30k.mplstyle")
```

## How to plot `suptitle`

```py
ax = plt.gca()
ax.get_position()

fig.suptitle("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\nSed ut perspiciatis unde omnis iste natus error.",
             fontfamily="Canela Text",
             ha='left', va='bottom',
             x=ax.get_position().x0/2, y=ax.get_position().y1*1.1)
```

## path effect

```py
path_width = 2.5
path_color = "white"
path_alpha = 0.8

path_effects=[patheffects.Stroke(linewidth=path_width, foreground=path_color, alpha=path_alpha),
                            patheffects.Normal()]
```

## Reference

- https://matplotlib.org/stable/tutorials/introductory/customizing.html?highlight=rc

## Issues

- Problems with `*.ttc` font in macOS: cannot set font weight to bold.
