/* DCS PCCC Takeoff – giao diện */
"use strict";
const UI_VERSION = "1.0.3"; // build.py tự đồng bộ với __version__

/* ------------------------------------------------------------------ icons */
const IC = {
  home: '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  folder: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
  file: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
  pages: '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
  shapes: '<circle cx="7" cy="7" r="3"/><rect x="14" y="4" width="6" height="6" rx="1.5"/><path d="M7 13.5 11 20H3z"/><path d="M14 17h7M17.5 13.5v7"/>',
  table: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16"/>',
  book: '<path d="M5 4h9a4 4 0 0 1 4 4v12H9a4 4 0 0 1-4-4z"/><path d="M18 20H9a4 4 0 0 1-4-4"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
  check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
  x: '<path d="M6 6l12 12M18 6 6 18"/>',
  alert: '<path d="M10.3 3.9 2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17v.5"/>',
  download: '<path d="M12 4v11M7 10l5 5 5-5"/><path d="M4 20h16"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
  zin: '<circle cx="11" cy="11" r="7"/><path d="M8 11h6M11 8v6"/><path d="m20 20-4-4"/>',
  zout: '<circle cx="11" cy="11" r="7"/><path d="M8 11h6"/><path d="m20 20-4-4"/>',
  fit: '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>',
  trash: '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
  loader: '<path d="M12 3a9 9 0 1 0 9 9"/>',
  arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  spark: '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
  eyeoff: '<path d="M3 3l18 18"/><path d="M10.6 6.1A9.8 9.8 0 0 1 12 6c5 0 9 6 9 6a17 17 0 0 1-3.1 3.6M6.4 7.5C4.2 9.1 3 12 3 12s4 6 9 6a9 9 0 0 0 4.2-1"/>',
  flame: '<path d="M12 3c1 4 5 5.5 5 10a5 5 0 0 1-10 0c0-2.5 1.5-3.6 2-5 1 1.5 1.2 3 2.2 3 0-3-1.2-5 .8-8z"/>',
  ruler: '<path d="M3 17 17 3l4 4L7 21z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  ext: '<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
  layers: '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
  target: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
  shield: '<path d="M12 3 4 6v6c0 4.5 3.4 8 8 9 4.6-1 8-4.5 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
  excel: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m9 12 4 5M13 12l-4 5"/>',
  edit: '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
  bolt: '<path d="M13 3 5 14h6l-1 7 8-11h-6z"/>',
  left: '<path d="M19 12H5M11 6l-6 6 6 6"/>',
};
const ico = (n, cls = "") => `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">${IC[n] || ""}</svg>`;

/* ------------------------------------------------------------------ helpers */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = (n, d = 0) => (Number(n) || 0).toLocaleString("vi-VN", { maximumFractionDigits: d, minimumFractionDigits: 0 });
const fmtQ = (n, unit) => fmt(n, unit === "m" ? 1 : 0);
const fdate = (s) => { if (!s) return ""; const d = new Date(s); return d.toLocaleDateString("vi-VN") + " " + d.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }); };
const SYS_COLOR = { CC: "#ED1844", BC: "#F97316", EX: "#10B981", LOA: "#8B5CF6", HK: "#0891B2", TMB: "#64748B", KHAC: "#64748B" };
const SYS_SHORT = { CC: "Chữa cháy", BC: "Báo cháy", EX: "Đèn thoát nạn", LOA: "Loa", HK: "Hút khói", TMB: "Tổng mặt bằng", KHAC: "Khác" };
const sysChip = (c) => `<span class="chip sys" style="background:${SYS_COLOR[c] || "#64748B"}">${esc(SYS_SHORT[c] || c)}</span>`;
const UNITS = ["cái", "bộ", "hộp", "bình", "tủ", "trụ", "vị trí", "m"];

let API = null;
async function call(name, ...args) {
  try {
    return await API[name](...args);
  } catch (e) {
    toast("Có lỗi: " + (e && e.message ? e.message : e), true);
    throw e;
  }
}

function toast(msg, err = false, actions = []) {
  const t = document.createElement("div");
  t.className = "toast" + (err ? " err" : "");
  t.innerHTML = ico(err ? "alert" : "check") + `<div>${msg}${actions.map((a, i) => `<a data-i="${i}">${esc(a.label)}</a>`).join("")}</div>`;
  $$("a", t).forEach((a) => (a.onclick = () => actions[+a.dataset.i].fn()));
  $("#toasts").appendChild(t);
  setTimeout(() => { t.style.transition = "opacity .3s"; t.style.opacity = 0; setTimeout(() => t.remove(), 300); }, actions.length ? 9000 : 3500);
}

/* ------------------------------------------------------------------ state */
const S = {
  info: null, view: "home", projects: [], pid: null, prj: null, tab: "pages",
  selPage: null, pFilter: "all", pSys: "all", pQ: "", sFilter: "all", sQ: "", sView: "symbols",
  resTab: "sum", result: null, sAll: false, geomCache: new Map(), hiKey: null, polling: null,
};

/* ------------------------------------------------------------------ shell */
function renderNav() {
  // Menu trái chỉ chứa phần CHUNG của phần mềm. Các bước của dự án nằm trong màn hình dự án.
  const cur = S.view === "ws" || S.view === "processing" ? "home" : S.view;
  const items = [
    { id: "home", ic: "layers", label: "Dự án", count: S.projects.length || "" },
    { id: "library", ic: "book", label: "Thư viện ký hiệu" },
    { id: "about", ic: "info", label: "Giới thiệu" },
  ];
  $("#nav").innerHTML = `<button class="btn primary nav-new" id="navNew">${ico("plus")} Tạo dự án mới</button>
    <div class="sec">Menu</div>` +
    items.map((it) => `<a data-id="${it.id}" class="${cur === it.id ? "active" : ""}">${ico(it.ic)}<span>${it.label}</span>${it.count ? `<span class="count">${it.count}</span>` : ""}</a>`).join("");
  $("#navNew").onclick = () => openNewProject();
  $$("#nav a").forEach((a) => (a.onclick = () => { S.view = a.dataset.id; render(); }));
}

/* Thanh điều hướng của dự án: "← Dự án › Tên dự án" */
function crumbs(name, meta = "") {
  return `<button class="btn ghost icon-btn" id="tBack" title="Về danh sách dự án">${ico("left")}</button>
    <div class="pj-ic">${ico("layers")}</div>
    <div class="bc"><div class="bc-path"><a id="tAll">Dự án</a><span>›</span></div>
      <div class="bc-title"><h1>${esc(name)}</h1>${meta ? `<span class="pj-meta">${meta}</span>` : ""}</div></div>`;
}
function bindCrumbs() {
  const go = () => { S.view = "home"; render(); };
  const b = $("#tBack"), a = $("#tAll");
  if (b) b.onclick = go;
  if (a) a.onclick = go;
}

function setTop(html) {
  $("#topbar").innerHTML = html;
  document.body.classList.toggle("in-project", S.view === "ws" || S.view === "processing");
}

async function render() {
  stopPolling();
  renderNav();
  const v = $("#view");
  v.className = "view";
  if (S.view === "home") return renderHome();
  if (S.view === "processing") return renderProcessing();
  if (S.view === "ws") return renderWorkspace();
  if (S.view === "library") return renderLibrary();
  if (S.view === "about") return renderAbout();
}

