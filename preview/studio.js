'use strict';
const $=id=>document.getElementById(id);
// Export surface is never attached to the page, so CSS cannot reveal a second map.
const exportCanvas=document.createElement('canvas');
const API_ORIGIN=location.hostname==='product-dna-studio-preview.onrender.com'?'https://product-dna-studio-ai.onrender.com':'';
const id=()=> 'src_'+crypto.randomUUID().replaceAll('-','');
let sourceIds={story:id(),voice:id(),cv:id()},cvName='',reading=false,uploadRun=0,recognition=null,recording=false;
let renderVariant=null;
let result=null,busy=false,controller=null,corrections=[],pendingQuestion='',generationNumber=null;
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
 $('generate').disabled=busy||reading||!canGenerate();$('save').disabled=busy||!result;
 for(const key of ['story','cv-text','voice-text','name','upload','voice','clear-cv','clear-voice','answer'])$(key).disabled=busy;
 $('cv-text').disabled=busy||reading;
 $('generate').textContent=busy?'Working…':result?'Regenerate My PM Career DNA':'Generate My PM Career DNA';
}
function sourceChanged(){
 corrections=[];pendingQuestion='';$('clarification').classList.add('hidden');
 if(result){result=null;generationNumber=null;$('result-panel').classList.add('hidden');status('')}
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
 $('loading-label').textContent='Reading your PM journey';const phases=['Identifying evidence-backed PM capabilities','Designing your map'];let phase=0;
 const timer=setInterval(()=>{$('loading-label').textContent=phases[Math.min(phase++,1)]},8000);
 const timeout=setTimeout(()=>controller.abort(),240000);
 try{return await request('/api/career-dna/'+kind,body)}
 catch(e){const message=e.name==='AbortError'?'Stopped waiting. A request already sent may still complete and use API quota.':e.message;showError(message);event(kind+'_failed');return null}
 finally{clearInterval(timer);clearTimeout(timeout);busy=false;controller=null;$('loading').classList.add('hidden');updateButtons()}
}
$('cancel').onclick=()=>controller?.abort();
function validSources(){if(sourceLength()>22000){status('Shorten the combined experience to 22,000 characters.');return false}if(!canGenerate()){status('Share a specific task, project or responsibility to begin.');return false}return true}
async function generate(){
 if(busy||reading||!validSources())return;if(recording){
  busy=true;updateButtons();await new Promise(resolve=>{const previousEnd=recognition.onend,timer=setTimeout(resolve,1500);recognition.onend=()=>{clearTimeout(timer);previousEnd?.();resolve()};try{recognition.stop()}catch{clearTimeout(timer);resolve()}});voiceIdle();busy=false;
 }
 result=null;generationNumber=null;$('result-panel').classList.add('hidden');
 event('experience_submitted');$('step-two').classList.remove('hidden');scrollToStep('step-two');
 const data=await run('generate',{sources:sources(),clarification_context:pendingQuestion});if(!data)return;
 if(data.map.status==='needs_more_info'){
  pendingQuestion=data.map.clarification_question;$('clarification-question').textContent=pendingQuestion;$('clarification').classList.remove('hidden');$('clarification-answer').focus();return;
 }
 result=data.map;renderVariant=nextPMVariant();generationNumber=data.generation_number??null;if(data.stats)showStats(data.stats);else loadStats();pendingQuestion='';$('clarification').classList.add('hidden');busy=true;updateButtons();try{await renderResult()}finally{busy=false;updateButtons()}event('generation_succeeded');scrollToStep('result-panel');
}
$('generate').onclick=generate;
$('answer').onclick=async()=>{const answer=$('clarification-answer').value.trim();if(!answer){$('clarification-answer').focus();return}corrections.push({source_id:id(),source_type:'typed_story',source_label:'Follow-up answer',content:answer});$('clarification-answer').value='';await generate()};
async function renderResult(){
 if(!result)return;
 $('generation-number').classList.toggle('hidden',!generationNumber);$('generation-number').textContent=generationNumber?'Generation #'+generationNumber:'';
 $('result-panel').classList.remove('hidden');$('save-status').textContent='';
 await window.pmFontsReady;renderDNAMap($('map-visual'),result,renderVariant);
 $('full-journey').open=false;$('journey-evidence').replaceChildren();
 for(const [group,heading]of [['journey','PM Journey'],['strengths','Core Capabilities']]){
  const title=document.createElement('h4');title.textContent=heading;$('journey-evidence').append(title);
  for(const item of result[group]){
   const section=document.createElement('section'),h=document.createElement('h5'),note=document.createElement('p');h.textContent=item.label+(item.date_label?' · '+item.date_label:'');note.textContent=item.evidence_note;section.append(h,note);
   for(const q of item.evidence_quotes){const quote=document.createElement('blockquote');quote.textContent=q.quote;section.append(quote)}
   for(const method of [...(item.highlights||[]),...(item.methods||[])]){const label=document.createElement('p'),quote=document.createElement('blockquote');label.textContent=method.label;quote.textContent=method.evidence_quote.quote;section.append(label,quote)}
   $('journey-evidence').append(section);
  }
 }
 const original=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Original experience';original.append(summary);
 for(const source of sources()){const heading=document.createElement('h5'),content=document.createElement('p');heading.textContent=source.source_label;content.textContent=source.content;content.className='original-context';original.append(heading,content)}
 $('journey-evidence').append(original);
 try{await renderDNAPoster(exportCanvas,result,renderVariant)}catch{$('save-status').textContent='The image could not render. Try generating again.'}
}
$('save').onclick=async()=>{
 if(!result||busy)return;
 busy=true;updateButtons();$('save-status').textContent='Preparing your image…';
 try{
  const drawing=await renderDNAPoster(exportCanvas,result,renderVariant);
  if(!drawing.ok)throw Error('Some wording is too long. Adjust your story and generate again.');
  const blob=await new Promise(resolve=>exportCanvas.toBlob(resolve,'image/png'));
  if(!blob)throw Error('Image export failed. Please try again.');
  const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='my-pm-career-dna.png';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);$('save-status').textContent='Your PM Career DNA image is ready.';
 }catch(e){$('save-status').textContent=e.message}finally{busy=false;updateButtons()}
};
updateButtons();

function showStats(stats){
 const scope=stats.scope==='process'?' · this server run':'';
 $('usage-count').textContent=stats.total_generations+' maps created'+scope;
}
async function loadStats(){try{const response=await fetch(API_ORIGIN+'/api/stats');if(!response.ok)throw Error();showStats(await response.json())}catch{$('usage-count').textContent='Generation count temporarily unavailable'}}
document.addEventListener('keydown',e=>{if(e.key==='Tab')document.body.classList.add('keyboard-nav')});
document.addEventListener('pointerdown',()=>document.body.classList.remove('keyboard-nav'));
loadStats();
