'use strict';
const $=id=>document.getElementById(id),exportCanvas=document.createElement('canvas');
const API_ORIGIN=location.hostname==='product-dna-studio-preview.onrender.com'?'https://product-dna-studio-ai.onrender.com':'';
const id=()=> 'src_'+crypto.randomUUID().replaceAll('-',''),requestId=()=> 'req_'+crypto.randomUUID().replaceAll('-','');
let cvName='',cvText='',cvId=id(),reading=false,uploadRun=0,recognition=null,voiceState='idle',voiceTarget='idle',voiceRunning=false,voiceStopping=false;
let result=null,renderVariant=null,generationNumber=null,busy=false,controller=null,pendingQuestion='',pendingRequest=null;
let versions=[],activeVersion=null,versionSerial=0,storyId=id();
const clone=x=>structuredClone(x);
function event(){} // No visitor analytics.
function status(s){$('input-status').textContent=s}
function scrollToStep(key){$(key).scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}
$('begin').onclick=()=>{$('studio').classList.remove('hidden');history.replaceState(null,'','#studio');scrollToStep('step-one');$('step-one').focus({preventScroll:true})};
if(location.hash==='#studio')$('studio').classList.remove('hidden');
function initialSources(){return [{source_id:storyId,source_type:'typed_story',source_label:'Career journey',content:$('story').value.trim()},{source_id:cvId,source_type:'cv',source_label:cvName,content:cvText}].filter(s=>s.content)}
function sources(){return activeVersion?clone(activeVersion.sources):initialSources()}
function canGenerate(){return activeVersion?$('story').value.trim().length>=3||Boolean(cvText&&!activeVersion.sources.some(s=>s.source_id===cvId)):initialSources().some(s=>(s.content.match(/\p{L}/gu)||[]).length>=8)}
function updateButtons(){
 $('generate').disabled=busy||reading||!canGenerate();$('generate').textContent=busy?'Working…':activeVersion?'Update My DNA Map':'Generate';
 for(const key of ['story','upload','replace-cv','clear-cv','voice','pause-voice','stop-voice','version-select','edit-map'])$(key).disabled=busy||reading||(key==='pause-voice'&&voiceStopping);
 $('save').disabled=busy||!result;$('undo').disabled=busy||!versions.some(v=>v.number===activeVersion?.parent_id);$('retry').disabled=busy;
 $('composer-label').textContent=activeVersion?'Refine your map':'Your career journey';$('story').placeholder=activeVersion?'Describe a change to your DNA map...':'Tell me about your career journey...';
}
function sourceChanged(){pendingRequest=null;$('generation-error').classList.add('hidden');$('retry').classList.add('hidden');updateButtons()}
$('story').addEventListener('input',sourceChanged);
function fileStatus(label,failed=false){$('cv-panel').classList.remove('hidden');$('cv-panel').classList.toggle('failed',failed);$('cv-status').textContent=(failed?'✕ ':'✓ ')+label}
function syncCV(){if(cvName)fileStatus(cvName+' · Ready');else $('cv-panel').classList.add('hidden')}
$('clear-cv').onclick=()=>{uploadRun++;reading=false;cvName='';cvText='';cvId=id();$('file').value='';syncCV();sourceChanged();status('')};
$('upload').onclick=$('replace-cv').onclick=()=>$('file').click();
async function loadScript(src,key){if(window[key])return;await new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=src;script.onload=resolve;script.onerror=()=>reject(Error('The file reader could not load. Paste your career journey instead.'));document.head.append(script)})}
$('file').onchange=async e=>{
 if(busy||reading)return;const files=e.target.files;if(!files?.length)return;
 if(files.length!==1){e.target.value='';status('Upload one CV at a time.');return}
 const file=files[0];e.target.value='';const ext=file.name.split('.').pop().toLowerCase(),run=++uploadRun;
 if(file.size>5*1024*1024){status('Choose a file smaller than 5 MB.');return}
 if(ext==='doc'){status('Older DOC files cannot be read reliably. Save as DOCX or PDF and upload again.');return}
 if(!['pdf','docx','txt'].includes(ext)){status('Choose a PDF, DOCX or TXT file.');return}
 reading=true;updateButtons();status('Reading your CV…');
 try{
  const bytes=new Uint8Array(await file.arrayBuffer());let text='';
  if(ext==='txt'){if(bytes.includes(0))throw Error('This does not look like a text file.');text=new TextDecoder('utf-8',{fatal:true}).decode(bytes)}
  if(ext==='docx'){if(bytes[0]!==80||bytes[1]!==75)throw Error('This is not a valid Word document.');await loadScript('https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.9.1/mammoth.browser.min.js','mammoth');text=(await mammoth.extractRawText({arrayBuffer:bytes.buffer})).value}
  if(ext==='pdf'){
   if(new TextDecoder().decode(bytes.slice(0,5))!=='%PDF-')throw Error('This is not a valid PDF file.');
   if(!window.pdfjsLib)window.pdfjsLib=await import('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.min.mjs');pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.worker.min.mjs';
   const doc=await pdfjsLib.getDocument({data:bytes}).promise;try{if(doc.numPages>15)throw Error('Use a PDF with 15 pages or fewer.');for(let i=1;i<=doc.numPages;i++)text+='\n'+(await(await doc.getPage(i)).getTextContent()).items.map(x=>x.str+(x.hasEOL?'\n':' ')).join('')}finally{await doc.destroy()}
  }
  if(run!==uploadRun)return;text=text.normalize('NFKC').replace(/[\u00ad\u200b]/g,'').trim();
  if(text.length<12)throw Error('No readable text. Scanned PDFs need OCR; paste your career journey instead.');
  if(text.length>18000)throw Error('Shorten your CV to 18,000 characters.');
  cvName=file.name.slice(0,150);cvText=text;cvId=id();fileStatus(cvName+' · Ready');sourceChanged();status('');
 }catch(err){if(run===uploadRun){if(cvName)syncCV();else fileStatus(file.name+' · Could not read',true);status(err.message+(cvName?' Your previous CV is unchanged.':''))}}
 finally{if(run===uploadRun){reading=false;updateButtons()}}
};
function syncVoice(){
 const listening=voiceState==='recording',paused=voiceState==='paused';$('voice').classList.toggle('recording',listening);$('voice').setAttribute('aria-pressed',String(listening));$('voice').setAttribute('aria-label',paused?'Resume voice recording':listening?'Stop voice recording':'Start voice recording');
 $('pause-voice').classList.toggle('hidden',!listening&&!paused);$('stop-voice').classList.toggle('hidden',!listening&&!paused);$('pause-voice').textContent=paused?'Resume':'Pause';$('pause-voice').disabled=busy||reading||voiceStopping;$('voice-status').textContent=listening?'Listening…':paused?'Paused':'';
}
function stopVoice(target='idle'){voiceTarget=target;voiceState=target;voiceStopping=voiceRunning;syncVoice();try{recognition?.stop()}catch{}}
function startVoice(){
 const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){status('Voice input is unavailable in this browser. Type your journey or upload a CV.');return}
 recognition=new SR();recognition.lang=navigator.language||'en-US';recognition.continuous=true;recognition.interimResults=false;voiceTarget='recording';
 recognition.onstart=()=>{voiceRunning=true;voiceStopping=false;voiceState='recording';syncVoice()};
 recognition.onresult=e=>{for(let i=e.resultIndex;i<e.results.length;i++)if(e.results[i].isFinal){const t=e.results[i][0].transcript;if($('story').value.length+t.length+1>18000){status('Shorten the composer text to continue.');stopVoice();return}const el=$('story'),at=el.selectionStart??el.value.length,before=el.value.slice(0,at),after=el.value.slice(el.selectionEnd??at);const insert=(before&&!/\s$/.test(before)?' ':'')+t+(after&&!/^\s/.test(after)?' ':'');el.value=before+insert+after;el.setSelectionRange(before.length+insert.length,before.length+insert.length);sourceChanged()}};
 recognition.onend=()=>{voiceRunning=false;voiceStopping=false;voiceState=voiceTarget==='paused'?'paused':'idle';syncVoice()};recognition.onerror=e=>{voiceRunning=false;voiceStopping=false;voiceTarget='idle';voiceState='idle';syncVoice();status(e.error==='not-allowed'?'Microphone permission was denied. You can still type.':'Voice input stopped. Your text is unchanged; you can resume recording.')};
 try{recognition.start()}catch{status('The microphone could not start. You can still type.')}
}
$('voice').onclick=()=>voiceState==='recording'?stopVoice():startVoice();$('pause-voice').onclick=()=>voiceState==='paused'?startVoice():stopVoice('paused');$('stop-voice').onclick=()=>stopVoice();
async function finishVoice(){if(!voiceRunning)return;await new Promise(resolve=>{const previous=recognition.onend,timer=setTimeout(resolve,1500);recognition.onend=()=>{clearTimeout(timer);previous?.();resolve()};stopVoice()})}
function showError(s){$('generation-error').textContent=s;$('generation-error').classList.remove('hidden');$('retry').classList.toggle('hidden',!pendingRequest)}
async function run(kind,body){
 busy=true;controller=new AbortController();$('loading').classList.remove('hidden');$('step-two').classList.remove('hidden');$('generation-error').classList.add('hidden');$('retry').classList.add('hidden');updateButtons();
 $('loading-title').textContent=kind==='refine'?'Updating Your PM Career DNA...':'Creating Your PM Career DNA...';$('loading-label').textContent='Your experience is being processed. You can stay on this page.';
 const began=Date.now();$('loading-elapsed').textContent='Elapsed 0:00';const elapsed=setInterval(()=>{const n=Math.floor((Date.now()-began)/1000);$('loading-elapsed').textContent='Elapsed '+Math.floor(n/60)+':'+String(n%60).padStart(2,'0')},1000);
 const slow=setTimeout(()=>{$('loading-label').textContent='This is taking longer. Your input and previous versions are still here.'},90000),timeout=setTimeout(()=>controller.abort(),300000);
 try{const response=await fetch(API_ORIGIN+'/api/career-dna/'+kind,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),signal:controller.signal});let data;try{data=await response.json()}catch{throw Error('The AI service is waking up. Wait a moment, then retry.')}if(!response.ok)throw Error(data.error||'This request could not complete. Please retry.');return data}
 catch(e){showError(e.name==='AbortError'?'Stopped waiting. Your request may still finish; retry retrieves it when available.':e.message);return null}
 finally{clearInterval(elapsed);clearTimeout(slow);clearTimeout(timeout);controller=null;busy=false;$('loading').classList.add('hidden');updateButtons()}
}
$('cancel').onclick=()=>controller?.abort();
async function generate(retry=false){
 if(busy||reading||(!retry&&!canGenerate()))return;busy=true;updateButtons();await finishVoice();busy=false;
 let work=retry?pendingRequest:null;
 if(!work){
  const kind=activeVersion?'refine':'generate',src=activeVersion?clone(activeVersion.sources):initialSources();
  if(activeVersion&&cvText&&!src.some(s=>s.source_id===cvId))src.push({source_id:cvId,source_type:'cv',source_label:cvName,content:cvText});
  if(src.reduce((n,s)=>n+s.content.length,0)+(activeVersion?$('story').value.length:0)>22000){status('Shorten the combined CV, career journey and update notes to 22,000 characters.');updateButtons();return}
  const body={sources:src,request_id:requestId(),next_version:versionSerial+1,clarification_context:pendingQuestion};
  if(activeVersion)Object.assign(body,{previous:clone(activeVersion.map),map_version:activeVersion.number,message:$('story').value.trim()||'Use my newly uploaded CV to update the existing map. Preserve unchanged facts and clarify conflicts.',context_consent:true});
  work={kind,body,base:activeVersion?.number??null,variant:activeVersion?clone(activeVersion.variant):null};pendingRequest=work;
 }
 if(!work){updateButtons();return}scrollToStep('step-two');const data=await run(work.kind,work.body);if(!data)return;
 if(data.map.status==='needs_more_info'){pendingQuestion=data.map.clarification_question;$('clarification-question').textContent=pendingQuestion;$('clarification').classList.remove('hidden');pendingRequest=null;scrollToStep('step-one');$('story').focus();return}
 if(work.base!==null&&data.base_version!==work.base){showError('This update belongs to a different version. Restore your preferred version and retry.');return}
 const src=clone(work.body.sources);if(data.accepted_source&&!src.some(s=>s.source_id===data.accepted_source.source_id))src.push(data.accepted_source);
 const visual=clone(work.variant||nextPMVariant());if(data.presentation_patch?.theme_id&&PM_LIBRARY.themes.some(t=>t.id===data.presentation_patch.theme_id))visual.theme_id=data.presentation_patch.theme_id;if(data.presentation_patch?.next_neutral_avatar===true){const pool=Array.from({length:24},(_,i)=>'pm_avatar_'+String(i+1).padStart(2,'0')).filter(x=>x!==visual.avatar_id),random=new Uint32Array(1);crypto.getRandomValues(random);visual.avatar_id=pool[random[0]%pool.length]}
 const version={number:++versionSerial,parent_id:work.base,map:clone(data.map),sources:src,variant:visual,generation_number:data.generation_number??activeVersion?.generation_number??null,cv:{name:cvName,text:cvText,id:cvId},change_summary:data.change_summary||''};
 versions.push(version);if(versions.length>30)versions.shift();activeVersion=version;result=version.map;renderVariant=version.variant;generationNumber=version.generation_number;pendingQuestion='';pendingRequest=null;$('clarification').classList.add('hidden');$('story').value='';storyId=id();if(data.stats)showStats(data.stats);else loadStats();
 busy=true;updateButtons();try{await renderResult()}finally{busy=false;updateButtons()}scrollToStep('result-panel');
}
$('generate').onclick=()=>generate();$('retry').onclick=()=>generate(true);
function versionMenu(){const menu=$('version-select');menu.replaceChildren();for(const v of versions){const o=document.createElement('option');o.value=v.number;o.textContent='Version '+v.number;o.selected=v.number===activeVersion?.number;menu.append(o)}}
async function restore(number){if(busy)return;const v=versions.find(v=>v.number===Number(number));if(!v)return;activeVersion=v;result=v.map;renderVariant=v.variant;generationNumber=v.generation_number;cvName=v.cv.name;cvText=v.cv.text;cvId=v.cv.id;syncCV();pendingRequest=null;pendingQuestion='';$('clarification').classList.add('hidden');$('generation-error').classList.add('hidden');busy=true;updateButtons();try{await renderResult();status('Version '+v.number+' restored. Refine it in the composer.')}finally{busy=false;updateButtons()}}
$('version-select').onchange=e=>restore(e.target.value);$('undo').onclick=()=>restore(activeVersion?.parent_id);$('edit-map').onclick=()=>{scrollToStep('step-one');$('story').focus({preventScroll:true})};
async function renderResult(){
 if(!result)return;versionMenu();$('generation-number').classList.add('hidden');$('result-panel').classList.remove('hidden');$('save-status').textContent='';await pmFontsReady;renderDNAMap($('map-visual'),result,renderVariant);$('full-journey').open=false;$('journey-evidence').replaceChildren();
 for(const [group,heading]of [['journey','Career experience'],['strengths','PM capabilities']]){const title=document.createElement('h4');title.textContent=heading;$('journey-evidence').append(title);for(const item of result[group]){const section=document.createElement('section'),h=document.createElement('h5'),note=document.createElement('p');h.textContent=item.label+(item.date_label?' · '+item.date_label:'');note.textContent=(item.evidence_status==='inferred'?'Inferred transferable capability. ':'')+item.evidence_note;section.append(h,note);for(const q of item.evidence_quotes){const quote=document.createElement('blockquote');quote.textContent=q.quote;section.append(quote)}for(const method of [...(item.highlights||[]),...(item.methods||[])]){const label=document.createElement('p'),quote=document.createElement('blockquote');label.textContent=method.label;quote.textContent=method.evidence_quote.quote;section.append(label,quote)}$('journey-evidence').append(section)}}
 try{await renderDNAPoster(exportCanvas,result,renderVariant)}catch{$('save-status').textContent='The image could not render. Please retry your change.'}
}
$('save').onclick=async()=>{if(!result||busy)return;busy=true;updateButtons();$('save-status').textContent='Preparing your image…';try{const drawing=await renderDNAPoster(exportCanvas,result,renderVariant);if(!drawing.ok)throw Error('Some wording does not fit. Ask for shorter wording in the composer.');const blob=await new Promise(resolve=>exportCanvas.toBlob(resolve,'image/png'));if(!blob)throw Error('Image export failed. Please retry.');const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='my-pm-career-dna.png';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);$('save-status').textContent='Your image is ready.'}catch(e){$('save-status').textContent=e.message}finally{busy=false;updateButtons()}};
function showStats(stats){$('usage-count').textContent=stats.total_generations+' PM Career DNA Maps Created';$('counter-note').textContent=stats.legacy_total_unverified!==null&&stats.legacy_total_unverified!==undefined?'New tracking since '+stats.tracking_started_on+'. Earlier totals included test runs.':stats.scope==='process'?'Preview count · not a persistent production total.':''}
async function loadStats(){try{const r=await fetch(API_ORIGIN+'/api/stats');if(!r.ok)throw Error();showStats(await r.json())}catch{$('usage-count').textContent='Map count temporarily unavailable'}}
document.addEventListener('keydown',e=>{if(e.key==='Tab')document.body.classList.add('keyboard-nav')});document.addEventListener('pointerdown',()=>document.body.classList.remove('keyboard-nav'));
window.addEventListener('pagehide',()=>{stopVoice();controller?.abort();$('story').value='';$('map-visual').replaceChildren();$('journey-evidence').replaceChildren();$('version-select').replaceChildren();$('result-panel').classList.add('hidden');window.clearDNAMap?.();versions=[];versionSerial=0;activeVersion=null;result=null;cvName='';cvText='';pendingRequest=null;syncCV();updateButtons();exportCanvas.width=0;exportCanvas.height=0});
updateButtons();loadStats();
