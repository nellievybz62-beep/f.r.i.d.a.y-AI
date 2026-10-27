# Project FRIDAY 🤖👓

> An open-source AI-powered wearable assistant designed to improve independence for blind and visually impaired individuals.

![Status](https://img.shields.io/badge/Status-MVP%20Planning-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Made in](https://img.shields.io/badge/Made%20in-Kenya-red)

---

## Vision

Project FRIDAY aims to build an intelligent wearable assistant that empowers blind and visually impaired people to better understand, navigate, and interact with the world using artificial intelligence.

By combining computer vision, speech technologies, and conversational AI, FRIDAY delivers real-time assistance through smart glasses and a connected smartphone.

---

## The Problem

Millions of people with visual impairments face daily challenges such as:

- Reading printed text
- Identifying everyday objects
- Navigating unfamiliar environments
- Understanding surrounding scenes
- Accessing information independently

Existing assistive technologies are often expensive, limited, or inaccessible.

---

## Our Solution

Project FRIDAY combines AI and wearable technology to provide:

- 🎯 Real-time object detection
- 📖 Optical Character Recognition (OCR)
- 🎤 Speech-to-Text
- 🔊 Natural Text-to-Speech
- 🧠 AI-powered conversational assistance
- 🧭 Environmental awareness
- 🚶 Navigation assistance
- 🌍 Offline + Cloud AI support

---

## MVP Roadmap

### Phase 1
- Smartphone application
- Camera pipeline
- Object detection
- Voice interaction

### Phase 2
- OCR
- Scene understanding
- Environmental awareness

### Phase 3
- Smart glasses integration
- Hands-free interaction
- Real-world user testing

### Phase 4
- Advanced navigation
- Personalized AI assistant
- Production prototype

---

## Planned Technology Stack

### Computer Vision
- YOLOv8
- OpenCV

### OCR
- PaddleOCR

### Speech Recognition
- Whisper

### Text-to-Speech
- Piper

### AI Assistant
- Gemma / Phi
- OpenAI API (optional)
- Hybrid Edge + Cloud Architecture

---

## Current Status

🚧 Project FRIDAY is an evolving prototype, with core assistant development and sponsor integration testing underway.

### Verified Progress
- A local Zetaris bridge successfully executed a test query and returned `seven: 7`.
- The bridge requires authentication for query requests.
- Android connectivity to the bridge health endpoint has been tested.
- Full authenticated Android-to-Zetaris integration remains in progress.

Some listed technologies and accessibility features represent planned architecture, not yet completed capabilities.

We are actively seeking collaborators, mentors, accessibility experts, AI engineers, hardware engineers, designers, researchers, and strategic partners.

---

## Contributing

We welcome contributions from developers, students, researchers, accessibility advocates, and anyone passionate about building technology that improves lives.

If you'd like to contribute, feel free to open an Issue or submit a Pull Request.

---

## Mission

Our mission is to make artificial intelligence accessible through wearable technology that enhances independence, safety, and quality of life for people with visual impairments.

---

## Founder

**David Nelson Njeka**

Nairobi, Kenya

---

*"Technology should not only be intelligent—it should be empowering."*

## Meterless H-MEM status

A standalone Meterless H-MEM starter has been tested for memory mining,
retrieval with provenance, and recall across separate command runs.
See `docs/METERLESS_HMEM_TEST.md` for the recorded test and setup steps.
The Meterless agent and PC API have now returned a live Nemotron-generated answer using H-MEM context, with memory provenance. Browser UI operation and full Android integration remain unverified.

## Zetaris + Meterless workflow

A combined smoke test has successfully queried Zetaris (`seven = 7`), stored
the result in Meterless H-MEM, and recalled it with memory provenance.
Reproduction steps and limitations are documented in
`docs/ZETARIS_HMEM_WORKFLOW.md`. This is not yet the full F.R.I.D.A.Y.
backend, and NVIDIA Nemotron is not yet verified.
