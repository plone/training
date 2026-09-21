---
myst:
  html_meta:
    "description": "Site setup"
    "property=og:description": "Options in the standard control panel"
    "property=og:title": "Site setup"
    "keywords": "Site setup"
---

# Plone 6.1+ Site Setup (Control Panel) – Training & Documentation

## Overview

The **Site Setup** (also called "Control Panel") is the central administration interface in Plone where site managers and advanced editors can configure and customize the Plone site. It is accessible to users with the **Manager** role through the gear icon at the bottom left of the Plone interface.

> **Note:** Some control panels are available in both Volto (frontend) and Classic UI (backend). This outline focuses on the **Classic UI**, which provides access to all available configuration options.

Access path: `http://localhost:8080/Plone/@@overview-controlpanel`

---

## Table of Contents

1. [General Configuration](#general-configuration)
2. [Content Management](#content-management)
3. [Users & Groups](#users--groups)
4. [Security & Permissions](#security--permissions)
5. [Advanced Settings](#advanced-settings)
6. [Add-ons Management](#add-ons-management)

---

## General Configuration

Settings that affect the overall site behavior and presentation.

### Site

**Purpose:** Configure basic site properties and metadata.

**Key Settings:**
- **Site Title** – The name of your Plone site (appears in page titles and headers)
- **Site Subtitle** – A tagline or short description of the site
- **Site Logo** – Upload a logo image for the site
- **Default Page** – Set a custom page to display as the site home
- **Enable Self Registration** – Allow anonymous users to create accounts
  - Options: Enabled / Disabled
- **Email Validation Required** – Require email confirmation for new accounts
  - Options: Enabled / Disabled
- **Allow Members to Change Their Own Email** – Users can modify their email address
  - Options: Enabled / Disabled
- **Allow Members to Request Password Resets** – Enable "Forgot Password" functionality
  - Options: Enabled / Disabled

### Date and Time

**Purpose:** Set timezone, date formats, and time-related settings.

**Key Settings:**
- **Timezone** – Select the default timezone for content creation and display
  - Options: List of available timezones (e.g., UTC, Europe/Brussels, America/New_York)
- **Date Format** – Define how dates are displayed throughout the site
  - Common formats: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD
- **Include Time Zone Info** – Show timezone abbreviation in timestamp displays
  - Options: Yes / No

### Language

**Purpose:** Configure language settings and multilingual support.

**Key Settings:**
- **Available Languages** – Choose which languages are available on the site
  - Options: Checkboxes for each supported language (English, German, French, Spanish, etc.)
- **Default Language** – Set the default language for new content
  - Options: Dropdown list of available languages
- **Allow Automatic Language Selection** – Detect user's browser language
  - Options: Enabled / Disabled
- **Use Content Negotiation** – Automatically serve content in the user's preferred language
  - Options: Enabled / Disabled

### Navigation

**Purpose:** Configure site navigation and menu structure.

**Key Settings:**
- **Generate Automatically** – Auto-generate navigation from folder structure
  - Options: Enabled / Disabled
- **Root Depth** – How many levels to include in automatic navigation
- **Tab Depth** – How deep to display dropdown menus
- **Exclude from Navigation** – Hide specific content types from menus
- **Show Non-Viewable Items** – Display items user doesn't have permission to view
  - Options: Yes / No

### Search

**Purpose:** Configure search functionality and indexing behavior.

**Key Settings:**
- **Enable Live Search** – Show instant search suggestions as user types
  - Options: Enabled / Disabled
- **Live Search Results Limit** – Number of suggestions to display
  - Common values: 5, 10, 15, 20
- **Indexes to Include** – Choose which content fields are searchable
  - Options: Title, Description, Body, Keywords, etc. (checkboxes)
- **Results Per Page** – How many search results to show on each page
  - Default: 25
- **Enable Simple Search** – Allow basic keyword search (vs. advanced search)
  - Options: Enabled / Disabled

### Mail

**Purpose:** Configure email settings for notifications and messaging.

**Key Settings:**
- **SMTP Server** – Address of outgoing mail server
  - Example: smtp.gmail.com
- **SMTP Port** – Port number for SMTP connection
  - Default: 25 (standard), 587 (TLS), 465 (SSL)
- **SMTP Username** – Username for SMTP authentication
- **SMTP Password** – Password for SMTP authentication
- **SMTP Connection Security** – Encryption method
  - Options: None / TLS / SSL
- **Site E-mail Address** – From address for automated emails
  - Example: noreply@example.com
- **Send Password Reset E-mail** – Allow password reset emails
  - Options: Enabled / Disabled
- **Enable User Folders** – Create personal folders for each user
  - Options: Enabled / Disabled

### URL Management

**Purpose:** Configure URL rewriting and site accessibility settings.

**Key Settings:**
- **Pretty URLs** – Use clean URLs without .html extensions
  - Options: Enabled / Disabled
- **Assume URL Rewriting** – Assume web server handles URL rewriting
  - Options: Yes / No
- **Virtual Hosting** – Configure virtual hosting paths
- **Canonical URL** – Set the preferred domain/protocol for the site
  - Example: https://example.com

### Database

**Purpose:** View database connection information and status.

**Key Information:**
- **Database Type** – Type of database in use (e.g., FileStorage, RelStorage)
- **Database Size** – Current size of the database
- **Connection Status** – Whether database is connected and healthy
- **Last Pack** – Date/time of last database optimization
- **Pack Database** – Manual database optimization button
  - Use to reclaim space from deleted content

### Undo

**Purpose:** Configure undo/transaction settings.

**Key Settings:**
- **Enable Undo** – Allow users to undo changes
  - Options: Enabled / Disabled
- **Keep Undo Transactions** – Number of transactions to keep for undo
  - Default: 30
- **Undo Limit (Days)** – Maximum age of transactions available for undo
  - Default: 7 days

### Volto Settings

**Purpose:** Configure frontend (Volto) specific options when using React-based frontend.

**Key Settings:**
- **Volto Instance URL** – URL of the Volto frontend
  - Example: http://localhost:3000
- **Edit URL** – Path for edit mode in Volto
- **API Endpoint** – URL of the API that Volto should use
- **OAuth Settings** – Configure OAuth for Volto authentication
- **Allowed CORS Origins** – Domains allowed to access the API
  - Example: https://example.com, https://www.example.com

### Add-ons

**Purpose:** Manage and view installed add-on packages.

**Key Settings:**
- **Installed Add-ons** – List of currently installed packages
- **Available Add-ons** – List of available (but not yet installed) add-ons
- **Install** – Install a new add-on package
- **Uninstall** – Remove an installed add-on
- **Upgrade** – Update an add-on to a newer version
- **Activate/Deactivate** – Enable or disable add-on features

---

## Content Management

Settings related to content types, creation, editing, and display.

### Content Types

**Purpose:** Manage content type definitions and their properties.

**Key Actions:**
- **View Content Types** – List all available content types
- **Add Content Type** – Create a new custom content type
- **Edit Content Type** – Modify existing content type definition
  - Configure fields
  - Set default values
  - Manage behaviors/mixins
  - Configure security/workflow
- **Delete Content Type** – Remove a custom content type
- **Export/Import** – Export content type definitions for backup/migration

**Content Type Properties:**
- **Title** – Display name of the content type
- **Description** – Purpose and usage of this content type
- **Icon** – Image representation in menus
- **Allowed Content Types** – What content can be created inside this type
- **Default View** – Template used to display the content
- **Automatically Added Fields** – Standard fields included in all instances
- **Workflow** – Transition states available for this type

### Editing

**Purpose:** Configure content editing interface and behavior.

**Key Settings:**
- **Enable Inline Editing** – Allow editing content directly on the page
  - Options: Enabled / Disabled
- **Rich Text Editor** – Choose default HTML editor
  - Options: TinyMCE, CKEditor, or other configured editors
- **Markup Language** – Default text format for body fields
  - Options: HTML, Markdown, Structured Text, Plain Text
- **Link Types** – Allow different types of links in content
  - Options: Internal links, External links, Email links, Anchors
- **Enable Auto-Save** – Save content automatically while editing
  - Options: Enabled / Disabled
- **Auto-Save Interval** – How often to save (in seconds)
  - Default: 60
- **Show Deactivated Content Types** – Display inactive content types in creation menu
  - Options: Yes / No

### Image Handling

**Purpose:** Configure image processing and display settings.

**Key Settings:**
- **Allowed Image Types** – File formats users can upload
  - Options: JPEG, PNG, GIF, TIFF, BMP (checkboxes)
- **Maximum Image Size** – Max file size in bytes
  - Example: 5242880 (5 MB)
- **Image Scaling** – Automatically resize large images
  - Options: Enabled / Disabled
- **Thumbnail Size** – Default thumbnail dimensions
  - Default: 128x128 pixels
- **Image Variants** – Create multiple sizes automatically
  - Example: Small (200px), Medium (400px), Large (800px)
- **Quality/Compression** – JPEG compression level
  - Scale: 1-100 (higher = better quality, larger files)
- **Auto Thumbnail Generation** – Create thumbnails on upload
  - Options: Enabled / Disabled

### Block Types

**Purpose:** Configure available content blocks in Volto frontend.

**Key Actions:**
- **Available Blocks** – List of block types that can be added
  - Text, Image, Video, Grid, Listing, Search, Maps, etc.
- **Required Blocks** – Blocks that must appear in certain content types
- **Restricted Blocks** – Limit which blocks certain user roles can use
- **Block Settings** – Configure defaults for each block type
  - Size limits, preview options, allowed formats

### Relations

**Purpose:** Configure how content items can be related to each other.

**Key Settings:**
- **Available Relation Types** – Define custom relationship types
  - Example: "Related To", "Requires", "References"
- **Bidirectional Relations** – Automatically create reverse links
  - Options: Enabled / Disabled
- **Allow User Relations** – Let content editors create custom relations
  - Options: Enabled / Disabled
- **Display Relations** – Show relation links on content view
  - Options: Always, Never, Editor's choice

### Content Rules

**Purpose:** Create automated actions triggered by content events.

**Key Features:**
- **Trigger Events** – What action starts the rule
  - Options: Workflow transition, Content added, Content modified, State changed
- **Conditions** – Requirements that must be met
  - Examples: Content type is "News Item", User has role "Reviewer"
- **Actions** – What happens when rule is triggered
  - Examples: Send email, Move to folder, Change workflow state, Assign permissions
- **Rule Management** – Enable/disable, edit, delete, test rules

---

## Users & Groups

Settings for user management, authentication, and permissions.

### Users

**Purpose:** Manage individual user accounts on the site.

**Key Actions:**
- **Add User** – Create new user account
  - Set username, password, email
- **Edit User** – Modify existing user properties
  - Change password, email, full name
  - Add/remove roles
  - Assign to groups
- **Delete User** – Remove user account (content usually preserved)
- **Reset Password** – Force user to change password on next login
- **Lock/Unlock User** – Temporarily disable account without deleting
- **View User Properties:**
  - Username
  - Email
  - Full Name
  - Roles (Site Managers, Editors, Reviewers, etc.)
  - Groups (assigned group memberships)
  - Last Login
  - Account Created Date

### Groups

**Purpose:** Organize users into groups for easier permission management.

**Key Actions:**
- **Create Group** – Create new user group
- **Edit Group** – Modify group properties
  - Name, description, members
- **Delete Group** – Remove group (members retain other permissions)
- **Assign Members** – Add/remove users from group
- **Set Group Roles** – Assign roles to entire group
  - Example: Make group "Reviewers" → All members get Reviewer role

**Common Group Types:**
- Editors – Can create/edit content
- Reviewers – Can approve content for publishing
- Contributors – Can add content but not publish
- Translators – Can translate content to other languages

### User Group Membership

**Purpose:** Manage which groups individual users belong to.

**Key Features:**
- **View Group Membership** – See all groups a user is in
- **Add User to Group** – Make user a member of a group
- **Remove User from Group** – Remove group membership
- **Bulk Operations** – Add multiple users to group at once
- **Import Users** – Import user list from file (CSV, LDAP, etc.)

### User and Group Settings

**Purpose:** Configure default user and group behavior.

**Key Settings:**
- **Allow User Folders** – Create personal folders for each user
  - Options: Enabled / Disabled
- **User Folder Path** – Where user folders are created
  - Default: /Users
- **User Folder Template** – Template for new user folders
- **Enable Self Registration** – Allow anonymous users to create accounts
  - Options: Enabled / Disabled
- **Auto-Approve Registration** – Approve accounts automatically
  - Options: Enabled / Disabled (if disabled, admin must approve)
- **Require Email Verification** – Confirm email before account activation
  - Options: Enabled / Disabled
- **Member Registration** – Allow members to create groups
  - Options: Enabled / Disabled

---

## Security & Permissions

Settings related to access control, authentication, and data protection.

### Security

**Purpose:** Configure security policies and access control.

**Key Settings:**
- **Enable HTTPS/SSL** – Force encrypted connections
  - Options: Enabled / Disabled
- **Require HTTPS** – Redirect HTTP to HTTPS
  - Options: Enabled / Disabled
- **Session Timeout** – How long before user is logged out due to inactivity
  - Default: 24 hours
  - Values in minutes or "never"
- **Authentication Method** – How users log in
  - Options: Standard (username/password), LDAP, OAuth, CAS, SAML
- **Password Policy:**
  - Minimum length (default: 5 characters)
  - Require uppercase/lowercase/numbers/special characters
  - Password expiration period
  - Prevent reuse of recent passwords
  - Force password change on first login
- **Account Lockout** – Lock accounts after failed login attempts
  - Number of failures: 3, 5, 10 (configurable)
  - Lockout duration: 15, 30, 60 minutes (configurable)
- **CORS Settings** – Allow cross-origin requests for APIs
  - Allowed domains/origins list
- **API Token Settings** – Configure access tokens for API authentication
  - Token expiration
  - Token revocation

### Permissions Management

**Purpose:** Control what different user roles can do.

**Key Concepts:**
- **Global Roles** – Assigned to all content
  - Manager, Owner, Reviewer, Editor, Contributor, Member, Anonymous
- **Local Roles** – Assigned per content item
  - Can grant role to user/group on specific folder/page
- **Role Definitions** – What permissions each role has
  - Can add/edit content, publish, delete, manage users, etc.

**Key Actions:**
- **View Role Permissions** – See what each role can do
- **Add Local Role** – Grant role to user/group on specific content
- **Remove Local Role** – Revoke role from user/group
- **Inherit Permissions** – Set whether subfolder inherits parent permissions
  - Options: Yes / No / Custom

### HTML Filtering

**Purpose:** Control what HTML tags and attributes are allowed in content.

**Key Settings:**
- **Allowed Tags** – HTML elements users can include in content
  - Common: p, div, span, a, img, strong, em, h1-h6, ul, ol, li
  - Restricted by default: script, iframe, form, etc.
- **Allowed Attributes** – Attributes allowed on tags
  - Example: href, src, alt, class, id
- **Filtering Behavior:**
  - Strip all HTML except safe tags
  - Allow user HTML tags but filter dangerous ones
  - Disable filtering (not recommended)
- **Custom Filters** – Create rules for specific content types

### Errors

**Purpose:** Configure error logging and reporting.

**Key Settings:**
- **Error Logging Level** – How verbose to be
  - Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log to File** – Write errors to disk
  - Options: Enabled / Disabled
- **Log File Location** – Path where error logs are stored
- **Email Admin on Errors** – Send notification when errors occur
  - Options: Enabled / Disabled
- **Error Email Recipients** – Who receives error notifications
- **Clear Old Logs** – Auto-delete old log files after N days
- **Error Page Display** – What users see when errors occur
  - Options: Full error details, Generic message, Custom page

---

## Advanced Settings

Configuration options for experienced administrators.

### Caching

**Purpose:** Optimize site performance through caching.

**Key Settings:**
- **Enable Page Caching** – Cache generated HTML pages
  - Options: Enabled / Disabled
- **Cache Duration** – How long to keep cached pages (in seconds)
  - Default: 3600 (1 hour)
- **Cache Invalidation Rules** – When cache is cleared
  - On content creation, modification, workflow transition
- **Purge Cache** – Manually clear all cached content
- **Cache Backend** – Where cache is stored
  - Options: Memory, File, Memcached, Redis
- **Exclude from Caching** – Content types/paths never to cache
  - Example: Personalized content, dynamic feeds
- **Cache Statistics** – View cache hit/miss rates

### Configuration Registry

**Purpose:** Manage low-level configuration settings via user interface.

**Key Features:**
- **View Registry** – See all registered configuration keys
- **Edit Registry Values** – Modify settings directly
  - Interface for strings, integers, booleans, lists, objects
- **Import Registry** – Load settings from XML file
- **Export Registry** – Save current settings to XML file
- **Reset to Defaults** – Restore factory default settings
- **Search Registry** – Find specific settings by keyword

### Resource Registries

**Purpose:** Manage CSS and JavaScript resources included in site.

**Key Features:**
- **CSS Registry** – View, enable, disable, edit CSS files
  - Bundle/minify options
  - Conditional loading (IE, mobile, etc.)
- **JavaScript Registry** – View, enable, disable, edit JS files
  - Compression options
  - Load order/dependencies
- **Add Resource** – Include custom CSS or JS files
- **Resource Conditions** – Only load resource for specific conditions
  - Example: Only on home page, only for authenticated users
- **Resource Merge** – Combine multiple files into single request
  - Reduces HTTP requests, improves performance

### Maintenance

**Purpose:** Perform site maintenance tasks.

**Key Actions:**

- **Database Optimization** – Pack database to reclaim space
  - Regular packing recommended (monthly)
- **Clear Temporary Files** – Remove temporary uploads/cache
- **Cleanup Old Logs** – Archive or delete old log files
- **Repair Corrupted Data** – Detect and fix data inconsistencies
- **Backup/Restore** – Create/restore database backups
- **Check Integrity** – Verify database/file system consistency
- **System Status** – View memory usage, disk space, uptime

### Discussion

**Purpose:** Configure content discussion/comments settings.

**Key Settings:**

- **Enable Comments** – Allow users to comment on content
  - Options: Globally enabled, Per-content-type, Per-item
- **Comment Moderation** – Require approval before display
  - Options: Auto-approve, Require review, Anonymous spam filter
- **Notary Settings** – Display commenter information
  - Show user name, avatar, comment date/time
- **Comment Anonymity** – Allow anonymous comments
  - Options: Allow all, Members only, Authenticated users only
- **Discussion Workflow** – Approval process for comments
  - States: Pending, Published, Private, Spam
- **Notification** – Email site admins when new comments arrive
  - Options: Enabled / Disabled

### Syndication

**Purpose:** Configure RSS/Atom feed generation.

**Key Settings:**

- **Enable Syndication** – Allow RSS feeds
  - Options: Enabled / Disabled
- **Feed Content** – What to include in feed items
  - Full content or excerpt
  - Number of words to include
- **Number of Items** – How many recent items in feed
  - Default: 15
- **Allow Comments in Feed** – Include comment feeds
  - Options: Enabled / Disabled
- **Feed Image** – Logo to include in feed
- **Feed ID** – Unique identifier for the feed

### Actions

**Purpose:** Configure content actions and menu items.

**Key Features:**

- **View Actions** – See all available content actions
  - Edit, Copy, Delete, Cut, Paste, Rename, etc.
- **Edit Actions** – Modify or customize actions
  - Name, description, URL pattern, visibility conditions
- **Create Custom Action** – Add new action to content menu
- **Condition Actions** – Control when action appears
  - Show only for certain content types, user roles, states

---

## Add-ons Management

Additional configuration panels provided by installed packages.

### Add-ons Panel

**Purpose:** View and manage installed add-on packages.

**Key Information:**

- **List of Installed Add-ons** – Packages currently running
  - Package name, version, author, description
- **Available Add-ons** – Packages available but not installed
- **Installation Status** – Which add-ons are active/inactive
- **Dependencies** – What each add-on requires
- **Documentation** – Links to add-on documentation

**Common Add-ons Include:**

- **plone.app.dexterity** – Custom content type builder
- **plone.app.workflowstate** – Workflow management
- **plone.app.relationfield** – Content relations/linking
- **plone.app.discussion** – Comments on content
- **plone.app.multilingual** – Multilingual content management
- **eea.facetednavigation** – Advanced filtering/faceted search
- **collective.foldercontents** – Enhanced folder view
- **plone.app.blocks** – Block-based page layout

---

## System Information

Located at the bottom of the Site Setup page.

**Version Information Displayed:**

- **Plone Version** – Current version of Plone
- **Zope Version** – Version of underlying Zope framework
- **Python Version** – Python interpreter version
- **Database Type** – Type of database in use
- **Server Mode** – Production or Development mode indicator
- **Deployment Type** – Docker, standalone, etc.

---

## Best Practices for Advanced Editors

### General Guidelines

1. **Document Changes** – Keep notes of what you configure and why
2. **Test Before Deploying** – Test in development environment first
3. **Backup Regularly** – Create database backups before major changes
4. **Review Permissions** – Periodically audit user roles and permissions
5. **Monitor Performance** – Check caching and resource usage regularly
6. **Update Add-ons** – Keep installed packages up-to-date for security
7. **Security First** – Use strong passwords, enable HTTPS, update regularly

### Common Tasks

- **Creating a new content type** → Content Management > Content Types > Add
- **Assigning an editor role** → Users & Groups > Users > Edit user > Add role
- **Allowing comments on articles** → Advanced > Discussion > Enable for content type
- **Improving performance** → Advanced > Caching > Enable and configure
- **Creating content rules** → Content Management > Content Rules > Add
- **Managing multiple languages** → General > Language > Add languages and set default

---

## Related Resources

- You can see a demo at [SIte setup on a demo plone site](https://classic.demo.plone.org/)@@overview-controlpanel (login as Manager)
- [Plone Training - Content Editing](https://training.plone.org/content-editing/site-setup-and-configuration.html)
- [Plone Training - Mastering Plone](https://training.plone.org/mastering-plone/configuring_customizing.html)
- [Plone Official Documentation](https://plone.org/documentation)


---

**Last Updated:** 2026  
**Plone Version:** 6.1+  
**Target Audience:** Advanced Editors and Site Managers
