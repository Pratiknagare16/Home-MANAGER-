// Home Manager – animations, toasts, count-up, expense delete
(function () {
  var DUR_MS = 250;
  var TOAST_PAUSE_MS = 4000;

  function initToasts() {
    document.querySelectorAll('.toast-container .alert').forEach(function (el) {
      el.classList.add('toast-in');
      setTimeout(function () {
        var alert = bootstrap.Alert.getOrCreateInstance(el);
        if (alert) alert.close();
      }, TOAST_PAUSE_MS);
    });
  }

  function initExpenseDelete() {
    document.querySelectorAll('.expense-delete-form').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        if (form.getAttribute('data-animating') === '1') return;
        e.preventDefault();
        var row = form.closest('.expense-row');
        if (!row) { form.submit(); return; }
        row.classList.add('expense-row-removing');
        setTimeout(function () {
          form.setAttribute('data-animating', '1');
          form.submit();
        }, DUR_MS);
      });
    });
  }

  function initCountUp() {
    document.querySelectorAll('.count-up').forEach(function (el) {
      var target = parseFloat(el.getAttribute('data-count')) || 0;
      var format = el.getAttribute('data-format') || 'integer';
      var duration = 600;
      var start = 0;
      var startTime = null;
      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        progress = 1 - Math.pow(1 - progress, 2);
        var current = start + (target - start) * progress;
        if (format === 'currency') {
          el.textContent = '₹' + current.toFixed(2);
        } else {
          el.textContent = Math.round(current);
        }
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initToasts();
    initExpenseDelete();
    initCountUp();
  });
})();
