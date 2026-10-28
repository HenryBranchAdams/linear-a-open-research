import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
const missions=JSON.parse(fs.readFileSync('content/missions.json','utf8')),findings=JSON.parse(fs.readFileSync('content/findings.json','utf8')),imageCredits=JSON.parse(fs.readFileSync('content/image-credits.json','utf8'));
const assets={};
const mediaTypes={'.jpg':'image/jpeg','.woff2':'font/woff2'};
for(const filename of fs.readdirSync('public/assets').sort()){
 const type=mediaTypes[path.extname(filename)];
 if(type)assets[filename]={type,data:fs.readFileSync(path.join('public/assets',filename)).toString('base64')};
}
const files={};
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(/\.(md|json|py|csv|txt)$/.test(p))files[p]=fs.readFileSync(p,'utf8');}}
for(const p of ['research','analysis','missions','release'])walk(p);
for(const p of ['README.md','CURRENT_STATE.md','START_HERE.md','CONTRIBUTING.md','CONTRIBUTION_TEMPLATE.md','AGENTS.md','DESIGN.md','LICENSES.md','LICENSE','LICENSE-KAMI'])files[p]=fs.readFileSync(p,'utf8');
fs.rmSync('dist',{recursive:true,force:true});fs.mkdirSync('dist/server',{recursive:true});fs.mkdirSync('dist/.openai',{recursive:true});fs.copyFileSync('.openai/hosting.json','dist/.openai/hosting.json');
if(fs.existsSync('drizzle'))fs.cpSync('drizzle','dist/drizzle',{recursive:true});
execFileSync('python3',['scripts/package-release.py']);
const packets={};for(const m of missions)packets[m.id]=fs.readFileSync(`dist/packets/${m.id}.zip`).toString('base64');
const style=fs.readFileSync('src/kami.css','utf8')+'\n'+fs.readFileSync('src/research.css','utf8'),client=fs.readFileSync('src/client.js','utf8');
const db=fs.readFileSync('src/db.js','utf8').replaceAll('export ',''),worker=fs.readFileSync('src/worker.js','utf8').replace(/^import .*\n/,'');
const journal=fs.existsSync('content/journal.json')?JSON.parse(fs.readFileSync('content/journal.json','utf8')):[];
const constants=`const DATA=${JSON.stringify({missions,findings,packets,imageCredits,journal})};\nconst FILES=${JSON.stringify(files)};\nconst ASSETS=${JSON.stringify(assets)};\nconst STYLE=${JSON.stringify(style)};\nconst CLIENT=${JSON.stringify(client)};\nconst RELEASE_ZIP=${JSON.stringify(fs.readFileSync('dist/release.zip').toString('base64'))};\n`;
const contributionData=fs.readFileSync('src/contribution-data.js','utf8').replace(/^export /gm,'');
fs.writeFileSync('dist/server/index.js',constants+db+'\n'+contributionData+'\n'+fs.readFileSync('src/editorial.js','utf8')+'\n'+fs.readFileSync('src/contribution-ui.js','utf8')+'\n'+fs.readFileSync('src/journal-ui.js','utf8')+'\n'+worker);
console.log('Built Worker, current baseline, public source release, assets, and eight archival input packets.');
