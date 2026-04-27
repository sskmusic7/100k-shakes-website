# Instagram Embed Codes - Ready to Use

## Files Created:
1. **`instagram-embeds.html`** - All 12 embed codes
2. **`instagram-social-section.html`** - Complete HTML section to paste into index.html

## Instructions:

### Option 1: Quick Replace (Recommended)
1. Open `/Users/sskmusic/100K SHAKES SITE/index.html`
2. Find the `<!-- Social Media Feed Section -->` (around line 187)
3. Replace the entire `<section class="social-feed">` block with content from `instagram-social-section.html`
4. Add this script at the end of `<body>` (before closing `</body>` tag):
   ```html
   <script async src="//www.instagram.com/embed.js"></script>
   ```

### Option 2: Manual Embed
Get official embed codes from Instagram:
1. Go to any post on Instagram (web or app)
2. Click **⋮** (three dots) → **Embed**
3. Copy the full embed code
4. Replace the placeholder `<div class="social-post">` blocks

## Current Placeholders to Replace:
In `index.html` around line 188-233, replace:
```html
<div class="social-grid">
    <div class="social-post">
        <div class="social-image" style="background: ..."></div>
        ...
    </div>
    <!-- Repeat 6 times -->
</div>
```

With actual Instagram embeds from the file above.

## Posts Ready to Embed:
1. ✅ C1xnwkbMOYE - Post
2. ✅ C1xnoFDMggy - Post
3. ✅ C1xmx4PsVVO - Post
4. ✅ C1vbqKnIYis - Post
5. ✅ C1JCAP4C0kO - Reel
6. ✅ C0uOLC6si15 - Post
7. ✅ C0t5QORsZBn - Post
8. ✅ CzTR6-Tsj43 - Post
9. ✅ CzTLUoRs6KA - Post
10. ✅ CzS8KnTsGYd - Post
11. ✅ CzS2kX_s5ha - Post
12. ✅ CxJsWWbIrJa - Post

## CSS Already Set:
The `.social-feed`, `.social-grid`, and `.social-post` styles are already in `styles.css` - they'll work with Instagram embeds.

## Note:
- Instagram embed script (`//www.instagram.com/embed.js`) loads the actual post content
- Embeds are responsive and work on mobile
- Instagram handles all updates automatically
- No API key needed for this method

## Testing After Install:
1. Hard refresh the page (Cmd+Shift+R)
2. Instagram embeds may take 2-3 seconds to load
3. If you see "View on Instagram" links only, check browser console for errors
4. Make sure the embed.js script is loaded (check Network tab in DevTools)
