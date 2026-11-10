# Prompt for Claude in Chrome: update the 7-Day Reset flow in Klaviyo

Copy everything below the line into the Claude extension while logged in to Klaviyo.

---

You are updating an existing, live email flow in my Klaviyo account (SitComfort). Work carefully in the Klaviyo web app. Do not delete anything, do not touch any other flow, and do not change the flow's trigger. If something on screen doesn't match these instructions, stop and tell me instead of guessing.

## Goal

The flow "7-Day Reset Program New" currently sends 7 emails (Day 1 to Day 7). I want to:
1. Add a new welcome email (Day 0) at the very start.
2. Swap each of the 7 existing emails to a new coded template I've already created.
3. Update every email's subject line and preview text.
4. Make every wait step send the next email the following morning at 7:00 am.
5. Turn off UTM tracking parameters on every email.

## Step 0: Open the flow

1. Go to Flows: https://www.klaviyo.com/flows
2. Open **"7-Day Reset Program New"** (flow ID WWH762). Direct link: https://www.klaviyo.com/flow/WWH762/edit
   - Do NOT open "7-Day Reset Program" (without "New"). That one is an old draft.
3. Confirm the flow looks like this, top to bottom:
   Trigger "Delivered Shipment" → Email "Your Sitting Foundation" → Wait 1 day → Email "Setting Up Your Support" → Wait 1 day → Email "Screen, Desk & Keyboard Setup" → Wait 1 day → Email "Breaking the Slouch Habit" → Wait 1 day → Email "Move Better, Feel Better" → Wait 1 day → Email "Build Strength, Not Strain" → Wait 1 day → Email "Reset, Recover & Keep It Going".

## Step 1: Add the Day 0 welcome email at the top

1. Drag an **Email** action onto the canvas directly **below the trigger and above** the "Your Sitting Foundation" email.
2. Directly below that new email, and still above "Your Sitting Foundation", add a **Time Delay** of **1 day**. Set it as described in Step 3 (wait until 7:00 am).
3. Open the new email and set:
   - Email name: `Day 0 - Welcome`
   - Subject line: `Your SitComfort has arrived. Your 7-Day Reset starts tomorrow`
   - Preview text: `One short step and a short video each morning. Here's your week.`
   - Sender name: `SitComfort`, sender email: `info@sitcomfort.com.au` (same as the other emails)
   - Smart Sending: **OFF**
   - Add UTM tracking parameters: **OFF**
4. Set the content: choose the template **"7-Day Reset v2 - Day 0 Welcome"** (Templates → Saved templates, search "7-Day Reset v2"). Save.
5. Set this email's status to **Live** (same as the other emails). New emails in a live flow often start as Draft or Manual, so check this.

## Step 2: Update the 7 existing emails

For EACH row in this table, click the email in the flow, then:
- Click **Edit** on the content, choose **Change template** (or "Select a template"), go to **Saved templates**, search "7-Day Reset v2", pick the template in the table and confirm the replacement. Save.
- Update **Subject line** and **Preview text** exactly as in the table.
- In the email's settings, make sure **Smart Sending is OFF** and **Add UTM tracking parameters is OFF**.
- Keep the email **Live**.
- Optionally rename the email to the "New email name" column.

| Current email in flow | New template to select | New email name | Subject line | Preview text |
|---|---|---|---|---|
| Your Sitting Foundation | 7-Day Reset v2 - Day 1 | Day 1 - Your Sitting Foundation | Day 1 of 7: let's fix how you sit | Four small alignment checks that make everything else work. |
| Setting Up Your Support | 7-Day Reset v2 - Day 2 | Day 2 - Setting Up Your Support | Day 2 of 7: set up your support in 3 minutes | Where your cushion and lumbar support should actually sit. |
| Screen, Desk & Keyboard Setup | 7-Day Reset v2 - Day 3 | Day 3 - Screen, Desk & Keyboard | Day 3 of 7: your screen, desk and keyboard | Small workspace tweaks that stop you leaning forward. |
| Breaking the Slouch Habit | 7-Day Reset v2 - Day 4 | Day 4 - Breaking the Slouch Habit | Day 4 of 7: breaking the slouch habit | The 20-second reset that keeps you upright all day. |
| Move Better, Feel Better | 7-Day Reset v2 - Day 5 | Day 5 - Quick Desk Stretches | Day 5 of 7: quick desk stretches that release tension | Chest opener, chin tucks, hip flexor stretch and thoracic rotation, right at your desk. |
| Build Strength, Not Strain | 7-Day Reset v2 - Day 6 | Day 6 - Reset. Work. Move. | Day 6 of 7: reset, work, move (your daily routine) | How the whole week fits into one simple workday routine. |
| Reset, Recover & Keep It Going | 7-Day Reset v2 - Day 7 | Day 7 - 7 Days, One Simple System | Day 7 of 7: look how far you've come | Compare how you sat 7 days ago, and how to keep it going. |

Important: pick the templates whose names start with **"7-Day Reset v2"**. Do NOT pick any template whose name starts with "BACKUP old 7-Day Reset". Those are backups of the old designs.

## Step 3: Make every wait send at 7:00 am

There should now be 7 Time Delay steps (the new one after Day 0, plus the 6 existing ones). For EACH Time Delay:
1. Click it.
2. Keep the delay at **1 day**.
3. Turn on **"Delay until a specific time"** (or "Send at specific time") and set **7:00 AM**.
4. If there's a timezone option, choose the **recipient's / profile's local timezone**. If not, use Australia/Sydney.
5. Leave "delay until specific days of the week" off, so all days are allowed.
6. Save.

## Step 4: Check everything

1. The flow should now read, top to bottom:
   Trigger → Day 0 - Welcome → Wait 1 day @ 7am → Day 1 → Wait → Day 2 → Wait → Day 3 → Wait → Day 4 → Wait → Day 5 → Wait → Day 6 → Wait → Day 7.
2. All 8 emails show status **Live**. The flow itself is still **Live**.
3. Open each email's preview and confirm:
   - the header shows the right day (Day 0 "Welcome", then "Day 1 of 7" to "Day 7 of 7")
   - the green "Today's video" button is there (Day 0's button says "See the full 7-Day Reset" instead)
   - there's an "Unsubscribe" link at the bottom.
4. Send a test of **Day 0** and **Day 5** to **info@sitcomfort.com.au** with "Preview & test" → "Send test email".
5. Click **Save**, or **Update flow** if Klaviyo asks.

## Report back

When done, give me a short summary:
- what you changed, email by email
- the status of each email (Live / Draft / Manual)
- the delay setting on each wait step
- anything you couldn't do or weren't sure about.

Do not turn the flow off, archive it, or delete any email or template at any point.
