# Project Athena — Cloudflare Static Website

Put the public portfolio website inside `website/`.

Example:

website/
├── index.html
├── style.css
└── images/

Cloudflare Workers Builds settings:

- Git repository: `Fanu2/Project-Athena`
- Branch: `main`
- Build command: `exit 0`
- Deploy command: `npx wrangler deploy`
- Root directory: `/`

The supplied `wrangler.jsonc` publishes only `./website` as static assets.

If your existing landing page is currently at the repository root, move its
public files into `website/`. Keep application/source-code files outside
`website/`.

After committing to `main`, Cloudflare should automatically create a new
deployment.
