# Phalom Discord server blueprint

A starting setup for a small team developing Sabaidee Merchant for the Innovative Business Challenge. Channel names and messages below are ready to copy. Start with these channels and add more when the team needs them.

## 1. Server identity

**Server name:** Phalom | Sabaidee Merchant

**Short description:** Our team workspace for building Sabaidee Merchant: ideas, research, tasks, decisions, and pitch preparation.

**Icon idea:** A simple P on a teal background. Use the team logo if one already exists.

**Language:** Lao or English, whichever helps the author explain clearly. Summarize key decisions in the language everyone on the team understands.

## 2. Channel structure

```text
START HERE
  #welcome
  #announcements
  #project-overview

TEAM SPACE
  #general
  #ideas
  #research

PROJECT WORK
  #tasks
  #product-and-demo
  #business-and-pitch
  #decisions-and-notes

VOICE
  Team Room
  Focus Room
```

### START HERE

| Channel | Copy this channel topic | Posting approach |
| --- | --- | --- |
| #welcome | Start here: team introductions, working agreements, and where to post. | Everyone can introduce themselves. Pin the welcome message. |
| #announcements | Confirmed deadlines, meeting schedules, and important team updates. | Leads post; discussion goes in a thread. |
| #project-overview | The current project brief, scope, milestones, and links to our latest materials. | Leads maintain the main post; members suggest changes in a thread. |

### TEAM SPACE

| Channel | Copy this channel topic | How to use it |
| --- | --- | --- |
| #general | Daily conversation, quick questions, progress updates, and team support. | Anything that does not need a dedicated work discussion. |
| #ideas | Rough ideas are welcome. One idea per message; discuss it in a thread. | Use the idea template below when useful. |
| #research | Merchant insights, competition, payment partners, sources, and assumptions to test. | Include a source or label the statement as an assumption. |

### PROJECT WORK

| Channel | Copy this channel topic | How to use it |
| --- | --- | --- |
| #tasks | Agreed work with one owner, a due date, and a clear result. | One task per message; updates and deliverables in its thread. |
| #product-and-demo | Merchant experience, payment flows, interface designs, and concept demos. | Share screenshots, sketches, feedback, and demo links. |
| #business-and-pitch | Business model, costs, partners, slides, pitch script, and rehearsal feedback. | Keep assumptions visible in financial and partner claims. |
| #decisions-and-notes | Meeting notes and agreed decisions, with owners and next actions. | Record the outcome here; link to the original discussion. |

### VOICE

- **Team Room:** meetings, brainstorming, and pitch practice.
- **Focus Room:** quiet coworking and short working sessions.

## 3. Roles and access

Keep the role structure small. Track responsibilities in the project overview rather than creating a role for every job.

| Role | Who gets it | Intended access |
| --- | --- | --- |
| Server Owner | The person accountable for the server | Ownership and server administration. |
| Team Lead | One or two people coordinating the project | Manage channels and messages, maintain reference posts, and post announcements. Grant only the management permissions they need. |
| Team Member | Everyone working on the project | Read team channels, post and reply in work channels, share files, and join voice rooms. |
| Guest / Mentor | An invited reviewer or advisor | Only explicitly selected channels. Allow posting where feedback is wanted. |

**Access setup:** Keep project categories private by default. Give Team Lead and Team Member access to them. Give Guest / Mentor access only to the specific channels needed for a review. Verify access with a guest role before inviting an outside reviewer.

**Announcements:** Allow members to read and discuss announcements in threads; reserve new announcement posts for leads. Configure available thread permissions to match that arrangement.

**Invitations:** Let the owner and leads handle team invitations.

## 4. Ready-to-copy welcome message

Post this in **#welcome** and pin it:

```text
Welcome to Phalom! 👋

This is our shared workspace for Sabaidee Merchant and the Innovative Business Challenge.

We use this server to share ideas, test assumptions, organize work, and prepare our pitch together.

START HERE
1. Read #project-overview.
2. Introduce yourself below.
3. Check #tasks for current work.

INTRODUCE YOURSELF
Name / nickname:
What you enjoy or can help with:
What you want to work on:
Usual availability:

WHERE TO POST
Quick question or casual chat → #general
New idea → #ideas
Evidence or competitor insight → #research
Work to complete → #tasks
App, user experience, or demo → #product-and-demo
Business model or pitch → #business-and-pitch
Agreed decision or meeting notes → #decisions-and-notes

HOW WE WORK
• Rough ideas are welcome. You do not need a polished proposal.
• Keep replies about one topic in its thread.
• Challenge the idea respectfully and explain your reasoning.
• Label assumptions so we know what still needs checking.
• Every agreed task needs one owner and a clear result.
• If you are stuck or cannot meet a deadline, tell the team early.
• Use @everyone only for an urgent update affecting the whole team.

Lao and English are both welcome. Clarity matters more than perfect wording.
```

## 5. Ready-to-copy project overview

Post this in **#project-overview** and pin it. Replace bracketed fields before inviting the team.

