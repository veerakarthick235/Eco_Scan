# EcoScan ♻️

**Submission for the Zero Boundaries Hackathon**

EcoScan is a smart waste-sorting assistant designed to make recycling and composting simple and intuitive for everyone. Just snap a picture of an item, and EcoScan will tell you exactly how to dispose of it responsibly.

### **Track**

Social Good (Main Theme)

### **Inspiration ✨**

Our world is facing a waste crisis. Many people want to recycle and compost correctly but are often confused by complex local regulations and packaging. Inspired by the hackathon's "Social Good" theme and the **Zero Dump Initiative**, we created **EcoScan** to eliminate this confusion. Our goal is to empower individuals to make a tangible environmental impact, one piece of trash at a time, pushing past the boundaries of waste ignorance.

### **What it does 🎯**

EcoScan is a web-based tool that simplifies waste disposal.

1.  **Upload:** A user uploads an image of a waste item.
2.  **Analyze:** A (currently simulated) AI model analyzes the image to identify the object.
3.  **Instruct:** The app provides clear, immediate instructions: **Recycle**, **Compost**, or **Trash**.
4.  **Educate:** It also offers a "Pro Tip" to educate the user on best practices and the environmental impact of their choice.

### **How we built it 💻**

We used a simple and accessible tech stack, making it a perfect beginner-friendly project:

* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **AI/ML:** For this hackathon prototype, we simulated the AI classification using JavaScript logic that checks the image's filename. This allows us to demonstrate the full user flow effectively. The code is structured to easily integrate a real browser-based model (like TensorFlow.js) in the future.

### **Challenges we ran into 🤔**

The main challenge was designing a user experience that was both instant and informative without being overwhelming. We also had to create a "mock" AI that felt realistic enough for a prototype, which involved mapping keywords in filenames to specific waste categories.

### **What's next for EcoScan 🚀**

* **Real AI Integration:** Replace the mock AI with a trained TensorFlow.js model for real-time image recognition directly in the browser.
* **Geolocation-Based Rules:** Integrate location services to provide disposal guidelines specific to the user's city or municipality.
* **Gamification:** Add a points system to track a user's positive impact and encourage consistent use.

### **Demo Video Link**

[Link to your 2-5 minute demo video will go here]