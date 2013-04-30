#!/usr/bin/env python
#nathive C extension (dotcy spec 1)

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.buftools import bufindex


def __over_color(bv, fv, ba, fa, fma, 'ccccf:c'):
    """Calculate final channel value for the given channel and alpha values
    using the over algorithm.
    @bv: Background channel value.
    @fv: Foreground channel value.
    @ba: Background alpha.
    @fa: Foreground alpha.
    @fma: Foreground master alpha value as float.
    =return: Final background channel value."""

    if ba == 0: return fv
    type f: bad, fad, fadx
    bad = (f)ba / 255
    fad = (f)fa / 255 * fma
    fadx = 1 - fad

    return ((bv*bad*fadx) + (fv*fad)) / (fad + (bad*fadx)) + 0.5
    #       +-----------+   +------+    +----------------+ +---+
    #           back          fore           corrector     round

def getOverColor(bv, fv, ba, fa, fma, 'ccccf:c'):
    """Calculate final channel value for the given channel and alpha values
    using the over algorithm.
    @bv: Background channel value.
    @fv: Foreground channel value.
    @ba: Background alpha.
    @fa: Foreground alpha.
    @fma: Foreground master alpha value as float.
    =return: Final background channel value."""

    if ba == 0: return fv
    type f: bad, fad, fadx
    bad = (f)ba / 255
    fad = (f)fa / 255 * fma
    fadx = 1 - fad

    return ((bv*bad*fadx) + (fv*fad)) / (fad + (bad*fadx)) + 0.5
    #       +-----------+   +------+    +----------------+ +---+
    #           back          fore           corrector     round

def __over_alpha(ba, fa, fma, 'ccf:c'):
    """Calculate alpha for the given alpha values using the over algorithm.
    @ba: Background alpha.
    @fa: Foreground alpha.
    @fma: Foreground master alpha value as float.
    =return: Final background alpha value."""

    if ba == 255: return ba
    fa = fa * fma
    return fa + (ba * (255-fa) / 255)

def getOverAlpha(ba, fa, 'ff:f'):
    """Calculate alpha for the given alpha values using the over algorithm.
    @ba: Background alpha.
    @fa: Foreground alpha.
    @fma: Foreground master alpha value as float.
    =return: Final background alpha value."""

    if ba == 255.0: return ba
    return fa + (ba * (255.0-fa) / 255.0)


def __sub_color(bv, fv, ba, fa, fma, 'ccccf:c'):
    """Calculate final channel value for the given channel and alpha values
    using the subtractive algorithm.
    @bv: Background channel value.
    @fv: Foreground channel value.
    @ba: Background alpha.
    @fa: Foreground alpha.
    @fma: Foreground master alpha value as float.
    =return: Final background channel value."""

    if fv == 0 or fa == 0: return bv
    type f: fad
    fad = (f)fa / 255 * fma

    type í: value
    value = (bv - (fv*fad))
    if value < 0: return 0
    return value


def __sub_alpha(ba, fa, fma, 'ccf:c'):
    """Calculate alpha for the given alpha values using subtractive algorithm.
    @ba: Background alpha.
    @fa: Foreground alpha.
    @fma: Foreground master alpha value as float.
    =return: Final background alpha value."""

    type í: alpha
    alpha = ba - (fa * fma)
    if alpha < 0: return 0
    return alpha


def composite(mode, b, f, bw, bh, fx, fy, fw, fh, fma,
        ax, ay, aw, ah, 'iPPiiiiiifiiii:'):
    """Composite an area of an image over other image.
    @mode: Composite mode as int, 0=copy, 1=over, 2=subtractive.
    @b: Background memory address as int.
    @f: Foreground memory address as int.
    @bw: Base width.
    @bh: Base height.
    @fx: Foreground x offset.
    @fy: Foreground y offset.
    @fw: Foreground width.
    @fh: Foreground height.
    @fma: Foreground master alpha value as float from 0 to 1.
    @ax: Target Area x offset.
    @ay: Target Area y offset.
    @aw: Target Area width.
    @ah: Target Area height."""

    # Init Base and Over buffer position.
    type i: bp, fp
    bp = 0
    fp = 0

    # Init boolean flag that prevent to recalculate
    # buffer positions while is the same row.
    type i: same_row
    same_row = 0

    # Looping over pixel buffers.
    type i: x, y
    for y in range(ah):

        same_row = 0

        # Row into over.
        if y+ay - fy < 0: continue
        if y+ay - fy >= fh: continue

        # Row into base.
        if y+ay < 0: continue
        if y+ay >= bh: continue

        for x in range(aw):

            # Column into over.
            if x+ax - fx < 0: continue
            if x+ax - fx >= fw: continue

            # Column into base.
            if x+ax < 0: continue
            if x+ax >= bw: continue

            if same_row:
                bp += 4
                fp += 4
            else:
                bp = bufindex(x+ax, y+ay, bw)
                fp = bufindex(x-fx+ax, y-fy+ay, fw)
                same_row = 1

            # Over composition mode.
            if mode == 1:
                if f[fp+3] == 0: continue
                b[bp+0] = over_color( b[bp+0], f[fp+0], b[bp+3], f[fp+3], fma)
                b[bp+1] = over_color( b[bp+1], f[fp+1], b[bp+3], f[fp+3], fma)
                b[bp+2] = over_color( b[bp+2], f[fp+2], b[bp+3], f[fp+3], fma)
                b[bp+3] = over_alpha( b[bp+3], f[fp+3], fma)

            # Subtractive composition mode.
            if mode == 2:
                b[bp+0] = sub_color( b[bp+0], f[fp+0], b[bp+3], f[fp+3], fma)
                b[bp+1] = sub_color( b[bp+1], f[fp+1], b[bp+3], f[fp+3], fma)
                b[bp+2] = sub_color( b[bp+2], f[fp+2], b[bp+3], f[fp+3], fma)
                b[bp+3] = sub_alpha( b[bp+3], f[fp+3], fma)


def diff(orig, mod, width, height, restore, 'PPiii:'):
    """Create or restore a diff between two diverged images overwriting the
    original image.
    @orig: Original image pointer as long int.
    @mod: Modified image pointer as long int.
    @width: Both images width in pixels.
    @height: Both images height in pixels.
    @restore: Boolean flag, false creates the diff, true restore it."""

    type l: i, length
    length = width * height * 4

    if not restore:
        for i in range(length):
            orig[i] = orig[i] - mod[i]
    else:
        for i in range(length):
            orig[i] = orig[i] + mod[i]


def clear(pixbuf, width, height, x, y, w, h, 'Piiiiii:'):
    """Fill the given pixbuf area with zero values.
    @pixbuf: Pixbuf pointer as long int.
    @width: Pixbuf width in pixels.
    @height: Pixbuf height in pixels.
    @x: Area x offset.
    @y: Area y offset.
    @w: Area width in pixels.
    @h: Area height in pixels."""

    type l: pos
    type i: xi, yi
    for yi in range(h):
        for xi in range(w):
            if x+xi < 0 or x+xi >= width: continue
            if y+yi < 0 or y+yi >= height: continue
            pos = bufindex(x+xi, y+yi, width)
            pixbuf[pos+0] = 0
            pixbuf[pos+1] = 0
            pixbuf[pos+2] = 0
            pixbuf[pos+3] = 0