```text
SABAIDEE MERCHANT — PROJECT OVERVIEW

TEAM
Phalom

CHALLENGE
Innovative Business Challenge

WHAT WE ARE EXPLORING
A merchant payment-management service for street-food and souvenir shops in Lao tourist areas.

Tourists would pay using supported wallets or bank apps they already use. Merchants would see fees, net LAK proceeds, and expected payout timing, with Lao audio alerts based on verified transaction results.

CURRENT STAGE
Pitch concept and concept demo.
Payment integrations, partner agreements, pricing, and pilot results still need validation.

OUR CURRENT FOCUS
1. Understand the merchant problem.
2. Explain why merchants would choose us.
3. Validate the payment route and business economics.
4. Build a clear demo and convincing pitch.

LATEST MATERIALS
Team brief: [upload PDF or add a shared link]
Interactive concept brief: [attach HTML or add an accessible hosted link]
Competition requirements: [upload source PDFs or add shared links]
Slides: [add link when ready]

PEOPLE AND RESPONSIBILITIES
Coordinator: [name]
Merchant research: [name]
Product / demo: [name]
Business model / partners: [name]
Pitch / design: [name]
One person can cover more than one area.

NEXT MILESTONE
Deliverable: [specific result]
Due: [date and time, ICT / UTC+7]
Owner: [name]

OPEN QUESTIONS
• Which merchant problem is most painful and frequent?
• Which payment routes can a partner actually support?
• What do small transactions cost to serve?
• What evidence would make our pitch credible?

Last updated: [date]
```

## 6. Copy-and-paste working templates

### Idea — #ideas

```text
IDEA: [short title]
Problem / opportunity:
My suggestion:
Who benefits and how:
What we would need to check:
Feedback wanted:
```

### Research — #research

```text
FINDING: [short title]
What I found:
Source / interview reference:
Source date and date checked:
Why it matters:
What remains uncertain:
Suggested next action:
```

For merchant interviews, summarize the relevant insight and use a merchant code if names are unnecessary.

### Task — #tasks

```text
[TODO] [short task title]
Owner: @name
Due: [date and time, ICT / UTC+7]
Expected result:
Done when:
Depends on:
Deliverable / discussion link:
```

The task owner edits the first line as work changes:

```text
[TODO] → [DOING] → [REVIEW] → [DONE]
Use [BLOCKED] when a dependency prevents progress.
```

Keep progress updates in the task thread. When blocked, explain what is needed and who can help. The reviewer confirms that the “Done when” condition is met.

### Decision — #decisions-and-notes

```text
DECISION: [short title]
Date:
Status: Agreed / Provisional
Decision:
Reason and supporting evidence:
Agreed by:
What could make us revisit this:
Next action + owner:
Discussion link:
```

### Meeting notes — #decisions-and-notes

```text
MEETING: [topic]
Date and time: [ICT / UTC+7]
Attendees:
Main points:
Decisions:
Tasks + owners + due dates:
Open questions:
Next check-in:
```

## 7. A simple team rhythm

- **Start of week:** Each person posts their main commitment in #general and links the relevant task.
- **During the week:** Share progress when something changes. Raise blockers promptly.
- **Weekly team meeting:** Aim for 30 minutes: progress, blockers, decisions, and next commitments. Extend it when a work session is needed.
- **After a meeting:** One person posts notes and creates or updates agreed tasks.
- **Before a submission:** Review the current pitch against competition requirements, assign final checks, and confirm the submission owner.

An emoji reaction can show support for an idea. A decision becomes official when the team records it in #decisions-and-notes.

## 8. Suggested first tasks

These are proposed starting tasks, not existing commitments. Agree owners and dates together.

| Task | Done when |
| --- | --- |
| Confirm competition requirements | Submission format, deadline, judging criteria, and required materials are summarized from the competition documents. |
| Agree team responsibilities | Every active member has an agreed area of responsibility and availability recorded in the overview. |
| Prepare merchant interviews | The team agrees a short question list, target merchant types, and who will conduct interviews. |
| Review competitor evidence | Key comparisons have source links and dates, with unknowns marked clearly. |
| Write the core value proposition | The team agrees one clear sentence describing the customer, problem, and benefit. |
| Review partner feasibility | Required payment capabilities and unanswered partner questions are documented. |
| Review the concept demo | The payment flow is understandable, and simulated behavior is labeled. |
| Prepare the pitch outline | The story covers the problem, solution, difference, business model, evidence, and next step. |

## 9. Build and launch sequence

1. Create the server and set its name and icon.
2. Create roles and configure category access.
3. Create the categories and channels shown above; add their topics.
4. Configure announcement posting and guest access.
5. Post and pin the welcome message and project overview.
6. Add a pinned template message in #ideas, #research, #tasks, and #decisions-and-notes.
7. Upload the current brief and competition documents; put their Discord message links in the overview. Use shared online links for materials the team edits together. Local computer paths will not work for teammates.
8. Seed the first agreed tasks with owners and dates.
9. Invite teammates and assign their roles.
10. Hold a short kickoff to confirm the next milestone and responsibilities.

Launch without bots. Add automation later when the team has a specific recurring need.

## 10. First announcement

```text
Our Phalom project server is ready! 🚀

Please introduce yourself in #welcome and read #project-overview.

For our kickoff, we will confirm:
• Competition requirements and the next deadline
• Each person's responsibilities
• Our first milestone
• The questions we need to validate for Sabaidee Merchant

Kickoff: [date and time, ICT / UTC+7]
Location: Team Room

Before the meeting, bring one question, idea, or concern about the project. Post it in #ideas or #general so we can prepare.
```
