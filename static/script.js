// === SMART Reply App: script.js ===

// === DOM SELECTORS ===
function getElement(id) {
  return document.getElementById(id);
}

// Tab buttons and panels
const inboxTabButton = getElement('tab-inbox');
const replyTabButton = getElement('tab-reply');
const crmTabButton = getElement('tab-crm');
const inboxTabContent = getElement('tab-inbox-content');
const replyTabContent = getElement('tab-reply-content');
const crmTabContent = getElement('tab-crm-content');

// Smart Reply panel elements
const submitButton = getElement('submitBtn');
const clearButton = getElement('clearBtn');
const loadingSpinner = getElement('loading');
const replyBox = getElement('replyBox');
const sentimentBox = getElement('sentimentBox');
const errorBox = getElement('errorBox');
const parentMessageTextarea = getElement('parentMessage');
const instructionTextarea = getElement('instructionBox');
const urlTextarea = getElement('urlBox');
const reviseTextarea = getElement('reviseBox');
const reviseButton = getElement('reviseBtn');
const saveButton = getElement('saveBtn');
const reviseSection = getElement('reviseSection');

let lastParentMessage = '';
let lastReply = '';
if (parentMessageTextarea) parentMessageTextarea.focus();

// === TAB HANDLING ===
function showTab(tabName) {
  inboxTabContent.style.display = 'none';
  replyTabContent.style.display = 'none';
  crmTabContent.style.display = 'none';
  inboxTabButton.classList.remove('active');
  replyTabButton.classList.remove('active');
  crmTabButton.classList.remove('active');

  if (tabName === 'inbox') {
    inboxTabContent.style.display = 'block';
    inboxTabButton.classList.add('active');
  } else if (tabName === 'reply') {
    replyTabContent.style.display = 'block';
    replyTabButton.classList.add('active');
  } else if (tabName === 'crm') {
    crmTabContent.style.display = 'block';
    crmTabButton.classList.add('active');
    clearCrmResults();
  }
}

inboxTabButton.onclick = function() { showTab('inbox'); };
replyTabButton.onclick = function() { showTab('reply'); };
crmTabButton.onclick = function() { showTab('crm'); };

showTab('inbox');

// === INBOX LOGIC ===
let inboxEmailList = [];
let activeEmailId = null;

window.onload = loadInbox;
setInterval(loadInbox, 20000);

function loadInbox() {
  fetch('/inbox?customer_id=LOCAL-TEST')
    .then(response => response.json())
    .then(data => {
      inboxEmailList = data;
      renderInboxList();
    });
}

function renderInboxList() {
  const inboxListElement = getElement('inbox-list');
  if (!inboxEmailList.length) {
    inboxListElement.innerHTML = '<div style="color:#aaa;text-align:center;margin-top:70px;">No new emails found.</div>';
    getElement('inbox-detail').innerHTML = '<div class="inbox-detail-empty">Select an email to view details.</div>';
    return;
  }
  inboxListElement.innerHTML = inboxEmailList.map(email =>
    `<div class="inbox-card${activeEmailId === email.id ? ' active' : ''}" onclick="viewEmail(${email.id})">
      <div class="email-subject">${email.subject || '(No subject)'}</div>
      <div class="email-from">${email.from_address || ''}
        <span class="email-date">${email.date_received || ''}</span>
      </div>
      <div class="email-preview">${email.body || ''}</div>
    </div>`
  ).join('');
}

window.viewEmail = function(emailId) {
  activeEmailId = emailId;
  renderInboxList();
  fetch(`/inbox/email/${emailId}?customer_id=LOCAL-TEST`)
    .then(response => response.json())
    .then(email => {
      getElement('inbox-detail').innerHTML =
        `<div class="email-detail-label">Subject:</div>
        <div class="email-detail-value">${email.subject || '(No subject)'}</div>
        <div class="email-detail-label">From:</div>
        <div class="email-detail-value">${email.from_address || ''}</div>
        <div class="email-detail-label">Received:</div>
        <div class="email-detail-value">${email.date_received || ''}</div>
        <div class="email-detail-label">Message:</div>
        <div class="email-body-detail">${email.body || ''}</div>
        <div class="email-actions">
          <button onclick="replyToEmail(${email.id})">Reply</button>
          <button onclick="dismissEmail(${email.id})" style="background:#d33c3c;">Dismiss</button>
        </div>`;
    });
};

