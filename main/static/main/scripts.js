const hamburger = document.getElementById('hamburger');
const dropdown = document.getElementById('dropdown');
hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  dropdown.classList.toggle('active');
});

function toggleDetails(button) {
  const confirmation = button.nextElementSibling;
  confirmation.classList.toggle("open");

  if (confirmation.classList.contains("open")) {
      confirmation.style.maxHeight = "150px";
  } else {
      confirmation.style.maxHeight = null;
  }
}

setTimeout(() => {
  document.querySelectorAll('.alert').forEach(alert => {
    alert.classList.add('fade-out');
    setTimeout(() => {
      alert.remove();
    }, 800); // Match the CSS transition duration
  });
}, 3000); // Wait 3 seconds before fading out