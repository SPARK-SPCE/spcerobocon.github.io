const grid = document.getElementById('team-grid');
const buttons = document.querySelectorAll('.year-btn');
let teamMembers = [];

function getPlatformIcon(platform) {
    switch (platform.toLowerCase()) {
        case "instagram":
            return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>`;
        case "linkedin":
            return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4V24h-4V8zm7.5 0h3.7v2.2h.1c.5-.9 1.8-2.2 3.8-2.2 4 0 4.8 2.6 4.8 6V24h-4v-7.9c0-1.9 0-4.4-2.7-4.4-2.7 0-3.1 2.1-3.1 4.3V24h-4V8z"/></svg>`;
        case "github":
            return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 .5C5.73.5.5 5.73.5 12c0 5.1 3.29 9.4 7.86 10.94.58.1.79-.25.79-.56v-2.17c-3.2.7-3.88-1.39-3.88-1.39-.52-1.32-1.27-1.68-1.27-1.68-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.76 2.68 1.25 3.34.95.1-.74.4-1.25.72-1.54-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.28 1.18-3.09-.12-.29-.51-1.45.11-3.02 0 0 .96-.31 3.15 1.18a10.9 10.9 0 0 1 5.74 0c2.19-1.49 3.15-1.18 3.15-1.18.62 1.57.23 2.73.11 3.02.74.81 1.18 1.83 1.18 3.09 0 4.43-2.69 5.41-5.25 5.69.41.35.77 1.05.77 2.12v3.14c0 .31.21.66.79.55A10.51 10.51 0 0 0 23.5 12c0-6.27-5.23-11.5-11.5-11.5z"/></svg>`;
        default:
            return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>`;
    }
}

function renderMembers(filterDept) {
    grid.innerHTML = "";
    const filtered = (filterDept === 'all' || !filterDept) 
        ? teamMembers 
        : teamMembers.filter(m => m.dept === filterDept);

    filtered.forEach(m => {
        const card = document.createElement('div');
        card.className = "member-card";
        const skillsHtml = (m.skills || []).map(sk => `<span class="skill-tag">${sk}</span>`).join('');
        
        card.innerHTML = `
            <div class="dept-badge dept-${m.dept || 'general'}">${m.dept_label || ''}</div>
            <img src="${m.photo || ''}" alt="${m.name || ''}" class="member-photo" loading="lazy">
            <div class="member-name">${m.name || ''}</div>
            <div class="member-role">${m.role || ''}</div>
            <div class="member-skills">${skillsHtml}</div>
            <div class="socials">
              ${(m.socials || []).map(s => `<a href="${s.url}" target="_blank" rel="noopener" aria-label="${s.platform}">${getPlatformIcon(s.platform)}</a>`).join('')}
            </div>
        `;
        grid.appendChild(card);
    });
}

async function initTeam() {
    grid.innerHTML = "<div style='grid-column: 1/-1; text-align: center; color: #888;'>Loading team roster...</div>";
    try {
        const resp = await fetch("/src/data/team/active.json", { cache: "no-cache" });
        if (!resp.ok) throw new Error("Failed to load");
        teamMembers = await resp.json();
        renderMembers('all');
    } catch(err) {
        grid.innerHTML = "<div style='grid-column: 1/-1; text-align: center; color: #ff6b6b;'>Failed to load team data</div>";
    }
}

buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const dept = btn.dataset.dept;
        renderMembers(dept);
    });
});

initTeam();
