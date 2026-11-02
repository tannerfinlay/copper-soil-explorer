# Design Choices

The design system for Copper Soil Explorer. `src/styles/tokens.css` implements every value below as a CSS custom property; change both together, and never hardcode a value in component CSS that a token covers.

## Inspiration

- **QGIS / ArcGIS Pro:** a docked panel beside a full-bleed map, and a status bar with cursor coordinates. The hover readout lives in the status bar, not in a floating tooltip card.
- **Felt:** a light, quiet UI where the map is the focus and the controls stay out of the way.
- **Datawrapper:** plain legends and histograms with direct labels, units in the axis title, and no gridline clutter.
- **USGS / US Web Design System:** a sober, government-data tone. That is why the UI font is Public Sans, the USWDS typeface.

## Fonts

| Font          | Token         | Use                                             | Weights  |
| ------------- | ------------- | ----------------------------------------------- | -------- |
| Public Sans   | `--font-ui`   | All UI text                                     | 400, 600 |
| IBM Plex Mono | `--font-mono` | Coordinates, values, and units (aligned digits) | 400      |

Both are self-hosted with `@fontsource/public-sans` and `@fontsource/ibm-plex-mono`, imported in `src/main.tsx`. Fallbacks: Helvetica, Arial, sans-serif for UI; Menlo, monospace for values.

## Type scale

| Role                   | Size | Weight | Line height | Tokens                                                                  | Where                |
| ---------------------- | ---- | ------ | ----------- | ----------------------------------------------------------------------- | -------------------- |
| App title              | 20px | 600    | 1.3         | `--font-size-title`, `--font-weight-title`, `--line-height-heading`     | `h1`                 |
| Section heading        | 16px | 600    | 1.3         | `--font-size-heading`, `--font-weight-heading`, `--line-height-heading` | `h2`                 |
| Body                   | 16px | 400    | 1.5         | `--font-size-body`, `--font-weight-body` (1.5 is set in `index.css`)    | `:root` default      |
| Labels and captions    | 14px | 400    | 20px        | `--font-size-label`, `--font-weight-label`, `--line-height-label`       | `.label`, `.caption` |
| Values                 | 14px | 400    | inherited   | `--font-mono`, `--font-size-label`                                      | `.value`             |
| Chart ticks (story 16) | 12px | 400    | n/a         | not yet tokenized                                                       | histogram axis only  |

The app title and section headings share one line-height token (`--line-height-heading`); split it only if they ever need different values. 12px chart ticks are the only text below 14px. Headings get more space above (24px) than below (8px). Sentence case everywhere ("Map layer", not "MAP LAYER").

## Color

Contrast ratios are WCAG 2 values computed from the hex codes. Body text needs 4.5:1; UI component borders need 3:1.

| Token             | Hex       | Use                                                                  | Contrast                              |
| ----------------- | --------- | -------------------------------------------------------------------- | ------------------------------------- |
| `--surface-app`   | `#f3f4f5` | Page background behind panels, map placeholder                       | n/a                                   |
| `--surface-panel` | `#ffffff` | Top bar, side panel, status bar                                      | n/a                                   |
| `--ink`           | `#1c2024` | Primary text                                                         | 16.4:1 on panel, 14.9:1 on app        |
| `--ink-2`         | `#4b535c` | Secondary text, labels                                               | 7.8:1 on panel, 7.1:1 on app          |
| `--ink-3`         | `#646c75` | Captions, citations                                                  | 5.3:1 on panel, 4.8:1 on app          |
| `--line-subtle`   | `#e3e6e9` | Panel borders and section dividers (decorative only)                 | n/a                                   |
| `--line`          | `#c9ced3` | Stronger divider, where `--line-subtle` is too faint (unused so far) | n/a                                   |
| `--line-strong`   | `#8a939c` | Control borders (inputs, toggles, select)                            | 3.1:1 on panel                        |
| `--accent`        | `#a4481f` | Copper: selected state, primary button, focus ring, brush, links     | 6.0:1 on panel; white on accent 6.0:1 |
| `--accent-weak`   | `#f7e9e1` | Selected toggle background                                           | n/a                                   |
| `--accent-ink`    | `#7a3415` | Text on `--accent-weak`                                              | 7.6:1 on `--accent-weak`              |
| `--danger`        | `#b42318` | Error text                                                           | 6.6:1 on panel                        |

