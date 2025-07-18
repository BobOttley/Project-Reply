// === SMART Reply App: script.js ===

// === DOM SELECTORS ===
const $ = id => document.getElementById(id);

// Tabs and main panels
const tabInboxBtn = $('tab-inbox');
const tabReplyBtn = $('tab-reply');
const tabInbox = $('tab-inbox-content');
const tabReply = $('tab-reply-content');

// Smart Reply panel elements
const submitBtn = $('submitBtn'), clearBtn = $('clearBtn'),
      loadingSp = $('loading'), replyBox = $('replyBox'), sentimentBox = $('sentimentBox'),
      errorBox = $('errorBox'), textarea = $('parentMessage'),
      instructionEl = $('instructionBox'), urlEl = $('urlBox'),
      reviseEl = $('reviseBox'), reviseBtn = $('reviseBtn'), saveBtn = $('saveBtn'),
      reviseSection = $('reviseSection');

let lastMessage = '', lastReply = '';
textarea && textarea.focus();

// === TAB HANDLING ===
tabInboxBtn.onclick = function() {
  tabInboxBtn.classList.add('active');
  tabReplyBtn.classList.remove('active');
  tabInbox.style.display = 'block';
  tabReply.style.display = 'none';
};
tabReplyBtn.onclick = function() {
  tabReplyBtn.classList.add('active');
  tabInboxBtn.classList.remove('active');
  tabReply.style.display = 'block';
  tabInbox.style.display = 'none';
};

// === INBOX LOGIC ===
let lastInbox = [];
let activeEmailId = null;

// Load inbox on startup and every 20s
window.onload = loadInbox;
setInterval(loadInbox, 20000);

function loadInbox() {
  fetch('/inbox?customer_id=LOCAL-TEST')
    .then(r => r.json())
    .then(data => {
      lastInbox = data;
      renderInboxList();
    });
}

function renderInboxList() {
  const inboxList = $('inbox-list');
  if (!lastInbox.length) {
    inboxList.innerHTML = '<div style="color:#aaa;text-align:center;margin-top:70px;">No new emails found.</div>';
    $('inbox-detail').innerHTML = '<div class="inbox-detail-empty">Select an email to view details.</div>';
    return;
  }
  inboxList.innerHTML = lastInbox.map(email =>
    `<div class="inbox-card${activeEmailId===email.id?' active':''}" onclick="viewEmail(${email.id})">
      <div class="email-subject">${email.subject||'(No subject)'}</div>
      <div class="email-from">${email.from_address||''}
        <span class="email-date">${email.date_received||''}</span>
      </div>
      <div class="email-preview">${email.body||''}</div>
    </div>`
  ).join('');
}

window.viewEmail = function(email_id) {
  activeEmailId = email_id;
  renderInboxList();
  fetch(`/inbox/email/${email_id}?customer_id=LOCAL-TEST`)
    .then(r => r.json())
    .then(email => {
      $('inbox-detail').innerHTML =
        `<div class="email-detail-label">Subject:</div>
        <div class="email-detail-value">${email.subject||'(No subject)'}</div>
        <div class="email-detail-label">From:</div>
        <div class="email-detail-value">${email.from_address||''}</div>
        <div class="email-detail-label">Received:</div>
        <div class="email-detail-value">${email.date_received||''}</div>
        <div class="email-detail-label">Message:</div>
        <div class="email-body-detail">${email.body||''}</div>
        <div class="email-actions">
          <button onclick="replyToEmail(${email.id})">Reply</button>
          <button onclick="dismissEmail(${email.id})" style="background:#d33c3c;">Dismiss</button>
        </div>`;
    });
};

window.dismissEmail = function(email_id) {
  fetch(`/inbox/email/${email_id}/dismiss`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ customer_id: "LOCAL-TEST" })
  }).then(() => {
    activeEmailId = null;
    loadInbox();
  });
};

// When "Reply" in inbox clicked, switch tab and populate textarea
window.replyToEmail = function(email_id) {
  const email = lastInbox.find(e => e.id === email_id);
  if (!email) return alert("Email not found.");
  tabReplyBtn.classList.add('active');
  tabInboxBtn.classList.remove('active');
  tabReply.style.display = 'block';
  tabInbox.style.display = 'none';
  // Build the FULL email context for extraction
  $('parentMessage').value =
    "Subject: " + (email.subject || '') + "\n" +
    "From: " + (email.from_address || '') + "\n" +
    "Received: " + (email.date_received || '') + "\n\n" +
    (email.body || '');
  $('parentMessage').focus();
  setTimeout(() => { $('parentMessage').scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 100);
};


// === MAIN SMART REPLY LOGIC ===

// --- Submit free-text email reply ---
submitBtn.onclick = async () => {
  const message = textarea.value.trim();
  // Assume from_address was stored as a data attribute in window.replyToEmail
  const from_address = textarea.dataset.fromAddress || "";
  const instruction = instructionEl.value.trim();
  const url_box = urlEl?.value.trim() || "";

  if (!message) { alert("Please paste an email before submitting."); return; }
  prepUI("Generating new response…");

  try {
    const r = await fetch("/reply/email", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, instruction, url_box, from_address })
    });
    const data = await r.json();
    if (r.ok && data.reply) {
      lastMessage = message;
      lastReply = data.reply;
      renderReply(data);
    } else {
      throw new Error(data.error || "No reply generated.");
    }
  } catch (err) {
    showError(err.message);
  }
};


