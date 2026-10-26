"""The /plan/ page: an interactive "plan your clean" builder.

Visitors tap through a few choices and get a tailored cleaning plan on the spot
(no prices). They can then send the plan with their contact details as a quote
request through the same FormSubmit endpoint the home page uses.
"""
import json
from html import escape

PLAN_CSS = """
/* Plan your clean */
.planner { display: grid; grid-template-columns: 1.25fr 1fr; gap: var(--space-4); align-items: start; padding-block: var(--space-2) var(--section); }
.planner fieldset { border: 0; margin: 0; padding: var(--space-3) 0; border-top: 1px solid var(--line); min-width: 0; }
.planner fieldset:first-child { border-top: 1px solid var(--ink); }
.planner legend { font-family: var(--display); font-size: var(--step-1); padding: 0; margin-bottom: 14px; }
.planner legend small { font-family: var(--body); font-size: var(--step--1); color: var(--muted); margin-left: 8px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chips label { position: relative; }
.chips input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.chips span { display: inline-block; padding: 10px 16px; border: 1px solid var(--line); border-radius: 999px; background: var(--paper); cursor: pointer; transition: border-color 150ms var(--ease), background 150ms var(--ease), color 150ms var(--ease); }
.chips span:hover { border-color: var(--tan); }
.chips input:checked + span { background: var(--walnut); border-color: var(--walnut); color: var(--on-walnut); }
.chips input:focus-visible + span { outline: 2px solid var(--walnut); outline-offset: 2px; }
.plan-card { position: sticky; top: 96px; background: var(--paper); border: 1px solid var(--line); border-radius: var(--radius); padding: var(--space-3); display: grid; gap: 14px; }
.plan-card h2 { font-size: var(--step-2); line-height: 1.1; }
.plan-card .meta { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; color: var(--muted); }
.plan-card .meta b { color: var(--ink); font-weight: 600; }
.plan-card .ticks { grid-template-columns: 1fr; gap: 8px; }
.plan-card .empty { color: var(--muted); }
.plan-form { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; border-top: 1px solid var(--line); padding-top: 14px; }
.plan-form .field { display: grid; gap: 6px; min-width: 0; }
.plan-form .full { grid-column: 1 / -1; }
.plan-form label { font-weight: 600; font-size: 0.93rem; }
.plan-form input { font: inherit; color: var(--ink); background: var(--linen); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; width: 100%; }
.plan-form input:focus { outline: 2px solid var(--walnut); outline-offset: 0; border-color: var(--walnut); }
.plan-form .btn { width: 100%; justify-content: center; }
.plan-msg { color: var(--muted); font-size: var(--step--1); }
@media (max-width: 860px) { .planner { grid-template-columns: 1fr; } .plan-card { position: static; } }
@media (max-width: 420px) { .plan-form { grid-template-columns: 1fr; } }
"""

STEPS = [
    ("property", "The place", "radio", ["House", "Apartment or condo", "Multi-family building", "Office or business", "Short-term rental", "Vacant property"]),
    ("job", "The job", "radio", ["Move-in or move-out", "Deep clean", "Recurring cleaning", "Rental turnover", "Airbnb turnover", "Pre-sale or listing prep", "Common areas", "Office cleaning", "Something else"]),
    ("size", "Size", "radio", ["Studio or 1 bedroom", "2 bedrooms", "3 bedrooms", "4+ bedrooms", "Small office or unit", "Whole building"]),
    ("condition", "Condition right now", "radio", ["Pretty tidy", "Lived-in", "Needs real work", "Empty"]),
    ("when", "When", "radio", ["This week", "Next 2 weeks", "This month", "Ongoing schedule", "Just planning"]),
    ("extras", "Extras", "checkbox", ["Inside fridge", "Inside oven", "Inside cabinets", "Interior windows", "Laundry", "Stairs and hallways"]),
]