### Data scales

- **Prediction and sample points:** `d3.interpolateYlOrBr` on a log scale (ColorBrewer: perceptually ordered, color-blind safe, and earth-toned to fit soil and copper).
- **Uncertainty:** `d3.interpolateBlues`.
- Never reuse `--accent` as a data color, so selection and data never look alike.

## Shape and space

| Token               | Value          | Use                                         |
| ------------------- | -------------- | ------------------------------------------- |
| `--radius-controls` | 4px            | Inputs, toggles, select, buttons            |
| `--radius-popover`  | 6px            | Popovers and tooltips                       |
| (none)              | 0              | Panels: they are docked, not floating cards |
| `--spacing-1`       | 0.25rem (4px)  |                                             |
| `--spacing-2`       | 0.5rem (8px)   | Space below a section heading               |
| `--spacing-3`       | 0.75rem (12px) | Panel and bar inline padding                |
| `--spacing-4`       | 1rem (16px)    | Gaps between items in a bar                 |
| `--spacing-6`       | 1.5rem (24px)  | Space above a section heading               |
| `--spacing-8`       | 2rem (32px)    |                                             |

Spacing is in rem so it scales with the user's browser font size; the px values assume the 16px default.

- **Borders, not shadows:** panels are separated by a 1px `--line-subtle` border.
- **One shadow:** used only on controls that float over the map (zoom).
- **Motion:** functional only. 150ms fades for layer changes, no bounce easing.

## Layout

Desktop is a CSS grid in `src/styles/App.module.css`:

```
+--------------------------------------------------+
| header (48px)                                    |
+--------------+-----------------------------------+
| sidebar      | map (fills remaining space)       |
| (340px,      |                                   |
|  full        +-----------------------------------+
|  height)     | status bar (32px, under map only) |
+--------------+-----------------------------------+
```

- The grid fills `100dvh`; the sidebar scrolls on its own (`overflow-y: auto`).
- The map grid area needs `min-height: 0` and `min-width: 0` so Leaflet gets a stable size.
- The data citation sits at the bottom of the sidebar (`margin-top: auto` in the sidebar's flex column).
- Landmarks: the top bar is `<header>`, the sidebar `<aside>` with a `<section>` per group, and the map `<main>`. The status bar is a `<section aria-label="Map readout">`, not `role="status"`: a live region would announce every hover.
- Mobile (below 768px, story 20): top bar, map at about 55% of the viewport height, status bar, then the panel content scrolling below. Tap targets at least 40px tall.

## Styling conventions

- **CSS Modules** for component styles (`*.module.css`), used as `className={styles.name}`.
- **Global classes** in `src/index.css` for shared text roles: `.label`, `.value`, `.caption`. Used as plain strings, e.g. `className="value"`.
- **The parent owns placement** (grid area, width, margin between siblings); the component owns its appearance (padding, color, type, internal layout). Components accept a `className` prop for placement.
- **Components:** Radix UI primitives (toggle group, slider, select, tooltip), styled with these tokens. No full component library.
- **Focus:** a global `:focus-visible` rule in `index.css` draws a 2px `--accent` outline with a 2px offset. Component CSS must not reset `outline`.
- **Links** (navigate somewhere, e.g. Code): `--ink`, no underline; `--accent` on hover.
- **Text buttons** (act on the page, e.g. About opens a dialog): a `<button>` with the browser styling removed so it matches the links: no background or border, inherited font and color, `--accent` on hover.

## Rules

Do:

- Let the map dominate. The panel is a working tool: dense, quiet, left-aligned.
- Separate sections with spacing and a thin divider, not boxes inside boxes.
- Write units on everything (mg/kg, km, %) and say what a number means.
- Show model stats as a plain two-column list.

Don't:

- Use Inter or Geist, gradients or gradient text, glassmorphism, glows, or neon accents on dark backgrounds.
- Use cards with large rounded corners, a colored stripe on one side, or a border plus a large shadow.
- Show "hero metric" tiles (giant numbers in cards).
- Put a small label or badge above a heading, or icon tiles above headings.
- Use pulsing dots, spinners that never stop, or emoji as icons.
- Write marketing copy. The UI says plainly what the thing does.
