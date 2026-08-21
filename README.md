# PLSC 508 Fall 2026 — presentation sign-ups

Two separate sign-ups:

- **[METHODS.md](METHODS.md)** — Methods Tutorial sign-up sheet
- **[READINGS.md](READINGS.md)** — Application Reading Review sign-up sheet

Each week has two slots per sheet. Sign up for a second slot (Slot 2) only if Slot 1 on the respective day is already full; the claim bot enforces this by always filling Slot 1 first. For a reading review, state which reading you are reviewing in the claim form. Claims are processed automatically, first come first served.

## Manual edits (instructor)

The sheets are plain Markdown tables and can be edited directly (on GitHub: open METHODS.md or READINGS.md, click the pencil icon, commit). The bot never rewrites the whole sheet; it only fills the single cell being claimed, so manual edits are preserved. Rules the bot relies on:

- Keep the table structure intact (the `|` separators and the `| MM/DD | Topic | ... |` row format).
- A cell containing exactly `OPEN` is claimable; any other text counts as taken.
- To assign a student by hand, replace `OPEN` with their name. To clear an assignment, replace it with `OPEN`.
