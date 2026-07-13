from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

router = APIRouter()
TOOL_META = {"label": "Theme Designer", "icon": "&#x1F3A8;", "description": "Edit server, module, and personal theme layers"}
ENV = {}

def init_module(env: dict):
    global ENV
    ENV = env

@router.get("/", response_class=HTMLResponse)
async def theme_designer(request: Request, auth=Depends(lambda: None)):
    user = request.state.user
    modules = ENV["get_modules"]()
    admin_opts = ""
    if user.role == "admin":
        mod_links = "".join(f'<option value="/control-panel/theme/module-default/{m}">{m}</option>' for m in modules)
        admin_opts = f'<option value="/control-panel/theme/server-default">Server Default (all users, all modules)</option><optgroup label="Module Defaults">{mod_links}</optgroup>'
    user_mod_links = "".join(f'<option value="/control-panel/theme/module-user/{m}">{m}</option>' for m in modules)
    return HTMLResponse(f"""<div style="max-width:60rem;margin:0 auto;padding:1.5rem;">
        <h2 style="margin-top:0;">Theme Designer</h2>
        <select onchange="htmx.ajax('GET', this.value, {{target:'#td-panel', swap:'innerHTML'}})" style="background:var(--bg);border:var(--border-thick) solid var(--border);color:var(--text);padding:0.5rem;border-radius:var(--radius);width:100%;margin-bottom:1rem;">
            <option value="">Select what to edit...</option>
            {admin_opts}
            <optgroup label="My Personal Theme"><option value="/control-panel/appearance">General (all modules)</option>{user_mod_links}</optgroup>
        </select>
        <div id="td-panel" class="glass" style="padding:1.5rem;"></div>
    </div>""")