/* ------------------------------------------------------------------ home */
async function renderHome() {
  setTop(`<h1>Dự án</h1><span class="crumb">· Danh sách dự án bóc tách</span><div class="grow"></div><button class="btn primary" id="tNew">${ico("plus")} Tạo dự án mới</button>`);
  $("#tNew").onclick = openNewProject;
  S.projects = await call("list_projects");
  renderNav();
  const v = $("#view");
  const feats = [
    ["bolt", "#EDF3FF", "#055FD1", "Đọc thẳng file DWG", "Tự chuyển đổi, không cần mở AutoCAD hay xuất DXF thủ công."],
    ["target", "#FDECEF", "#ED1844", "Đếm & đo tự động", "Đếm thiết bị, đo chiều dài ống và dây theo từng trang, từng tầng."],
    ["shield", "#E7F8F1", "#059669", "Chống đếm trùng", "Tự bỏ trang đối chiếu, sơ đồ 3D, bảng chú thích và ống vẽ lặp."],
    ["excel", "#FFF6E6", "#D97706", "Xuất Excel chuẩn", "Bảng tổng hợp, chi tiết theo trang, danh sách cần kiểm tra."],
  ];
  v.innerHTML = `
  <div class="hero">
    <div>
      <span class="eyebrow">${ico("flame")} DC Software · PCCC Takeoff</span>
      <h2>Bóc tách khối lượng PCCC<br>từ bản vẽ CAD <span>trong vài phút</span></h2>
      <p>Tải bộ bản vẽ DWG lên, phần mềm tự chia trang, nhận diện ký hiệu, đếm thiết bị và đo chiều dài đường ống – người dùng chỉ việc xác nhận và xuất Excel.</p>
      <div class="actions">
        <button class="btn lg white" id="hNew">${ico("folder")} Chọn thư mục bản vẽ</button>
        <button class="btn lg glass" id="hFiles">${ico("file")} Chọn file DWG</button>
      </div>
    </div>
    <div class="steps3">
      <div class="step3"><div class="n">1</div><div><b>Tải bản vẽ</b><span>Chọn thư mục chứa file .dwg và thư mục Xref đi kèm</span></div></div>
      <div class="step3"><div class="n">2</div><div><b>Kiểm tra & xác nhận</b><span>Chọn trang cần tính, xác nhận ký hiệu là vật tư gì</span></div></div>
      <div class="step3"><div class="n">3</div><div><b>Xuất bảng khối lượng</b><span>File Excel theo hệ, theo tòa nhà, theo tầng</span></div></div>
    </div>
  </div>
  <div class="section-h"><h3>Tất cả dự án</h3><span class="muted">${S.projects.length} dự án</span></div>
  <div id="plist"></div>
  <div class="section-h"><h3>Phần mềm làm được gì</h3></div>
  <div class="features">${feats.map(([i, bg, fg, b, s]) => `<div class="card feat"><div class="fi" style="background:${bg};color:${fg}">${ico(i)}</div><b>${b}</b><span>${s}</span></div>`).join("")}</div>`;
  $("#hNew").onclick = () => openNewProject("folder");
  $("#hFiles").onclick = () => openNewProject("files");
  const pl = $("#plist");
  if (!S.projects.length) {
    pl.innerHTML = `<div class="card empty">${ico("folder")}<b>Chưa có dự án nào</b><span>Bấm “Chọn thư mục bản vẽ” để bắt đầu dự án đầu tiên.</span></div>`;
    return;
  }
  pl.className = "grid-proj";
  pl.innerHTML = S.projects.map((p) => `
    <div class="card proj" data-id="${p.id}">
      <button class="btn ghost icon-btn del" data-del="${p.id}" title="Xoá dự án">${ico("trash")}</button>
      <div class="row"><div class="ic">${ico("layers")}</div>
        <div style="min-width:0"><h4>${esc(p.name)}</h4><div class="meta">${ico("clock", "").replace("<svg", '<svg style="width:12px;height:12px;vertical-align:-2px"')} ${fdate(p.updated)}</div></div></div>
      <div class="row" style="flex-wrap:wrap;gap:6px">${p.id === S.pid ? '<span class="chip ok"><span class="dot"></span>Đang mở</span>' : ""}${(p.systems || []).map(sysChip).join("")}
        ${p.status === "ready" ? "" : p.status === "empty" ? '<span class="chip info">Chưa có bản vẽ</span>' : p.status === "error" ? '<span class="chip bad">Lỗi xử lý</span>' : '<span class="chip warn">Chưa xử lý xong</span>'}</div>
      <div class="stats"><div><b>${p.files}</b>file bản vẽ</div><div><b>${p.pages_used}<span class="muted" style="font-size:13px;font-weight:500">/${p.pages}</span></b>trang được tính</div><div><b>${p.symbols}</b>loại ký hiệu</div></div>
    </div>`).join("");
  $$(".proj", pl).forEach((c) => (c.onclick = (e) => {
    if (e.target.closest("[data-del]")) return;
    openProject(c.dataset.id);
  }));
  $$("[data-del]", pl).forEach((b) => (b.onclick = async (e) => {
    e.stopPropagation();
    const p = S.projects.find((x) => x.id === b.dataset.del);
    if (!confirm(`Xoá dự án “${p.name}”?\nFile bản vẽ gốc của bạn không bị ảnh hưởng.`)) return;
    await call("delete_project", p.id);
    if (S.pid === p.id) { S.pid = null; S.prj = null; }
    toast("Đã xoá dự án");
    renderNav();
    renderHome();
  }));
}

/* ------------------------------------------------------------------ new project / drawings */
function openNewProject(mode) { openDrawingDialog({ kind: "new", pick: mode }); }

/* kind: "new" = tạo dự án mới; "replace" = thêm / thay bản vẽ cho dự án đang mở */
async function openDrawingDialog({ kind = "new", pick = null } = {}) {
  let files = [], paths = [];
  const isNew = kind === "new";
  const hasOld = !isNew && S.prj && S.prj.files && S.prj.files.some((f) => f.role === "main");
  const bg = document.createElement("div");
  bg.className = "modal-bg";
  bg.innerHTML = `<div class="modal">
    <div class="mh">${ico(isNew ? "plus" : "folder").replace("<svg", '<svg style="width:20px;height:20px;color:var(--brand)"')}<h3>${isNew ? "Tạo dự án mới" : hasOld ? "Cập nhật bản vẽ" : "Thêm bản vẽ cho dự án"}</h3><div class="grow"></div><button class="btn ghost icon-btn" id="mClose">${ico("x")}</button></div>
    <div class="mb">
      ${isNew ? `<label class="field" style="margin-bottom:16px">Tên dự án<input class="input" id="mName" placeholder="Ví dụ: Nhà máy Youngone Bắc Giang"></label>` : ""}
      ${hasOld ? `<div class="infoline">${ico("info")}<div>Phần mềm sẽ <b>xử lý lại toàn bộ</b> với bộ bản vẽ mới. Ký hiệu bạn đã xác nhận vẫn được giữ (lấy từ thư viện); việc chọn trang và hệ số tầng sẽ được tính lại.</div></div>` : ""}
      <div class="drop" id="mDrop">
        ${ico("folder", "big")}
        <div><b style="color:var(--ink);font-size:15px">Chọn bộ bản vẽ CAD</b><div class="muted" style="margin-top:4px">Nên chọn cả thư mục để phần mềm lấy luôn thư mục <b>Xref</b> (khung tên, bản vẽ nền)</div></div>
        <div class="row"><button class="btn primary" id="mFolder">${ico("folder")} Chọn thư mục</button><button class="btn" id="mFiles">${ico("file")} Chọn file .dwg</button></div>
      </div>
      <div id="mFiles2"></div>
    </div>
    <div class="mf"><span class="muted grow" id="mSum" style="align-self:center;font-size:13px"></span><button class="btn" id="mCancel">Huỷ</button><button class="btn primary" id="mGo" disabled></button></div>
  </div>`;
  document.body.appendChild(bg);
  const close = () => bg.remove();
  $("#mClose", bg).onclick = close;
  $("#mCancel", bg).onclick = close;
  const mains = () => files.filter((f) => f.role === "main");
  const update = () => {
    const m = mains().length, x = files.filter((f) => f.role === "xref").length;
    const name = isNew ? $("#mName", bg).value.trim() : "";
    const go = $("#mGo", bg), sum = $("#mSum", bg);
    if (m) {
      go.innerHTML = `${ico("bolt")} ${isNew || !hasOld ? "Bắt đầu xử lý" : "Xử lý lại với bản vẽ mới"}`;
      go.disabled = isNew && !name;
      const tot = files.reduce((acc, f) => acc + f.size, 0);
      sum.textContent = `${m} bản vẽ chính, ${x} bản vẽ nền · ${fmt(tot / 1048576, 1)} MB` + (x ? "" : " · ⚠ không thấy thư mục Xref");
      if (isNew && !name) sum.textContent = "Nhập tên dự án để bắt đầu";
    } else if (isNew) {
      go.innerHTML = `${ico("plus")} Tạo dự án, thêm bản vẽ sau`;
      go.disabled = !name;
      sum.textContent = name ? "Chưa chọn bản vẽ – có thể tạo dự án trước, thêm bản vẽ sau" : "Nhập tên dự án, rồi chọn bộ bản vẽ (có thể chọn sau)";
    } else {
      go.innerHTML = `${ico("bolt")} Bắt đầu xử lý`;
      go.disabled = true;
      sum.textContent = "Hãy chọn thư mục hoặc file bản vẽ";
    }
  };
  const showFiles = () => {
    const xrefs = files.filter((f) => f.role === "xref");
    const row = (f) => `<div class="fr">${ico("file").replace("<svg", '<svg style="width:16px;height:16px;color:var(--muted)"')}<span class="nm">${esc(f.name)}</span>${f.role === "main" ? sysChip(f.system) : '<span class="chip ghost">Xref</span>'}<span class="muted mono">${fmt(f.size / 1048576, 1)} MB</span></div>`;
    $("#mFiles2", bg).innerHTML = files.length ? `<div class="filelist">
      <div class="grp">Bản vẽ chính · ${mains().length}</div>${mains().map(row).join("")}
      ${xrefs.length ? `<div class="grp">Bản vẽ nền (Xref) · ${xrefs.length}</div>${xrefs.map(row).join("")}` : ""}</div>` : "";
    update();
  };
  const doPick = async (how) => {
    const r = how === "folder" ? await call("pick_folder") : await call("pick_files");
    const sel = how === "folder" ? (r ? [r] : []) : (r || []);
    if (!sel.length) return;
    const sc = await call("scan", sel);
    if (sc.error) return toast(sc.error, true);
    if (!sc.files.some((f) => f.role === "main")) return toast("Không tìm thấy file .dwg/.dxf trong lựa chọn này", true);
    paths = sel; files = sc.files;
    if (isNew && !$("#mName", bg).value) $("#mName", bg).value = sc.suggested_name || "";
    showFiles();
  };
  $("#mFolder", bg).onclick = () => doPick("folder");
  $("#mFiles", bg).onclick = () => doPick("files");
  if (isNew) $("#mName", bg).oninput = update;
  $("#mGo", bg).onclick = async () => {
    $("#mGo", bg).disabled = true;
    if (isNew) {
      const name = $("#mName", bg).value.trim() || "Dự án mới";
      const r = await call("create_project", name, paths);
      if (r.error) { update(); return toast(r.error, true); }
      close();
      if (r.processing) { S.pid = r.id; S.prj = { name, status: "processing" }; S.view = "processing"; return render(); }
      await loadProject(r.id);
      S.view = "ws"; S.tab = "pages"; render();
      toast(`Đã tạo dự án “${esc(name)}”`);
    } else {
      const r = await call("set_drawings", S.pid, paths);
      if (r.error) { update(); return toast(r.error, true); }
      close();
      S.prj = { ...S.prj, status: "processing" }; S.view = "processing"; render();
    }
  };
  update();
  if (isNew) setTimeout(() => $("#mName", bg).focus(), 50);
  if (pick) doPick(pick);
}

