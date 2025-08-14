# WWW2026 Conference Website Maintenance Guide

This document summarizes the architecture and common maintenance tasks for the WWW2026 conference website.

## Repository Details
- GitHub: https://github.com/thewebconf2026/www2026

## Important Setup
1. Always configure git with: `git config user.name "thewebconf2026" && git config user.email "thewebconf2026@users.noreply.github.com"`
2. Always pull before making changes: `git pull origin main`
3. Use descriptive commit messages.
4. Test changes on the live site after deployment.

## Website Architecture
- **Modular Header System**: `components/header.html` loaded by `js/header-loader.js`
- **Modular Footer System**: `components/footer.html` loaded by `js/footer-loader.js`
- **Modular Dates System**: `data/important-dates.json` loaded by `js/dates-loader.js`
- **Main Pages**: `index.html`, `about.html`, `important-dates.html`, `calls.html`, `program.html`
- **Call Pages**: `calls/industry.html`, `calls/tutorials.html`, etc.

## Current Status
- Industry CFP: Complete and integrated
- Tutorial CFP: Complete and integrated
- Important dates: Centralized and modular
- Program: Shows "Coming Soon"
- Domain: Active at www2026.thewebconf.org

## Common Tasks
- **Adding new CFPs**: Create HTML in `calls/`, add dates to JSON, update navigation (`components/header.html`)
- **Updating dates**: Edit `data/important-dates.json` (auto-updates all pages)
- **Adding content**: Follow existing patterns and modular structure
- **Fixing issues**: Check modular components first


