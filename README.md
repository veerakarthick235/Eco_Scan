# EcoScan ♻️

**_Snap, Sort, Sustain._ Your AI-powered guide to responsible waste disposal.**

This project is a submission for the **Zero Boundaries Hackathon** in the **Social Good** track.

---

## ## Inspiration ✨

Every day, countless recyclable and compostable items end up in landfills due to confusion about local disposal rules. Inspired by the hackathon's mission of "impact without borders" and the **Zero Dump Initiative**, we created **EcoScan**. Our goal is to break down the barriers of confusion and empower anyone, anywhere, to make environmentally responsible decisions with a simple photo.

---

## ## What It Does 🎯

EcoScan is a smart web application that uses real-time AI to identify waste items from an uploaded image. It instantly tells the user whether to **Recycle**, **Compost**, or put the item in the **Trash**, providing clear instructions and educational tips to encourage sustainable habits.

---

## ## Live Demo

[**Insert Link to Your 2-5 Minute YouTube Demo Video Here**]

---

## ## Key Features 🚀

* **🧠 Real-Time AI Classification:** Utilizes a **TensorFlow** model (`MobileNetV2`) on a Python backend to recognize over 1,000 common objects from a user's photo.
* **📍 Location-Aware Suggestions:** Uses the browser's **Geolocation API** to fetch the user's coordinates, enabling future expansion for city-specific disposal rules.
* **📈 User Impact Tracking:** Leverages browser **localStorage** to keep a persistent history of scanned items, gamifying the experience by tracking the number of items recycled and composted.
* ** expandable Knowledge Base:** The AI's "vocabulary" can be easily expanded by mapping new object labels to disposal categories directly in the backend code.

---

## ## Tech Stack 🛠️

### ### Backend

* **Language:** Python
* **Framework:** Flask
* **AI/ML:** TensorFlow, Keras, Pillow, NumPy
* **API:** RESTful endpoint for classification

### ### Frontend

* **Core:** HTML5, CSS3, Vanilla JavaScript
* **APIs:** Fetch API, Geolocation API, LocalStorage API

---

## ## How to Run Locally

Follow these steps to get EcoScan running on your local machine.

### ### Prerequisites

* **Python 3.8+** and `pip` installed.
* **Visual Studio Code** with the **Live Server** extension.
