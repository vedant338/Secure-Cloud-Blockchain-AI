/**
 * Secure Cloud Blockchain AI - Frontend
 */
const API_BASE = "http://localhost:8000";
const TOKEN_KEY = "secure_cloud_token";
const USER_KEY = "secure_cloud_user";
const USER_JOINED_KEY = "secure_cloud_joined";
const USER_LAST_ACTIVE_KEY = "secure_cloud_last_active";
const STORAGE_KEY = "secure_cloud_uploads";

// --- Auth ---
function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setAuth(token, username) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, username);
  const now = new Date().toISOString();
  if (!localStorage.getItem(USER_JOINED_KEY)) {
    localStorage.setItem(USER_JOINED_KEY, now);
  }
  updateLastActive();
}

function updateLastActive() {
  localStorage.setItem(USER_LAST_ACTIVE_KEY, new Date().toISOString());
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem(USER_JOINED_KEY);
  localStorage.removeItem(USER_LAST_ACTIVE_KEY);
}

function isLoggedIn() {
  return !!getToken();
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// --- Storage ---
function getStoredFiles() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

function saveFile(meta) {
  const files = getStoredFiles();
  const entry = {
    id: meta.filename || `file_${Date.now()}`,
    filename: meta.filename,
    originalName: meta.originalName || meta.filename,
    hash: meta.hash,
    signature: meta.signature,
    publicKey: meta.public_key,
    aesKey: meta.aes_key,
    nonce: meta.nonce,
    aiRisk: meta.ai_analysis?.risk,
    uploadedAt: new Date().toISOString(),
  };
  files.unshift(entry);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(files));
  return entry;
}

// --- API ---
async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health/`);
    const data = await res.json();
    setHealthStatus(res.ok ? "up" : "down", data);
  } catch (err) {
    setHealthStatus("down", { error: err.message });
  }
}

async function login(username, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) {
    const err = await parseErrorResponse(res);
    throw new Error(err);
  }
  return res.json();
}

async function register(username, password) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) {
    const err = await parseErrorResponse(res);
    throw new Error(err);
  }
  return res.json();
}

async function uploadFile(file) {
  if (!file || file.size === 0) throw new Error("Please select a non-empty file.");
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/upload/upload/upload`, {
    method: "POST",
    headers: authHeaders(),
    body: formData,
  });
  if (!res.ok) throw new Error(await parseErrorResponse(res));
  return res.json();
}