/* ------------------------------------------------------------------ processing */
const STAGES = [["convert", "Chuyển đổi DWG sang DXF"], ["read", "Đọc bản vẽ"], ["pages", "Chia trang theo khung tên"], ["symbols", "Nhận diện ký hiệu"], ["done", "Hoàn tất"]];
function stopPolling() { if (S.polling) { clearInterval(S.polling); S.polling = null; } }
function renderProcessing() {
  setTop(`${crumbs(S.prj?.name || "Dự án", "Đang xử lý bản vẽ")}`);
  bindCrumbs();
  const v = $("#view");
  v.innerHTML = `<div class="card proc">
      <div class="row"><div style="width:52px;height:52px;border-radius:14px;background:var(--grad);display:grid;place-items:center;color:#fff">${ico("loader", "spin").replace("<svg", '<svg style="width:26px;height:26px"')}</div>
      <div><h2>Đang xử lý bộ bản vẽ</h2><div class="muted">Bộ bản vẽ cỡ trung bình mất khoảng 1–2 phút. Bạn có thể để phần mềm chạy.</div></div></div>
      <div class="bar"><i id="pBar" style="width:2%"></i></div>
      <div class="row muted" style="font-size:13px"><span id="pMsg">Chuẩn bị…</span><div class="grow"></div><span id="pPct">0%</span><span>·</span><span id="pTime">0 giây</span></div>
      <div class="stages" id="pStages"></div>
      <div class="logbox mono" id="pLog"></div>
    </div>`;
  const tick = async () => {
    const pr = await API.progress(S.pid);
    const idx = Math.max(0, STAGES.findIndex((s) => s[0] === pr.stage));
    $("#pBar").style.width = Math.max(2, Math.round((pr.pct || 0) * 100)) + "%";
    $("#pPct").textContent = Math.round((pr.pct || 0) * 100) + "%";
    $("#pMsg").textContent = pr.msg || "";
    $("#pTime").textContent = fmt(pr.elapsed || 0) + " giây";
    $("#pStages").innerHTML = STAGES.map(([k, l], i) => {
      const st = pr.stage === "done" || i < idx ? "done" : i === idx ? "cur" : "";
      return `<div class="stage ${st}"><div class="si">${st === "done" ? ico("check") : st === "cur" ? ico("loader", "spin") : ""}</div>${l}</div>`;
    }).join("");
    $("#pLog").innerHTML = (pr.log || []).slice(-6).map(esc).join("<br>");
    if (pr.done) {
      stopPolling();
      if (pr.error) {
        $("#pMsg").textContent = "Lỗi: " + pr.error;
        toast("Xử lý không thành công: " + pr.error, true);
        return;
      }
      await loadProject(S.pid);
      toast(`Đã xử lý xong ${S.prj.pages.length} trang bản vẽ`);
      S.view = "ws"; S.tab = "pages"; render();
    }
  };
  tick();
  S.polling = setInterval(tick, 700);
}

/* ------------------------------------------------------------------ project */
async function loadProject(pid) {
  S.prj = await call("get_project", pid);
  S.pid = pid;
  S.result = null;
  S.geomCache.clear();
  if (!S.selPage || !S.prj.pages.find((p) => p.id === S.selPage)) {
    const first = S.prj.pages.find((p) => p.include) || S.prj.pages[0];
    S.selPage = first ? first.id : null;
  }
}
async function openProject(pid) {
  const pr = await API.progress(pid);
  if (pr && pr.stage !== "idle" && !pr.done) { S.pid = pid; S.prj = { name: "", status: "processing" }; S.view = "processing"; return render(); }
  await loadProject(pid);
  if (S.prj.status === "empty") { S.view = "ws"; S.tab = "pages"; return render(); }
  if (S.prj.status !== "ready") {
    if (confirm(S.prj.status === "error" ? `Dự án bị lỗi ở lần xử lý trước:\n${S.prj.error}\n\nXử lý lại?` : "Dự án chưa xử lý xong. Xử lý lại?")) {
      await call("start_processing", pid);
      S.view = "processing";
      return render();
    }
    return;
  }
  S.view = "ws"; S.tab = "pages";
  render();
}

function renderEmptyProject() {
  const p = S.prj;
  setTop(`${crumbs(p.name, "Chưa có bản vẽ")}<div class="grow"></div>
    <button class="btn" id="tRen">${ico("edit")} Đổi tên</button>`);
  bindCrumbs();
  $("#tRen").onclick = async () => { const n = prompt("Tên dự án", p.name); if (n && n.trim()) { p.name = await call("rename_project", S.pid, n.trim()); renderEmptyProject(); } };
  const v = $("#view");
  v.className = "view";
  v.innerHTML = `<div class="card" style="max-width:760px;margin:6vh auto 0"><div class="empty" style="padding:56px 32px">
      <div style="width:64px;height:64px;border-radius:18px;background:var(--soft);display:grid;place-items:center;margin-bottom:16px">${ico("folder").replace("<svg", '<svg style="width:30px;height:30px;color:var(--brand);margin:0"')}</div>
      <b style="font-size:18px">Dự án chưa có bản vẽ</b>
      <span style="max-width:460px;line-height:1.6;margin-top:6px">Thêm bộ bản vẽ CAD (.dwg) của dự án. Nên chọn cả thư mục để phần mềm lấy luôn thư mục <b>Xref</b> đi kèm.</span>
      <div class="row" style="margin-top:22px"><button class="btn primary lg" id="eFolder">${ico("folder")} Chọn thư mục bản vẽ</button><button class="btn lg" id="eFiles">${ico("file")} Chọn file DWG</button></div>
    </div></div>`;
  $("#eFolder").onclick = () => openDrawingDialog({ kind: "replace", pick: "folder" });
  $("#eFiles").onclick = () => openDrawingDialog({ kind: "replace", pick: "files" });
}

function renderWorkspace() {
  const p = S.prj;
  if (!p.files || !p.files.some((f) => f.role === "main")) return renderEmptyProject();
  const unk = p.symbols.filter((s) => s.count > 0 && !s.map).length;
  setTop(`${crumbs(p.name, `${p.files.filter((f) => f.role === "main").length} bản vẽ · ${p.pages.length} trang${p.process_seconds ? ` · xử lý ${fmt(p.process_seconds)} giây` : ""}`)}
    <div class="grow"></div>
    <button class="btn" id="tRen">${ico("edit")} Đổi tên</button>
    <button class="btn" id="tDraw">${ico("folder")} Cập nhật bản vẽ</button>
    <button class="btn primary" id="tExp">${ico("download")} Xuất Excel</button>`);
  bindCrumbs();
  $("#tExp").onclick = exportExcel;
  $("#tDraw").onclick = () => openDrawingDialog({ kind: "replace" });
  $("#tRen").onclick = async () => {
    const n = prompt("Tên dự án", p.name);
    if (n && n.trim()) { p.name = await call("rename_project", S.pid, n.trim()); renderWorkspace(); }
  };
  const v = $("#view");
  v.className = "view flush";
  const tabs = [
    ["pages", "1", "Trang bản vẽ", `${p.pages.filter((x) => x.include).length}/${p.pages.length} trang được tính`],
    ["symbols", "2", "Ký hiệu & vật tư", unk ? `${unk} ký hiệu chưa xác định` : "Đã xác định đủ"],
    ["results", "3", "Kết quả", "Bảng khối lượng"],
  ];
  v.innerHTML = `<div class="ws-head"><span class="ws-label">Các bước</span><div class="tabs">${tabs.map(([k, n, l, s]) => `<div class="tab ${S.tab === k ? "on" : ""}" data-t="${k}"><div class="tn">${n}</div><div>${l}<small>${s}</small></div></div>`).join('<span class="step-sep"></span>')}</div></div><div class="ws-body" id="wsBody"></div>`;
  $$(".tab", v).forEach((t) => (t.onclick = () => { S.tab = t.dataset.t; renderWorkspace(); }));
  if (S.tab === "pages") renderPagesTab();
  else if (S.tab === "symbols") renderSymbolsTab();
  else renderResultsTab();
}

