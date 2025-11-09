# CodeQL Configuration Fix

## Issue
CodeQL analyses from advanced configurations cannot be processed when the default setup is enabled.

## Solution
Disabled GitHub's default CodeQL setup to allow custom security workflows.

## Changes Made
- Disabled default CodeQL setup via GitHub API
- Custom security.yml workflow now works without conflicts

## Date
$(date)# Updated Sun Nov  9 12:49:45 CET 2025
# Updated Sun Nov  9 12:52:32 CET 2025
# Updated Sun Nov  9 12:56:17 CET 2025