window.dismissEmail = function(emailId) {
  fetch(`/inbox/email/${emailId}/dismiss`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ customer_id: "LOCAL-TEST" })
  }).then(() => {
    activeEmailId = null;
    loadInbox();
  });
};

window.replyToEmail = function(emailId) {
  const email = inboxEmailList.find(e => e.id === emailId);
  if (!email) return alert("Email not found.");
  showTab('reply');
  getElement('parentMessage').value =
    "Subject: " + (email.subject || '') + "\n" +
    "From: " + (email.from_address || '') + "\n" +
    "Received: " + (email.date_received || '') + "\n\n" +
    (email.body || '');
  getElement('parentMessage').focus();
  setTimeout(() => { getElement('parentMessage').scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 100);
};

// === SMART REPLY LOGIC ===

submitButton.onclick = async () => {
  const message = parentMessageTextarea.value.trim();
  const fromAddress = parentMessageTextarea.dataset.fromAddress || "";
  const instruction = instructionTextarea.value.trim();
  const urlBox = urlTextarea?.value.trim() || "";

  if (!message) {
    alert("Please paste an email before submitting.");
    return;
  }
  prepUI("Generating new response…");

  try {
    const response = await fetch("/reply/email", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, instruction, url_box: urlBox, from_address: fromAddress })
    });
    const data = await response.json();
    if (response.ok && data.reply) {
      lastParentMessage = message;
      lastReply = data.reply;
      renderReply(data);
      // Optional: If reply triggers CRM account creation, ensure CRM tab starts blank on next open
      clearCrmResults();
    } else {
      throw new Error(data.error || "No reply generated.");
    }
  } catch (err) {
    showError(err.message);
  }
};

parentMessageTextarea.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    submitButton.click();
  }
});

reviseButton.onclick = async () => {
  const instruction = reviseTextarea.value.trim();
  const urlBox = urlTextarea.value.trim();
  if (!lastParentMessage || !lastReply) {
    alert("Missing previous reply.");
    return;
  }
  if (!instruction && !urlBox) {
    alert("Please enter a revision instruction or updated links.");
    return;
  }
  prepUI("Revising response…");
  try {
    const response = await fetch("/revise", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: lastParentMessage,
        previous_reply: lastReply,
        instruction,
        url_box: urlBox
      })
    });
    const data = await response.json();
    if (response.ok && data.reply) {
      lastReply = data.reply;
      renderReply(data);
    } else {
      throw new Error(data.error || "No revision generated.");
    }
  } catch (err) {
    showError(err.message);
  }
};

saveButton.onclick = async () => {
  if (!lastParentMessage || !lastReply) {
    alert("Nothing to save.");
    return;
  }
  const urls = urlTextarea.value.split(';').map(x => x.trim()).filter(Boolean);
  const response = await fetch("/save-standard", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: lastParentMessage, reply: lastReply, urls })
  });
  getElement('saveStatus').textContent = response.ok ? "Saved!" : "Error!";
  setTimeout(() => { getElement('saveStatus').textContent = ''; }, 2000);
};

clearButton.onclick = () => {
  ['parentMessage', 'instructionBox', 'urlBox', 'reviseBox'].forEach(id => getElement(id).value = '');
  lastParentMessage = lastReply = '';
  ['replyBox', 'sentimentBox', 'errorBox'].forEach(id => { getElement(id).style.display = 'none'; getElement(id).innerHTML = ''; });
  reviseSection.style.display = 'none';
  parentMessageTextarea.focus();
};

