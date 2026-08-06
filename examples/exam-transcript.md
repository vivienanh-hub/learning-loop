# Example: /exam Transcript

This is an example of what a `/exam` session looks like. Topic: **RAG (Retrieval-Augmented Generation)** — knowledge exam, Attempt 1.

---

**The Lab.** Let's see what you actually know about RAG. This is Attempt 1 — closed-book, no notes.

Explain the core architecture of a RAG system: what the three main components are and what each one does. Then tell me what problem RAG solves that a vanilla LLM cannot.

> "No notes. No progress file. Write your answer."

---

**User answer:**

RAG has three main parts: a retrieval system that searches a knowledge base, an embedding model that turns text into vectors for similarity search, and the LLM itself that generates the final answer. The retrieval system finds relevant chunks from your documents, passes them as context to the LLM, and the LLM uses both the retrieved content and its training to generate a grounded answer.

The problem it solves: LLMs have a knowledge cutoff and can't access private or frequently-updated data. RAG lets you inject fresh, proprietary information at inference time without retraining the model.

---

**Pass.** The retrieval → context injection → generation loop is correctly described, and the knowledge cutoff / private data trade-off is the right answer to "what vanilla LLM cannot do." Minor note: you didn't name vector similarity search explicitly — mentioning cosine similarity or embedding-based retrieval would sharpen the retrieval component description.

---

*This exam logged a Pass on first attempt. Progress file updated at `personal-professional-profile/learning/progress/rag.md`. Spaced retrieval rep scheduled: re-test in 3 weeks.*

*_Complexity: ~3K input / ~400 output tokens (est.)_*
