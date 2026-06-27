# Design System & UI/UX Specification
## AI Travel Planner (Traveller)

This document defines the visual design system, UI/UX guidelines, and design tokens for the AI Travel Planner ("Traveller"). It is structured for direct reference by design teams and AI design generators like **Stitch by Google** to maintain absolute visual consistency.

---

## 1. Design Vision & Philosophy

Traveller is a premium, AI-native travel assistant. The visual design must evoke a sense of **wanderlust, precision, and luxury**. It is not a generic forms-based utility; it is a digital travel journal that feels alive, interactive, and personalized.

*   **Premium Tech-Traveler Vibe**: The aesthetic should feel like a high-end travel journal merged with a futuristic AI flight deck.
*   **Wanderlust Imagery & Deep Atmosphere**: Use of dark obsidian palettes combined with glowing gradients that recall night flights, glowing city lights, and golden sunrises.
*   **Immersive Glassmorphism**: Cards and panels float above ambient, blurred backgrounds, creating depth.
*   **No Placeholders**: High-quality travel imagery and rich maps are core to the experience.

---

## 2. Color Palette (Design Tokens)

The system uses a dark mode design system as the default interface to feel premium, sleek, and reduce eye strain during hours of travel planning.

### 2.1 Theme Colors

| Role | Color Name | Hex Code | Visual Application |
|---|---|---|---|
| **Background (Dark)** | Obsidian Void | `#0B0F19` | Main viewport background |
| **Surface (Base)** | Slate Glass | `rgba(15, 23, 42, 0.65)` | Cards, panels, inputs (needs `backdrop-filter: blur(16px)`) |
| **Surface (Active)** | Slate Light | `rgba(30, 41, 59, 0.8)` | Selected states, popovers, active cards |
| **Border** | Frost Border | `rgba(255, 255, 255, 0.08)` | Thin 1px panel and card borders |
| **Primary Accent** | Aurora Teal | `#0D9488` | Primary CTA, active selections, transit highlights |
| **Secondary Accent** | Sunset Coral | `#F43F5E` | Secondary buttons, food tags, price warnings |
| **Tertiary Accent** | Temple Gold | `#D97706` | Special experiences, temple tags, budget success |
| **Text (Primary)** | Frost White | `#F8FAFC` | Headings, main text, high contrast labels |
| **Text (Muted)** | Silver Sage | `#94A3B8` | Body copy, subtitles, placeholder text |

### 2.2 Category Color Coding (Badges & Timelines)

*   **Food & Dining:** Sunset Coral (`#F43F5E`) with 10% opacity background.
*   **Sightseeing & Temples:** Temple Gold (`#D97706`) with 10% opacity background.
*   **Transit & Logistics:** Aurora Teal (`#0D9488`) with 10% opacity background.
*   **Accommodation:** Electric Purple (`#8B5CF6`) with 10% opacity background.

---

## 3. Typography & Hierarchy

To elevate the visual feel, we use a distinct combination of a bold geometric font for headings and a clean, legible font for controls and data.

*   **Primary Headings (H1, H2, H3):** **Plus Jakarta Sans** (Google Fonts)
    *   *Alternative:* Clash Display
    *   *Characteristics:* Modern, clean, geometric, high-impact.
*   **Body Text & Interactive Elements:** **Outfit** (Google Fonts)
    *   *Alternative:* Inter
    *   *Characteristics:* Humanist curves, extremely legible at small sizes, premium editorial feel.

### Type scale:
*   **Hero H1:** 3.5rem (56px) | Bold | tracking-tight
*   **Section H2:** 2rem (32px) | Semi-Bold | tracking-normal
*   **Card Header H3:** 1.25rem (20px) | Medium
*   **Body Large:** 1rem (16px) | Regular | line-height: 1.6
*   **Body Small/Labels:** 0.875rem (14px) | Regular
*   **Muted Data:** 0.75rem (12px) | Medium | tracking-wider | Uppercase

---

## 4. Layout, Grids & Spacing

*   **Responsive Grid:** 12-column grid on desktop (1440px max width). Fluid single-column on mobile.
*   **Margins:** 5% horizontal margin on desktop, 16px on mobile.
*   **Spacing System (Tailwind Scale):**
    *   `8px` (xs): Between tag badges and small labels.
    *   `16px` (sm): Internal padding of smaller controls or items.
    *   `24px` (md): Card padding, space between adjacent sections.
    *   `48px` (lg): Large section gaps, layout columns spacing.
*   **Border Radii:**
    *   `24px` (Large): High-level panels, main search inputs.
    *   `16px` (Medium): Itinerary cards, budget panels, map containers.
    *   `8px` (Small): Buttons, dropdowns, status badges.

---

## 5. UI Elements & Component Rules

### 5.1 Glassmorphic Cards
All dashboard elements must use a layered glass effect:
*   `background: rgba(15, 23, 42, 0.65)`
*   `backdrop-filter: blur(16px)`
*   `border: 1px solid rgba(255, 255, 255, 0.08)`
*   `box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3)`

### 5.2 Buttons & CTAs
*   **Primary Action Button:** Gradient fill (Aurora Teal `#0D9488` to Emerald `#10B981`), white text, bold. Hover scale `1.02x` with a glow effect.
*   **Secondary Action Button:** Border outline (`1px solid rgba(255, 255, 255, 0.2)`), background translucent. Hover turns solid Aurora Teal.
*   **Destructive/Alert Button:** Gradient fill (Sunset Coral `#F43F5E` to `#E11D48`).

### 5.3 Inputs & Conversational Boxes
*   Large inputs must have a glow effect on focus (`box-shadow: 0 0 15px rgba(13, 148, 136, 0.4)`).
*   Text areas should support multi-line styling with auto-growing height.

---

## 6. Motion & Micro-Interactions

An interface that feels alive encourages usage. Stitch should model the following transitions:
1.  **Card Expansion:** Day cards accordion expand with a smooth spring transition (`duration: 400ms`, `ease-out`).
2.  **State Changes:** Transitioning between tabs or budget adjustments must use fading slides (`ease-in-out`, `300ms`).
3.  **Hover States:** Interactive timeline items must lift up by `4px` and outline brightness increases on cursor hover.
4.  **Agent Loading Loop:** The processing state should show glowing circuit paths linking 5 nodes representing the agents, pulsed with teal and gold light particles.
