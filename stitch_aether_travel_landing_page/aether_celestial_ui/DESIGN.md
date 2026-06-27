---
name: Aether Celestial UI
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e18'
  surface-container-low: '#171b26'
  surface-container: '#1c1f2a'
  surface-container-high: '#262a35'
  surface-container-highest: '#313540'
  on-surface: '#dfe2f1'
  on-surface-variant: '#bcc9c6'
  inverse-surface: '#dfe2f1'
  inverse-on-surface: '#2c303b'
  outline: '#879391'
  outline-variant: '#3d4947'
  surface-tint: '#6bd8cb'
  primary: '#6bd8cb'
  on-primary: '#003732'
  primary-container: '#29a195'
  on-primary-container: '#00302b'
  inverse-primary: '#006a61'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb2b7'
  on-tertiary: '#67001b'
  tertiary-container: '#ff516a'
  on-tertiary-container: '#5b0017'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdadb'
  tertiary-fixed-dim: '#ffb2b7'
  on-tertiary-fixed: '#40000d'
  on-tertiary-fixed-variant: '#92002a'
  background: '#0f131d'
  on-background: '#dfe2f1'
  surface-variant: '#313540'
  obsidian: '#0B0F19'
  aurora-teal: '#0D9488'
  emerald: '#10B981'
  sunset-coral: '#F43F5E'
  frost-white: '#F8FAFC'
  silver-sage: '#94A3B8'
  deep-indigo: '#312E81'
  glass-bg: rgba(15, 23, 42, 0.65)
  glass-border: rgba(255, 255, 255, 0.08)
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Outfit
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Outfit
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Outfit
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Outfit
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-desktop: 80px
  margin-tablet: 40px
  margin-mobile: 20px
  container-max: 1440px
---

## Brand & Style

The design system for this AI-native travel planner is built on a "Celestial Glass" aesthetic, targeting sophisticated travelers who seek a frictionless, intelligent, and premium planning experience. The brand personality is visionary, calm, and highly technical, yet deeply connected to the visceral beauty of global travel.

The UI employs a refined **Glassmorphism** style mixed with **Modern Minimalism**. It evokes the feeling of looking through a high-tech observatory at a night sky. Elements feel ethereal and light, utilizing soft blurs, vibrant glows, and deep-space backgrounds to create a sense of infinite possibility. The emotional response is one of "curated discovery"—where the complexity of AI is masked by a serene, high-fidelity interface.

## Colors

The palette is anchored in **Deep Obsidian**, providing a high-contrast foundation for the luminous accents. 

- **Primary Glow:** Aurora Teal is the primary signal for action and intelligence. It should be used for primary accents and combined with Emerald in linear gradients (135°) for interactive elements.
- **Ambient Depth:** Deep Indigo and Sunset Coral are reserved for background ambient blurs and atmospheric gradients, representing the dusk horizon.
- **Content Hierarchy:** Frost White is utilized for high-priority information and headlines to ensure maximum legibility against the dark void. Silver Sage is used for secondary body text to reduce eye strain and establish a clear information hierarchy.
- **Surface Logic:** Backgrounds are never pure black but rather deep navy-tinted obsidian, creating a softer, more premium depth.

## Typography

This design system uses a dual-font strategy to balance character with clarity. 

**Plus Jakarta Sans** provides a bold, geometric presence for headlines, mirroring the modern and innovative nature of the AI. It is set with tighter letter spacing in larger formats to maintain a high-fashion, editorial look.

**Outfit** serves as the functional workhorse for body copy and UI labels. Its humanist proportions ensure readability even at small sizes within dense travel itineraries. Labels should use slightly increased letter spacing and medium weights to remain distinct against glassmorphic backgrounds.

## Layout & Spacing

The layout follows a **Fluid Grid** model with generous white space (or "dark space") to allow the glassmorphic elements to breathe. 

- **Desktop:** 12-column grid with 24px gutters. Content is centered with a max-width of 1440px.
- **Tablet:** 8-column grid with 20px gutters.
- **Mobile:** 4-column grid with 16px gutters.

The spacing rhythm is based on a **4px base unit**. Component padding should generally favor larger horizontal values (e.g., 12px vertical, 24px horizontal) to support the "pill" and "capsule" shape language. Large sections should be separated by 80px-120px to maintain a premium, uncluttered feel.

## Elevation & Depth

Depth is not communicated through traditional drop shadows, but through **Tonal Layers** and **Backdrop Blurs**.

1.  **Level 0 (Background):** Deep Obsidian (#0B0F19) with subtle radial gradients of Indigo in the corners.
2.  **Level 1 (Cards/Panels):** Semi-transparent glass (`rgba(15, 23, 42, 0.65)`) with a 16px backdrop blur. Borders are a crisp 1px solid `rgba(255, 255, 255, 0.08)`.
3.  **Level 2 (Modals/Popovers):** Higher transparency glass with an increased border opacity and a subtle "Aurora" outer glow (`0 0 20px rgba(13, 148, 136, 0.15)`).
4.  **Interaction:** When hovered, glass elements should increase their background opacity slightly and the border should brighten to `rgba(255, 255, 255, 0.15)`.

## Shapes

The shape language is dominated by **Pill-shaped (Level 3)** geometry. This evokes a sense of fluid movement and friendliness, softening the "hard" technology of the AI.

- **Primary Buttons & Chips:** Always fully rounded (pill-shaped).
- **Large Containers/Cards:** Use `rounded-xl` (1.5rem / 24px) to maintain a soft but structured appearance.
- **Form Inputs:** Fully rounded to match the buttons, creating a cohesive "capsule" aesthetic across all interactive surfaces.

## Components

### Buttons
Primary buttons use a 135-degree gradient from Aurora Teal to Emerald. They feature a subtle outer glow of the same color. Text is always Frost White, semi-bold. Secondary buttons use the glassmorphic style with white text and a 1px border.

### Prompt Chips
Small, pill-shaped elements for AI suggestions. They feature a semi-transparent border and no fill. On hover, they transition to a soft Aurora Teal fill (20% opacity) and gain a faint glowing border.

### Search Containers
The central AI search bar is a large, glassmorphic capsule. It should have a high backdrop blur (24px) to ensure text input is legible over dynamic background imagery. The "Search" or "Submit" icon should be housed in an Aurora Teal circle within the capsule.

### Cards (Itineraries/Destinations)
Cards use the standard glassmorphic treatment. Images within cards should have a subtle dark-to-transparent gradient overlay at the bottom to ensure Silver Sage body copy is readable when placed over the image.

### Input Fields
Inputs are pill-shaped with a subtle `rgba(255, 255, 255, 0.05)` fill. The focus state is indicated by the border changing to Aurora Teal and a soft inner glow.