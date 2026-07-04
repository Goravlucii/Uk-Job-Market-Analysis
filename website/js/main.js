// ── UK JOB MARKET ANALYSIS — CHART DATA ─────────────────────

const NAVY   = '#0d1b2a';
const BLUE   = '#1e88e5';
const RED    = '#ef5350';
const GREEN  = '#43a047';
const GOLD   = '#f9a825';
const GREY   = 'rgba(255,255,255,0.15)';

// Shared defaults for dark background charts
Chart.defaults.color = 'rgba(255,255,255,0.65)';
Chart.defaults.borderColor = GREY;

// ── 1. EMPLOYMENT RATE ───────────────────────────────────────
const empCtx = document.getElementById('empChart').getContext('2d');
new Chart(empCtx, {
  type: 'line',
  data: {
    labels: ['Q1 2019','Q2 2019','Q3 2019','Q4 2019','Q1 2020','Q2 2020',
             'Q3 2020','Q4 2020','Q1 2021','Q2 2021','Q3 2021','Q4 2021',
             'Q1 2022','Q2 2022','Q3 2022','Q4 2022','Q1 2023','Q2 2023',
             'Q3 2023','Q4 2023','Q1 2024','Q2 2024','Q3 2024','Q4 2024',
             'Q1 2025','Q2 2025','Q3 2025','Q4 2025','Q1 2026'],
    datasets: [
      {
        label: 'Employment Rate (%)',
        data: [76.1,76.3,76.5,76.6,76.0,74.4,74.6,75.0,75.2,75.4,
               75.6,75.7,75.8,75.9,76.0,75.8,75.5,75.3,75.1,75.0,
               75.1,75.3,75.4,75.5,75.5,75.6,75.6,75.7,75.7],
        borderColor: BLUE, backgroundColor: 'rgba(30,136,229,0.1)',
        borderWidth: 2.5, tension: 0.3, fill: true, pointRadius: 0, pointHoverRadius: 5
      },
      {
        label: 'Pre-pandemic baseline (76.6%)',
        data: Array(29).fill(76.6),
        borderColor: GOLD, borderDash: [6,4], borderWidth: 1.5,
        pointRadius: 0, fill: false
      }
    ]
  },
  options: {
    responsive: true, maintainAspectRatio: true, aspectRatio: 1.8,
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 14, padding: 16 } } },
    scales: {
      x: { grid: { color: GREY }, ticks: { maxTicksLimit: 8, font: { size: 10 } } },
      y: { grid: { color: GREY }, min: 73, max: 77.5,
           ticks: { callback: v => v + '%', font: { size: 10 } } }
    }
  }
});

// ── 2. VACANCIES ─────────────────────────────────────────────
const vacCtx = document.getElementById('vacChart').getContext('2d');
new Chart(vacCtx, {
  type: 'bar',
  data: {
    labels: ['Q1 2019','Q2 2019','Q3 2019','Q4 2019','Q1 2020','Q2 2020',
             'Q3 2020','Q4 2020','Q1 2021','Q2 2021','Q3 2021','Q4 2021',
             'Q1 2022','Q2 2022','Q3 2022','Q4 2022','Q1 2023','Q2 2023',
             'Q3 2023','Q4 2023','Q1 2024','Q2 2024','Q3 2024','Q4 2024',
             'Q1 2025','Q2 2025','Q3 2025','Q4 2025','Q1 2026'],
    datasets: [{
      label: 'Total Vacancies (thousands)',
      data: [810,830,845,820,780,476,620,740,820,980,1120,1210,
             1280,1295,1270,1220,1150,1080,1020,980,960,940,920,905,
             895,890,888,890,893],
      backgroundColor: (ctx) => {
        const v = ctx.raw;
        if (v >= 1200) return 'rgba(198,40,40,0.8)';
        if (v <= 500)  return 'rgba(198,40,40,0.8)';
        return 'rgba(30,136,229,0.75)';
      },
      borderRadius: 3
    }]
  },
  options: {
    responsive: true, maintainAspectRatio: true, aspectRatio: 1.8,
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 14, padding: 16 } },
      annotation: {}
    },
    scales: {
      x: { grid: { color: GREY }, ticks: { maxTicksLimit: 8, font: { size: 10 } } },
      y: { grid: { color: GREY }, min: 400,
           ticks: { callback: v => v + 'k', font: { size: 10 } } }
    }
  }
});

// ── 3. CPI vs BASE RATE ──────────────────────────────────────
const ecoCtx = document.getElementById('ecoChart').getContext('2d');
new Chart(ecoCtx, {
  type: 'line',
  data: {
    labels: ['Jan 19','Jul 19','Jan 20','Jul 20','Jan 21','Jul 21',
             'Jan 22','Jul 22','Jan 23','Jul 23','Jan 24','Jul 24',
             'Jan 25','Jul 25','Jan 26','Jun 26'],
    datasets: [
      {
        label: 'CPI Inflation (%)',
        data: [1.8,2.1,1.7,0.6,0.7,2.1,5.4,10.1,10.1,6.8,4.0,2.2,2.8,2.4,2.5,2.3],
        borderColor: RED, backgroundColor: 'rgba(239,83,80,0.1)',
        borderWidth: 2.5, tension: 0.3, fill: true, pointRadius: 0, yAxisID: 'y'
      },
      {
        label: 'BoE Base Rate (%)',
        data: [0.75,0.75,0.75,0.1,0.1,0.1,0.25,1.25,3.5,5.0,5.25,5.0,4.5,4.25,3.75,3.25],
        borderColor: GOLD, borderWidth: 2.5, tension: 0.1,
        pointRadius: 0, fill: false, stepped: 'after', yAxisID: 'y'
      }
    ]
  },
  options: {
    responsive: true, maintainAspectRatio: true, aspectRatio: 1.8,
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 14, padding: 16 } } },
    scales: {
      x: { grid: { color: GREY }, ticks: { maxTicksLimit: 10, font: { size: 10 } } },
      y: { grid: { color: GREY }, min: 0, max: 12,
           ticks: { callback: v => v + '%', font: { size: 10 } } }
    }
  }
});

// ── 4. SKILLS DEMAND ─────────────────────────────────────────
const skillsCtx = document.getElementById('skillsChart').getContext('2d');
new Chart(skillsCtx, {
  type: 'bar',
  data: {
    labels: ['Communication','Excel','SQL','PowerPoint','Python','Data Vis',
             'Power BI','Teamwork','Problem Solving','Tableau'],
    datasets: [{
      label: '% of postings',
      data: [89.9, 82.1, 74.4, 71.2, 62.8, 58.3, 54.7, 52.1, 49.6, 41.3],
      backgroundColor: [
        'rgba(30,136,229,0.85)','rgba(30,136,229,0.85)','rgba(30,136,229,0.85)',
        'rgba(30,136,229,0.85)','rgba(249,168,37,0.85)','rgba(249,168,37,0.85)',
        'rgba(249,168,37,0.85)','rgba(30,136,229,0.7)','rgba(30,136,229,0.7)',
        'rgba(249,168,37,0.85)'
      ],
      borderRadius: 4
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true, maintainAspectRatio: true, aspectRatio: 1.4,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { color: GREY }, min: 0, max: 100,
           ticks: { callback: v => v + '%', font: { size: 10 } } },
      y: { grid: { display: false }, ticks: { font: { size: 10 } } }
    }
  }
});

// ── SCROLL ANIMATIONS ─────────────────────────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.kpi-card, .cause-card, .forecast-card, .paradox-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});
