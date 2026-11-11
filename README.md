# Rabin ERPNext Theme

A custom Frappe app that applies a modern-minimal visual layer to the Frappe Desk,
with Persian typography and RTL-aware CSS. It does not patch Frappe or ERPNext core.

## Target environment

- Frappe Framework: v16 (`version-16`)
- ERPNext: v16 (`version-16`)
- Current tested-by-user environment at package preparation: Frappe 16.55.2,
  ERPNext 16.54.0, Python 3.14.10
- Docker deployment: `frappe_docker` layered image

The app declares a Frappe 16 dependency range. It has not been runtime-tested in
your instance; use the verification checklist below after installing it.

## Features in this starter implementation

- Desk-wide Yekan font stack with local WOFF2 assets
- Modern visual treatment for navbar, sidebar, page header, cards, forms,
  controls, buttons, lists, dropdowns and dialogs
- Semantic Frappe color tokens with fallbacks, preserving native light/dark theme
- RTL-aware logical layout rules; does not hard-code `dir="rtl"`
- LTR handling for email, URL, telephone, numeric and technical values
- No database schema, patches, permission changes or business logic

## Font files

Font binaries are not included. Add licensed files to:

`rabin_theme/public/fonts/`

Expected names:

- `Yekan-Regular.woff2`
- `Yekan-Medium.woff2`
- `Yekan-Bold.woff2`

If your Yekan package has different filenames or is a variable font, update the
`@font-face` declarations in `rabin_theme/public/css/rabin_theme.css` accordingly.
Do not commit font files unless your font license permits redistribution in the
repository and Docker image.

## RTL requirement

Set the user's Frappe language to Persian. Frappe is responsible for rendering
its document with the correct direction and loading its RTL styles. This app
adds targeted RTL refinements but does not force the whole document direction.

## Install in a Docker image

The recommended deployment path for `frappe_docker` is to include this app in
`apps.json`, build a new immutable image, and recreate the application services.
Do not edit files inside a running container as the only source of truth.

1. Push this repository to a Git remote accessible by the Docker build machine.
2. Add the repository to the existing `apps.json` (see `docs/apps-json.example`).
   Keep the ERPNext and Persian Calendar entries already present.
3. Build a new image using the same Frappe v16 base/build branch and BuildKit secret
   used by your existing setup. Example:

   ```powershell
   docker build `
     --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe `
     --build-arg=FRAPPE_BRANCH=version-16 `
     --build-arg=CACHE_BUST=rabin-theme-v1 `
     --secret=id=apps_json,src=apps.json `
     --tag=erpnext-rabin-theme:16 `
     --file=images/layered/Containerfile .
   ```

4. In `pwd.yml`, change only the ERPNext application image references to
   `erpnext-rabin-theme:16`. Keep MariaDB, Redis, ports and existing named volumes.
5. Recreate the application containers:

   ```powershell
   docker compose -f pwd.yml up -d --force-recreate
   ```

6. Install the app on the existing site (the default `pwd.yml` site is usually
   `frontend`; verify with `bench list-sites`):

   ```powershell
   docker compose -f pwd.yml exec backend bench --site frontend install-app rabin_theme
   docker compose -f pwd.yml exec backend bench build --app rabin_theme
   docker compose -f pwd.yml exec backend bench --site frontend clear-cache
   docker compose -f pwd.yml restart backend frontend websocket queue-long queue-short scheduler
   ```

7. Open Desk and hard-refresh the browser (`Ctrl+Shift+R`).

Important:
- Never run `docker compose down -v` when you need to retain site data.
- Keep the previous working image tag for rollback.
- `version-16` is a moving branch. For a reproducible release, pin Frappe,
  ERPNext, Persian Calendar and this app to reviewed commit SHAs/tags in your
  build process rather than silently following branch heads.
- Private Git remotes require credentials configured for the Docker BuildKit
  build; do not put personal access tokens in a committed `apps.json`.

## Verification checklist

1. `bench --site frontend list-apps` includes `rabin_theme`.
2. Browser DevTools → Network shows HTTP 200 for:
   - `/assets/rabin_theme/css/rabin_theme.css`
   - `/assets/rabin_theme/css/rabin_rtl.css`
   - `/assets/rabin_theme/fonts/Yekan-Regular.woff2`
3. Browser DevTools → Elements shows `html[dir="rtl"]` for a Persian-language user.
4. Check Workspace, List, Form, child table, report, dialogs, dropdowns,
   notifications, numeric fields, email and URL fields.
5. Repeat the checks in Dark mode and at a narrow viewport.

## Rollback

Set the previous application image tag back in `pwd.yml`, then run
`docker compose -f pwd.yml up -d --force-recreate`. If the app itself must be
removed from the site, take a database backup first and use the supported
`bench uninstall-app` flow; do not manually delete app folders from a live site.

## Customization

- Color and radius tokens: `rabin_theme/public/css/rabin_theme.css`
- RTL-specific refinements: `rabin_theme/public/css/rabin_rtl.css`
- Asset inclusion: `rabin_theme/hooks.py`
