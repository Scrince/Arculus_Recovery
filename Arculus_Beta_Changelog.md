# Arculus Beta Changelog

## Browser download reliability

- Created `Arculus_Beta.html` from the current `Arculus_Recovery.html` application.
- Deferred browser object-URL revocation for 10 seconds after initiating a download.
- This gives Safari, Firefox, and other browsers time to begin consuming the Blob URL before it is released, reducing the risk of failed or empty browser downloads.
- The Tauri native export path is unchanged.

## Global keyboard handling

- Consolidated the output-panel and QR-modal `Escape` handlers into one global keydown dispatcher.
- The dispatcher prioritizes closing the QR modal, then collapses the expanded output panel when applicable.
- Centralizing global keyboard behavior makes future shortcuts and modal handling easier to audit and extend.

## Idle-warning cleanup

- `handleClearAll` now cancels and resets the pending idle-warning timer on every clear path.
- Any visible idle countdown banner is dismissed when sensitive fields are cleared.
- Manual clears, visibility-security clears, and idle-timeout clears can no longer leave or revive a stale countdown warning.
