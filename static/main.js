/* ── main.js ── */
// Mobile sidebar toggle
const menuToggle    = document.getElementById('menuToggle');
const sidebar       = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

if (menuToggle) {
  menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    sidebarOverlay.classList.toggle('show');
  });
}
if (sidebarOverlay) {
  sidebarOverlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('show');
  });
}

// Auto-dismiss alerts after 4 seconds
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity 0.5s ease';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  }, 4000);
});

// Animate number counters on dashboard
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  if (isNaN(target)) return;
  let start = 0;
  const step = Math.ceil(target / 40);
  const timer = setInterval(() => {
    start = Math.min(start + step, target);
    el.textContent = start.toLocaleString();
    if (start >= target) clearInterval(timer);
  }, 30);
}
document.querySelectorAll('[data-target]').forEach(animateCounter);

// Mark Attendance – dynamic student list via AJAX
const courseSelect = document.getElementById('att_course_select');
const dateSelect   = document.getElementById('att_date_select');
const studentsBody = document.getElementById('students_tbody');

function loadStudents() {
  if (!courseSelect || !studentsBody) return;
  const courseId = courseSelect.value;
  const date     = dateSelect ? dateSelect.value : '';
  if (!courseId) { studentsBody.innerHTML = '<tr><td colspan="3" class="empty-state"><i class="bi bi-person-x"></i><p>Select a course to load students.</p></td></tr>'; return; }

  studentsBody.innerHTML = '<tr><td colspan="3" style="text-align:center;padding:20px;color:var(--text-muted)"><i class="bi bi-hourglass-split"></i> Loading…</td></tr>';

  fetch(`/api/enrolled_students?course_id=${courseId}&date=${date}`)
    .then(r => r.json())
    .then(data => {
      if (!data.length) {
        studentsBody.innerHTML = '<tr><td colspan="3" class="empty-state"><i class="bi bi-person-x"></i><p>No students enrolled in this course.</p></td></tr>';
        return;
      }
      studentsBody.innerHTML = data.map((s, i) => `
        <tr>
          <td><input type="hidden" name="student_ids" value="${s.student_id}">${i+1}. ${s.name}</td>
          <td>
            <div class="att-toggle">
              <input class="att-radio att-radio-present" type="radio" name="status_${s.student_id}" id="p_${s.student_id}" value="Present" ${s.status==='Present'?'checked':''}>
              <label class="att-label att-label-present" for="p_${s.student_id}">✓ Present</label>

              <input class="att-radio att-radio-absent" type="radio" name="status_${s.student_id}" id="a_${s.student_id}" value="Absent" ${s.status==='Absent'?'checked':''}>
              <label class="att-label att-label-absent" for="a_${s.student_id}">✗ Absent</label>

              <input class="att-radio att-radio-late" type="radio" name="status_${s.student_id}" id="l_${s.student_id}" value="Late" ${s.status==='Late'?'checked':''}>
              <label class="att-label att-label-late" for="l_${s.student_id}">⏱ Late</label>
            </div>
          </td>
        </tr>
      `).join('');

      // Collect status values on form submit
      const form = document.getElementById('att_form');
      if (form) {
        form.onsubmit = () => {
          document.querySelectorAll('[name^="status_"]').forEach(radio => {
            if (radio.checked) {
              const hi = document.createElement('input');
              hi.type = 'hidden'; hi.name = 'statuses'; hi.value = radio.value;
              form.appendChild(hi);
            }
          });
        };
      }
    })
    .catch(() => {
      studentsBody.innerHTML = '<tr><td colspan="3" style="color:var(--danger);padding:16px">Failed to load students.</td></tr>';
    });
}

if (courseSelect) { courseSelect.addEventListener('change', loadStudents); loadStudents(); }
if (dateSelect)   { dateSelect.addEventListener('change', loadStudents); }

// Confirm delete
document.querySelectorAll('.btn-delete-confirm').forEach(btn => {
  btn.addEventListener('click', e => {
    if (!confirm('Are you sure you want to delete this record?')) e.preventDefault();
  });
});

// Progress bar animation
document.querySelectorAll('.progress-bar-fill').forEach(bar => {
  const w = bar.dataset.width || '0';
  bar.style.width = '0';
  setTimeout(() => { bar.style.width = w + '%'; }, 100);
});
