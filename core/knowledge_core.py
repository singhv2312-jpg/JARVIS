import re


class KnowledgeCore:
    def __init__(self) -> None:
        self.knowledge = {
            "python": "Python is a high-level, readable language used for automation, scripting, AI, data science, and application development.",
            "variables": "Variables hold data values in memory. They are named containers for numbers, strings, lists, and more.",
            "functions": "Functions encapsulate reusable logic so code can be organized and reused efficiently.",
            "lists": "Lists are ordered collections of values. They are mutable and can be indexed by position.",
            "dictionaries": "Dictionaries map keys to values and are ideal for structured data lookup.",
            "loops": "Loops repeat instructions until a condition changes, useful for iteration and automation.",
            "classes": "Classes define templates for objects. They group data and behavior into reusable units.",
            "objects": "Objects are instances of classes and can store state and expose methods.",
            "oop": "OOP organizes code into objects and classes, supporting modularity and encapsulation.",
            "exceptions": "Exceptions represent runtime errors. They can be handled using try/except blocks.",
            "modules": "Modules are reusable Python files that can be imported into other programs.",
            "ai": "Artificial Intelligence is the design of systems that can reason, learn patterns, and automate decisions.",
            "machine learning": "Machine learning uses data to train models that can identify patterns and predict outcomes.",
            "neural networks": "Neural networks are computational models inspired by biological networks for pattern recognition.",
            "generative ai": "Generative AI creates new content such as text, code, or images based on learned patterns.",
            "llms": "Large language models generate and understand human language using statistical patterns.",
            "algorithms": "Algorithms are structured procedures for solving problems and performing computations.",
            "operating systems": "Operating systems coordinate hardware, software, and user interaction across a computer.",
            "cpu": "The CPU executes instructions and handles the main computation of a system.",
            "ram": "RAM is temporary memory used for actively running processes and fast data access.",
            "cybersecurity": "Cybersecurity protects systems, networks, and data from misuse and digital threats.",
            "databases": "Databases store and organize data efficiently so it can be queried and managed reliably.",
            "gravity": "Gravity is the force that attracts masses toward each other and governs motion in space.",
            "relativity": "Relativity explores how space and time change under motion and strong gravitational fields.",
            "atoms": "Atoms are the basic building blocks of matter, made of protons, neutrons, and electrons.",
            "dna": "DNA contains genetic instructions for growth and function in living organisms.",
            "quantum computing": "Quantum computing uses quantum effects to process information in ways that differ from classical computers.",
            "jarvis": "J.A.R.V.I.S. is a modular offline AI-inspired command platform built with Python for command routing, diagnostics, telemetry, and local knowledge assistance.",
            "who are you": "I am J.A.R.V.I.S., a modular offline AI-inspired command platform built in Python.",
            "how do you work": "I parse commands, classify intent, route them to deterministic system functions or local knowledge, and synchronize the UI and telemetry.",
            "what is your architecture": "My architecture is layered: UI, router, command engine, knowledge core, optional local LLM, response manager, and telemetry system.",
            "are you offline": "Yes. The core system is designed to run without internet access and without cloud APIs.",
            "do you use an llm": "I can use an optional local LLM when available, but my core system remains fully functional without it.",
            "how were you built": "I was built using Python with Tkinter, modular logic, local knowledge, telemetry, and optional local generative support.",
            "what language are you written in": "I am written in Python 3.11+.",
            "what is the hud": "The HUD is the central visual system showing reactor activity, scan rings, telemetry overlays, and operational status.",
            "what is telemetry": "Telemetry captures command logs, timing, system status, and operational event data for analysis and reporting.",
        }

    def answer(self, question: str) -> str:
        text = self._normalize(question)
        if not text:
            return "I do not have enough context to answer that question accurately."

        for key, answer in self.knowledge.items():
            if key in text:
                return answer

        if "artificial intelligence" in text or "ai" in text:
            return self.knowledge["ai"]
        if "python" in text:
            return self.knowledge["python"]
        if "jarvis" in text:
            return self.knowledge["jarvis"]

        return (
            "I don't have a dedicated knowledge module for that query in my offline knowledge core. "
            "I can currently assist with: Python, Artificial Intelligence, Computer Science, "
            "System Diagnostics, Telemetry, and J.A.R.V.I.S. Architecture."
        )

    @staticmethod
    def _normalize(text: str) -> str:
        text = (text or "").lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