function prepUI(message) {
  replyBox.innerHTML = lastReply.replace(/<a /g, '<a target="_blank" rel="noopener noreferrer" ');
  replyBox.style.display = 'block';
  sentimentBox.style.display = 'none';
  errorBox.style.display = 'none';
  submitButton.disabled = true;
  loadingSpinner.style.display = 'inline-block';
}

function renderReply(data) {
  replyBox.innerHTML = data.reply;
  replyBox.querySelectorAll("a").forEach(link => {
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noopener noreferrer");
  });
  replyBox.style.display = 'block';
  loadingSpinner.style.display = 'none';
  submitButton.disabled = false;
  reviseSection.style.display = 'block';
  if (data.sentiment_score !== undefined) {
    sentimentBox.innerHTML = `<strong>Sentiment Score:</strong> ${data.sentiment_score}/10<br><strong>Strategy:</strong> ${data.strategy_explanation}`;
    sentimentBox.style.display = 'block';
  }
}

function showError(message) {
  loadingSpinner.style.display = 'none';
  submitButton.disabled = false;
  errorBox.innerHTML = message;
  errorBox.style.display = 'block';
}

// === CRM LOGIC ===

function clearCrmResults() {
  getElement('crm-results').innerHTML = '';
  getElement('crm-clear-btn').style.display = 'none';
}

getElement('crm-search-btn').onclick = function() {
  const query = getElement('crm-search').value.trim();
  if (query) {
    fetchAccounts(query);
    getElement('crm-clear-btn').style.display = 'inline-block';
  }
};

getElement('crm-clear-btn').onclick = function() {
  clearCrmResults();
  getElement('crm-search').value = '';
};

function fetchAccounts(query) {
  fetch('/api/accounts/search?q=' + encodeURIComponent(query))
    .then(response => response.json())
    .then(accounts => {
      const html = accounts.length
        ? accounts.map(account => `
            <div class="crm-result-card">
              <div class="crm-result-header">${account.name ? account.name : '(No name)'}</div>
              <div class="crm-result-fields">
                <span class="crm-result-label">Email:</span>
                <span class="crm-result-value">${account.email ? account.email : '-'}</span><br>
                <span class="crm-result-label">Child:</span>
                <span class="crm-result-value">${account.child_name ? account.child_name : '-'}</span><br>
                <span class="crm-result-label">Stage:</span>
                <span class="crm-result-value">${account.admissions_stage ? account.admissions_stage : '-'}</span>
              </div>
              <div class="crm-result-actions">
                <button onclick="viewAccount(${account.id})">View</button>
              </div>
            </div>
          `).join('')
        : '<div style="color:#aaa;text-align:center;padding:2em;">No accounts found.</div>';
      getElement('crm-results').innerHTML = html;
      if (query) {
        getElement('crm-clear-btn').style.display = 'inline-block';
      } else {
        getElement('crm-clear-btn').style.display = 'none';
      }
    });
}

getElement('crm-add-form').onsubmit = function(event) {
  event.preventDefault();
  const form = event.target;
  const data = {
    name: form.name.value,
    email: form.email.value,
    phone: form.phone.value,
    child_name: form.child_name.value,
    admissions_stage: form.year_group.value, // corrected to match your form input
    notes: form.notes.value
  };
  fetch('/api/accounts', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(response => response.json()).then(result => {
    if(result.success){
      alert('Account added!');
      clearCrmResults();
      form.reset();
    } else {
      alert('Error: ' + (result.error || 'Unknown'));
    }
  });
};

window.viewAccount = function(id) {
  fetch('/api/accounts/' + id)
    .then(response => response.json())
    .then(account => {
      if(account.error) return alert(account.error);
      alert(
        `Name: ${account.name || ''}\nEmail: ${account.email}\nPhone: ${account.phone || '-'}\nChild: ${account.child_name || '-'}\nStage: ${account.admissions_stage || '-'}\nNotes: ${account.notes || '-'}\nCreated: ${account.created_at}\nUpdated: ${account.updated_at}`
      );
    });
};