/* ------------------------------------------------------------------ pages tab */
function pageStatus(pg) { return pg.include ? (pg.warnings.length ? "warn" : "on") : "off"; }
function filteredPages() {
  const q = S.pQ.trim().toLowerCase();
  return S.prj.pages.filter((pg) => {
    if (S.pFilter === "on" && !pg.include) return false;
    if (S.pFilter === "off" && pg.include) return false;
    if (S.pFilter === "warn" && !(pg.include && pg.warnings.length)) return false;
    if (S.pSys !== "all" && pg.system !== S.pSys) return false;
    if (q && !(pg.title.toLowerCase().includes(q) || (pg.building || "").toLowerCase().includes(q))) return false;
    return true;
  });
}
function renderPagesTab() {
  const p = S.prj;
  const body = $("#wsBody");
  const systems = [...new Set(p.pages.map((x) => x.system))];
  const n = { all: p.pages.length, on: p.pages.filter((x) => x.include).length, off: p.pages.filter((x) => !x.include).length, warn: p.pages.filter((x) => x.include && x.warnings.length).length };
  body.innerHTML = `
    <div class="pane-list">
      <div class="tools">
        <div class="search">${ico("search")}<input class="input" id="pQ" placeholder="Tìm theo tiêu đề, tòa nhà…" value="${esc(S.pQ)}"></div>
        <div class="seg" id="pF">${[["all", "Tất cả"], ["on", "Được tính"], ["off", "Bỏ qua"], ["warn", "Cảnh báo"]].map(([k, l]) => `<button data-k="${k}" class="${S.pFilter === k ? "on" : ""}">${l}<span class="n">${n[k]}</span></button>`).join("")}</div>
        <div class="row" style="gap:8px"><span class="muted" style="font-size:12.5px;white-space:nowrap">Hệ thống</span><select class="input sm" id="pS"><option value="all">Tất cả hệ (${p.pages.length} trang)</option>${systems.map((s) => `<option value="${s}" ${S.pSys === s ? "selected" : ""}>${SYS_SHORT[s] || s} (${p.pages.filter((x) => x.system === s).length} trang)</option>`).join("")}</select>
          <button class="btn sm" id="pAllOn" title="Tính tất cả trang đang lọc">${ico("check")}</button></div>
      </div>
      <div class="plist" id="plist"></div>
    </div>
    <div class="pane-view" id="pview"></div>`;
  $("#pQ").oninput = (e) => { S.pQ = e.target.value; drawPageList(); };
  $$("#pF button").forEach((b) => (b.onclick = () => { S.pFilter = b.dataset.k; renderPagesTab(); }));
  $("#pS").onchange = (e) => { S.pSys = e.target.value; renderPagesTab(); };
  $("#pAllOn").onclick = async () => {
    const list = filteredPages().filter((x) => !x.include);
    if (!list.length) return toast("Các trang đang lọc đều đã được tính");
    if (!confirm(`Bật tính ${list.length} trang đang hiển thị?`)) return;
    list.forEach((x) => (x.include = true));
    await call("bulk_include", S.pid, list.map((x) => x.id), true);
    S.result = null; await refreshCounts(); renderPagesTab(); renderNav();
  };
  drawPageList();
  drawPageView();
}
function drawPageList() {
  const pages = filteredPages();
  const byFile = new Map();
  pages.forEach((pg) => { if (!byFile.has(pg.file)) byFile.set(pg.file, []); byFile.get(pg.file).push(pg); });
  const el = $("#plist");
  if (!pages.length) { el.innerHTML = `<div class="empty">${ico("search")}<b>Không có trang phù hợp</b></div>`; return; }
  el.innerHTML = [...byFile.entries()].map(([fid, list]) => {
    const f = S.prj.files.find((x) => x.id === fid) || {};
    return `<div class="pgrp"><span class="bar2" style="background:${SYS_COLOR[f.system] || "#94A3B8"}"></span>${esc(SYS_SHORT[f.system] || "")} · ${esc(f.name || "")}</div>` +
      list.map((pg) => `<div class="pitem ${pg.include ? "" : "off"} ${S.selPage === pg.id ? "sel" : ""}" data-id="${pg.id}">
        <label class="switch" title="${pg.include ? "Đang tính – bấm để bỏ" : "Đang bỏ qua – bấm để tính"}"><input type="checkbox" ${pg.include ? "checked" : ""} data-inc="${pg.id}"><span></span></label>
        <div class="pn">#${pg.index}</div>
        <div style="min-width:0;flex:1"><div class="pt">${esc(pg.title)}</div>
          <div class="pm">${pg.include ? `<span class="chip info">${esc(pg.building)}</span>${pg.floor_label ? `<span class="chip">${esc(pg.floor_label)}</span>` : ""}${pg.multiplier != 1 ? `<span class="chip warn">× ${fmt(pg.multiplier, 2)} tầng</span>` : ""}${pg.n_symbols ? `<span class="chip ghost">${fmt(pg.n_symbols)} ký hiệu</span>` : ""}${pg.warnings.length ? `<span class="chip warn">${ico("alert").replace("<svg", '<svg style="width:12px;height:12px"')} ${pg.warnings.length}</span>` : ""}`
          : `<span class="chip ghost">${esc(pg.auto_reason || "Đã bỏ chọn")}</span>`}</div></div>
      </div>`).join("");
  }).join("");
  $$(".pitem", el).forEach((it) => (it.onclick = (e) => {
    if (e.target.closest(".switch")) return;
    S.selPage = it.dataset.id; S.hiKey = null;
    $$(".pitem.sel", el).forEach((x) => x.classList.remove("sel"));
    it.classList.add("sel");
    drawPageView();
  }));
  $$("[data-inc]", el).forEach((cb) => (cb.onchange = async () => {
    const pg = S.prj.pages.find((x) => x.id === cb.dataset.inc);
    pg.include = cb.checked;
    await call("update_page", S.pid, pg.id, { include: pg.include });
    S.result = null;
    refreshCounts();
    drawPageList();
    if (S.selPage === pg.id) drawPageView();
    renderNav();
  }));
}
async function refreshCounts() {
  const fresh = await call("get_project", S.pid);
  S.prj.symbols = fresh.symbols; S.prj.layers = fresh.layers;
}

function symMap(key) { const s = S.prj.symbols.find((x) => x.key === key); return s ? s.map : null; }
function symState(key) { const m = symMap(key); return !m ? "none" : m.ignore ? "ignore" : "ok"; }

