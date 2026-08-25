# Emails-Klavio

Klaviyo email templates for use in Klaviyo flows and campaigns.

## Templates

The `templates/` directory contains ready-to-use transactional email templates,
vendored from [vendo-dev/klaviyo-email-templates](https://github.com/vendo-dev/klaviyo-email-templates)
(MIT licensed — see `templates/LICENSE`):

- `Abandoned_Cart.html`
- `Order_Cancelled.html`
- `Order_Completed.html`
- `Order_Fulfilled.html`
- `Package_shipped.html`
- `order_shipped.html`

To use one, import the HTML into a new email template in Klaviyo
(Content → Templates → Create Template → Import from HTML) and adjust
branding, copy, and merge fields (`{{ }}`) to fit your account.
