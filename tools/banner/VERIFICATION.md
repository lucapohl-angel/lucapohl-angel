# Banner performance update

The animated README banner used continuous SVG animation over large illustration caches. Three dense vector eyes added more work, but removing them alone did not fix the repeated full-image painting.

The published version removes the eyes, raster-caches the detailed image layers at the 1800 x 1000 banner resolution, and synchronizes wing and Matrix changes to 12 updates per second. Rain columns retain varied speeds and offsets, quantized to the same clock. The carbon grain, lettering, foreground fingers, portal, terminals, cursor blinking, and both Matrix Easter eggs remain. Reduced-motion preferences stop the animation. Native editable artwork remains in the local banner source folder.

## Focused measurement

Microsoft Edge, headless, 1000 x 800 viewport, banner embedded as an img at 840px width, device pixel ratio 1; five-second trace samples after loading. Two final samples bracketed one baseline sample. These are local measurements, not a universal frame-rate guarantee.

| Sample | Main-thread task time | Summed raster-worker time |
| --- | ---: | ---: |
| Baseline | 5367 ms | 13747 ms |
| Updated, first run | 419 ms | 2919 ms |
| Updated, repeat | 406 ms | 2871 ms |

Approximately 92% less main-thread work and 79% less summed raster work in this comparison. Summed raster time spans multiple worker threads and can exceed wall-clock time.

Export size: 3,092,195 bytes before; 1570948 bytes after.

Verified: eyes absent; wing transforms change; both Easter eggs appear at their intended times; zero running animations with reduced motion; standalone SVG contains no script; mobile img preview fits 390px; no browser errors. Compared the rendered composition with the baseline.

## Rebuild

`python optimize_banner.py source.svg output.svg` requires Pillow and CairoSVG. Supply the layered source SVG; keep that editable source separately. The output is self-contained and uses lossless WebP caches, without external resources.
