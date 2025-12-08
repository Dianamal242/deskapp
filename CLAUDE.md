# CLAUDE.md - AI Assistant Guide for DeskApp

## Project Overview

DeskApp is a free, open-source Bootstrap 4 admin dashboard template (v3.0.0). It provides a comprehensive foundation for building admin panels, back-end dashboards, and control centers with pre-built components, charts, tables, and UI elements.

**Repository:** https://github.com/dropways/deskapp
**Author:** Ankit Hingarajiya (Dropways)
**License:** MIT

## Technology Stack

### Core Framework
- **Bootstrap 4** - CSS framework
- **jQuery 3.5.1** - DOM manipulation and utilities
- **Node.js/npm** - Package management

### Build Tools
- **Gulp 4.0.2** - Task automation
- **node-sass 5.0.0** - SCSS compilation
- **browser-sync** - Live reload development server

### Key Libraries & Plugins
| Category | Libraries |
|----------|-----------|
| Charts | ApexCharts, Highcharts 6.0.7, jQuery Knob |
| Data | DataTables (with Bootstrap4 styling) |
| Maps | jVectorMap |
| Forms | Select2, Bootstrap Select, Bootstrap Tagsinput, Bootstrap Touchspin |
| Date/Time | Air Datepicker, Moment.js, Timedropper |
| Editor | Bootstrap-wysihtml5 |
| File Upload | Dropzone, Cropperjs |
| UI | Sweetalert2, Switchery, Slick Slider, Fancybox 3 |
| Utilities | Clipboard.js, Highlight.js, mCustomScrollbar |

### Icon Libraries
- Bootstrap Icons
- Font Awesome
- Ionicons
- Themify Icons
- Foundation Icons
- Dropways (custom)

## Directory Structure

```
deskapp/
├── src/                          # Source files (edit these)
│   ├── fonts/                    # Icon font files (6 sets)
│   │   ├── bootstrap/
│   │   ├── dropways/
│   │   ├── font-awesome/
│   │   ├── foundation-icons/
│   │   ├── ionicons-master/
│   │   └── themify-icons/
│   ├── images/                   # Source images
│   ├── plugins/                  # Third-party plugins (31+)
│   │   ├── bootstrap/
│   │   ├── datatables/
│   │   ├── select2/
│   │   └── ... (many more)
│   ├── scripts/                  # Custom JavaScript
│   │   ├── setting.js           # Core app functionality
│   │   ├── jquery.min.js
│   │   ├── moment.js
│   │   └── clipboard.min.js
│   └── styles/                   # Custom CSS
│       ├── style.css            # Main styles (4000+ lines)
│       ├── media.css            # Responsive breakpoints
│       └── theme.css            # Theme overrides
│
├── vendors/                      # Compiled output (DO NOT EDIT DIRECTLY)
│   ├── fonts/                   # Compiled fonts
│   ├── images/                  # Optimized images
│   ├── scripts/                 # Bundled JS
│   │   ├── core.js              # All libraries bundled
│   │   ├── script.js            # Custom scripts bundled
│   │   ├── dashboard.js         # Dashboard-specific
│   │   └── *.js                 # Page-specific scripts
│   └── styles/                  # Compiled CSS
│       ├── core.css             # All plugin CSS bundled
│       ├── style.css            # Custom CSS compiled
│       └── icon-font.css        # All icon CSS bundled
│
├── *.html                        # 64 HTML template pages
├── gulpfile.js                   # Gulp build configuration
├── package.json                  # npm dependencies
└── .github/workflows/            # CI/CD pipeline
```

## Development Setup

### Prerequisites
- Node.js (v12+ recommended)
- npm

### Installation
```bash
# Clone the repository
git clone https://github.com/dropways/deskapp.git
cd deskapp

# Install dependencies
npm install
```

### Running Development Server
```bash
# Start Gulp (compiles assets + live reload)
gulp
```

This starts:
- Browser-sync on `localhost:3000`
- File watchers for automatic recompilation
- Live reload on file changes

**Note:** The default Gulp proxy points to `localhost/deskapp`. Modify `gulpfile.js` line 231 if using a different local URL.

### Build Commands
```bash
gulp                 # Full build + watch + browser-sync
gulp styles          # Compile custom CSS only
gulp corestyle       # Compile plugin CSS bundle
gulp icon_styles     # Compile icon font CSS
gulp scripts         # Compile custom JS
gulp core            # Compile core JS bundle
gulp fonts           # Copy fonts to vendors/
gulp images          # Optimize images
```

## Key Files Reference

### HTML Templates (64 pages)
| Category | Files |
|----------|-------|
| Dashboards | `index.html`, `index2.html`, `index3.html` |
| Auth | `login.html`, `register.html`, `forgot-password.html`, `reset-password.html` |
| UI Components | `ui-buttons.html`, `ui-cards.html`, `ui-modals.html`, `ui-tabs.html`, etc. |
| Charts | `apexcharts.html`, `highchart.html`, `knob-chart.html` |
| Tables | `datatable.html`, `basic-table.html` |
| Forms | `form-basic.html`, `form-pickers.html`, `form-wizard.html` |
| Error Pages | `400.html`, `403.html`, `404.html`, `500.html`, `503.html` |
| Content | `blog.html`, `profile.html`, `calendar.html`, `chat.html`, `gallery.html` |
| Blank | `blank.html` (use as template for new pages) |

