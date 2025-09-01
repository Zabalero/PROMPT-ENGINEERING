# 🔣 Symbol Reference Guide
*v1.0 | Created: 2025-08-05 | Updated: 2025-08-05*

## 📁 File Symbols
- 📂 = /memory-bank/
- 📦 = /memory-bank/backups/

## 🧠 Memory Documents (σ)
- σ₁: Project Brief → projectbrief.md
- σ₂: System Patterns → systemPatterns.md
- σ₃: Technical Context → techContext.md
- σ₄: Active Context → activeContext.md
- σ₅: Progress Tracker → progress.md
- σ₆: Protection Registry → protection.md

## 🧭 Modes (Ω)
- Ω₁: RESEARCH
- Ω₂: INNOVATE
- Ω₃: PLAN
- Ω₄: EXECUTE
- Ω₅: REVIEW

## 🔐 Protections (Ψ)
- PROTECTED (!cp) ... END-P
- GUARDED (!cg) ... END-G
- INFO (!ci) ... END-I
- DEBUG (!cd) ... END-D
- TEST (!ct) ... END-T
- CRITICAL (!cc) ... END-C

## 🧾 Permissions (ℙ)
- C: create, R: read, U: update, D: delete
- Mode defaults:
  - Ω₁: R ✓, C ✗, U ✗, D ✗
  - Ω₂: R ✓, C ~, U ✗, D ✗
  - Ω₃: R ✓, C ✓, U ~, D ✗
  - Ω₄: R ✓, C ✓, U ✓, D ~
  - Ω₅: R ✓, C ✗, U ✗, D ✗

## 🔗 Cross-References (χ)
- Standard: [↗️σ₁:R₁]
- With context: [↗️σ₁:R₁|Γ₃]
- Context only: [Γ₃:ClassA]
- Protection+Context: [Ψ₁+Γ₃:validate()]
- Permission+Context: [ℙ(Ω₁):read_only]

## 📎 Context Types (Γ)
- Γ₁: 📄 Files
- Γ₂: 📁 Folders
- Γ₃: 💻 Code
- Γ₄: 📚 Docs
- Γ₅: 📏 Rules
- Γ₆: 🔄 Git
- Γ₇: 📝 Notepads
- Γ₈: 📌 Pinned

## ⌨️ Context Commands (quick)
- !af file.md, !ad folder/, !ac CodeRef, !adoc DocRef
- !ag main, !ar rule, !an note, !pf file, !cs ref status
- !cr ref, !cc clear, !cm set for current mode

## 🚨 Violation Severity
- CRITICAL/HIGH → backup + safe transition
- MEDIUM/LOW → notify and log
