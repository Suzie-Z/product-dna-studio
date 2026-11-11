'use strict';
const $=id=>document.getElementById(id);
const API_ORIGIN=location.hostname==='product-dna-studio-preview.onrender.com'?'https://product-dna-studio-ai.onrender.com':'';
const id=()=> 'src_'+crypto.randomUUID().replaceAll('-','');
let sourceIds={story:id(),voice:id(),cv:id()},cvName='',reading=false,uploadRun=0,recognition=null,recording=false;
let result=null,busy=false,controller=null,history=[],corrections=[],chat=[],pendingQuestion='',pendingRefinement='',dirty=false,editor=null,generationNumber=null;
function event(){} // No visitor-level analytics or client tracking.
function sources(){return [
 {source_id:sourceIds.story,source_type:'typed_story',source_label:'Written story',content:$('story').value.trim()},
 {source_id:sourceIds.cv,source_type:'cv',source_label:cvName||'CV',content:cvName?$('cv-text').value.trim():''},
 {source_id:sourceIds.voice,source_type:'voice_transcript',source_label:'Voice transcript',content:$('voice-text').value.trim()},...corrections
].filter(s=>s.content)}
function sourceLength(){return sources().reduce((n,s)=>n+s.content.length,0)}
function status(text){$('input-status').textContent=text}
function scrollToStep(which){$(which).scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}
function showStudio(){$('studio').classList.remove('hidden');historyUrl();scrollToStep('step-one');$('step-one').focus({preventScroll:true});event('hero_cta_clicked')}
function historyUrl(){window.history.replaceState(null,'','#studio')}
$('begin').onclick=showStudio;if(location.hash==='#studio')$('studio').classList.remove('hidden');
function canGenerate(){return sources().some(s=>(s.content.match(/\p{L}/gu)||[]).length>=8)}
function updateButtons(){
 $('generate').disabled=busy||reading||!canGenerate();$('update').disabled=busy||!result||!$('refinement').value.trim()||!$('refine-consent').checked;
 $('save').disabled=busy||!result||(dirty&&!$('review-confirm').checked);$('copy-caption').disabled=busy||!result||dirty;$('undo').disabled=busy||!history.length;
 for(const key of ['story','cv-text','voice-text','name','upload','voice','clear-cv','clear-voice','start-over','format','answer','edit-experience','refinement','refine-consent','review-confirm'])$(key).disabled=busy;
 $('cv-text').disabled=busy||reading;for(const field of $('direct-editor').querySelectorAll('input,textarea,button'))field.disabled=busy;
 $('generate').textContent=busy?'Working…':'Generate My Career DNA';
}
function sourceChanged(){
 if(result){result=null;history=[];chat=[];corrections=[];dirty=false;$('result-panel').classList.add('hidden');$('step-three').classList.add('hidden');status('Your experience changed. Generate a new draft to use it.')}
 $('generation-error').classList.add('hidden');updateButtons();
}
for(const key of ['story','cv-text','voice-text'])$(key).addEventListener('input',sourceChanged);
$('story').addEventListener('input',()=>event('input_mode_selected:text'));
function clearCV(){uploadRun++;reading=false;cvName='';$('cv-text').value='';$('file').value='';$('cv-panel').classList.add('hidden');sourceIds.cv=id();status('');sourceChanged()}
$('clear-cv').onclick=()=>{if($('cv-text').value&&!confirm('Remove this CV and its corrected text? Your other notes will stay.'))return;clearCV()};
$('clear-voice').onclick=()=>{if(!confirm('Clear the voice transcript?'))return;$('voice-text').value='';$('voice-panel').classList.add('hidden');sourceIds.voice=id();sourceChanged()};
$('upload').onclick=()=>{if(cvName||reading){status('Only one CV at a time. Remove your current CV to upload another.');return}event('input_mode_selected:cv');$('file').click()};
function fileStatus(text,failed=false){$('cv-panel').classList.remove('hidden');$('cv-panel').classList.toggle('failed',failed);$('cv-status').textContent=(failed?'✕ ':'✓ ')+text}
async function loadScript(src,key){if(window[key])return;await new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=src;script.onload=resolve;script.onerror=()=>reject(Error('The file reader could not load. Paste your experience instead.'));document.head.append(script)})}
$('file').onchange=async e=>{
 const files=e.target.files;if(!files?.length)return;
 if(files.length!==1||cvName||reading){e.target.value='';status('Only one CV at a time. Remove your current CV first.');return}
 const file=files[0];e.target.value='';const run=++uploadRun;
 if(file.size>5*1024*1024){status('Choose a file smaller than 5 MB.');return}
 const ext=file.name.split('.').pop().toLowerCase();if(!['pdf','docx','txt'].includes(ext)){status('Choose a PDF, DOCX or TXT file.');return}
 reading=true;updateButtons();$('cv-panel').classList.remove('hidden');$('cv-status').textContent='Reading '+file.name+'…';$('cv-text').value='';
 try{
  const bytes=new Uint8Array(await file.arrayBuffer());let text='';
  if(ext==='txt'){if(bytes.includes(0))throw Error('This does not look like a text file.');text=new TextDecoder('utf-8',{fatal:true}).decode(bytes)}
  if(ext==='docx'){
   if(bytes[0]!==80||bytes[1]!==75)throw Error('This is not a valid Word document.');
   await loadScript('https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.9.1/mammoth.browser.min.js','mammoth');text=(await mammoth.extractRawText({arrayBuffer:bytes.buffer})).value;
  }
  if(ext==='pdf'){
   if(new TextDecoder().decode(bytes.slice(0,5))!=='%PDF-')throw Error('This is not a valid PDF file.');
   if(!window.pdfjsLib)window.pdfjsLib=await import('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.min.mjs');
   pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.worker.min.mjs';
   const doc=await pdfjsLib.getDocument({data:bytes}).promise;
   if(doc.numPages>15)throw Error('Use a PDF with 15 pages or fewer.');
   for(let i=1;i<=doc.numPages;i++)text+='\n'+(await(await doc.getPage(i)).getTextContent()).items.map(x=>x.str+(x.hasEOL?'\n':' ')).join('');
   await doc.destroy();
  }
  if(run!==uploadRun)return;text=text.normalize('NFKC').replace(/[\u00ad\u200b]/g,'').trim();
  if(text.length<12)throw Error('No readable text. Scanned PDFs need OCR; paste your story instead.');
  if(text.length>18000||text.length+sourceLength()>22000)throw Error('Shorten your CV and notes to 22,000 characters in total.');
  cvName=file.name.slice(0,150);$('cv-text').value=text;fileStatus(cvName+' · Ready');sourceChanged();status('');
 }catch(err){if(run===uploadRun){cvName='';fileStatus(file.name+' · '+err.message,true);status('Remove the failed file to try another, or write your story.')}}
 finally{if(run===uploadRun){reading=false;updateButtons()}}
};
function voiceIdle(){recording=false;$('voice').classList.remove('recording');$('voice').querySelector('span').textContent='Record your story'}
$('voice').onclick=()=>{
 if(recording){recognition.stop();return}
 const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){status('Voice input is unavailable in this browser. Write your story or upload a CV.');return}
 recognition=new SR();recognition.lang=navigator.language||'en-US';recognition.continuous=true;recognition.interimResults=false;
 recognition.onresult=e=>{for(let i=e.resultIndex;i<e.results.length;i++)if(e.results[i].isFinal){
  const next=$('voice-text').value+($('voice-text').value?' ':'')+e.results[i][0].transcript;
  if(next.length>12000){status('The voice transcript is full. Shorten it to continue.');recognition.stop();return}
  $('voice-panel').classList.remove('hidden');$('voice-text').value=next;sourceChanged();
 }};
 recognition.onstart=()=>{recording=true;$('voice').classList.add('recording');$('voice').querySelector('span').textContent='Stop recording';status('Listening…');event('input_mode_selected:voice')};
 recognition.onend=()=>{voiceIdle();if($('input-status').textContent==='Listening…')status('')};
 recognition.onerror=e=>{status(e.error==='not-allowed'?'Microphone permission was denied. Write your story or upload a CV.':'Voice input stopped. Try again or write your story.');voiceIdle()};
 try{recognition.start()}catch{status('The microphone could not start. Write your story instead.')}
};
function snapshot(){return {map:structuredClone(result),corrections:structuredClone(corrections),chat:structuredClone(chat),dirty}}
function remember(){if(result){history.push(snapshot());if(history.length>6)history.shift()}}
function renderChat(){
 $('chat-log').replaceChildren();for(const msg of chat){const row=document.createElement('div');row.className='chat-message '+msg.role;row.textContent=msg.text;$('chat-log').append(row)}
}
function addChat(role,text){chat.push({role,text});renderChat()}
function showError(text){$('generation-error').textContent=text;$('generation-error').classList.remove('hidden')}
async function request(path,body){
 const ownController=controller||new AbortController(),timeout=controller?null:setTimeout(()=>ownController.abort(),120000);
 try{
  const response=await fetch(API_ORIGIN+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),signal:ownController.signal});
  let data;try{data=await response.json()}catch{throw Error('The AI service is waking up. Please wait a moment and try again.')}
  if(!response.ok)throw Error(data.error||'This request could not complete. Please try again.');return data;
 }finally{if(timeout)clearTimeout(timeout)}
}
async function run(kind,body){
 busy=true;controller=new AbortController();$('loading').classList.remove('hidden');$('generation-error').classList.add('hidden');$('step-two').classList.remove('hidden');updateButtons();
 $('loading-label').textContent='Reading your journey';const phases=['Identifying evidence-backed strengths','Designing your map'];let phase=0;
 const timer=setInterval(()=>{$('loading-label').textContent=phases[Math.min(phase++,1)]},8000);
 const timeout=setTimeout(()=>controller.abort(),240000);
 try{return await request('/api/career-dna/'+kind,body)}
 catch(e){const message=e.name==='AbortError'?'Stopped waiting. A request already sent may still complete and use API quota.':e.message;showError(message);if(kind==='refine')$('refine-status').textContent=message;event(kind+'_failed');return null}
 finally{clearInterval(timer);clearTimeout(timeout);busy=false;controller=null;$('loading').classList.add('hidden');updateButtons()}
}
$('cancel').onclick=()=>controller?.abort();
function validSources(){if(sourceLength()>22000){status('Shorten the combined experience to 22,000 characters.');return false}if(!canGenerate()){status('Share a specific task, project or responsibility to begin.');return false}return true}
async function generate(){
 if(busy||reading||!validSources())return;if(recording){
  busy=true;updateButtons();await new Promise(resolve=>{const previousEnd=recognition.onend,timer=setTimeout(resolve,1500);recognition.onend=()=>{clearTimeout(timer);previousEnd?.();resolve()};try{recognition.stop()}catch{clearTimeout(timer);resolve()}});voiceIdle();busy=false;
 }
 event('experience_submitted');$('step-two').classList.remove('hidden');scrollToStep('step-two');
 const data=await run('generate',{sources:sources(),clarification_context:pendingQuestion});if(!data)return;
 if(data.map.status==='needs_more_info'){
  pendingQuestion=data.map.clarification_question;$('clarification-question').textContent=pendingQuestion;$('clarification').classList.remove('hidden');$('clarification-answer').focus();return;
 }
 result=data.map;generationNumber=data.generation_number??null;if(data.stats)showStats(data.stats);else loadStats();history=[];chat=[];dirty=false;pendingQuestion='';pendingRefinement='';$('clarification').classList.add('hidden');renderResult();event('generation_succeeded');scrollToStep('result-panel');
}
$('generate').onclick=generate;
$('answer').onclick=async()=>{const answer=$('clarification-answer').value.trim();if(!answer){$('clarification-answer').focus();return}corrections.push({source_id:id(),source_type:'typed_story',source_label:'Follow-up answer',content:answer});$('clarification-answer').value='';await generate()};
function renderResult(){
 if(!result)return;
 $('generation-number').classList.toggle('hidden',!generationNumber);$('generation-number').textContent=generationNumber?'Generation #'+generationNumber:'';
 $('result-panel').classList.remove('hidden');$('step-three').classList.remove('hidden');$('review-line').classList.toggle('hidden',!dirty);$('review-confirm').checked=false;
 const alt=`Career DNA: ${result.career_signature}. ${result.journey_type==='chronological'?'Career journey':'Experience areas'}: ${result.journey.map(x=>x.label).join(', ')}. Strengths: ${result.strengths.map(x=>x.label).join(', ')}. ${result.superpower}`;
 $('poster').setAttribute('aria-label',alt);$('poster').textContent=alt;renderDNAPoster($('poster'),result,$('format').value);
 $('map-outline').replaceChildren();
 const signature=document.createElement('div');signature.className='outline-card signature';
 const signatureEdit=document.createElement('button');signatureEdit.textContent='My Career Signature · '+result.career_signature;signatureEdit.onclick=()=>openEditor('signature');
 const superpower=document.createElement('p');superpower.textContent=result.superpower;signature.append(signatureEdit,superpower);$('map-outline').append(signature);
 for(const group of ['journey','strengths'])for(const item of result[group]){
  const card=document.createElement('div');card.className='outline-card';const button=document.createElement('button');button.textContent=item.label;button.setAttribute('aria-label','Edit '+(group==='journey'?'journey stage ':'strength ')+item.label);button.onclick=()=>openEditor(group,item.id);
  const desc=document.createElement('p');desc.textContent=item.description;const status=document.createElement('small');status.textContent=group==='journey'?(result.journey_type==='chronological'?(item.date_label||'Career stage'):'Experience area'):item.evidence_status.replaceAll('_',' ');card.append(button,desc,status);$('map-outline').append(card);
 }
 $('evidence').replaceChildren();for(const group of ['journey','strengths'])for(const item of result[group]){
  const section=document.createElement('section');section.className='evidence-item';const h=document.createElement('h4');h.textContent=item.label;const note=document.createElement('p');note.textContent=item.evidence_note;section.append(h,note);
  for(const q of item.evidence_quotes){const quote=document.createElement('blockquote');quote.textContent=q.quote;const origin=document.createElement('p');origin.textContent=sources().find(s=>s.source_id===q.source_id)?.source_label||'Experience source';section.append(quote,origin)}
  if(group==='strengths'){const linked=document.createElement('p');linked.textContent='Shaped by: '+item.journey_ids.map(j=>result.journey.find(x=>x.id===j)?.label).filter(Boolean).join(', ');section.append(linked)}
  $('evidence').append(section);
 }
 for(const warning of result.warnings||[]){const p=document.createElement('p');p.textContent=warning;$('evidence').append(p)}renderChat();updateButtons();
}
$('format').onchange=()=>{if(result)renderDNAPoster($('poster'),result,$('format').value)};
$('refinement').oninput=updateButtons;$('refine-consent').onchange=updateButtons;$('review-confirm').onchange=updateButtons;
$('update').onclick=async()=>{
 if(busy||!result)return;
 if(!$('refine-consent').checked){$('refine-status').textContent='Allow source context to be resent before refining.';return}
 const message=$('refinement').value.trim();if(message.length<3){$('refine-status').textContent='Describe the change in at least three characters.';return}
 const before=snapshot();addChat('user',message);event('refinement_requested');
 const data=await run('refine',{sources:sources(),previous:result,message,clarification_context:pendingRefinement,context_consent:true});if(!data)return;
 $('refinement').value='';
 if(data.map.status==='needs_more_info'){pendingRefinement=(message+'\nFollow-up: '+data.map.clarification_question).slice(0,2000);addChat('assistant',data.map.clarification_question);$('refine-status').textContent='Your existing map is unchanged. Answer the question to continue.';$('refinement').focus();updateButtons();return}
 history.push(before);if(history.length>6)history.shift();result=data.map;if(data.accepted_source)corrections.push(data.accepted_source);pendingRefinement='';dirty=false;addChat('assistant',data.change_summary);$('refine-status').textContent='Your map is updated.';renderResult();event('refinement_succeeded');
};
$('undo').onclick=()=>{if(!history.length||busy)return;const old=history.pop();result=old.map;corrections=old.corrections;chat=old.chat;dirty=old.dirty;pendingRefinement='';$('direct-editor').classList.add('hidden');renderResult();$('refine-status').textContent='The last change was undone.'};
$('edit-experience').onclick=()=>{scrollToStep('step-one');$('story').focus({preventScroll:true})};
$('start-over').onclick=()=>{if(!confirm('Start over and clear your experience, map and edit history?'))return;if(recording)recognition.stop();for(const key of ['story','name','cv-text','voice-text','refinement','clarification-answer'])$(key).value='';result=null;generationNumber=null;history=[];corrections=[];chat=[];pendingQuestion='';pendingRefinement='';dirty=false;cvName='';sourceIds={story:id(),voice:id(),cv:id()};for(const key of ['cv-panel','voice-panel','step-two','step-three','result-panel','clarification','direct-editor'])$(key).classList.add('hidden');$('refine-consent').checked=false;status('');updateButtons();scrollToStep('step-one')};
function openEditor(group,ident){
 if(busy)return;editor={group,id:ident};$('editor-fields').replaceChildren();$('editor-error').textContent='';
 const target=group==='signature'?result:result[group].find(x=>x.id===ident);const fields=group==='signature'?[['career_signature','Career signature',65],['superpower','Superpower',100]]:[['label','Title',group==='journey'?36:35],['description','Description',group==='journey'?80:95]];
 for(const [key,label,limit]of fields){const l=document.createElement('label');l.htmlFor='edit-'+key;l.textContent=label;const input=document.createElement(key==='description'?'textarea':'input');input.id='edit-'+key;input.name=key;input.maxLength=limit;input.value=target[key];input.required=true;$('editor-fields').append(l,input)}
 $('editor-title').textContent=group==='signature'?'Edit your Career Signature':'Edit '+target.label;$('direct-editor').classList.remove('hidden');scrollToStep('direct-editor');$('editor-fields').querySelector('input,textarea').focus({preventScroll:true});
}
function safeEnglish(value){return value.trim()&&!/[<>\u0000-\u0008]|[\p{Script=Han}\p{Script=Cyrillic}\p{Script=Arabic}\p{Script=Devanagari}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/u.test(value)&&!/[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}/.test(value)&&!/(?:https?:\/\/|www\.)/i.test(value)&&!/(?:\+?\d[\d ()-]{7,}\d)/.test(value)}
$('direct-editor').onsubmit=e=>{
 e.preventDefault();if(!result||busy)return;const draft=structuredClone(result),target=editor.group==='signature'?draft:draft[editor.group].find(x=>x.id===editor.id);
 for(const field of $('editor-fields').querySelectorAll('input,textarea')){const value=field.value.trim();if(!safeEnglish(value)){$('editor-error').textContent='Use English map text without markup or private contact details. Use chat for translation.';return}target[field.name]=value}
 if(editor.group==='signature'&&(!(target.career_signature.split(/\s+/).length>=2&&target.career_signature.split(/\s+/).length<=7)||!(target.superpower.split(/\s+/).length>=3&&target.superpower.split(/\s+/).length<=12))){$('editor-error').textContent='Use 2–7 words for your signature and 3–12 for your superpower.';return}
 if(target.description&&target.description.split(/\s+/).length>12){$('editor-error').textContent='Keep the description to 12 words or fewer.';return}
 remember();if(editor.group==='strengths'){target.evidence_status='inferred';target.evidence_note='User-edited interpretation. Review against the linked source evidence.'}result=draft;dirty=true;$('direct-editor').classList.add('hidden');renderResult();$('refine-status').textContent='Preview updated locally. Review your edits before downloading.';
};
$('close-editor').onclick=()=>$('direct-editor').classList.add('hidden');
$('copy-caption').onclick=async()=>{if(!result)return;const text=`My Career DNA: ${result.career_signature}. ${result.superpower}\n${result.strengths.map(k=>k.label).join(' · ')}`;try{await navigator.clipboard.writeText(text);$('save-status').textContent='Share text copied.'}catch{$('save-status').textContent='Clipboard access is unavailable. You can copy the map text above.'}};
$('save').onclick=async()=>{
 if(!result||busy)return;
 if(dirty&&!$('review-confirm').checked){$('save-status').textContent='Review your local edits and allow the export safety review first.';return}
 if(dirty){busy=true;updateButtons();$('save-status').textContent='Reviewing edited map text…';try{const data=await request('/api/career-dna/review',{map:result,sources:sources(),context_consent:true});result=data.map;dirty=false;renderResult()}catch(e){$('save-status').textContent=e.message;return}finally{busy=false;updateButtons()}}
 await document.fonts.ready;const drawing=renderDNAPoster($('poster'),result,$('format').value);
 if(!drawing.ok){$('save-status').textContent='Some wording is too long for the image. Shorten it using the editor or chat.';return}
 $('poster').toBlob(blob=>{if(!blob){$('save-status').textContent='Image export failed. Please try again.';return}const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='my-career-dna.png';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);$('save-status').textContent='Your Career DNA image is ready.';event('export_downloaded')},'image/png');
};
updateButtons();

function showStats(stats){
 const scope=stats.scope==='process'?' · this server run':'';
 $('usage-count').textContent=stats.total_generations+' maps created'+scope+' · '+stats.today_generations+' today';
}
async function loadStats(){try{const response=await fetch(API_ORIGIN+'/api/stats');if(!response.ok)throw Error();showStats(await response.json())}catch{$('usage-count').textContent='Generation count temporarily unavailable'}}
document.addEventListener('keydown',e=>{if(e.key==='Tab')document.body.classList.add('keyboard-nav')});
document.addEventListener('pointerdown',()=>document.body.classList.remove('keyboard-nav'));
loadStats();
