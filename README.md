# Tata Suraksha AI: Industrial Safety Training & Assessment Platform

A next-generation AI-powered safety training and diagnostic platform developed for **Tata Steel**. Instead of static multiple-choice tests or standard chatbots, **Tata Suraksha AI** dynamically generates context-aware plant floor scenarios, evaluates worker decisions in real-time, identifies personal safety vulnerabilities, and generates personalized adaptive retests.

---

## 🏭 Key Features

1. **Employee Profile & Department Context**:
   - Integrated profiles tailored for high-risk operations: *Blast Furnace & Hot Metal*, *Steel Melting Shop (SMS / LD Shop)*, *Rolling Mills*, *Coke Ovens*, *Electrical Substations*, and *Logistics*.
   - Includes 1-click demo profiles (*Ramesh Kumar, Priya Sharma, Amit Verma*).

2. **Dual AI Scenario Generation**:
   - **Live Gemini AI Integration**: Dynamically synthesizes endless realistic plant dilemmas via Google Gemini API.
   - **Built-in Tata Steel Knowledge Engine**: 50+ authentic shop-floor scenarios covering *TSS-01 (PPE)*, *TSS-02 (Fire & Gas)*, *TSS-03 (Electrical LOTOTO)*, *TSS-04 (Heights & Confined Spaces)*, *TSS-05 (Molten Metal & Heavy Cranes)*, and *TSS-06 (Emergency Protocols)*.

3. **Real-Time Decision Evaluation & Catastrophe Breakdown**:
   - Instant scoring (+10 per compliant decision).
   - Real-world catastrophic consequence analysis ("What could happen in the plant if you did that?").
   - Citations of Tata Steel Safety Standards (TSS) and Indian Factories Act 1948.

4. **Weak Area Detection & Adaptive Retest Engine**:
   - Diagnostic analysis tracking accuracy across all safety domains.
   - Automatically flags vulnerable topics (e.g. accuracy < 70%).
   - **"Train My Weak Areas (AI Retest)"** button generates targeted remediation drills focusing strictly on the employee's past mistakes.

5. **Safety Profile & Supervisor Analytics**:
   - Complete safety domain mastery radar.
   - Recent assessment history log with compliance status.

---

## 🚀 Getting Started

### 1. Development Mode
Run the development server locally:
```bash
npm run dev
```
Open your browser at [http://localhost:3000](http://localhost:3000).

### 2. Production Build
```bash
npm run build
npm run preview
```

### 3. Optional: Live Gemini AI Setup
Click the **"AI Engine"** button in the top navigation bar and enter your Google Gemini API key to activate live generative scenario creation. (The platform also works 100% offline out-of-the-box).
