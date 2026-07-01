(function() {
  // The user answers in the terminal, not the browser — so there is no click
  // capture and no WebSocket. The only job here is to keep the page in sync
  // with the newest screen the agent writes: poll /poll, reload on change.
  const POLL_MS = 1000;
  let current = null;

  async function poll() {
    try {
      const res = await fetch('/poll', { cache: 'no-store' });
      if (!res.ok) return;
      const stamp = await res.json();
      const signature = stamp.file + '@' + stamp.mtime;
      if (current === null) {
        current = signature;
      } else if (signature !== current) {
        window.location.reload();
      }
    } catch (e) {
      // Server may be momentarily unreachable (restart/idle) — retry next tick.
    }
  }

  setInterval(poll, POLL_MS);
  poll();
})();
