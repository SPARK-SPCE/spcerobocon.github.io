(function() {
  const AUTH_KEY = 'spark_site_unlocked';
  const PASSWORD = 'PAPPA@123';

  function isUnlocked() {
    try {
      return localStorage.getItem(AUTH_KEY) === 'true';
    } catch(e) {
      return false;
    }
  }

  if (isUnlocked()) {
    return;
  }

  // Prevent scroll immediately
  try {
    document.documentElement.style.overflow = 'hidden';
    if (document.body) document.body.style.overflow = 'hidden';
  } catch(e) {}

  function renderLockscreen() {
    if (isUnlocked()) return;
    if (document.getElementById('spark-lockscreen-root')) return;

    const overlay = document.createElement('div');
    overlay.id = 'spark-lockscreen-root';
    overlay.innerHTML = `
      <style>
        #spark-lockscreen-root {
          position: fixed;
          top: 0; left: 0; width: 100vw; height: 100vh;
          background: #08080c;
          background-image: 
            radial-gradient(ellipse at 50% 20%, rgba(0, 245, 255, 0.08) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 80%, rgba(255, 107, 0, 0.05) 0%, transparent 50%),
            linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
          background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
          z-index: 2147483647;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 1.5rem;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
          color: #f0f0f5;
          box-sizing: border-box;
        }
        .lock-card {
          width: 100%;
          max-width: 440px;
          background: rgba(14, 15, 23, 0.92);
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          border: 1px solid rgba(0, 245, 255, 0.25);
          border-radius: 16px;
          padding: 2.5rem 2rem;
          box-shadow: 0 0 50px rgba(0, 245, 255, 0.1), 0 20px 40px rgba(0, 0, 0, 0.7);
          text-align: center;
          position: relative;
          overflow: hidden;
        }
        .lock-card::before {
          content: '';
          position: absolute;
          top: 0; left: 0; right: 0;
          height: 3px;
          background: linear-gradient(90deg, #00f5ff, #ff6b00, #c084fc);
        }
        .lock-badge {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 4px 12px;
          background: rgba(255, 107, 0, 0.12);
          border: 1px solid rgba(255, 107, 0, 0.4);
          color: #ff914d;
          font-family: 'Orbitron', monospace, sans-serif;
          font-size: 0.72rem;
          font-weight: 700;
          letter-spacing: 0.12em;
          border-radius: 999px;
          margin-bottom: 1.25rem;
          text-transform: uppercase;
        }
        .lock-pulse-dot {
          width: 7px;
          height: 7px;
          background: #ff6b00;
          border-radius: 50%;
          box-shadow: 0 0 8px #ff6b00;
          animation: lockPulse 1.4s ease-in-out infinite;
        }
        @keyframes lockPulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.3; transform: scale(0.7); }
        }
        .lock-logo {
          width: 58px;
          height: 58px;
          margin: 0 auto 1.25rem;
          display: block;
          filter: drop-shadow(0 0 16px rgba(0, 245, 255, 0.45));
        }
        .lock-title {
          font-family: 'Orbitron', sans-serif;
          font-size: 1.35rem;
          font-weight: 700;
          letter-spacing: 0.08em;
          margin: 0 0 0.5rem;
          color: #ffffff;
        }
        .lock-sub {
          font-size: 0.8rem;
          color: #00f5ff;
          letter-spacing: 0.1em;
          font-family: 'Orbitron', monospace;
          margin-bottom: 1rem;
          text-transform: uppercase;
        }
        .lock-desc {
          font-size: 0.88rem;
          color: #94a3b8;
          line-height: 1.5;
          margin-bottom: 1.75rem;
        }
        .lock-form {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .lock-input {
          width: 100%;
          box-sizing: border-box;
          padding: 12px 16px;
          background: rgba(5, 7, 12, 0.8);
          border: 1px solid rgba(255, 255, 255, 0.15);
          border-radius: 8px;
          color: #fff;
          font-size: 0.95rem;
          font-family: inherit;
          outline: none;
          transition: all 0.2s ease;
          text-align: center;
          letter-spacing: 0.15em;
        }
        .lock-input:focus {
          border-color: #00f5ff;
          box-shadow: 0 0 15px rgba(0, 245, 255, 0.25);
        }
        .lock-btn {
          width: 100%;
          padding: 12px 18px;
          background: linear-gradient(135deg, #00f5ff, #0088cc);
          color: #020617;
          border: none;
          border-radius: 8px;
          font-family: 'Orbitron', sans-serif;
          font-size: 0.88rem;
          font-weight: 700;
          letter-spacing: 0.1em;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        .lock-btn:hover {
          filter: brightness(1.15);
          box-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
          transform: translateY(-1px);
        }
        .lock-btn:active {
          transform: translateY(0);
        }
        .lock-error {
          color: #ff4757;
          font-size: 0.8rem;
          margin-top: 0.75rem;
          display: none;
          letter-spacing: 0.05em;
          font-family: 'Orbitron', monospace;
        }
        .lock-success {
          color: #2ed573;
          font-size: 0.8rem;
          margin-top: 0.75rem;
          display: none;
          letter-spacing: 0.05em;
          font-family: 'Orbitron', monospace;
        }
      </style>
      <div class="lock-card">
        <div class="lock-badge">
          <span class="lock-pulse-dot"></span>
          <span>System Maintenance</span>
        </div>
        <img src="/assets/img/favicon.svg" alt="SPARK Logo" class="lock-logo" />
        <h1 class="lock-title">UNDER MAINTENANCE</h1>
        <div class="lock-sub">SPARK — SPCE ROBOCON</div>
        <p class="lock-desc">
          This portal is undergoing scheduled maintenance. Enter administrator authorization key to view the environment.
        </p>
        <form class="lock-form" id="spark-lock-form">
          <input
            type="password"
            id="spark-lock-pass"
            class="lock-input"
            placeholder="ENTER ACCESS KEY"
            autocomplete="current-password"
            required
          />
          <button type="submit" class="lock-btn">AUTHENTICATE →</button>
        </form>
        <div id="spark-lock-err" class="lock-error">ACCESS DENIED // INCORRECT KEY</div>
        <div id="spark-lock-ok" class="lock-success">ACCESS GRANTED // INITIALIZING...</div>
      </div>
    `;

    document.body.prepend(overlay);

    const form = document.getElementById('spark-lock-form');
    const input = document.getElementById('spark-lock-pass');
    const err = document.getElementById('spark-lock-err');
    const ok = document.getElementById('spark-lock-ok');

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const val = input.value.trim();
      if (val === PASSWORD) {
        err.style.display = 'none';
        ok.style.display = 'block';
        try {
          localStorage.setItem(AUTH_KEY, 'true');
        } catch(e) {}
        setTimeout(() => {
          overlay.style.transition = 'opacity 0.4s ease';
          overlay.style.opacity = '0';
          setTimeout(() => {
            overlay.remove();
            document.documentElement.style.overflow = '';
            if (document.body) document.body.style.overflow = '';
          }, 400);
        }, 300);
      } else {
        err.style.display = 'block';
        input.value = '';
        input.focus();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderLockscreen);
  } else {
    renderLockscreen();
  }
})();
