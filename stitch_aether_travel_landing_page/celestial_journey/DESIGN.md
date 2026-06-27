---
name: Celestial Journey
colors:
  surface: '#081425'
  surface-dim: '#081425'
  surface-bright: '#2f3a4c'
  surface-container-lowest: '#040e1f'
  surface-container-low: '#111c2d'
  surface-container: '#152031'
  surface-container-high: '#1f2a3c'
  surface-container-highest: '#2a3548'
  on-surface: '#d8e3fb'
  on-surface-variant: '#c6c6cd'
  inverse-surface: '#d8e3fb'
  inverse-on-surface: '#263143'
  outline: '#909097'
  outline-variant: '#45464d'
  surface-tint: '#bec6e0'
  primary: '#bec6e0'
  on-primary: '#283044'
  primary-container: '#0f172a'
  on-primary-container: '#798098'
  inverse-primary: '#565e74'
  secondary: '#dcc66e'
  on-secondary: '#3a3000'
  secondary-container: '#615200'
  on-secondary-container: '#dbc66d'
  tertiary: '#d2bbff'
  on-tertiary: '#3f008e'
  tertiary-container: '#200050'
  on-tertiary-container: '#965fff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#f9e287'
  secondary-fixed-dim: '#dcc66e'
  on-secondary-fixed: '#221b00'
  on-secondary-fixed-variant: '#534600'
  tertiary-fixed: '#eaddff'
  tertiary-fixed-dim: '#d2bbff'
  on-tertiary-fixed: '#25005a'
  on-tertiary-fixed-variant: '#5a00c6'
  background: '#081425'
  on-background: '#d8e3fb'
  surface-variant: '#2a3548'
typography:
  headline-lg:
    fontFamily: Noto Serif
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Noto Serif
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Noto Serif
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Noto Serif
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
---

## Brand & Style

This design system is crafted for high-end travel experiences with a celestial, exploratory narrative. It evokes a sense of wonder, premium reliability, and the vastness of the cosmos. The target audience consists of modern explorers who seek both luxury and adventure. 

The aesthetic is a hybrid of **Minimalism** and **Glassmorphism**. It utilizes expansive whitespace (or "space" in a literal sense) to provide clarity, while employing translucent layers and soft background blurs to mimic the ethereal quality of stardust and nebulae. The emotional response is one of calm, curiosity, and sophistication.

## Colors

The palette for this design system is rooted in deep space and stellar light. 

- **Primary:** A deep Midnight Navy used for primary surfaces and backgrounds, providing a sense of infinite depth.
- **Secondary:** A Starlight Gold used for high-priority actions and accents, representing the guiding light of a star.
- **Tertiary:** A Nebula Purple used sparingly for gradients and interactive highlights to add a touch of cosmic mystery.
- **Neutral:** A range of slate and zinc tones to handle borders, secondary text, and UI plumbing.

The default color mode is **dark**, prioritizing high-contrast legibility against deep backgrounds.

## Typography

Typography in this design system balances traditional elegance with modern approachability. 

**Noto Serif** is used for headlines to provide a sense of authority, luxury, and timelessness. It carries an editorial feel that suits high-end travel narratives. 

**Plus Jakarta Sans** is used for all body text and labels. Its soft, rounded terminals provide a friendly and optimistic counterpoint to the formal headlines, ensuring that the UI remains inviting and highly readable at smaller scales. Letter spacing is increased slightly for labels to improve legibility against dark, translucent backgrounds.

## Layout & Spacing

The layout philosophy follows a **fluid grid** model with a generous 12-column structure for desktop. To reflect the "space" theme, the design system utilizes an 8px base unit with significant padding to avoid visual clutter.

- **Desktop:** 12 columns, 24px gutters, 64px outside margins. Large sections should use "XL" spacing (40px+) to maintain a sense of openness.
- **Mobile:** 4 columns, 16px gutters, 16px outside margins. Headlines scale down to mobile-specific tokens to prevent clipping.
- **Reflow:** Content should stack vertically on mobile, with cards spanning the full width of the 4-column grid. On tablet, elements should ideally span 6 or 12 columns.

## Elevation & Depth

Visual hierarchy is established through **Glassmorphism** and tonal layering. Rather than traditional heavy shadows, this design system uses the following techniques:

1.  **Backdrop Blurs:** Floating elements like navigation bars and modal overlays use a 20px background blur with a 10% opacity white tint.
2.  **Tonal Stacking:** Surfaces closer to the user are lighter in tone. The background is `#0F172A`, while primary containers are `#1E293B`.
3.  **Inner Glows:** To simulate starlight, high-elevation components (like active cards) feature a 1px subtle inner border in a faint gold or purple, suggesting a light source from within.
4.  **Ambient Shadows:** When shadows are used, they are highly diffused (30px-40px blur) and tinted with the primary navy color to maintain a cohesive atmospheric feel.

## Shapes

The shape language is defined by **Rounded (Level 2)** corners. This choice softens the technical nature of the dark UI and makes the experience feel more welcoming. 

Large containers like cards and image carousels should use `rounded-xl` (1.5rem) to emphasize a soft, organic feel. Interaction elements like buttons and input fields utilize the base `rounded` (0.5rem) setting for a precise yet approachable look.

## Components

- **Buttons:** Primary buttons use a solid gradient from the tertiary purple to the starlight gold, or a solid gold fill with dark navy text. They should have a subtle outer glow on hover.
- **Chips:** Small, pill-shaped tags used for destinations or categories. Use a semi-transparent stroke (1px) and no fill unless active.
- **Lists:** Items should be separated by low-contrast lines (5% white). Icons within lists should be monolinear and use the starlight gold color.
- **Inputs:** Fields are dark with a 1px border. Upon focus, the border transitions to the starlight gold with a soft outer glow.
- **Cards:** The signature component of the design system. Cards use a "glass" effect with a 1px border and 20px backdrop blur. Images inside cards should have a subtle darkened overlay to ensure white text remains legible.
- **Navigation:** A persistent top bar with a glass effect, keeping the background visible but blurred as the user scrolls, maintaining the sense of immersion in the celestial environment.