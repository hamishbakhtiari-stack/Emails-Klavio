# 7-Day Reset Program emails

One master template (`template.html`) plus per-day content (`content.json`) builds the
seven emails of the SitComfort 7-Day Reset Klaviyo flow.

## Edit and rebuild

1. Change copy, video IDs, links, signer or colours in `content.json`.
2. Run `python3 seven-day-reset/build.py`.
3. The emails are written to `dist/day-1.html` … `dist/day-7.html`.

## Put them in Klaviyo

1. Content → Templates → Create template → **Import HTML**, then paste or upload `dist/day-N.html`.
2. In the flow "7-Day Reset Program New", open each email, choose **Change template**, and pick the new one.
3. Copy the `subject` and `preview` for that day from `content.json` into the email's subject and preview text.

Klaviyo fills in these tags when it sends: `{{ first_name|default:'there' }}`, `{{ organization.name }}`,
`{{ organization.full_address }}`, `{% unsubscribe 'Unsubscribe' %}`.

## Recommended flow settings

- Sender: a program-specific sender, e.g. "Your SitComfort coach" `reset@sitcomfort.com.au`, with a monitored reply-to.
- Time delays: 1 day, then wait until 7:00 am in the profile's timezone.
- Turn off "Add tracking parameters" (UTMs) for this flow.
