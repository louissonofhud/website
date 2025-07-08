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

document.addEventListener("DOMContentLoaded", function () {
  const accordions = document.querySelectorAll(".accordion");

  accordions.forEach(button => {
    button.addEventListener("click", function () {
      this.classList.toggle("selected");
      const panel = this.nextElementSibling;
      const isOpen = panel.classList.contains("open");

      if (isOpen) {
        panel.style.maxHeight = null;
        panel.classList.remove("open");
      } else {
        panel.classList.add("open");

        // Defer setting the height of this panel
        requestAnimationFrame(() => {
          panel.style.maxHeight = panel.scrollHeight + "px";

          // After it's open, update parent panels
          requestAnimationFrame(() => {
            updateAncestorHeights(panel);
            
            // Safety pass: handle edge case where content reflows
            setTimeout(() => {
              if (panel) {
                panel.style.maxHeight = panel.scrollHeight + "px";
                updateAncestorHeights(panel);
              }
            }, 0);
          });
        });
      }
    });
  });

function updateAncestorHeights(startFrom) {
  let parent = startFrom?.parentElement;

  while (parent) {
    if (parent.classList.contains("panel")) {
      let subItemHeight = parseFloat(startFrom.style.maxHeight) || 0;
      let scrollHeight = parseFloat(parent.scrollHeight) || 0;
      parent.style.maxHeight = scrollHeight + subItemHeight + "px";
    }
    parent = parent.parentElement;
  }
}
});

