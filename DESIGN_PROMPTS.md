# Stitch by Google — UI Design Prompts
## AI Travel Planner (Traveller)

This document provides copy-pasteable, high-fidelity design prompts optimized for **Stitch by Google**. These prompts incorporate the design system tokens from [DESIGN.md](file:///c:/Projects/Ai%20travel%20agent/DESIGN.md) to generate a set of premium, cohesive screens for our AI Travel Planner.

---

## Screen 1: Landing Page & Conversational Input (The Entrance)

### Prompt for Stitch:
```text
Design a premium, high-fidelity landing page for a web application called "Traveller" (an AI-native travel planner). 

1. Theme & Colors:
   - Default theme is a dark obsidian-sky palette. Use Deep Obsidian (#0B0F19) for the main background.
   - Primary Accent: Aurora Teal (#0D9488) used for key highlights and glowing elements.
   - Ambient styling: A subtle, blurred background gradient in the upper-right corner blending Navy Blue, Deep Indigo, and a hint of Sunset Coral (#F43F5E), representing a dusk sky.
   - Text color: Primary headings in Frost White (#F8FAFC), body copy in Silver Sage (#94A3B8).

2. Typography:
   - Headings: Bold geometric "Plus Jakarta Sans" font.
   - Body/Controls: Clean humanist "Outfit" font.

3. Hero Layout:
   - A minimalist, spacious layout with a centered value proposition.
   - Header: A bold, clean H1 reading "Your Next Journey, Orchestrated in Seconds." below it a subtitle "A multi-agent AI system that translates your wildest travel dreams into structured, budget-validated itineraries."
   - Central Element: A large, modern conversational search bar container (width 800px) with border-radius of 24px, glassmorphic styling (rgba(15, 23, 42, 0.65) background, backdrop-filter: blur(16px), border: 1px solid rgba(255, 255, 255, 0.08)).
   - Inside the search bar: 
     - A textarea with the placeholder text: "e.g., Plan a 5-day trip to Japan. Tokyo + Kyoto. $3,000 budget. Love food and temples, hate crowds."
     - A prominent primary action button on the far right of the input: A pill-shaped CTA with a vibrant gradient fill (Aurora Teal #0D9488 to Emerald #10B981) containing a clean spark/AI icon and the word "Orchestrate".
   
4. Quick-Start Suggestions:
   - Below the search bar, show 3 horizontal "Prompt Chips" with semi-transparent borders:
     - "🌸 5-Day Tokyo & Kyoto Foodie Escape"
     - "🏰 7-Day Romantic Castles in Germany"
     - "🏖️ 3-Day Spontaneous Weekend in Goa"
   - Active hover state: when hovered, the chips grow by 2% and show a soft Aurora Teal glow.

5. Footer/Social Proof:
   - At the bottom of the viewport, display a subtle line of logos representing integration partners: Booking.com, Agoda, Google Flights, Airbnb. Add a status label: "Powered by Gemini 2.5 Flash Lite".
```

---

## Screen 2: Constraint Editor & Loading States (The Orchestration View)

### Prompt for Stitch:
```text
Design the "Constraint Editor and Generation Loading State" screen for "Traveller". This screen displays what the AI Orchestrator has parsed from the user's input, allowing them to verify and tweak details while the agents run.

1. Layout Structure:
   - Split view or layered panel on a dark background (#0B0F19).
   - Main container: A large, centralized glassmorphic card (Slate Glass, rgba(15, 23, 42, 0.65) background, border-radius 24px, border 1px solid rgba(255, 255, 255, 0.08)).

2. Left Column - Constraint Editor Form (Width 45%):
   - Header: "Extracted Travel Constraints" (Plus Jakarta Sans, H3).
   - Create 4 input blocks using clean form fields:
     - Destination Tags: An interactive tag box containing "Tokyo (Japan)", "Kyoto (Japan)" with close 'x' buttons.
     - Trip Duration: A sleek stepper input showing "5 Days" with custom +/- icons.
     - Total Budget: A custom slider showing "$3,000" with a progress line filled in Sunset Coral (#F43F5E).
     - Preferences & Avoidances: Two columns of pill tags:
       - Preferences (Aurora Teal outline): "Food & Dining", "Temples & History", "Nature Walks"
       - Avoidances (Sunset Coral outline): "Large Crowds", "Early Mornings", "Luxury Hotels"
   - Bottom Actions: A secondary button "Update & Regenerate" and a primary CTA "Generate Itinerary".

3. Right Column - Multi-Agent Processing Panel (Width 50%):
   - Title: "AI Agent Orchestration Pipeline" (Plus Jakarta Sans, Muted H3).
   - Visual: A vertical flow chart of 5 agent nodes linked by glowing circuit lines.
     - Node 1: Orchestrator Agent (State: Completed, marked with a checkmark in Aurora Teal #0D9488).
     - Node 2: Destination Research Agent (State: Active/Processing, glowing with a pulsing gold border).
     - Node 3: Logistics Agent (State: Waiting, semi-transparent grey).
     - Node 4: Budget Agent (State: Waiting, semi-transparent grey).
     - Node 5: Review Agent (State: Waiting, semi-transparent grey).
   - Below the nodes: A progress tracker card showing: "Destination Research Agent is curating crowd-avoidant experiences in Yanaka and Arashiyama..." with a loading spinner.
```

---

## Screen 3: Main Itinerary & Interactive Map (The Plan Dashboard)

### Prompt for Stitch:
```text
Design the primary dashboard for "Traveller" presenting the completed trip itinerary. This is a split-screen layout for desktop, optimized for visual impact and density.

1. Overall Grid Layout:
   - Left Sidebar (Width 40%): Scrollable day-by-day itinerary feed.
   - Right Main Viewport (Width 60%): Interactive Map and floating budget panel.
   - Navigation Header: A thin, elegant header at the top with the logo "Traveller", sharing buttons, calendar export, and user profile bubble.

2. Left Column - Day-by-Day Timeline:
   - A vertical timeline.
   - Day Cards: Standard glassmorphic cards (Slate Glass, border-radius 16px).
   - Card structure (e.g., Day 1 - Tokyo: Quiet Temples & Local Flavors):
     - Header: Day name in Plus Jakarta Sans bold, a collapsible chevron, and a small total cost badge ($50).
     - Timeline Activities (Chronological):
       - Morning Slot: "Nezu Shrine (Low Crowds)" with a Temple Gold badge (#D97706), estimated cost "$4", duration "1.5h".
       - Afternoon Slot: "Yanaka Walking Trail & Local Coffee" with a Purple badge (#8B5CF6), cost "$8", duration "2.5h".
       - Evening Slot: "Koenji Ramen Alley Dinner" with a Sunset Coral badge (#F43F5E), cost "$12", duration "2h".
     - Between slots: transit connectors showing "Walk (12 mins)" or "Train (15 mins, $2)" in Aurora Teal (#0D9488).

3. Right Column - Map & Quick Actions:
   - Background: An immersive, dark-themed map (black/dark grey oceans and streets, with glowing routes).
   - Map elements: Colored pins corresponding to the Day 1 activities (Pin 1: Gold, Pin 2: Purple, Pin 3: Coral) connected by a dashed teal line showing the transit route.
   - Floating Action Cards:
     - Top Right: A floating group of buttons: "Export PDF", "Add to Google Calendar", "Share Plan".
     - Bottom Left: A floating card summary: "Total Cost: $1,787 / Remaining: $1,213" with a checkmark "Review Agent Passed".
```

---

## Screen 4: Visual Budget Dashboard & "What-If" Workspace

### Prompt for Stitch:
```text
Design the dedicated "Budget Analytics and Financial Workspace" dashboard for "Traveller". This screen allows travelers to visualize costs and perform interactive scenario adjustments.

1. Layout & Styling:
   - Full-width dark screen dashboard (#0B0F19).
   - Typography: Plus Jakarta Sans for numbers and headers, Outfit for descriptions.

2. Top Row - Financial Health Gauges (3 Columns):
   - Card 1: Circular Progress Gauge (Glassmorphism, 16px radius). Shows a neon ring representing budget allocation. Center text: "$1,787 spent / $3,000 total". Below it: "You are $1,213 under budget" in Emerald Green.
   - Card 2: Cost Forecast Card. "Review Agent Confidence: 92%". Shows a small sparkline chart tracking estimated vs actual costs across the 5 days.
   - Card 3: "What-If" Optimizer Panel. A large horizontal slider representing the target budget ceiling. Sliding it down shows an alert: "Adjusting to $1,500 will swap 4-star hotels for guesthouses in Kyoto."

3. Bottom Row - Category Cost Breakdown (Grid of 6 Cards):
   - Category Cards (Flights, Stay, Transit, Food, Activities, Buffer):
     - Each card has a colored category indicator at the top left.
     - Flight Card: Title "Flights (Budget Carrier)", allocation value "$720", progress bar representing 24% of total budget.
     - Stay Card: Title "Accommodation (Mid-Range Machiya)", allocation "$560" (Purple accent).
     - Transit Card: Title "Shinkansen + local IC Card", allocation "$127" (Teal accent).
     - Food Card: Title "Meals & Markets", allocation "$200" (Coral accent).
     - Activities Card: Title "Attractions & Temples", allocation "$30" (Gold accent).
     - Buffer Card: Title "Unplanned / Emergency", allocation "$150".
```

---

## Screen 5: AI Co-Pilot Chat & Collaboration Drawer (Refinement View)

### Prompt for Stitch:
```text
Design the "AI Co-Pilot Chat Drawer & Collaboration Panel" as an overlay overlaying the main Itinerary screen of "Traveller". This screen demonstrates real-time user-agent conversation and collaborative planning features.

1. Base Screen:
   - The Main Itinerary & Interactive Map Dashboard (Screen 3) is visible in the background, slightly dimmed.

2. Right Sidebar Chat Drawer (Width 30%):
   - Background: Solid Slate Glass (rgba(15, 23, 42, 0.95)) with a strong backdrop blur and a thin vertical divider in Frost Border (#ffffff14).
   - Header: "AI Travel Co-Pilot" with a pulsing online indicator.
   - Chat History Area:
     - User Message: "Let's move the Arashiyama visit from Day 3 afternoon to Day 4 morning, and swap Koenji Ramen for a sushi lunch."
     - Co-Pilot Response: A typewriter loading effect showing: "Recalculating logistics..." 
     - Followed by the updated proposal: "I've re-sequenced the route. Arashiyama fits perfectly on Day 4. Let's look at the changes:"
     - Diff Comparison Card inside the chat bubble:
       - "🗑️ Day 3 PM: Arashiyama Bamboo Grove -> Moved" (red strikeout text)
       - "✅ Day 4 AM: Arashiyama Bamboo Grove -> Added" (green text)
       - "🔄 Budget change: - $15 (Sushi swap)" (green text)
     - Quick Action Button: "Apply Changes to Itinerary" (Teal Gradient fill).
   - Bottom Input Area: A capsule-shaped message field with an attachment icon and microphone button.

3. Collaboration Indicators (Top Right Header):
   - Avatar stack showing 3 user bubbles: "Priya (Organizer - Green cursor)", "Marcus (Viewer - Orange cursor)", and a "+ Add Planner" invite button.
   - On the background itinerary card, show a small green floating cursor badge labeled "Priya is editing Day 3" to show real-time collaborative editing.
```
