# Project FRIDAY Architecture

## Overview

Project FRIDAY is an AI-powered wearable assistant designed to improve independence for blind and visually impaired individuals.

The MVP uses a smartphone as the primary compute device connected to lightweight smart glasses. This approach minimizes hardware costs while enabling rapid development and testing.

---

# High-Level Architecture

```
        Camera
           │
           ▼
    Video Processing
           │
           ▼
  Computer Vision Models
           │
           ▼
     AI Decision Layer
           │
   ┌───────┴────────┐
   ▼                ▼
Voice Output     User Commands
   ▲                │
   └────────────────┘
```

---

## Core Components

### Camera

Captures live video.

---

### Object Detection

Identifies objects in real time.

Example:

- Chair
- Person
- Car
- Door

---

### OCR

Reads printed text.

Examples:

- Medicine labels
- Menus
- Road signs

---

### Speech Recognition

Converts speech into text.

---

### AI Assistant

Processes user requests.

Example:

"What is in front of me?"

---

### Text-to-Speech

Reads responses aloud.

---

### Navigation

Provides obstacle warnings and guidance.

---

## Deployment

### Phase 1

Smartphone

↓

AI Processing

↓

Voice Feedback

---

### Phase 2

Smart Glasses

↓

Phone Processing

↓

Voice Feedback

---

### Phase 3

Standalone Smart Glasses
