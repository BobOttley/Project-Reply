// === SMART Reply App: script.js ===

// === DOM SELECTORS ===
const $ = id => document.getElementById(id);
const submitBtn = $('submitBtn'), clearBtn = $('clearBtn'),
      loadingSp = $('loading'), replyBox = $('replyBox'), sentimentBox = $('sentimentBox'),
      errorBox = $('errorBox'), textarea = $('parentMessage'),
      instructionEl = $('instructionBox'), urlEl = $('urlBox'),
      reviseEl = $('reviseBox'), reviseBtn = $('reviseBtn'), saveBtn = $('saveBtn'),
      reviseSection = $('reviseSection');

let lastMessage = '', lastReply = '';
textarea.focus();

// === MAIN REPLY SUBMISSION ===
submitBtn.onclick = async () => {
  const message = textarea.value.trim();
  const instruction = instructionEl.value.trim();
  const url_box = urlEl?.value.trim() || "";
  if (!message) { alert("Please paste an email before submitting."); return; }
  prepUI("Generating new response…");

  try {
    const r = await fetch("/reply", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, instruction, url_box })
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

// === SUBMIT ON ENTER ===
textarea.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    submitBtn.click();
  }
});

// === REVISE MODULE ===
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

// === SAVE STANDARD RESPONSE ===
saveBtn.onclick = async () => {
  if (!lastMessage || !lastReply) { alert("Nothing to save."); return; }
  const urls = urlEl.value.split(';').map(x => x.trim()).filter(Boolean);
  const res = await fetch("/save-standard", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: lastMessage, reply: lastReply, urls })
  });
  document.getElementById('saveStatus').textContent = res.ok ? "Saved!" : "Error!";
  setTimeout(() => { document.getElementById('saveStatus').textContent = ''; }, 2000);
};

// === CLEAR FORM ===
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

// === END ===
