document.addEventListener('DOMContentLoaded', () => {
  console.log('app.js loaded');

  // 1) Перевірка GET /api/ping/
  fetch('/api/ping/')
    .then(r => r.json())
    .then(d => console.log('fetch /api/ping ->', d))
    .catch(err => console.error(err));

  // CSRF helper (офіційний рецепт із документації)
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  const csrftoken = getCookie('csrftoken');

  // 2) Відправляємо форму POST /api/echo/
  const form = document.getElementById('echoForm');
  const input = document.getElementById('echoInput');
  const out = document.getElementById('echoOut');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    out.textContent = 'Відправляю...';
    try {
      const resp = await fetch('/api/echo/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ text: input.value })
      });
      const data = await resp.json();
      if (!resp.ok) throw data;
      out.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      console.error(err);
      out.textContent = 'Помилка: ' + JSON.stringify(err);
    }
  });
});