// --- Submit structured enquiry form ---
// Call this function on your form submit event instead of submitBtn.onclick if you have a form
async function submitEnquiryForm() {
  const formData = {
    parent_name: document.querySelector('[name="parent_name"]').value.trim(),
    parent_email: document.querySelector('[name="parent_email"]').value.trim(),
    parent_phone: document.querySelector('[name="parent_phone"]').value.trim(),
    child_name: document.querySelector('[name="child_name"]').value.trim(),
    child_year_group: document.querySelector('[name="child_year_group"]').value.trim(),
    additional_comments: document.querySelector('[name="additional_comments"]').value.trim(),
    // add more form fields here as needed
  };

  const instruction = instructionEl.value.trim();
  const url_box = urlEl?.value.trim() || "";
  const customer_id = "LOCAL-TEST";

  if (!formData.parent_email) {
    alert("Please enter a parent email.");
    return;
  }
  prepUI("Generating new response…");

  try {
    const r = await fetch("/reply/form", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ form_data: formData, instruction, url_box, customer_id })
    });
    const data = await r.json();
    if (r.ok && data.reply) {
      lastMessage = JSON.stringify(formData);
      lastReply = data.reply;
      renderReply(data);
    } else {
      throw new Error(data.error || "No reply generated.");
    }
  } catch (err) {
    showError(err.message);
  }
}

// --- Submit on Enter key for textarea ---
textarea.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    submitBtn.click();
  }
});

// --- Revision module ---
reviseBtn.onclick = async () => {
  const instruction = reviseEl.value.trim();
  const url_box = urlEl.value.trim();
  if (!lastMessage || !lastReply) {
    alert("Missing previous reply.");
    return;
  }
  if (!instruction && !url_box) {
    alert("Please enter a revision instruction or updated links.");
    return;
  }
  prepUI("Revising response…");
  try {
    const r = await fetch("/revise", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: lastMessage,
        previous_reply: lastReply,
        instruction,
        url_box
      })
    });
    const data = await r.json();
    if (r.ok && data.reply) {
      lastReply = data.reply;
      renderReply(data);
    } else {
      throw new Error(data.error || "No revision generated.");
    }
  } catch (err) {
    showError(err.message);
  }
};

// --- Save standard reply ---
saveBtn.onclick = async () => {
  if (!lastMessage || !lastReply) { alert("Nothing to save."); return; }
  const urls = urlEl.value.split(';').map(x => x.trim()).filter(Boolean);
  const res = await fetch("/save-standard", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: lastMessage, reply: lastReply, urls })
  });
  $('saveStatus').textContent = res.ok ? "Saved!" : "Error!";
  setTimeout(() => { $('saveStatus').textContent = ''; }, 2000);
};

// --- Clear form ---
clearBtn.onclick = () => {
  ['parentMessage', 'instructionBox', 'urlBox', 'reviseBox'].forEach(id => $(id).value = '');
  lastMessage = lastReply = '';
  ['replyBox', 'sentimentBox', 'errorBox'].forEach(id => { $(id).style.display = 'none'; $(id).innerHTML = ''; });
  reviseSection.style.display = 'none';
  textarea.focus();
};

// === UI HELPERS ===
function prepUI(msg) {
  replyBox.innerHTML = lastReply.replace(/<a /g, '<a target="_blank" rel="noopener noreferrer" ');
  replyBox.style.display = 'block';
  sentimentBox.style.display = 'none';
  errorBox.style.display = 'none';
  submitBtn.disabled = true;
  loadingSp.style.display = 'inline-block';
}

function renderReply(d) {
  replyBox.innerHTML = d.reply;
  replyBox.querySelectorAll("a").forEach(link => {
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noopener noreferrer");
  });
  replyBox.style.display = 'block';
  loadingSp.style.display = 'none';
  submitBtn.disabled = false;
  reviseSection.style.display = 'block';
  if (d.sentiment_score !== undefined) {
    sentimentBox.innerHTML = `<strong>Sentiment Score:</strong> ${d.sentiment_score}/10<br><strong>Strategy:</strong> ${d.strategy_explanation}`;
    sentimentBox.style.display = 'block';
  }
}

function showError(message) {
  loadingSp.style.display = 'none';
  submitBtn.disabled = false;
  errorBox.innerHTML = message;
  errorBox.style.display = 'block';
}