async function downloadFile(meta) {
  const params = new URLSearchParams({
    filename: meta.filename,
    aes_key: meta.aesKey,
    nonce: meta.nonce,
    expected_hash: meta.hash,
    signature_hex: meta.signature,
    public_key_pem: meta.publicKey,
  });
  if (meta.originalName) params.set("original_filename", meta.originalName);
  const res = await fetch(`${API_BASE}/download/download/file?${params}`, {
    method: "POST",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(await parseErrorResponse(res));
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = meta.originalName || meta.filename.replace(".enc", "") || "download";
  a.click();
  URL.revokeObjectURL(url);
}

async function parseErrorResponse(res) {
  if (res.status === 401) {
    clearAuth();
    showAuth();
    throw new Error("Session expired. Please sign in again.");
  }
  try {
    const body = await res.json();
    if (body.detail) return typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
  } catch {}
  return (await res.text()) || `Request failed (${res.status})`;
}

async function doDownload(btn, meta) {
  btn.disabled = true;
  btn.textContent = "Downloading...";
  try {
    updateLastActive();
    await downloadFile(meta);
  } catch (err) {
    alert("Download failed: " + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Download";
  }
}

// --- UI ---
function setHealthStatus(status, data) {
  const badge = document.getElementById("healthBadge");
  if (!badge) return;
  badge.className = "health-badge " + status;
  const text = badge.querySelector(".health-text");
  if (text) text.textContent = status === "up" ? "Online" : "Offline";
  badge.title = JSON.stringify(data, null, 2);
}

function escapeHtml(s) {
  if (s == null) return "";
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}

function showUploadResult(data, originalName) {
  const box = document.getElementById("uploadResult");
  box.classList.remove("hidden");
  const risk = data.ai_analysis?.risk || "N/A";
  const riskClass = risk === "HIGH" ? "risk-high" : "risk-low";
  box.innerHTML = `
    <div class="result-success">
      <h4>✓ Upload successful</h4>
      <p><strong>File:</strong> ${escapeHtml(originalName)}</p>
      <p><strong>Risk:</strong> <span class="risk-badge ${riskClass}">${risk}</span></p>
      <button type="button" class="btn btn-secondary btn-sm download-just-uploaded" data-file-id="${escapeHtml(data.filename)}">Download</button>
      <p class="hint">Use My Files to download later.</p>
    </div>
  `;
  box.querySelector(".download-just-uploaded")?.addEventListener("click", async function () {
    const meta = getStoredFiles().find((f) => f.id === this.dataset.fileId);
    if (meta) await doDownload(this, meta);
  });
}

function showUploadError(msg) {
  const box = document.getElementById("uploadResult");
  box.classList.remove("hidden");
  box.innerHTML = `<div class="result-error"><h4>Upload failed</h4><p>${escapeHtml(msg)}</p></div>`;
}

function renderFileCard(entry) {
  const div = document.createElement("div");
  div.className = "file-card";
  div.dataset.fileId = entry.id;
  const riskClass = entry.aiRisk === "HIGH" ? "risk-high" : "risk-low";
  div.innerHTML = `
    <div class="file-card-header">
      <span class="file-name">${escapeHtml(entry.originalName || entry.filename)}</span>
      <span class="risk-badge ${riskClass}">${escapeHtml(entry.aiRisk || "N/A")}</span>
    </div>
    <div class="file-card-body">
      <p><strong>Uploaded:</strong> ${new Date(entry.uploadedAt).toLocaleString()}</p>
      <div class="file-card-actions">
        <button type="button" class="btn btn-secondary btn-sm" data-action="download">Download</button>
      </div>
    </div>
  `;
  return div;
}

function renderRecentFile(entry) {
  const div = document.createElement("div");
  div.className = "file-item";
  div.dataset.fileId = entry.id;
  const riskClass = entry.aiRisk === "HIGH" ? "risk-high" : "risk-low";
  div.innerHTML = `
    <span class="file-name">${escapeHtml(entry.originalName || entry.filename)}</span>
    <span class="risk-badge ${riskClass}">${escapeHtml(entry.aiRisk || "N/A")}</span>
    <span class="file-date">${new Date(entry.uploadedAt).toLocaleDateString()}</span>
    <button type="button" class="btn btn-secondary btn-sm" data-action="download">Download</button>
  `;
  return div;
}

function refreshFileLists() {
  const files = getStoredFiles();
  const list = document.getElementById("filesList");
  const noFiles = document.getElementById("noFiles");
  if (list && noFiles) {
    list.innerHTML = "";
    if (files.length === 0) {
      list.classList.add("hidden");
      noFiles.classList.remove("hidden");
    } else {
      list.classList.remove("hidden");
      noFiles.classList.add("hidden");
      files.forEach((f) => list.appendChild(renderFileCard(f)));
    }
  }
  const recent = document.getElementById("recentFilesList");
  if (recent) {
    recent.innerHTML = "";
    files.slice(0, 5).forEach((f) => recent.appendChild(renderRecentFile(f)));
    if (files.length === 0) recent.innerHTML = '<p class="empty-hint">No uploads yet.</p>';
  }
}

function switchView(viewId) {
  document.querySelectorAll(".view").forEach((v) => v.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
  const view = document.getElementById(`view-${viewId}`);
  const btn = document.querySelector(`[data-view="${viewId}"]`);
  if (view) view.classList.add("active");
  if (btn) btn.classList.add("active");
  refreshFileLists();
}

function showApp() {
  document.getElementById("authScreen").classList.add("hidden");
  document.getElementById("appScreen").classList.remove("hidden");
  const username = localStorage.getItem(USER_KEY) || "";
  document.getElementById("userBadge").textContent = username;
  document.getElementById("userDetailName").textContent = username;
  const joined = localStorage.getItem(USER_JOINED_KEY);
  document.getElementById("userDetailJoined").textContent = joined
    ? new Date(joined).toLocaleDateString()
    : "—";
  initApp();
}

function showAuth() {
  document.getElementById("authScreen").classList.remove("hidden");
  document.getElementById("appScreen").classList.add("hidden");
}

// --- Auth event handlers ---
function initAuth() {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");
  const loginTab = document.querySelector('[data-tab="login"]');
  const registerTab = document.querySelector('[data-tab="register"]');

  document.querySelectorAll(".auth-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".auth-tab").forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      const isLogin = tab.dataset.tab === "login";
      loginForm.classList.toggle("hidden", !isLogin);
      registerForm.classList.toggle("hidden", isLogin);
      document.getElementById("authError").classList.add("hidden");
      document.getElementById("authErrorReg").classList.add("hidden");
    });
  });

  loginForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const errEl = document.getElementById("authError");
    errEl.classList.add("hidden");
    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value;
    try {
      const data = await login(username, password);
      setAuth(data.token, data.username);
      showApp();
    } catch (err) {
      errEl.textContent = err.message;
      errEl.classList.remove("hidden");
    }
  });

  registerForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const errEl = document.getElementById("authErrorReg");
    errEl.classList.add("hidden");
    const username = document.getElementById("registerUsername").value.trim();
    const password = document.getElementById("registerPassword").value;
    try {
      const data = await register(username, password);
      setAuth(data.token, data.username);
      showApp();
    } catch (err) {
      errEl.textContent = err.message;
      errEl.classList.remove("hidden");
    }
  });
}