async function drawPageView() {
  const pv = $("#pview");
  const pg = S.prj.pages.find((x) => x.id === S.selPage);
  if (!pg) { pv.innerHTML = `<div class="card empty">${ico("pages")}<b>Chọn một trang ở danh sách bên trái</b></div>`; return; }
  const f = S.prj.files.find((x) => x.id === pg.file) || {};
  const top = pg.top.map(([k, n]) => {
    const m = symMap(k);
    const name = !m ? `<span class="state none">Chưa xác định</span>` : m.ignore ? `<span class="state ignore">Bỏ qua</span>` : esc(m.material);
    return `<tr data-k="${esc(k)}" style="cursor:pointer"><td style="width:45%"><span class="mono">${esc(k.length > 36 ? k.slice(0, 36) + "…" : k)}</span></td><td>${name}</td><td class="num">${fmt(n)}</td></tr>`;
  }).join("");
  const lens = Object.entries(pg.lengths || {}).sort((a, b) => b[1] - a[1]).filter(([l]) => { const L = S.prj.layers.find((x) => x.layer === l); return L && L.map && !L.map.ignore; }).slice(0, 6);
  pv.innerHTML = `
    <div class="card viewer" id="vwrap">
      <div class="vtitle">${sysChip(pg.system)}<span class="chip" style="background:#fff">${esc(f.name || "")} · Trang ${pg.index}</span></div>
      <div class="vtools"><button class="btn" id="vIn" title="Phóng to">${ico("zin")}</button><button class="btn" id="vOut" title="Thu nhỏ">${ico("zout")}</button><button class="btn" id="vFit" title="Vừa khung">${ico("fit")}</button></div>
      <div class="vlegend"><span><i style="background:#10B981"></i>Được tính</span><span><i style="background:#ED1844"></i>Chưa xác định</span><span><i style="background:#94A3B8"></i>Bỏ qua</span><span><i style="background:transparent;border:2px solid #64748B"></i>Bảng chú thích</span></div>
      <div class="vloading" id="vLoad">${ico("loader", "spin").replace("<svg", '<svg style="width:26px;height:26px"')}</div>
      <canvas id="vc"></canvas>
    </div>
    <div class="pdetail">
      <div class="card">
        <div class="card-h"><h3>${esc(pg.title)}</h3></div>
        <div class="card-b">
          ${!pg.include && pg.auto_reason ? `<div class="infoline">${ico("info")}<div>Phần mềm đề xuất <b>bỏ qua</b> trang này: ${esc(pg.auto_reason)}. Bật công tắc nếu muốn tính.</div></div>` : ""}
          ${pg.warnings.map((w) => `<div class="warnline">${ico("alert")}<div>${esc(w)}</div></div>`).join("")}
          <div class="row" style="margin-bottom:14px"><label class="switch"><input type="checkbox" id="dInc" ${pg.include ? "checked" : ""}><span></span></label><b style="color:var(--ink)">${pg.include ? "Trang này đang được tính" : "Trang này đang bị bỏ qua"}</b></div>
          <div class="kv">
            <label class="field">Tòa nhà<input class="input sm" id="dB" value="${esc(pg.building)}"></label>
            <label class="field">Tầng<input class="input sm" id="dF" value="${esc(pg.floor_label)}" placeholder="—"></label>
            <label class="field">Hệ số tầng (×)<input class="input sm" id="dM" type="number" min="0" step="1" value="${pg.multiplier}"></label>
          </div>
          <div class="muted" style="font-size:12px;margin-top:8px">Hệ số tầng: số tầng mà trang vẽ này đại diện (ví dụ trang “Tầng 1, 2” dùng chung cho 2 tầng thì nhập 2).</div>
        </div>
      </div>
      <div class="card">
        <div class="card-h"><h3>Thiết bị trên trang</h3><span class="sub">${fmt(pg.n_symbols)} ký hiệu${pg.n_legend ? ` · đã loại ${pg.n_legend} ký hiệu ở bảng chú thích` : ""}</span></div>
        <div class="card-b" style="padding-top:6px">
          ${top ? `<table class="tl">${top}</table>` : '<div class="muted">Không có ký hiệu.</div>'}
          ${lens.length ? `<div style="margin-top:12px;font-size:12px;font-weight:600;color:var(--muted)">CHIỀU DÀI ĐO ĐƯỢC</div><table class="tl">${lens.map(([l, L]) => `<tr><td class="mono">${esc(l)}</td><td>${esc(S.prj.layers.find((x) => x.layer === l).map.material)}</td><td class="num">${fmt(L, 1)} m</td></tr>`).join("")}</table>` : ""}
        </div>
      </div>
    </div>`;
  const save = async (changes) => {
    Object.assign(pg, changes);
    await call("update_page", S.pid, pg.id, changes);
    S.result = null;
    drawPageList();
  };
  $("#dInc").onchange = async (e) => { await save({ include: e.target.checked }); refreshCounts(); drawPageView(); renderNav(); };
  $("#dB").onchange = (e) => save({ building: e.target.value.trim() || "Chung" });
  $("#dF").onchange = (e) => save({ floor_label: e.target.value.trim() });
  $("#dM").onchange = (e) => save({ multiplier: Math.max(0, parseFloat(e.target.value) || 1) });
  $$(".tl tr[data-k]", pv).forEach((tr) => (tr.onclick = () => { S.hiKey = S.hiKey === tr.dataset.k ? null : tr.dataset.k; $$(".tl tr[data-k]", pv).forEach((x) => x.style.background = x.dataset.k === S.hiKey ? "var(--soft)" : ""); viewer && viewer.draw(); }));

  const canvas = $("#vc");
  viewer = new Viewer(canvas);
  $("#vIn").onclick = () => viewer.zoom(1.4);
  $("#vOut").onclick = () => viewer.zoom(1 / 1.4);
  $("#vFit").onclick = () => viewer.fit();
  let g = S.geomCache.get(pg.id);
  if (!g) {
    try { g = await API.page_geometry(S.pid, pg.id); S.geomCache.set(pg.id, g); } catch (e) { $("#vLoad").textContent = "Không tải được hình trang"; return; }
  }
  if (S.selPage !== pg.id) return;
  $("#vLoad").remove();
  viewer.set(g);
}

