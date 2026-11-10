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

  // Forms: the site has no server, so each form opens the visitor's email app
  // with a message to MAHALO already written from the fields they filled in.
  var MAHALO_EMAIL = "info@mahalosecurity.com";

  function composeEmail(form) {
    var lines = [];
    form.querySelectorAll("[name]").forEach(function (field) {
      if (field.type === "checkbox" && !field.checked) return;
      var value = (field.value || "").trim();
      if (!value) return;
      var label = field.getAttribute("data-label") || field.name;
      lines.push(label + ": " + value);
    });
    var subject = form.getAttribute("data-subject") || "MAHALO inquiry";
    var name = form.querySelector("[name='name']");
    if (name && name.value.trim()) subject += " — " + name.value.trim();
    return "mailto:" + MAHALO_EMAIL +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(lines.join("\n") + "\n");
  }

  document.querySelectorAll("form[data-mahalo-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      window.location.href = composeEmail(form);
      var success = document.getElementById(form.getAttribute("data-success"));
      form.hidden = true;
      if (success) {
        success.hidden = false;
        success.focus();
      }
    });
  });

  // Arriving from a service page (consultation.html?service=estate) pre-selects that service
  try {
    var service = new URLSearchParams(window.location.search).get("service");
    var chip = service && document.getElementById("int-" + service.replace(/[^a-z]/g, ""));
    if (chip) chip.checked = true;
  } catch (err) { /* older browsers: nothing to pre-select */ }

  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
