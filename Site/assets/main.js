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

  function showSuccess(form) {
    var success = document.getElementById(form.getAttribute("data-success"));
    form.hidden = true;
    if (success) {
      success.hidden = false;
      success.focus();
    }
  }

  // HubSpot forms: the site's own form, submitted to HubSpot's Forms API so it
  // lands in HubSpot exactly as an embedded HubSpot form would. Field names must
  // match the HubSpot form's internal property names (firstname, email, ...).
  //
  // On the live site the form posts to /api/hubspot/submit/ on our own domain,
  // which Netlify forwards to HubSpot (see netlify.toml). Safari's tracker
  // blocking and content blockers can stop requests to HubSpot's own domain;
  // a same-site request is never blocked. The local preview has no forwarding,
  // so it posts to HubSpot directly.
  var HUBSPOT_DIRECT = "https://api.hsforms.com/submissions/v3/integration/submit/";
  var HUBSPOT_PROXY = "/api/hubspot/submit/";
  var isLocal = location.protocol === "file:" || /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  var HUBSPOT_SUBMIT = isLocal ? HUBSPOT_DIRECT : HUBSPOT_PROXY;
  var MIN_FILL_MS = 3000; // a submission this fast with no human interaction is a bot
  // Add ?debug=1 to a form page to see on screen what happens when it is sent.
  var DEBUG = /[?&]debug=1(&|$)/.test(location.search);

  function debugLog(form, line) {
    if (!DEBUG) return;
    var box = form.parentNode.querySelector(".form-debug");
    if (!box) {
      box = document.createElement("pre");
      box.className = "form-debug";
      form.parentNode.appendChild(box);
    }
    box.textContent += line + "\n";
  }

  function hubspotCookie() {
    var match = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/);
    return match ? match[1] : undefined;
  }

  document.querySelectorAll("form[data-hubspot-form]").forEach(function (form) {
    var openedAt = Date.now();
    // Real visitors touch, click or type on the page (autofill included);
    // scripted bots do not generate these trusted events.
    var interacted = false;
    ["pointerdown", "touchstart", "keydown", "input"].forEach(function (type) {
      form.addEventListener(type, function (ev) { if (ev.isTrusted) interacted = true; }, { passive: true });
    });
    var button = form.querySelector("button[type='submit']");
    var label = button && button.querySelector(".btn-label");
    var error = form.querySelector(".form-error");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      // Spam traps: a hidden field people never see, and an instant submission.
      // Both only count when nobody touched or typed on the page, so a real
      // visitor is never discarded, even if autofill fills the hidden field.
      // Bots that trip them see the thank-you without anything being sent.
      var trap = form.querySelector(".hp-field input");
      var trapFilled = !!(trap && trap.value);
      var seconds = (Date.now() - openedAt) / 1000;
      debugLog(form, "Human interaction: " + (interacted ? "yes" : "no"));
      debugLog(form, "Hidden field filled: " + (trapFilled ? "yes" : "no"));
      debugLog(form, "Seconds on page: " + seconds.toFixed(1));
      if (!interacted && (trapFilled || seconds * 1000 < MIN_FILL_MS)) {
        debugLog(form, "Result: treated as a bot, nothing sent");
        showSuccess(form);
        return;
      }

      // One entry per field name; ticked checkboxes sharing a name are joined
      // with ";", which is how HubSpot receives multiple-checkbox values.
      var values = {};
      form.querySelectorAll("[name]").forEach(function (field) {
        if (field.closest(".hp-field")) return;
        if (field.type === "checkbox" && !field.checked) return;
        var value = (field.value || "").trim();
        if (!value) return;
        (values[field.name] = values[field.name] || []).push(value);
      });
      var fields = Object.keys(values).map(function (name) {
        return { objectTypeId: "0-1", name: name, value: values[name].join(";") };
      });
      var context = { pageUri: window.location.href, pageName: document.title };
      var hutk = hubspotCookie();
      if (hutk) context.hutk = hutk;

      if (error) error.hidden = true;
      if (button) button.disabled = true;
      if (label) label.textContent = "Sending…";

      var endpoint = HUBSPOT_SUBMIT + form.getAttribute("data-hubspot-portal") + "/" + form.getAttribute("data-hubspot-form");
      debugLog(form, "Sending " + fields.length + " fields to " + endpoint);
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fields: fields, context: context })
      })
        .then(function (res) {
          debugLog(form, "Result: HTTP " + res.status);
          if (!res.ok) throw new Error("HubSpot responded " + res.status);
          showSuccess(form);
        })
        .catch(function (err) {
          debugLog(form, "Failed: " + (err && err.message ? err.message : err));
          if (error) error.hidden = false;
          if (button) button.disabled = false;
          if (label) label.textContent = label.getAttribute("data-default");
        });
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