/* ------------------------------------------------------------------ viewer */
let viewer = null;
const DN_COLORS = { 15: "#a855f7", 20: "#a855f7", 25: "#ef4444", 32: "#eab308", 40: "#22c55e", 50: "#3b82f6", 65: "#a855f7", 80: "#14b8a6", 100: "#0ea5e9", 125: "#0ea5e9", 150: "#f97316", 200: "#b45309", 250: "#7c2d12", 300: "#7c2d12" };
function layerColor(l) {
  const m = /^\s*DN\s*-?\s*(\d+)\s*$/i.exec(l);
  if (m) return [DN_COLORS[+m[1]] || "#0ea5e9", 1.6, 1];
  if (/DAY ?DIEN|DAYDIEN|CAP|CABLE|WIRE/i.test(l)) return ["#8b5cf6", 1.2, 0.95];
  if (/DUCT|ONG ?GIO|HVAC|CDFF/i.test(l)) return ["#06b6d4", 1.2, 0.9];
  return ["#94a3b8", 0.8, 0.55];
}
class Viewer {
  constructor(c) {
    this.c = c; this.ctx = c.getContext("2d"); this.g = null; this.s = 1; this.tx = 0; this.ty = 0;
    this.ro = new ResizeObserver(() => { this.resize(); this.g && (this.fitted ? this.fit() : this.draw()); });
    this.ro.observe(c.parentElement);
    let drag = null;
    c.onmousedown = (e) => { drag = { x: e.clientX, y: e.clientY, tx: this.tx, ty: this.ty }; c.classList.add("drag"); };
    window.addEventListener("mouseup", () => { drag = null; c.classList.remove("drag"); });
    c.onmousemove = (e) => { if (!drag) return; this.tx = drag.tx + (e.clientX - drag.x); this.ty = drag.ty + (e.clientY - drag.y); this.fitted = false; this.req(); };
    c.onwheel = (e) => { e.preventDefault(); const r = c.getBoundingClientRect(); this.zoom(e.deltaY < 0 ? 1.18 : 1 / 1.18, e.clientX - r.left, e.clientY - r.top); };
    c.ondblclick = () => this.fit();
    this.resize();
  }
  resize() { const r = this.c.parentElement.getBoundingClientRect(); const d = window.devicePixelRatio || 1; this.W = r.width; this.H = r.height; this.c.width = r.width * d; this.c.height = r.height * d; this.ctx.setTransform(d, 0, 0, d, 0, 0); }
  set(g) {
    this.g = g;
    // gom nét theo màu để vẽ nhanh
    const groups = new Map();
    g.polys.forEach((p) => { const l = g.layers[p[0]]; const k = layerColor(l).join("|"); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(p); });
    this.groups = [...groups.entries()].sort((a, b) => (a[0].startsWith("#94a3b8") ? -1 : 1));
    this.fit();
  }
  fit() { if (!this.g) return; const pad = 30; this.s = Math.min((this.W - pad * 2) / this.g.w, (this.H - pad * 2) / this.g.h); this.tx = (this.W - this.g.w * this.s) / 2; this.ty = (this.H + this.g.h * this.s) / 2; this.fitted = true; this.draw(); }
  zoom(f, cx = this.W / 2, cy = this.H / 2) { const ns = Math.max(1e-5, Math.min(this.s * f, 50)); const k = ns / this.s; this.tx = cx - (cx - this.tx) * k; this.ty = cy - (cy - this.ty) * k; this.s = ns; this.fitted = false; this.req(); }
  req() { if (this._raf) return; this._raf = requestAnimationFrame(() => { this._raf = null; this.draw(); }); }
  draw() {
    const { ctx, g } = this; if (!g) return;
    ctx.clearRect(0, 0, this.W, this.H);
    ctx.fillStyle = "#FBFCFE"; ctx.fillRect(0, 0, this.W, this.H);
    const s = this.s, tx = this.tx, ty = this.ty;
    ctx.save();
    ctx.strokeStyle = "#CBD5E1"; ctx.lineWidth = 1; ctx.strokeRect(tx, ty - g.h * s, g.w * s, g.h * s);
    ctx.fillStyle = "#fff"; ctx.fillRect(tx, ty - g.h * s, g.w * s, g.h * s);
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    for (const [k, polys] of this.groups) {
      const [col, w, a] = k.split("|");
      ctx.strokeStyle = col; ctx.globalAlpha = +a; ctx.lineWidth = +w;
      ctx.beginPath();
      for (const p of polys) {
        ctx.moveTo(tx + p[1] * s, ty - p[2] * s);
        for (let i = 3; i < p.length; i += 2) ctx.lineTo(tx + p[i] * s, ty - p[i + 1] * s);
      }
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
    const r = Math.max(2.2, Math.min(5, s * 400));
    const cols = { ok: "#10B981", none: "#ED1844", ignore: "#94A3B8" };
    const st = new Map();
    for (const [k, x, y, leg] of g.syms) {
      if (!st.has(k)) st.set(k, symState(k));
      const X = tx + x * s, Y = ty - y * s;
      if (X < -10 || Y < -10 || X > this.W + 10 || Y > this.H + 10) continue;
      const hi = S.hiKey && S.hiKey === k;
      if (leg) { ctx.strokeStyle = "#64748B"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(X, Y, r + 1, 0, 6.283); ctx.stroke(); continue; }
      ctx.fillStyle = cols[st.get(k)];
      ctx.globalAlpha = S.hiKey && !hi ? 0.25 : 1;
      ctx.beginPath(); ctx.arc(X, Y, hi ? r + 2.5 : r, 0, 6.283); ctx.fill();
      if (hi) { ctx.strokeStyle = "#0B1F4A"; ctx.lineWidth = 1.5; ctx.stroke(); }
    }
    ctx.restore();
  }
}

/* ------------------------------------------------------------------ symbols tab */
function stateOf(s) { if (!s.map) return "none"; if (s.map.ignore) return "ignore"; return s.source || "suggest"; }
const STATE_LABEL = { none: "Chưa xác định", ignore: "Bỏ qua", suggest: "Gợi ý", user: "Đã xác nhận", library: "Từ thư viện" };
function renderSymbolsTab() {
  const p = S.prj;
  const body = $("#wsBody");
  const syms = p.symbols.filter((s) => (S.sAll ? s.count_all : s.count) > 0);
  const n = { all: syms.length, none: 0, suggest: 0, user: 0, ignore: 0 };
  syms.forEach((s) => { const st = stateOf(s); if (st === "library") n.user++; else n[st]++; });
  body.innerHTML = `<div class="symwrap">
    <div class="toolbar">
      <div class="seg" id="sV"><button data-v="symbols" class="${S.sView === "symbols" ? "on" : ""}">${ico("shapes").replace("<svg", '<svg style="width:15px;height:15px"')} Ký hiệu thiết bị</button><button data-v="layers" class="${S.sView === "layers" ? "on" : ""}">${ico("ruler").replace("<svg", '<svg style="width:15px;height:15px"')} Đường ống & dây (đo dài)</button></div>
      <div class="grow"></div>
      <button class="btn" id="sAcc">${ico("spark")} Xác nhận tất cả gợi ý</button>
    </div>
    <div id="sBody"></div></div>`;
  $$("#sV button").forEach((b) => (b.onclick = () => { S.sView = b.dataset.v; renderSymbolsTab(); }));
  $("#sAcc").onclick = async () => { const k = await call("accept_suggestions", S.pid); await refreshCounts(); toast(`Đã xác nhận ${k} gợi ý và lưu vào thư viện`); renderSymbolsTab(); };
  if (S.sView === "layers") return renderLayers();
  $("#sBody").innerHTML = `
    <div class="toolbar">
      <div class="search" style="width:320px">${ico("search")}<input class="input" id="sQ" placeholder="Tìm ký hiệu hoặc vật tư…" value="${esc(S.sQ)}"></div>
      <div class="seg" id="sF">${[["all", "Tất cả"], ["none", "Chưa xác định"], ["suggest", "Gợi ý"], ["user", "Đã xác nhận"], ["ignore", "Bỏ qua"]].map(([k, l]) => `<button data-k="${k}" class="${S.sFilter === k ? "on" : ""}">${l}<span class="n">${n[k]}</span></button>`).join("")}</div>
      <label class="row muted" style="gap:8px;font-size:13px;cursor:pointer"><label class="switch"><input type="checkbox" id="sAll" ${S.sAll ? "checked" : ""}><span></span></label>Hiện cả ký hiệu chỉ có ở trang bị bỏ qua</label>
    </div>
    <div class="card" style="overflow:hidden"><table class="grid"><thead><tr><th style="width:72px">Hình</th><th>Ký hiệu trong bản vẽ</th><th style="width:90px;text-align:right">Số lượng</th><th>Là vật tư gì?</th><th style="width:130px">Trạng thái</th><th style="width:150px"></th></tr></thead><tbody id="sRows"></tbody></table></div>`;
  $("#sQ").oninput = (e) => { S.sQ = e.target.value; drawSymRows(); };
  $("#sAll").onchange = (e) => { S.sAll = e.target.checked; renderSymbolsTab(); };
  $$("#sF button").forEach((b) => (b.onclick = () => { S.sFilter = b.dataset.k; renderSymbolsTab(); }));
  drawSymRows();
}
function drawSymRows() {
  const q = S.sQ.trim().toLowerCase();
  const rows = S.prj.symbols.filter((s) => {
    if ((S.sAll ? s.count_all : s.count) <= 0) return false;
    const st = stateOf(s);
    if (S.sFilter !== "all" && !(S.sFilter === st || (S.sFilter === "user" && st === "library"))) return false;
    if (q && !(s.key.toLowerCase().includes(q) || (s.map && (s.map.material || "").toLowerCase().includes(q)))) return false;
    return true;
  });
  const tb = $("#sRows");
  if (!rows.length) { tb.innerHTML = `<tr><td colspan="6"><div class="empty">${ico("check")}<b>Không có ký hiệu nào ở mục này</b></div></td></tr>`; return; }
  tb.innerHTML = rows.slice(0, 400).map((s, i) => {
    const st = stateOf(s);
    const m = s.map || {};
    return `<tr data-i="${i}">
      <td><div class="thumb">${s.svg || ico("shapes")}</div></td>
      <td><div class="symname">${esc(s.eff)}${s.label ? `<span class="lab">${esc(s.label)}</span>` : ""}</div><div class="muted" style="font-size:12px;margin-top:3px">${s.files.map((f) => { const ff = S.prj.files.find((x) => x.id === f); return ff ? SYS_SHORT[ff.system] || "" : ""; }).filter(Boolean).join(" · ")}${s.count < s.count_all ? ` · ${fmt(s.count_all)} cái trên tất cả trang` : ""}</div></td>
      <td style="text-align:right"><span class="cnt">${fmt(s.count)}</span></td>
      <td><div class="matcell"><input class="input sm mat" list="catalog" value="${esc(m.ignore ? "" : m.material || "")}" placeholder="${m.ignore ? "(không tính)" : "Gõ hoặc chọn tên vật tư…"}" ${m.ignore ? "disabled" : ""}><select class="input sm unit" ${m.ignore ? "disabled" : ""}>${UNITS.map((u) => `<option ${u === (m.unit || "cái") ? "selected" : ""}>${u}</option>`).join("")}</select></div></td>
      <td><span class="state ${st}">${STATE_LABEL[st]}</span></td>
      <td><div class="row" style="gap:6px;justify-content:flex-end">
        ${st !== "user" && st !== "library" && !m.ignore ? `<button class="btn sm ok" title="Xác nhận">${ico("check")}</button>` : ""}
        ${m.ignore ? `<button class="btn sm unig">Tính lại</button>` : `<button class="btn sm ig" title="Không tính ký hiệu này">${ico("eyeoff")}</button>`}
        <button class="btn sm where" title="Xem trên bản vẽ">${ico("target")}</button></div></td></tr>`;
  }).join("");
  $$("tr[data-i]", tb).forEach((tr) => {
    const s = rows[+tr.dataset.i];
    const commit = async (mapping) => {
      await call("set_symbol", S.pid, s.key, mapping, true);
      s.map = mapping; s.source = mapping ? "user" : null;
      S.result = null;
      const st = stateOf(s);
      $(".state", tr).className = "state " + st; $(".state", tr).textContent = STATE_LABEL[st];
      renderNav();
    };
    const mat = $(".mat", tr), unit = $(".unit", tr);
    const doSave = () => { const v = mat.value.trim(); if (!v) return; const cat = (S.info.catalog || []).find((c) => c.name === v); if (cat && document.activeElement !== unit) unit.value = cat.unit; commit({ material: v, unit: unit.value, ignore: false }); };
    if (mat) { mat.onchange = doSave; mat.onkeydown = (e) => { if (e.key === "Enter") mat.blur(); }; }
    if (unit) unit.onchange = () => { if (mat.value.trim()) commit({ material: mat.value.trim(), unit: unit.value, ignore: false }); };
    const okb = $(".ok", tr); if (okb) okb.onclick = async () => { if (!mat.value.trim()) { mat.focus(); return toast("Hãy nhập tên vật tư trước", true); } await commit({ material: mat.value.trim(), unit: unit.value, ignore: false }); drawSymRows(); };
    const ig = $(".ig", tr); if (ig) ig.onclick = async () => { await commit({ material: "", unit: "", ignore: true }); drawSymRows(); };
    const un = $(".unig", tr); if (un) un.onclick = async () => { await commit(null); drawSymRows(); };
    $(".where", tr).onclick = () => {
      const pg = S.prj.pages.find((p) => p.include && p.top.some(([k]) => k === s.key)) || S.prj.pages.find((p) => p.top.some(([k]) => k === s.key));
      if (!pg) return toast("Ký hiệu này không nằm trong nhóm nhiều nhất của trang nào – hãy tìm ở tab Trang bản vẽ", true);
      S.selPage = pg.id; S.hiKey = s.key; S.tab = "pages"; renderNav(); renderWorkspace();
    };
  });
}
function renderLayers() {
  const rows = S.prj.layers.filter((l) => l.length_all > 0.5);
  $("#sBody").innerHTML = `
    <div class="infoline" style="margin-bottom:14px">${ico("info")}<div>Phần mềm đo tổng chiều dài các nét vẽ theo <b>lớp (layer)</b> trên các trang được tính. Gán lớp nào là loại ống / dây nào. <b>Hệ số</b>: ống gió vẽ bằng 2 nét viền thì nhập 0,5.</div></div>
    <div class="card" style="overflow:hidden"><table class="grid"><thead><tr><th>Lớp vẽ (layer)</th><th style="width:140px;text-align:right">Chiều dài đo</th><th>Là loại ống / dây gì?</th><th style="width:100px">Hệ số</th><th style="width:130px">Trạng thái</th><th style="width:110px"></th></tr></thead><tbody>
    ${rows.map((l, i) => { const st = stateOf(l); const m = l.map || {}; return `<tr data-i="${i}">
      <td><span class="mono" style="font-weight:600;color:var(--ink)">${esc(l.layer)}</span></td>
      <td style="text-align:right"><span class="cnt" style="font-size:14px">${fmt(l.length, 1)} m</span>${l.length < l.length_all - 0.5 ? `<div class="muted" style="font-size:11px">${fmt(l.length_all, 0)} m trên tất cả trang</div>` : ""}</td>
      <td><input class="input sm mat" list="catalog" value="${esc(m.ignore ? "" : m.material || "")}" placeholder="${m.ignore ? "(không tính)" : "Ví dụ: Ống thép DN50"}" ${m.ignore ? "disabled" : ""}></td>
      <td><input class="input sm fac" type="number" step="0.1" min="0" value="${m.factor ?? 1}" ${m.ignore ? "disabled" : ""}></td>
      <td><span class="state ${st}">${STATE_LABEL[st]}</span></td>
      <td><div class="row" style="gap:6px;justify-content:flex-end">${m.ignore || !l.map ? "" : ""}${m.ignore ? `<button class="btn sm unig">Tính lại</button>` : `<button class="btn sm ig" title="Không đo lớp này">${ico("eyeoff")}</button>`}</div></td></tr>`; }).join("")}
    </tbody></table></div>`;
  $$("#sBody tr[data-i]").forEach((tr) => {
    const l = rows[+tr.dataset.i];
    const commit = async (mapping) => { await call("set_layer", S.pid, l.layer, mapping, true); l.map = mapping; l.source = mapping ? "user" : null; S.result = null; const st = stateOf(l); $(".state", tr).className = "state " + st; $(".state", tr).textContent = STATE_LABEL[st]; };
    const mat = $(".mat", tr), fac = $(".fac", tr);
    const save = () => { const v = mat.value.trim(); if (!v) return; commit({ material: v, unit: "m", factor: parseFloat(fac.value) || 1, ignore: false }); };
    mat.onchange = save; fac.onchange = save;
    const ig = $(".ig", tr); if (ig) ig.onclick = async () => { await commit({ material: "", unit: "m", factor: 1, ignore: true }); renderLayers(); };
    const un = $(".unig", tr); if (un) un.onclick = async () => { await commit(null); renderLayers(); };
  });
}

/* ------------------------------------------------------------------ results tab */
async function renderResultsTab() {
  const body = $("#wsBody");
  body.innerHTML = `<div class="symwrap"><div class="empty">${ico("loader", "spin")}<b>Đang tính khối lượng…</b></div></div>`;
  if (!S.result) S.result = await call("compute", S.pid);
  const r = S.result, st = S.prj.settings || {};
  const kpis = [
    ["table", "#EDF3FF", "#055FD1", fmt(r.stats.items), "hạng mục khối lượng"],
    ["pages", "#E7F8F1", "#059669", `${r.stats.pages_used}<span class="muted" style="font-size:15px;font-weight:500">/${r.stats.pages_total}</span>`, "trang bản vẽ được tính"],
    ["alert", "#FFF6E6", "#D97706", fmt(r.warnings.filter((w) => w.type !== "symbol").length), "chỗ cần kiểm tra"],
    ["shapes", "#FDECEF", "#ED1844", fmt(r.stats.unmapped), "ký hiệu chưa xác định"],
  ];
  body.innerHTML = `<div class="symwrap">
    <div class="kpis">${kpis.map(([i, bg, fg, b, s]) => `<div class="card kpi"><div class="ki" style="background:${bg};color:${fg}">${ico(i)}</div><div><b>${b}</b><span>${s}</span></div></div>`).join("")}</div>
    <div class="res-grid">
      <div class="card" style="overflow:hidden">
        <div class="card-h"><div class="seg" id="rT">${[["sum", "Tổng hợp"], ["detail", "Chi tiết theo trang"], ["warn", `Cần kiểm tra`]].map(([k, l]) => `<button data-k="${k}" class="${S.resTab === k ? "on" : ""}">${l}${k === "warn" ? `<span class="n">${r.warnings.length}</span>` : ""}</button>`).join("")}</div></div>
        <div id="rBody" style="max-height:calc(100vh - 360px);overflow:auto"></div>
      </div>
      <div class="col">
        <div class="card settings"><div class="card-h"><h3>Cài đặt tính toán</h3></div><div class="card-b" style="padding-top:6px">
          <div class="setrow"><span>Hao hụt ống thép (%)</span><input class="input sm" type="number" min="0" step="1" data-s="waste_pipe" value="${st.waste_pipe ?? 0}"></div>
          <div class="setrow"><span>Hao hụt dây, cáp (%)</span><input class="input sm" type="number" min="0" step="1" data-s="waste_cable" value="${st.waste_cable ?? 0}"></div>
          <div class="setrow"><span>Hao hụt ống gió (%)</span><input class="input sm" type="number" min="0" step="1" data-s="waste_duct" value="${st.waste_duct ?? 0}"></div>
          <div class="setrow"><span>Làm tròn ống thép theo cây 6 m</span><label class="switch"><input type="checkbox" data-s="round_pipe_6m" ${st.round_pipe_6m ? "checked" : ""}><span></span></label></div>
        </div></div>
        <div class="card"><div class="card-b">
          <div class="row" style="margin-bottom:10px"><div class="ki" style="width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:#E7F8F1;color:#059669">${ico("excel")}</div><div><b style="color:var(--ink)">Xuất file Excel</b><div class="muted" style="font-size:12.5px">5 sheet: tổng hợp, chi tiết, cần kiểm tra, nhập tay, bảng ký hiệu</div></div></div>
          <button class="btn primary" style="width:100%" id="rExp">${ico("download")} Xuất Excel</button>
        </div></div>
        <div class="card"><div class="card-b muted" style="font-size:12.5px;line-height:1.6">${ico("info").replace("<svg", '<svg style="width:15px;height:15px;vertical-align:-3px;color:var(--brand)"')} Số liệu là khối lượng <b>đọc được từ bản vẽ</b>. Các hạng mục không thể hiện trên bản vẽ (máy bơm, tủ điện, phụ kiện, vật tư phụ…) được liệt kê ở sheet “Nhập tay” trong file Excel.</div></div>
      </div>
    </div></div>`;
  $$("#rT button").forEach((b) => (b.onclick = () => { S.resTab = b.dataset.k; $$("#rT button").forEach((x) => x.classList.toggle("on", x === b)); drawResBody(); }));
  $$("[data-s]").forEach((inp) => (inp.onchange = async () => {
    const k = inp.dataset.s;
    const val = inp.type === "checkbox" ? inp.checked : Math.max(0, parseFloat(inp.value) || 0);
    S.prj.settings = await call("update_settings", S.pid, { [k]: val });
    S.result = await call("compute", S.pid);
    drawResBody();
    toast("Đã tính lại khối lượng");
  }));
  $("#rExp").onclick = exportExcel;
  drawResBody();
}
function drawResBody() {
  const r = S.result, el = $("#rBody");
  if (!el) return;
  if (S.resTab === "sum") {
    if (!r.groups.length) { el.innerHTML = `<div class="empty">${ico("table")}<b>Chưa có khối lượng</b><span>Hãy chọn trang cần tính và xác nhận ký hiệu.</span></div>`; return; }
    el.innerHTML = `<table class="res"><thead><tr><th style="width:56px">STT</th><th>Hạng mục</th><th style="width:70px" class="c">Đơn vị</th><th style="width:120px;text-align:right">Khối lượng</th><th style="width:90px" class="c">Cách ra số</th></tr></thead><tbody>
      ${r.groups.map((g) => `<tr class="sys"><td class="c">${g.roman}</td><td colspan="4">${esc(g.name.toUpperCase())}</td></tr>` + g.buildings.map((b) => `<tr class="bld"><td class="c">*</td><td colspan="4">${esc(b.name)}</td></tr>` + b.items.map((it, i) => `<tr><td class="c muted">${i + 1}</td><td>${esc(it.material)}</td><td class="c">${esc(it.unit)}</td><td class="q">${fmtQ(it.qty, it.unit)}</td><td class="c"><span class="src ${it.source === "Đếm" ? "dem" : "do"}">${it.source}</span></td></tr>`).join("")).join("")).join("")}
      </tbody></table>`;
  } else if (S.resTab === "detail") {
    el.innerHTML = `<table class="res"><thead><tr><th>Hệ</th><th>Trang</th><th>Tòa nhà · Tầng</th><th>Hạng mục</th><th style="text-align:right">Trên bản vẽ</th><th class="c">× tầng</th><th style="text-align:right">Khối lượng</th></tr></thead><tbody>
      ${r.detail.map((d) => `<tr><td>${sysChip(d.system)}</td><td><a class="pg" data-p="${d.page_id}" style="color:var(--brand);cursor:pointer;font-weight:600">#${d.page}</a> <span class="muted">${esc(d.title.slice(0, 48))}</span></td><td>${esc(d.building)}${d.floor ? " · " + esc(d.floor) : ""}</td><td>${esc(d.material)}</td><td class="q" style="font-weight:500">${fmtQ(d.base, d.unit)}</td><td class="c">${fmt(d.multiplier, 2)}</td><td class="q">${fmtQ(d.qty, d.unit)} ${esc(d.unit)}</td></tr>`).join("")}
      </tbody></table>`;
  } else {
    el.innerHTML = r.warnings.length ? `<div class="wlist" style="padding:6px 18px 12px">${r.warnings.map((w) => `<div class="w"><div class="wi" style="background:${w.type === "symbol" ? "#FDECEF" : w.type === "dup" ? "#E0F2FE" : "#FFF6E6"};color:${w.type === "symbol" ? "#ED1844" : w.type === "dup" ? "#0369A1" : "#D97706"}">${ico(w.type === "symbol" ? "shapes" : w.type === "dup" ? "layers" : "alert")}</div><div style="flex:1"><b>${esc(w.text)}</b><span>${esc(w.where)}</span></div>${w.page_id ? `<button class="btn sm pg" data-p="${w.page_id}">Xem trang</button>` : w.key ? `<button class="btn sm sy" data-k="${esc(w.key)}">Xác định</button>` : ""}</div>`).join("")}</div>` : `<div class="empty">${ico("check")}<b>Không có cảnh báo</b></div>`;
  }
  $$(".pg", el).forEach((a) => (a.onclick = () => { S.selPage = a.dataset.p; S.hiKey = null; S.tab = "pages"; renderNav(); renderWorkspace(); }));
  $$(".sy", el).forEach((a) => (a.onclick = () => { S.tab = "symbols"; S.sView = "symbols"; S.sFilter = "all"; S.sQ = a.dataset.k; renderNav(); renderWorkspace(); }));
}
async function exportExcel() {
  const r = await call("export_excel", S.pid);
  if (!r) return;
  if (r.error) return toast(r.error, true);
  toast("Đã xuất file Excel", false, [{ label: "Mở file", fn: () => API.open_path(r.path) }, { label: "Mở thư mục", fn: () => API.reveal(r.path) }]);
}

/* ------------------------------------------------------------------ library */
async function renderLibrary() {
  setTop(`<h1>Thư viện ký hiệu</h1><span class="crumb">· Những ký hiệu đã xác nhận được nhớ cho các dự án sau</span>`);
  const lib = await call("library");
  const v = $("#view");
  const tbl = (rows, kind) => rows.length ? `<table class="grid"><thead><tr><th>${kind === "symbols" ? "Ký hiệu trong bản vẽ" : "Lớp vẽ (layer)"}</th><th>Vật tư</th><th style="width:90px">Đơn vị</th><th style="width:80px"></th></tr></thead><tbody>${rows.map((r) => `<tr><td class="mono" style="color:var(--ink);font-weight:600">${esc(r.key)}</td><td>${r.ignore ? '<span class="state ignore">Không tính</span>' : esc(r.material)}${kind === "layers" && r.factor && r.factor != 1 ? ` <span class="chip">× ${fmt(r.factor, 2)}</span>` : ""}</td><td>${esc(r.unit || "")}</td><td><button class="btn sm danger" data-kind="${kind}" data-key="${esc(r.key)}">${ico("trash")}</button></td></tr>`).join("")}</tbody></table>` : `<div class="empty">${ico("book")}<b>Chưa có mục nào</b><span>Khi bạn xác nhận ký hiệu trong một dự án, phần mềm sẽ ghi nhớ ở đây.</span></div>`;
  v.innerHTML = `<div class="col" style="gap:18px">
    <div class="infoline">${ico("info")}<div>Phần mềm nhớ theo <b>tên ký hiệu + chữ hiện ra</b> trong bản vẽ. Dự án mới có cùng ký hiệu sẽ được tự điền – bạn chỉ cần xác nhận những ký hiệu mới.</div></div>
    <div class="card" style="overflow:hidden"><div class="card-h"><h3>Ký hiệu thiết bị</h3><span class="sub">${lib.symbols.length} mục</span></div>${tbl(lib.symbols, "symbols")}</div>
    <div class="card" style="overflow:hidden"><div class="card-h"><h3>Lớp đo chiều dài</h3><span class="sub">${lib.layers.length} mục</span></div>${tbl(lib.layers, "layers")}</div></div>`;
  $$("[data-kind]", v).forEach((b) => (b.onclick = async () => { await call("library_remove", b.dataset.kind, b.dataset.key); toast("Đã xoá khỏi thư viện"); renderLibrary(); }));
}

/* ------------------------------------------------------------------ about */
function renderAbout() {
  setTop(`<h1>Giới thiệu</h1>`);
  $("#view").innerHTML = `<div class="col about" style="gap:18px">
    <div class="card"><div class="card-b" style="padding:28px">
      <img src="assets/logo-dark.png" class="logo-big" alt="DC Software">
      <h2 style="margin:18px 0 6px;color:var(--ink)">DCS PCCC Takeoff <span class="chip info" style="vertical-align:4px">v${esc(S.info.version)}</span></h2>
      <div class="muted" style="font-size:15px">Phần mềm bóc tách khối lượng phòng cháy chữa cháy từ bản vẽ CAD.</div>
      <div class="row" style="margin-top:18px;gap:10px"><button class="btn primary" id="aWeb">${ico("ext")} dcsoftware.vn</button><span class="muted">DC Software – Đối tác triển khai phần mềm tin cậy</span></div>
    </div></div>
    <div class="card"><div class="card-h"><h3>Cách phần mềm hoạt động</h3></div><div class="card-b lic">
      1. Chuyển file DWG sang DXF bằng <b>LibreDWG</b> (chạy ngay trên máy, không gửi bản vẽ ra ngoài).<br>
      2. Chia bản vẽ theo khung tên, đọc tiêu đề để biết tòa nhà, tầng; tự bỏ trang trùng (đối chiếu kết cấu, sơ đồ 3D, chỉ dẫn thoát nạn, ký hiệu, chi tiết).<br>
      3. Đếm ký hiệu thiết bị (loại bỏ ký hiệu trong bảng chú thích), đo chiều dài nét vẽ theo lớp; đường ống vẽ lặp ở nhiều trang cùng tầng chỉ tính 1 lần.<br>
      4. Gợi ý ký hiệu là vật tư gì theo quy tắc; người dùng xác nhận, phần mềm ghi nhớ cho dự án sau.
    </div></div>
    <div class="card"><div class="card-h"><h3>Phần mềm nguồn mở được sử dụng</h3></div><div class="card-b lic">
      <b>LibreDWG</b> – GNU GPL v3 (chạy như chương trình riêng, mã nguồn: github.com/LibreDWG/libredwg; bản giấy phép đi kèm thư mục vendor/libredwg)<br>
      <b>ezdxf</b> – MIT · <b>pywebview</b> – BSD · <b>openpyxl</b> – MIT · <b>IBM Plex Sans</b> – SIL Open Font License
    </div></div></div>`;
  $("#aWeb").onclick = () => API.open_website();
}

/* ------------------------------------------------------------------ boot */
window.__errs = [];
window.addEventListener("error", (e) => { window.__errs.push(String(e.message)); toast("Lỗi giao diện: " + e.message, true); });
window.addEventListener("unhandledrejection", (e) => { window.__errs.push(String(e.reason)); });
async function boot() {
  API = window.pywebview ? window.pywebview.api : window.__MOCK_API__;
  if (!API) { $("#view").innerHTML = '<div class="empty"><b>Không kết nối được phần xử lý.</b></div>'; return; }
  S.info = await call("app_info");
  $("#ver").textContent = "Phiên bản " + S.info.version;
  if (S.info.version !== UI_VERSION) toast(`Giao diện (${UI_VERSION}) chưa khớp phần xử lý (${S.info.version}). Hãy tắt hẳn phần mềm rồi mở lại.`, true);
  $("#site").onclick = () => API.open_website();
  $("#catalog").innerHTML = S.info.catalog.map((c) => `<option value="${esc(c.name)}">`).join("");
  render();
}
let booted = false;
const tryBoot = () => { if (booted) return; if ((window.pywebview && window.pywebview.api && window.pywebview.api.app_info) || window.__MOCK_API__) { booted = true; boot(); } };
window.addEventListener("pywebviewready", tryBoot);
tryBoot();
const bootTimer = setInterval(() => { if (booted) clearInterval(bootTimer); else tryBoot(); }, 150);
