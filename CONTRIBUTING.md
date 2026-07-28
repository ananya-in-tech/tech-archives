<!-- markdownlint-disable MD041 -->
<div align="center">
  <h1>🤝 Contributing to DSA Discussions</h1>
  <p><b>An elegant, community-driven ecosystem designed for mastering Data Structures and Algorithms.</b></p>

  <a href="https://github.com/ananya-09/DSA-Discussions">
    <img src="https://img.shields.io/github/repo-size/ananya-09/DSA-Discussions?color=FFE75E&style=flat-square" alt="Repo Size">
  </a>
  <a href="https://github.com/ananya-09/DSA-Discussions/discussions">
    <img src="https://img.shields.io/github/discussions/ananya-09/DSA-Discussions?color=00B8A9&style=flat-square" alt="Discussions">
  </a>
  <a href="https://github.com/ananya-09/DSA-Discussions/pulls">
    <img src="https://img.shields.io/github/issues-pr/ananya-09/DSA-Discussions?color=7B61FF&style=flat-square" alt="PRs Welcome">
  </a>
</div>

<!-- markdownlint-enable MD033 -->
---

## 🌟 Welcome to the Community!

First off, thank you for considering contributing to **DSA Discussions**! 🎉

Whether you are fixing a typo, adding an optimized solution, breaking down an advanced Dynamic Programming pattern, improving workflow automation, or helping a peer debug an edge case in the Doubt Box—**your contribution matters**.

This repository is built around a dual-pillar ecosystem:
1. **The Vault (Repository Core):** Topic-wise structured notes, conceptual breakdowns, curated problem lists, and multi-language solutions.
2. **The Forum (GitHub Discussions):** Real-time problem breakdowns, automated LeetCode & Codeforces briefings, contest strategy chats, and Q&A debugging.

Before contributing, please take a moment to read this guide to ensure your work aligns with our codebase design principles, directory structure, and community vision.

---

## 🧭 Principles & Vision

Every contribution to **DSA Discussions** should reflect our core values:

* **Structured Learning:** Avoid unstructured file dumps at the root directory. Everything has its designated home.
* **Intuition First:** Explain *why* a solution works before jumping into code.
* **Code Clarity & Quality:** Code should be clean, modular, and thoroughly commented so fellow learners can follow the algorithmic logic easily.
* **Complexity Awareness:** Always detail explicit Time Complexity and Auxiliary Space Complexity (e.g., Time: `O(N)`, Space: `O(1)`).
* **Inclusive & Supportive Collaboration:** Encourage peers, participate in code reviews constructively, and share knowledge generously.

---

## 🚀 Ways You Can Contribute

There are many ways to contribute to this ecosystem:

| Contribution Area | Description | Where it Happens |
| :--- | :--- | :--- |
| **📁 Code Solutions** | Add optimal or multi-approach solutions (C++, Java, Python, Go, JS/TS, Rust). | **The Vault** (`DSA/` subdirectories) |
| **📚 Topic Notes & Diagrams** | Enhance conceptual explanations, add visual diagrams, or update `Practice.md` sheets. | **The Vault** (`DSA/` subdirectories) |
| **🤖 Automated Discussions** | Start problem study threads in LeetCode/Codeforces Arena using automated bots. | **The Forum** (Discussions tab) |
| **❓ Peer Debugging** | Help resolve failing test cases or edge cases in **The Doubt Box**. | **The Forum** (Discussions tab) |
| **🛠️ Automation & Tooling** | Improve GitHub Actions workflows (`.github/workflows/`) or issue blueprints. | Repository Root |
| **🐛 Bug Reports & Ideas** | Report broken links, incorrect complexity notes, or feature proposals. | GitHub Issues |

---

## 🛠️ Step-by-Step Contribution Workflow

Follow these steps to submit your contributions smoothly:

```text
[Fork Repo] ➔ [Create Branch] ➔ [Write Solution & Notes] ➔ [Test & Format] ➔ [Submit PR] ➔ [Peer Review] ➔ [Merged! 🎉]
```

### 1️⃣ Fork & Clone the Repository
Start by forking the repository to your own GitHub account, then clone it locally:

```bash
git clone https://github.com/YOUR-USERNAME/DSA-Discussions.git
cd DSA-Discussions
```

### 2️⃣ Create a Descriptive Feature Branch
Always create a dedicated branch for your work. Never work directly on `main`:

```bash
# For adding solutions or notes
git checkout -b feat/arrays-two-sum-cpp

# For documentation improvements
git checkout -b docs/linked-list-guide

# For automation or workflow fixes
git checkout -b fix/lc-fetcher-script
```

### 3️⃣ Follow the Repository Directory Structure
Organize your solutions and notes within the appropriate module folder under `DSA/`:

