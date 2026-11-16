/* Tidy Edits app. Plain JS, no build step. Everything the customer saves stays on their phone (localStorage).
   Quotes and reviews go to the business inbox through FormSubmit, the same as the website forms.
   The inbox address lives once, in index.html (the quote form's action and the "Email us" link). */
(function () {
  "use strict";
  var PHONE = "857-753-5593";
  // Paste the Google review link here once the Google Business Profile gives it ("Ask for reviews").
  // It is shown to everyone, whatever rating they pick (no review gating).
  var GOOGLE_REVIEW_URL = "";
  var MAX_PHOTOS = 6;

  var SERVICES = [
    ["Recurring house cleaning", "Weekly, every two weeks or monthly upkeep."],
    ["Deep cleaning", "Top to bottom, inside the details people skip."],
    ["Move-in or move-out", "Empty home, every cabinet, ready for keys."],
    ["Rental turnover", "Apartments and units ready for the next tenant."],
    ["Airbnb and short-term rental", "Guest-ready between stays."],
    ["Pre-sale or listing prep", "Show-ready homes for sellers and agents."],
    ["Common areas", "Halls, stairs and entrances in multi-family buildings."],
    ["Office and small business", "One-time or on a schedule that fits your hours."],
    ["Kitchens and baths in detail", "Appliances, cabinets and drawers on request."],
    ["Windows", "Interior and reachable exterior glass."],
    ["Vacant property", "Post-construction dust, empty units, estates."],
    ["Something else", "Tell us the job. We take on all types."]
  ];

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("te." + k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("te." + k, JSON.stringify(v)); } catch (e) {} }
  };
  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    for (var k in attrs || {}) n.setAttribute(k, attrs[k]);
    if (text != null) n.textContent = text;
    return n;
  }
  function icon(id) {
    var ns = "http://www.w3.org/2000/svg", s = document.createElementNS(ns, "svg"), u = document.createElementNS(ns, "use");
    s.setAttribute("class", "ic"); s.setAttribute("aria-hidden", "true"); u.setAttribute("href", "#" + id); s.appendChild(u); return s;
  }
  function say(node, text) { node.textContent = text; node.hidden = !text; }

  /* ---------- Router: #home, #services, #quote, #me, #review, #sent ---------- */
  var VIEWS = ["home", "services", "quote", "me", "review", "sent"];
  var TAB_FOR = { review: "home", sent: "quote" };
  var TITLES = { home: "Tidy Edits app", services: "What we clean · Tidy Edits", quote: "Get a quote · Tidy Edits",
    me: "My home · Tidy Edits", review: "Leave a review · Tidy Edits", sent: "Request sent · Tidy Edits" };
  function route() {
    var name = (location.hash || "#home").slice(1);
    if (VIEWS.indexOf(name) < 0) name = "home";
    document.querySelectorAll(".view").forEach(function (v) { v.classList.toggle("on", v.dataset.view === name); });
    var tab = TAB_FOR[name] || name;
    document.querySelectorAll(".tabs a").forEach(function (a) {
      if (a.dataset.tab === tab) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    document.title = TITLES[name];
    window.scrollTo(0, 0);
    if (name === "me") renderHistory();
    if (name === "quote") prefillQuote();
  }
  window.addEventListener("hashchange", route);

  /* ---------- Services list + quote chips ---------- */
  var list = $("#svc-list"), chips = $("#svc-chips");
  SERVICES.forEach(function (s, i) {
    var b = el("button", { type: "button" });
    b.appendChild(el("strong", null, s[0])); b.appendChild(el("span", null, s[1])); b.appendChild(icon("i-arrow"));
    b.addEventListener("click", function () { pickService(s[0]); location.hash = "#quote"; });
    var li = el("li"); li.appendChild(b); list.appendChild(li);

    var lab = el("label"), inp = el("input", { type: "checkbox", name: "service", value: s[0] });
    lab.appendChild(inp); lab.appendChild(el("span", null, i === SERVICES.length - 1 ? "Another type of job" : s[0])); chips.appendChild(lab);
  });
  function pickService(name) {
    chips.querySelectorAll("input").forEach(function (c) { if (c.value === name) c.checked = true; });
    saveDraft();
  }

  /* ---------- Quote form ---------- */
  var qf = $("#quote-form"), qmsg = $("#q-msg"), qbtn = $("#q-submit");
  var AJAX_ENDPOINT = qf.getAttribute("action").replace("formsubmit.co/", "formsubmit.co/ajax/");
  var MAILTO = ($('a[href^="mailto:"]') || {}).getAttribute ? $('a[href^="mailto:"]').getAttribute("href") : "";
  var photos = []; // { blob, url, name }
  var DRAFT_FIELDS = ["property", "how_often", "town", "date", "size", "notes", "name", "phone", "email", "referred_by"];

  function saveDraft() {
    var d = {};
    DRAFT_FIELDS.forEach(function (f) { d[f] = qf.elements[f].value; });
    d.service = [].map.call(qf.querySelectorAll('input[name="service"]:checked'), function (c) { return c.value; });
    d.reach = (qf.querySelector('input[name="reach_me_by"]:checked') || {}).value;
    store.set("draft", d);
  }
  function loadDraft() {
    var d = store.get("draft", null); if (!d) return;
    DRAFT_FIELDS.forEach(function (f) { if (d[f]) qf.elements[f].value = d[f]; });
    (d.service || []).forEach(pickService);
    if (d.reach) qf.querySelectorAll('input[name="reach_me_by"]').forEach(function (r) { r.checked = r.value === d.reach; });
  }
  function prefillQuote() {
    var me = store.get("me", {});
    ["name", "phone", "email", "town", "size", "notes"].forEach(function (f) { if (me[f] && !qf.elements[f].value) qf.elements[f].value = me[f]; });
  }
  qf.addEventListener("input", saveDraft);
  qf.addEventListener("change", saveDraft);

  // Photos: shrink on the phone first (long side 1600 px, JPEG) so they upload fast on mobile data.
  function shrink(file) {
    return new Promise(function (resolve) {
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        var max = 1600, w = img.naturalWidth, h = img.naturalHeight, k = Math.min(1, max / Math.max(w, h));
        var c = document.createElement("canvas"); c.width = Math.round(w * k); c.height = Math.round(h * k);
        c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        c.toBlob(function (b) { resolve(b || file); }, "image/jpeg", 0.78);
      };
      img.onerror = function () { URL.revokeObjectURL(url); resolve(file); };
      img.src = url;
    });
  }
  function renderPhotos() {
    var g = $("#photo-grid"); g.textContent = "";
    photos.forEach(function (p, i) {
      var f = el("figure"), im = el("img", { src: p.url, alt: "Photo " + (i + 1) }), x = el("button", { type: "button", "aria-label": "Remove photo " + (i + 1) });
      x.appendChild(icon("i-x"));
      x.addEventListener("click", function () { URL.revokeObjectURL(p.url); photos.splice(i, 1); renderPhotos(); });
      f.appendChild(im); f.appendChild(x); g.appendChild(f);
    });
    $("#add-photo-label").textContent = photos.length ? "Add more (" + photos.length + "/" + MAX_PHOTOS + ")" : "Add photos";
  }
  $("#q-photos-pick").addEventListener("change", function (e) {
    var files = [].slice.call(e.target.files || [], 0, MAX_PHOTOS - photos.length);
    e.target.value = "";
    if (!files.length) { say(qmsg, "You can add up to " + MAX_PHOTOS + " photos."); return; }
    say(qmsg, "");
    Promise.all(files.map(shrink)).then(function (blobs) {
      blobs.forEach(function (b) { photos.push({ blob: b, url: URL.createObjectURL(b), name: "photo-" + (photos.length + 1) + ".jpg" }); });
      renderPhotos();
    });
  });

  function remember(entry) {
    var h = store.get("history", []); h.unshift(entry); store.set("history", h.slice(0, 30));
  }

  qf.addEventListener("submit", function (e) {
    e.preventDefault();
    var name = qf.elements.name.value.trim(), phone = qf.elements.phone.value.trim();
    if (!name || !phone) {
      say(qmsg, "Add your name and a phone number so we can reach you.");
      (name ? qf.elements.phone : qf.elements.name).focus();
      return;
    }
    if (!navigator.onLine) { say(qmsg, "You're offline. Your answers are saved here. Send again when you have signal, or call " + PHONE + "."); return; }
    var svc = [].map.call(qf.querySelectorAll('input[name="service"]:checked'), function (c) { return c.value; });
    qf.elements._subject.value = "New quote request from " + name + (svc.length ? ": " + svc.join(", ") : "") + " (Tidy Edits app)";
    qf.elements._next.value = location.origin + "/app/?sent=" + encodeURIComponent(name.split(/\s+/)[0]) + "#sent";

    // Put the shrunk photos into the real file field. Phones that can't do this send without photos and the email says so.
    var holder = $("#q-photos"), attached = 0;
    if (photos.length) {
      try {
        var dt = new DataTransfer();
        photos.forEach(function (p) { dt.items.add(new File([p.blob], p.name, { type: "image/jpeg" })); });
        holder.files = dt.files; attached = holder.files.length;
      } catch (err) { attached = 0; }
    }
    if (photos.length && !attached) qf.elements.notes.value += "\n(Customer added " + photos.length + " photos, but this phone couldn't attach them. Ask them to text the photos to " + PHONE + ".)";
    holder.disabled = !attached;

    var me = store.get("me", {});
    ["name", "phone", "email"].forEach(function (f) { if (!me[f] && qf.elements[f].value) me[f] = qf.elements[f].value.trim(); });
    store.set("me", me);
    remember({ at: new Date().toISOString(), what: svc.join(", ") || "Cleaning quote", town: qf.elements.town.value.trim(), photos: attached });
    store.set("draft", null);
    qbtn.disabled = true; qbtn.textContent = "Sending…";
    say(qmsg, attached ? "Uploading your photos. This can take a few seconds." : "");
    qf.submit(); // Normal form post (needed for photo attachments). FormSubmit sends the customer back to #sent.
  });

  /* ---------- Sent screen: greet by first name ---------- */
  try {
    var sentName = new URLSearchParams(location.search).get("sent");
    if (sentName) { sentName = sentName.trim().slice(0, 30); if (sentName) $("#h-sent").textContent = "Thank you, " + sentName + ". We got your request."; }
  } catch (e) {}

  /* ---------- My home ---------- */
  var mf = $("#me-form"), ME_FIELDS = ["name", "phone", "email", "town", "size", "notes"];
  var saved = store.get("me", {});
  ME_FIELDS.forEach(function (f) { if (saved[f]) mf.elements[f].value = saved[f]; });
  mf.addEventListener("submit", function (e) {
    e.preventDefault();
    var me = {}; ME_FIELDS.forEach(function (f) { me[f] = mf.elements[f].value.trim(); });
    store.set("me", me); greet();
    say($("#m-msg"), "Saved. Your next quote will fill itself in.");
  });
  function renderHistory() {
    var h = store.get("history", []), ul = $("#hist"); ul.textContent = "";
    $("#hist-empty").hidden = h.length > 0;
    h.forEach(function (r) {
      var li = el("li"), d = new Date(r.at);
      li.appendChild(el("strong", null, r.what));
      li.appendChild(el("span", null, "Sent " + d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" }) +
        (r.town ? " · " + r.town : "") + (r.photos ? " · " + r.photos + " photo" + (r.photos > 1 ? "s" : "") : "")));
      ul.appendChild(li);
    });
  }
  $("#share-ref").addEventListener("click", function () {
    var n = (mf.elements.name.value || store.get("me", {}).name || "").trim(), out = $("#ref-out");
    if (!n) { out.textContent = "Add your name above first so we know who to thank."; mf.elements.name.focus(); return; }
    var link = location.origin + "/app/?ref=" + encodeURIComponent(n) + "#quote";
    var text = "I use Tidy Edits for cleaning. Book with my link and we both get $25 off.";
    if (navigator.share) { navigator.share({ title: "Tidy Edits Cleaning", text: text, url: link }).catch(function () {}); out.textContent = link; return; }
    (navigator.clipboard ? navigator.clipboard.writeText(link) : Promise.reject()).then(function () { out.textContent = "Copied: " + link; }, function () { out.textContent = link; });
  });

  /* ---------- Referral link prefill (?ref=Name) ---------- */
  try { var ref = new URLSearchParams(location.search).get("ref"); if (ref) { qf.elements.referred_by.value = ref.slice(0, 60); saveDraft(); } } catch (e) {}

  /* ---------- Review ---------- */
  var rf = $("#rev-form"), rmsg = $("#r-msg"), starsBox = $("#stars"), rating = 0;
  for (var i = 1; i <= 5; i++) (function (n) {
    var lab = el("label"), inp = el("input", { type: "radio", name: "rating", value: String(n) });
    var ns = "http://www.w3.org/2000/svg", s = document.createElementNS(ns, "svg"), u = document.createElementNS(ns, "use");
    s.setAttribute("viewBox", "0 0 24 24"); s.setAttribute("aria-hidden", "true"); u.setAttribute("href", "#i-star"); s.appendChild(u);
    lab.appendChild(inp); lab.appendChild(s); lab.appendChild(el("span", { class: "sr" }, n + " star" + (n > 1 ? "s" : "")));
    inp.addEventListener("change", function () { rating = n; paint(); });
    starsBox.appendChild(lab);
  })(i);
  function paint() { starsBox.querySelectorAll("label").forEach(function (l, i) { l.classList.toggle("lit", i < rating); }); }
  if (GOOGLE_REVIEW_URL) { var g = $("#google-review"); g.href = GOOGLE_REVIEW_URL; g.hidden = false; }
  rf.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!rating && !rf.elements.review.value.trim()) { say(rmsg, "Pick a rating or write a few words first."); return; }
    var data = new FormData(rf), btn = $("#r-submit"), who = rf.elements.name.value.trim() || "a customer";
    data.append("_subject", "New review from " + who + (rating ? " (" + rating + " stars)" : "") + " (Tidy Edits app)");
    data.append("_template", "table");
    btn.disabled = true; btn.textContent = "Sending…";
    fetch(AJAX_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error(); return r.json(); })
      .then(function (res) {
        if (String(res.success) !== "true") throw new Error();
        rf.reset(); rating = 0; paint();
        say(rmsg, "Thank you. Your review went straight to the owner." + (GOOGLE_REVIEW_URL ? " You can also post it on Google below." : ""));
      })
      .catch(function () {
        if (!MAILTO) { say(rmsg, "That didn't send. Please text your review to " + PHONE + "."); return; }
        location.href = MAILTO + "?subject=" + encodeURIComponent("Review for Tidy Edits") + "&body=" +
          encodeURIComponent((rating ? rating + " stars\n\n" : "") + rf.elements.review.value);
        say(rmsg, "Your email app should open with your review filled in. Just press send.");
      })
      .then(function () { btn.disabled = false; btn.textContent = "Send my review"; });
  });

  /* ---------- Greeting ---------- */
  function greet() {
    var n = (store.get("me", {}).name || "").trim().split(/\s+/)[0];
    var h = new Date().getHours(), part = h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening";
    $("#hello").textContent = n ? part + ", " + n + ". Every detail," : "Every detail,";
  }

  /* ---------- Add to home screen ---------- */
  var standalone = matchMedia("(display-mode: standalone)").matches || navigator.standalone;
  var box = $("#install"), ibtn = $("#install-btn"), deferred = null;
  if (!standalone) {
    var ios = /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    if (ios) { $("#install-how").textContent = "In Safari, tap the Share button, then “Add to Home Screen”."; box.classList.add("on"); }
    window.addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); deferred = e; ibtn.hidden = false; box.classList.add("on"); });
    ibtn.addEventListener("click", function () {
      if (!deferred) return;
      deferred.prompt();
      deferred.userChoice.then(function (c) { if (c.outcome === "accepted") box.classList.remove("on"); deferred = null; });
    });
  }

  if ("serviceWorker" in navigator) window.addEventListener("load", function () { navigator.serviceWorker.register("/app/sw.js").catch(function () {}); });

  loadDraft(); greet(); route();
})();
