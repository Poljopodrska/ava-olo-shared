# AVA OLO Constitutional Design System v2

## Overview
This is the unified design system for all AVA OLO applications, shared between:
- **Monitoring Dashboards** (ava-olo-monitoring-dashboards)
- **Agricultural Core** (ava-olo-agricultural-core)
- Any future AVA OLO modules

## Key Features

### 1. Automatic Design Updates
The design system uses CSS Custom Properties (CSS Variables) which means:
- Change a color in the CSS file → All components using that color update automatically
- Change spacing values → All padding/margins update across the entire app
- Change font sizes → Typography scales consistently everywhere

### 2. Constitutional Compliance
- **Minimum 18px font size** for older farmers (Constitutional requirement)
- **Large touch targets** (min 48px height) for field use
- **High contrast colors** for outdoor visibility
- **Agricultural color theme** (browns, olives, greens)

### 3. Design Tokens
The system defines tokens for:
- **Colors**: Primary, agricultural, status, gradients
- **Typography**: Font families, sizes, weights, line heights
- **Spacing**: Consistent spacing scale from xs to 3xl
- **Shadows**: Multiple shadow levels for depth
- **Animations**: Smooth transitions and loading states
- **Border radius**: Consistent rounded corners

## Usage

### In Monitoring Dashboards
```html
<link rel="stylesheet" href="/static/css/constitutional-design-system-v2.css">
```

### In Agricultural Core
```html
<link rel="stylesheet" href="/static/css/constitutional-design-system-v2.css">
```

### Component Examples

#### Buttons
```html
<!-- Primary gradient button -->
<button class="btn btn-primary">Click Me</button>

<!-- Agricultural themed button -->
<button class="constitutional-button constitutional-button-primary">Farm Action</button>
```

#### Cards
```html
<div class="constitutional-card">
    <h3>Card Title</h3>
    <p>Card content goes here</p>
</div>
```

#### Form Elements
```html
<div class="constitutional-form-group">
    <label class="constitutional-label">Field Name</label>
    <input type="text" class="constitutional-input" placeholder="Enter field name">
</div>
```

## File Locations

### Primary Source
`/ava-olo-shared/src/styles/constitutional-design-system-v2.css`

### Deployed Copies
- `/ava-olo-monitoring-dashboards/static/css/constitutional-design-system-v2.css`
- `/ava-olo-agricultural-core/static/css/constitutional-design-system-v2.css`

## Updating the Design System

1. **Make changes** to the primary source in `ava-olo-shared`
2. **Copy to projects**:
   ```bash
   # From ava-olo-shared directory
   cp src/styles/constitutional-design-system-v2.css ../ava-olo-monitoring-dashboards/static/css/
   cp src/styles/constitutional-design-system-v2.css ../ava-olo-agricultural-core/static/css/
   ```
3. **Test** in both applications
4. **Commit** changes in all three repositories

## Design Principles

### 1. Farmer-First Design
- Large, readable text (18px minimum)
- Clear visual hierarchy
- Simple, intuitive interfaces
- Touch-friendly interactive elements

### 2. Agricultural Theme
- Earth tones (browns, olives, greens)
- Natural color palette
- Agricultural metaphors in design

### 3. Consistency
- Same components across all modules
- Predictable behavior
- Unified visual language

### 4. Accessibility
- WCAG compliance
- High contrast ratios
- Clear focus states
- Screen reader support

## CSS Variables Quick Reference

### Primary Colors
```css
--primary-brown: #6B5B73;
--primary-olive: #8B8C5A;
--color-agri-green: #2c5530;
--color-primary-gradient-start: #667eea;
--color-primary-gradient-end: #764ba2;
```

### Typography
```css
--font-size-base: 1.125rem; /* 18px */
--font-size-lg: 1.25rem;     /* 20px */
--font-size-xl: 1.5rem;      /* 24px */
--font-weight-semibold: 600;
--line-height-normal: 1.6;
```

### Spacing
```css
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
```

### Shadows
```css
--shadow-base: 0 4px 6px rgba(0, 0, 0, 0.05);
--shadow-lg: 0 12px 24px rgba(0, 0, 0, 0.1);
--shadow-primary: 0 4px 15px rgba(102, 126, 234, 0.3);
```

## Demo Page
View the design system demo at: `/design-demo` in the monitoring dashboards application.

This page showcases all design elements, components, and demonstrates how the unified system works.

## Constitutional Requirements
This design system enforces Constitutional Principle #14:
- Consistent design across all modules
- If we have a central file and central design steering, it will be easy to change it later
- Design changes automatically propagate across the entire application ecosystem