```text
DSA/
├── 01_Introduction/
├── 02_Time_and_Space_complexity/
├── 03_Mathematics_for_DSA/
├── 04_Arrays_Strings/
│   ├── README.md             # Topic conceptual breakdown & intuition
│   ├── Practice.md           # Curated problem lists (LeetCode, Codeforces, GFG)
│   ├── Resources.md          # External reading materials & video links
│   └── Two_Sum/              # Specific Problem Folder
│       ├── README.md         # Problem explanation & approach breakdown
│       ├── solution.cpp      # C++ implementation
│       ├── solution.py       # Python implementation
│       └── solution.java     # Java implementation
└── ...
```

> [!IMPORTANT]
> **No Root Dumps:** Do not create loose source files in the repository root directory. Always place code inside the relevant topic directory under `DSA/`.

---

## 💻 Code & Documentation Standards

To maintain high technical depth and interview readiness, please follow these guidelines when writing code and documentation:

### Code Formatting & Documentation
1. **Header Metadata:** Include a top comment block in every solution file with the problem link, difficulty, and complexities:
   ```cpp
   /**
    * Problem: Two Sum
    * Platform: LeetCode #1
    * Link: https://leetcode.com/problems/two-sum/
    * 
    * Time Complexity:  O(N) - Single pass using Hash Map
    * Space Complexity: O(N) - Auxiliary space for storing complement elements
    */
   ```
2. **Readable Variable Names:** Use self-explanatory variable names (`targetSum`, `seenMap`, `leftPtr`) rather than single-letter variables except for standard loop indices (`i`, `j`).
3. **Inline Comments:** Add inline comments explaining non-obvious logic, mathematical transformations, or edge case handling.
4. **Multiple Approaches:** When possible, demonstrate progression from Brute Force ➔ Better ➔ Optimal solution.

### Topic Documentation (`README.md`) Standards
When writing or improving conceptual guides in `DSA/`:
* Include an **Intuition & Real-world Motivation** section.
* Provide **Visual Diagrams** (using ASCII art or Mermaid diagrams).
* Highlight **Common Pitfalls & Edge Cases** (e.g., integer overflow, empty inputs, null pointers).
* Include **Complexity Analysis Tables**.

---

## 📝 Commit & PR Guidelines

### Commit Messages
We encourage clear, standard commit messages following Conventional Commits:

* `feat(arrays): add optimal O(N) hash map solution for Two Sum in C++`
* `docs(dp): add 0/1 knapsack pattern breakdown and state transition diagram`
* `fix(workflows): update LeetCode GraphQL query field for topic tags`

### Submitting a Pull Request (PR)

1. Push your branch to your forked repository:
   ```bash
   git push origin feat/arrays-two-sum-cpp
   ```
2. Open a Pull Request on GitHub against the `main` branch of `ananya-09/DSA-Discussions`.
3. Fill out the PR template or description completely:
   * Link relevant Issues or Discussions if applicable.
   * State the problem solved, language used, and complexities.
   * Confirm that your code has been tested locally against all platform test cases.

> [!TIP]
> **Issue Blueprints:** When proposing new solutions or features, you can also use our interactive GitHub Issue templates:
> * 💻 **Submit a Solution Blueprint**
> * 🐛 **Bug Report**
> * 🚀 **Feature Request**

---

## 💬 Community & Discussions Etiquette

Our **GitHub Discussions** space is the heartbeat of this community! When interacting in Discussions:

* **Use Automated Discussion Features:**
  * In **LeetCode Arena**, paste the direct problem link (e.g., `https://leetcode.com/problems/two-sum/`) to trigger our automated problem briefing bot.
  * In **Codeforces Arena**, paste the problem link or specify the contest ID and problem index format:
    ```markdown
    # Contest ID
    2074

    # Problem Index
    A
    ```
* **Keep Threads Consolidated:** Search for existing threads before creating a new discussion for the same problem. Add your approach or doubts as a reply inside the existing master thread.
* **Be Constructive in Code Reviews & Doubt Box:** When helping peers in **The Doubt Box**, highlight the bug clearly, explain the underlying cause, and offer hints before revealing full solutions.

---

## 📜 Code of Conduct

We are committed to making participation in **DSA Discussions** a welcoming, safe, and respectful experience for everyone:

* Be respectful and inclusive of all skill levels, from total beginners to experienced competitive programmers.
* Accept constructive criticism gracefully during peer reviews.
* Focus on community growth: teach, learn, and celebrate each other's progress! 🏆

---

## 👥 Questions or Need Help?

If you ever get stuck or need guidance on how to structure a contribution:
* Drop a post in [🤘 Chit-Chat](https://github.com/ananya-09/DSA-Discussions/discussions/categories/chit-chat) or [❓ Doubt Box](https://github.com/ananya-09/DSA-Discussions/discussions/categories/doubt-box-q-a).
* Tag the maintainers or repository creator [@ananya-09](https://github.com/ananya-09).

---

*Thank you for helping us build the ultimate community-driven DSA handbook! Let's engineer our growth one commit at a time.* 🟩🚀
