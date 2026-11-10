/* Mahalo — site behaviour */
(function () {
  document.documentElement.classList.add("js");

  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");

  // Sticky header: switch from transparent to solid once the page scrolls
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 40);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobile menu
  function setMenu(open) {
    header.classList.toggle("menu-open", open);
    document.body.classList.toggle("menu-locked", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      setMenu(!header.classList.contains("menu-open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.classList.contains("menu-open")) setMenu(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 900) setMenu(false);
    });
  }

  // Reveal on scroll — anything already in view shows immediately
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("is-in"); });
  }

  // Forms: no backend yet — validate, then show the confirmation state
  document.querySelectorAll("form[data-mahalo-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      var success = document.getElementById(form.getAttribute("data-success"));
      form.hidden = true;
      if (success) {
        success.hidden = false;
        success.focus();
      }
    });
  });

  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
