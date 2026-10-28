from pathlib import Path
import zipfile,json
root=Path('.');out=root/'dist';(out/'packets').mkdir(exist_ok=True)
def add(z,p):
 info=zipfile.ZipInfo(str(p));info.date_time=(2026,10,18,0,0,0);info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
with zipfile.ZipFile(out/'release.zip','w') as z:
 for p in sorted(root.rglob('*')):
  if not p.is_file() or any(s in p.parts for s in ('node_modules','.git','dist','.sites-runtime','.wrangler')):continue
  if p.suffix in ('.zip','.pdf') or p.name.startswith('.env'):continue
  if p.parts[0] in ('research','analysis','missions','release','src','scripts','tests','db','drizzle','content','public','.github') or str(p)=='.openai/hosting.json' or len(p.parts)==1:add(z,p)
for m in json.loads((root/'content/missions.json').read_text()):
 with zipfile.ZipFile(out/'packets'/f"{m['id']}.zip",'w') as z:
  for p in [Path('missions')/f"{m['id']}.md",Path('release/input-manifest.json'),Path('CURRENT_STATE.md'),Path('LICENSES.md')]+[Path(s) for s in m['inputs']]:add(z,p)
