# Task: read-only audit of Notes against the beginner ladder (NOTE-RULES §11) and step-by-step rule (§15)

Change nothing in the repo; no background agents. Read `docs/NOTE-RULES.md` in full first, especially §10, §11, §12, §15.

The user's complaints (examples of a class, §12):
- On a GMM Note: "do you really think it's friendly for a beginner? … There is no intuition no nothing, just directly math."
- On a chain-rule section: "You have not defined f and the inline math does not help… two products added, but you have not shown the products and then the addition. You cannot roll things into text like that… All notes need to be step and step and no inline math." "4.3 One picture of every shape makes no sense at all. Explanation is poor." "You keep using R^D etc but you don't explain the notation."

Read every Note on your list in full, with the eyes of a beginner with ADHD who has never seen the topic. For each numbered section and subsection record:
1. **Plain words first?** The first prose after the Key point explains the idea in everyday language, no formula, no undefined term (a Key point line alone does not count).
2. **Picture of the idea?** A figure or animation in or next to the section showing the idea itself (not just a formula's curve), and the text says what to see in it and why.
3. **Worked example before the formula?** The Note's own small numbers, step by step, before the general formula.
4. **Formal version with every symbol named?**
5. **§15 symbols:** every function, variable and notation (f, θ, ℝ^D, ∈, ∑, ∇, subscripts) defined at first use with a concrete value or instance. List each symbol used before it is defined.
6. **§15 steps:** every calculation shown one step per display line or table row (products on their lines, then the sum). List each place where maths is rolled into a sentence ("add the two products…") or inline maths carries the reasoning.
For the Note as a whole: starts from something visible before any symbol; a running example; an analogy; concrete-to-abstract order.

Score each Note: **PASS** (every section passes 1–6), **WEAK** (some sections fail), **FAIL** (organised like a textbook chapter, or §15 failures throughout). Be strict and honest; do not grade on length or figure count. Practical Notes (library usage, pipelines, Keras recipes) are judged the same way.

Write the audit to the file named in your task: a summary at the top (counts per score; the 10 worst Notes with one line each), then a table: Note | score | failing sections and what is missing (one line each, naming the exact symbols and sentences for 5 and 6). Report the summary as text.