// --- App event handlers ---
function initApp() {
  checkHealth();
  setInterval(checkHealth, 30000);

  document.querySelectorAll("[data-view]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      if (el.dataset.view) {
        updateLastActive();
        switchView(el.dataset.view);
      }
    });
  });

  updateLastActive();
  const userTrigger = document.getElementById("userTrigger");
  const userPanel = document.getElementById("userPanel");
  const userMenuWrap = document.querySelector(".user-menu-wrap");
  const lastActiveEl = document.getElementById("userLastActive");

  function updateLastActiveDisplay() {
    const last = localStorage.getItem(USER_LAST_ACTIVE_KEY);
    lastActiveEl.textContent = last
      ? new Date(last).toLocaleString()
      : "—";
  }

  userTrigger?.addEventListener("click", (e) => {
    e.stopPropagation();
    updateLastActive();
    const isOpen = !userPanel.classList.toggle("hidden");
    userMenuWrap?.classList.toggle("open", !isOpen);
    if (!userPanel.classList.contains("hidden")) {
      updateLastActiveDisplay();
    }
  });

  document.addEventListener("click", () => {
    userPanel.classList.add("hidden");
    userMenuWrap?.classList.remove("open");
  });

  userPanel?.addEventListener("click", (e) => e.stopPropagation());

  document.getElementById("logoutBtn")?.addEventListener("click", () => {
    clearAuth();
    showAuth();
  });

  document.getElementById("helpBtn")?.addEventListener("click", () => {
    alert("GUPTALAYA BLOCKSTORE\n\n• Upload: Encrypt and store files with AI risk analysis.\n• My Files: View and download your uploaded files.\n• Your keys are stored locally for decryption.");
  });

  const zone = document.getElementById("uploadZone");
  const input = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");

  const setFile = (file) => {
    if (file) {
      zone.classList.add("has-file");
      zone.querySelector("p").textContent = file.name;
      uploadBtn.disabled = false;
      zone._file = file;
    } else {
      zone.classList.remove("has-file");
      zone.querySelector("p").innerHTML = 'Drop a file here or <button type="button" class="link-btn" onclick="document.getElementById(\'fileInput\').click()">browse</button>';
      uploadBtn.disabled = true;
      zone._file = null;
    }
  };

  input?.addEventListener("change", () => setFile(input.files[0] || null));

  zone?.addEventListener("dragover", (e) => { e.preventDefault(); zone.classList.add("drag-over"); });
  zone?.addEventListener("dragleave", () => zone.classList.remove("drag-over"));
  zone?.addEventListener("drop", (e) => {
    e.preventDefault();
    zone.classList.remove("drag-over");
    const f = e.dataTransfer?.files?.[0];
    if (f) setFile(f);
  });

  uploadBtn?.addEventListener("click", async () => {
    const file = zone?._file;
    if (!file) return;
    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";
    try {
      const data = await uploadFile(file);
      saveFile({ ...data, originalName: file.name });
      updateLastActive();
      showUploadResult(data, file.name);
      setFile(null);
      input.value = "";
      refreshFileLists();
    } catch (err) {
      showUploadError(err.message);
    } finally {
      uploadBtn.disabled = false;
      uploadBtn.textContent = "Upload";
    }
  });

  document.getElementById("filesList")?.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-action='download']");
    if (!btn) return;
    e.preventDefault();
    const id = btn.closest(".file-card")?.dataset?.fileId;
    const meta = id ? getStoredFiles().find((f) => f.id === id) : null;
    if (meta) doDownload(btn, meta);
  });

  document.getElementById("recentFilesList")?.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-action='download']");
    if (!btn) return;
    e.preventDefault();
    const id = btn.closest(".file-item")?.dataset?.fileId;
    const meta = id ? getStoredFiles().find((f) => f.id === id) : null;
    if (meta) doDownload(btn, meta);
  });

  refreshFileLists();
}

// --- Init ---
document.addEventListener("DOMContentLoaded", () => {
  initAuth();
  if (isLoggedIn()) {
    showApp();
  } else {
    showAuth();
  }
});