# Which service page and checklist each job maps to.
JOB_SERVICE = {
    "Move-in or move-out": "move-out-cleaning",
    "Deep clean": "deep-cleaning",
    "Recurring cleaning": "recurring-house-cleaning",
    "Rental turnover": "rental-turnover-cleaning",
    "Airbnb turnover": "airbnb-cleaning",
    "Pre-sale or listing prep": "listing-prep-cleaning",
    "Common areas": "common-area-cleaning",
    "Office cleaning": "office-cleaning",
}


def step_html(name, legend, kind, options):
    hint = " <small>pick any</small>" if kind == "checkbox" else ""
    chips = "".join(
        f'<label><input type="{kind}" name="{name}" value="{escape(o)}"><span>{escape(o)}</span></label>'
        for o in options
    )
    return f'<fieldset><legend>{escape(legend)}{hint}</legend><div class="chips">{chips}</div></fieldset>'


def plan_body(services, guides):
    svc = {
        job: {
            "name": s["name"],
            "url": f"/services/{s['slug']}/",
            "included": s["included"],
            "guide": next((f"/guides/{g['slug']}/" for g in guides if g["slug"] == s["guide"]), None),
        }
        for job, slug in JOB_SERVICE.items()
        for s in services if s["slug"] == slug
    }
    steps = "".join(step_html(*st) for st in STEPS)
    data = json.dumps(svc).replace("</", "<\\/")
    return f"""    <div class="hero" style="padding-bottom: var(--space-3)"><h1>Plan your clean in one minute</h1><p class="lede">Tap what fits your place and get a cleaning plan right away. Send it to us if you'd like a free quote. We do all types of cleaning jobs, so pick the closest match.</p></div>
    <div class="planner">
      <form id="plan-choices" onsubmit="return false">{steps}</form>
      <aside class="plan-card" aria-live="polite">
        <h2 id="p-title">Your cleaning plan</h2>
        <div id="p-body"><p class="empty">Pick the place and the job to see your plan.</p></div>
        <form class="plan-form" id="plan-form" novalidate>
          <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
          <div class="field"><label for="p-name">Name</label><input id="p-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="p-phone">Phone</label><input id="p-phone" name="phone" type="tel" autocomplete="tel" required></div>
          <div class="field"><label for="p-email">Email</label><input id="p-email" name="email" type="email" autocomplete="email" spellcheck="false"></div>
          <div class="field"><label for="p-town">Town</label><input id="p-town" name="town" autocomplete="address-level2"></div>
          <div class="full"><button class="btn btn-solid" id="p-submit" type="submit">Send my plan for a free quote</button></div>
          <p class="plan-msg full" id="p-msg">We reply within one business day. No spam, no sharing your details.</p>
        </form>
      </aside>
    </div>
<script>
(function () {{
  var SVC = {data};
  var ENDPOINT = "https://formsubmit.co/ajax/info@tidyedits.com";
  var choices = document.getElementById("plan-choices");
  var body = document.getElementById("p-body"), title = document.getElementById("p-title");
  var form = document.getElementById("plan-form"), msg = document.getElementById("p-msg");
  var EXTRA_TASK = {{
    "Inside fridge": "Inside the fridge, shelves and drawers",
    "Inside oven": "Inside the oven and racks",
    "Inside cabinets": "Inside cabinets and drawers",
    "Interior windows": "Interior windows, sills and tracks",
    "Laundry": "Laundry washed and folded on site",
    "Stairs and hallways": "Stairs, railings and hallways"
  }};
  function pick() {{
    var d = new FormData(choices), o = {{ extras: d.getAll("extras") }};
    ["property", "job", "size", "condition", "when"].forEach(function (k) {{ o[k] = d.get(k) || ""; }});
    return o;
  }}
  function el(tag, text) {{ var e = document.createElement(tag); if (text) e.textContent = text; return e; }}
  function crew(o) {{
    if (o.size === "Whole building" || o.property === "Multi-family building") return "A full team, scheduled around your building";
    if (o.size === "4+ bedrooms" || o.condition === "Needs real work") return "A small team, so it's done in one visit";
    return "One or two cleaners who know your place";
  }}
  function notes(o) {{
    var n = [];
    if (o.job === "Move-in or move-out" || o.job === "Rental turnover") n.push("Near September 1? Book early. Good dates go fast.");
    if (o.condition === "Needs real work" && o.job === "Recurring cleaning") n.push("We'd suggest one deep clean first, so every regular visit stays quick.");
    if (o.job === "Airbnb turnover") n.push("Send your check-out and check-in times and we'll plan around them.");
    if (o.job === "Pre-sale or listing prep") n.push("Tell us your photo date. We aim to finish the day before.");
    if (o.when === "This week") n.push("This week: call or text 857-753-5593 for the fastest answer.");
    return n;
  }}
  function render() {{
    var o = pick(), s = SVC[o.job];
    body.textContent = "";
    if (!o.job && !o.property) {{ body.appendChild(el("p", "Pick the place and the job to see your plan.")).className = "empty"; return; }}
    title.textContent = s ? s.name : (o.job === "Something else" ? "A custom clean" : "Your cleaning plan");
    var meta = el("ul"); meta.className = "meta";
    [["Place", [o.property, o.size].filter(Boolean).join(", ")], ["Crew", crew(o)], ["Timing", o.when]].forEach(function (r) {{
      if (!r[1]) return; var li = el("li"); li.appendChild(el("b", r[0] + ": ")); li.appendChild(document.createTextNode(r[1])); meta.appendChild(li);
    }});
    body.appendChild(meta);
    var tasks = (s ? s.included.slice() : ["Every room cleaned to the same detailed standard", "Kitchens and bathrooms detailed", "Floors vacuumed and washed"]);
    o.extras.forEach(function (x) {{ if (tasks.indexOf(EXTRA_TASK[x]) < 0) tasks.push(EXTRA_TASK[x]); }});
    var ul = el("ul"); ul.className = "ticks"; tasks.forEach(function (t) {{ ul.appendChild(el("li", t)); }}); body.appendChild(ul);
    notes(o).forEach(function (t) {{ body.appendChild(el("p", t)).className = "note"; }});
    if (s) {{
      var p = el("p"); p.className = "note"; var a = el("a", "More about " + s.name.toLowerCase()); a.href = s.url; p.appendChild(a);
      if (s.guide) {{ p.appendChild(document.createTextNode(" · ")); var g = el("a", "free checklist"); g.href = s.guide; p.appendChild(g); }}
      body.appendChild(p);
    }}
  }}
  choices.addEventListener("change", render);
  form.addEventListener("submit", function (e) {{
    e.preventDefault();
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || !phone) {{ msg.textContent = "Add your name and a phone number so we can reach you."; (name ? form.elements.phone : form.elements.name).focus(); return; }}
    var o = pick(), data = new FormData(form);
    ["property", "job", "size", "condition", "when"].forEach(function (k) {{ if (o[k]) data.append(k, o[k]); }});
    if (o.extras.length) data.append("extras", o.extras.join(", "));
    data.append("source", "Plan your clean page");
    data.append("_subject", "New cleaning plan from " + name + (o.job ? ": " + o.job : "") + " (tidyedits.com/plan)");
    data.append("_template", "table");
    var btn = document.getElementById("p-submit"); btn.disabled = true; btn.textContent = "Sending…";
    fetch(ENDPOINT, {{ method: "POST", body: data, headers: {{ Accept: "application/json" }} }})
      .then(function (r) {{ if (!r.ok) throw new Error(); return r.json(); }})
      .then(function (res) {{ if (String(res.success) !== "true") throw new Error(); location.href = "/thank-you/?name=" + encodeURIComponent(name); }})
      .catch(function () {{
        var lines = []; data.forEach(function (v, k) {{ if (k[0] !== "_" && String(v).trim()) lines.push(k + ": " + v); }});
        location.href = "mailto:info@tidyedits.com?subject=" + encodeURIComponent("Cleaning plan from " + name) + "&body=" + encodeURIComponent(lines.join("\\n"));
        msg.textContent = "Your email app should open with your plan filled in. Just press send, or call or text 857-753-5593.";
      }})
      .then(function () {{ btn.disabled = false; btn.textContent = "Send my plan for a free quote"; }});
  }});
}})();
</script>
"""