### Core JavaScript Files

**`src/scripts/setting.js`** - Main application JavaScript containing:
- Bootstrap wysihtml5 editor init
- Custom scrollbar setup
- SVG image replacement
- Code syntax highlighting
- Select2/Bootstrap Select init
- Sidebar accordion menu
- Date/time picker configuration
- Clipboard functionality

**Page-specific scripts in `vendors/scripts/`:**
- `dashboard.js` - Main dashboard charts/tables
- `apexcharts-setting.js` - ApexCharts configuration
- `highchart-setting.js` - Highcharts configuration
- `datatable-setting.js` - DataTable initialization
- `calendar-setting.js` - FullCalendar setup
- `layout-settings.js` - Theme customization panel

### CSS Architecture

**Source files to edit:**
- `src/styles/style.css` - Main custom styles
- `src/styles/media.css` - Responsive breakpoints (1400px, 1300px, 1024px, 991px, 767px, 660px)
- `src/styles/theme.css` - Theme-specific overrides

**Compiled output (auto-generated):**
- `vendors/styles/core.css` - All plugin CSS bundled
- `vendors/styles/style.css` - Custom CSS compiled
- `vendors/styles/icon-font.css` - All icon fonts bundled

## Coding Conventions

### HTML Structure
Every page follows this structure:
```html
<!DOCTYPE html>
<html>
<head>
    <!-- Core CSS -->
    <link rel="stylesheet" href="vendors/styles/core.css">
    <link rel="stylesheet" href="vendors/styles/icon-font.min.css">
    <link rel="stylesheet" href="vendors/styles/style.css">
</head>
<body>
    <div class="pre-loader">...</div>
    <div class="header">...</div>
    <div class="left-side-bar">...</div>
    <div class="main-container">
        <div class="pd-ltr-20">
            <!-- Page content here -->
        </div>
    </div>

    <!-- Core JS -->
    <script src="vendors/scripts/core.js"></script>
    <script src="vendors/scripts/script.js"></script>
    <!-- Page-specific JS -->
</body>
</html>
```

### CSS Conventions
- Use Bootstrap 4 utility classes when possible
- Custom classes use lowercase with hyphens: `.card-box`, `.page-header`
- Color scheme uses CSS variables where applicable
- Primary text color: `#031e23`
- Background: `#ecf0f4`

### JavaScript Conventions
- jQuery is available globally as `$`
- Plugin initialization in `setting.js` or page-specific files
- Use data attributes for configuration: `data-color`, `data-bgcolor`, `data-border`

## Common Tasks for AI Assistants

### Adding a New Page
1. Copy `blank.html` as template
2. Update page title and content
3. Add to sidebar navigation in the HTML
4. Create page-specific JS in `vendors/scripts/` if needed

### Modifying Styles
1. Edit source files in `src/styles/`
2. Run `gulp styles` or let watcher recompile
3. Compiled output goes to `vendors/styles/`

### Adding a New Plugin
1. Add plugin files to `src/plugins/`
2. Update `gulpfile.js` to include in `path.corestyle` or `path.core`
3. Run full `gulp` build

### Updating Charts
- ApexCharts config: `vendors/scripts/apexcharts-setting.js`
- Highcharts config: `vendors/scripts/highchart-setting.js`
- Dashboard charts: `vendors/scripts/dashboard.js`

## Important Notes

### DO NOT Edit Directly
- Files in `vendors/` are auto-generated
- Edit source files in `src/` instead
- Run Gulp to recompile

### Browser Support
- CSS is autoprefixed for last 2 browser versions
- IE browser detection is included in `setting.js`

### Testing
- No automated tests configured (placeholder in package.json)
- Manual testing via browser-sync live reload

### CI/CD
- GitHub Actions workflow in `.github/workflows/npm-publish.yml`
- Triggers on GitHub releases
- Publishes to npm registry

## Demo Links
- GitHub Pages: https://dropways.github.io/deskapp/
- Heroku: https://deskapp-dashboard.herokuapp.com/
- Netlify: https://deskapp.netlify.app/

## File Modification Guidelines

When making changes:
1. **CSS changes**: Edit `src/styles/*.css`, not `vendors/styles/`
2. **JS changes**: Edit `src/scripts/setting.js` for core functionality
3. **New pages**: Base on `blank.html` template
4. **Plugins**: Add to `src/plugins/` and update `gulpfile.js`
5. **Images**: Add to `src/images/`, they auto-optimize on build

## Troubleshooting

### Gulp build fails
- Ensure Node.js v12+ is installed
- Run `npm install` to ensure all dependencies
- Check for syntax errors in source files

### Browser-sync not working
- Check proxy URL in `gulpfile.js` line 231
- Ensure no port conflicts on 3000

### Styles not updating
- Check Gulp watcher is running
- Clear browser cache
- Verify editing files in `src/` not `vendors/`
