# WWW2026 Website Automatic Deployment Configuration

## Overview

This repository is configured with GitHub Actions for automatic deployment. When you push code to the `main` branch, the website will be automatically updated.

## How to Enable Automatic Deployment

### 1. Enable GitHub Pages

1. Go to your GitHub repository page: `https://github.com/thewebconf2026/www2026`
2. Click the **Settings** tab
3. Find the **Pages** option in the left-hand menu
4. In the **Source** section, select **GitHub Actions**
5. Click **Save** to apply the settings

### 2. Verify Deployment

After enabling GitHub Pages, your website will be accessible at:
- `https://thewebconf2026.github.io/www2026/`

## Automatic Deployment Workflow

1. **Trigger Condition**: When you push code to the `main` branch
2. **Build Process**: GitHub Actions will automatically build the website
3. **Deployment Process**: Automatically deploys to GitHub Pages after the build is complete

## How to Update the Website

1. **Edit directly on GitHub web interface**:
   - Navigate to the file you want to edit in your GitHub repository
   - Click the filename to open the file
   - Click the edit button (pencil icon)
   - Make your changes, then fill in the commit message at the bottom of the page
   - Click **Commit changes** to submit

2. **Edit locally and push**:
   ```bash
   # Clone the repository (if you haven\'t already)
   git clone https://github.com/thewebconf2026/www2026.git
   cd www2026
   
   # Make your changes...
   
   # Commit and push
   git add .
   git commit -m "Update website content"
   git push origin main
   ```

3. **Automatic Deployment**:
   - After pushing, GitHub Actions will run automatically
   - You can view the deployment progress in the **Actions** tab of your repository
   - Once deployed, the website will automatically update

## Frequently Asked Questions

### Q: How to check deployment status?
A: On your GitHub repository page, click the **Actions** tab to see all deployment run records.

### Q: What if deployment fails?
A: Click on the failed run record in the **Actions** page to view the error logs. Common issues include:
- HTML syntax errors
- Incorrect file paths
- Overly large image files

### Q: How long does it take for the website to update?
A: Deployment usually completes within 2-5 minutes after pushing code.

## File Structure Explanation

```
www2026/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment configuration
├── css/                        # Stylesheet files
├── js/                         # JavaScript files
├── images/                     # Image assets
├── data/                       # Data files
├── index.html                  # Homepage
├── about.html                  # About page
├── calls.html                  # Calls page
├── program.html                # Program page
├── attending.html              # Attending page
└── README-DEPLOYMENT.md        # This document
```

## Technical Support

If you encounter any issues during use, please:
1. Check the GitHub Actions run logs
2. Confirm file paths and syntax are correct
3. Contact the technical support team


