/* PM Career DNA: one illustrated world, fixed geometry, stable per-result variant. */
(function(){
'use strict';
const WORLD='/assets/career-world-atlas.png',BRAND='/assets/pm-career-dna-logo.png',AVATARS='/assets/pm-characters-24.png',ICONS='/assets/pm-icons-24.png';
const lib=window.PM_LIBRARY;
document.querySelector('.brand-symbol').src=BRAND;
const favicon=document.createElement('link');favicon.rel='icon';favicon.href=BRAND;document.head.append(favicon);
const names=['growth','conversion','platform','api','operations','ai','analytics','experimentation','trust_safety','user_insight','strategy','roadmap','ux','commerce','mobile','saas','enterprise','content','marketplace','recommendation','monetization','collaboration','delivery','automation'];
const aliases={chart:'analytics','trending-up':'growth',layers:'platform',brain:'ai',shield:'trust_safety',code:'api',users:'user_insight',finance:'monetization',compass:'strategy',globe:'marketplace',spark:'strategy'};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const measure=document.createElement('canvas').getContext('2d');
let themeBag=[],avatarBag=[],lastTheme=-1,lastAvatar=-1;
function refill(size,previous){const a=Array.from({length:size},(_,i)=>i);for(let i=a.length-1;i>0;i--){const v=new Uint32Array(1);crypto.getRandomValues(v);const j=v[0]%(i+1);[a[i],a[j]]=[a[j],a[i]]}if(a[a.length-1]===previous)[a[0],a[a.length-1]]=[a[a.length-1],a[0]];return a}
window.nextPMVariant=()=>{if(!themeBag.length)themeBag=refill(lib.themes.length,lastTheme);if(!avatarBag.length)avatarBag=refill(24,lastAvatar);lastTheme=themeBag.pop();lastAvatar=avatarBag.pop();return Object.freeze({theme_id:lib.themes[lastTheme].id,avatar_id:'pm_avatar_'+String(lastAvatar+1).padStart(2,'0'),template_version:'pm-world-v3-editorial'})};
function resolveVariant(v){return {theme:lib.themes.find(t=>t.id===v?.theme_id)||lib.themes[0],avatar:/^pm_avatar_(0[1-9]|1[0-9]|2[0-4])$/.test(v?.avatar_id)?Number(v.avatar_id.slice(-2))-1:0}}
function tint(hex,white=.85){const rgb=hex.slice(1).match(/../g).map(v=>Math.round(parseInt(v,16)*(1-white)+255*white));return '#'+rgb.map(v=>v.toString(16).padStart(2,'0')).join('')}
function build(data,mobile=false,variant){
 if(data.status!=='ready'||!data.journey.length||data.journey.length>4||!data.strengths.length||data.strengths.length>4)throw Error('A PM map needs 1–4 supported roles and capabilities.');
 const {theme,avatar}=resolveVariant(variant),W=mobile?760:1600,n=data.journey.length,k=data.strengths.length;
 const hasMethods=data.strengths.some(s=>s.methods?.length),journeyY=200,journeyH=mobile?n*300+50:370,bridgeY=journeyY+journeyH+20,capY=bridgeY+80,cardH=300,capH=mobile?300+k*(cardH+20):cardH+30,H=capY+capH+(mobile?70:80);
 const prefix='pm-world-',parts=[],issues=[],boxes=[],foreground=[];
 const id=s=>prefix+s,url=s=>'url(#'+id(s)+')';
 function zone(key,x,y,w,h,kind){foreground.push({id:key,x,y,width:w,height:h,kind});return `data-foreground="${esc(key)}"`}
 function rect(x,y,w,h,r,fill,stroke='#ffffffe6',filter='shadow'){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="3"${filter?` filter="${url(filter)}"`:''}/>`}
 function text(s,x,y,size=26,weight=500,color='#171333'){return `<text x="${x}" y="${y}" text-anchor="middle" dominant-baseline="middle" font-size="${size}" font-weight="${weight}" fill="${color}">${esc(s)}</text>`}
 function fit(s,x,y,w,h,size=26,weight=500,maxLines=3,key=''){
  let f=size,rows=[];const min=key.includes(':method')?(mobile?24:18):mobile?(key==='signature'?22:30):20;
  for(;f>=min;f--){measure.font=`${weight} ${f}px Arial`;rows=[];let line='';for(const word of String(s).split(/\s+/)){const next=line?line+' '+word:word;if(line&&measure.measureText(next).width>w){rows.push(line);line=word}else line=next}if(line)rows.push(line);if(rows.length<=maxLines&&rows.length*f*1.2<=h&&rows.every(r=>measure.measureText(r).width<=w))break}
  if(f<min){issues.push('Text exceeds its reserved area: '+(key||'copy'));return text('Regenerate for shorter wording',x,y,min,500,'#77578d')}
  boxes.push({text:String(s),x:x-w/2,y:y-h/2,width:w,height:h,size:f,lines:rows.length,paintedHeight:rows.length*f*1.2});
  const attr=key?zone(key,x-w/2,y-h/2,w,h,'text'):'';
  return `<g ${attr}>`+rows.map((row,i)=>text(row,x,y+(i-(rows.length-1)/2)*f*1.2,f,weight)).join('')+'</g>';
 }
 function crop(atlas,view,x,y,w,h,key=''){
  const attr=key?zone(key,x,y,w,h,'illustration'):'';
  return `<svg ${attr} data-art="${esc(key||atlas)}" x="${x}" y="${y}" width="${w}" height="${h}" viewBox="${view.join(' ')}" preserveAspectRatio="none" overflow="hidden"><use href="#${id(atlas)}"/></svg>`;
 }
 function icon(name,x,y,size,key){const i=Math.max(0,names.indexOf(aliases[name]||name));return crop('icons',[(i%6)*256+8,Math.floor(i/6)*256+8,240,240],x,y,size,size,key)}
 function decor(name,x,y,w,h){const view=name==='cloud'?[520,1295,222,218]:[774,1286,243,243];return crop('world',view,x,y,w,h)}
 function pill(s,x,y,w){return rect(x,y,w,58,29,url('pill'),'#fff9')+text(s,x+w/2,y+31,31,750,'#fff')}
 function background(){return rect(0,0,W,H,36,url('background'),'none','')+decor('cloud',0,mobile?0:5,mobile?120:300,mobile?40:160)+decor('cloud',W-(mobile?120:300),mobile?0:5,mobile?120:300,mobile?40:160)}
 function connections(){
  const d=mobile?`M112 ${journeyY+160}V${journeyY+journeyH-40}`:`M60 515C260 480 350 525 500 510S750 490 900 520 1200 480 1540 515`;
  return `<g data-component="JourneyConnection"><path d="${d}" stroke="#ffda7e" stroke-width="17" opacity=".55" fill="none" filter="${url('glow')}"/><path d="${d}" stroke="#ffe69c" stroke-width="8" fill="none"/><path d="${d}" stroke="#fffef3" stroke-width="3" fill="none"/></g>`;
 }
 function role(j,i){
  const unit=(W-160)/n,x=mobile?485:80+unit*(i+.5),row=mobile?journeyY+25+i*300:0;
  const preferred=lib.roles.find(r=>r.display_label===j.label)?.preferred_icon_id;
  const symbol=preferred?names[Number(preferred.slice(-2))-1]:j.label==='Growth Hacker'?'growth':j.icon;
  let out=`<g data-component="CareerJourneyIsland">`+icon(symbol,mobile?70:x-40,mobile?row+25:235,mobile?88:72,j.id+':icon');
  out+=fit(j.label,x,mobile?row+60:340,mobile?400:unit-56,mobile?80:60,mobile?34:30,800,2,j.id+':label');
  out+=fit(j.description,x,mobile?row+155:403,mobile?400:unit-64,mobile?108:54,mobile?30:25,500,mobile?3:2,j.id+':description');
  if(j.date_label)out+=fit(j.date_label,x,mobile?row+246:450,mobile?400:unit-64,mobile?36:26,mobile?30:20,500,1,j.id+':date');
  out+=crop('world',[i*256,32,256,211],mobile?50:x-136,mobile?row+140:470,mobile?130:250,mobile?105:90,j.id+':island');
  if(data.journey_type==='chronological'&&i<n-1){const xx=mobile?112:x+unit/2,yy=mobile?row+285:392;out+=`<path d="${mobile?`m${xx-8} ${yy-7} 8 8 8-8`:`m${xx-7} ${yy-10} 10 10-10 10`}" fill="none" stroke="${theme.primary}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`}
  if(!mobile)out+=`<path d="M${x} ${journeyY+journeyH-10}Q${x} ${bridgeY+32} ${W/2} ${bridgeY+32}" fill="none" stroke="#ffe8ad" stroke-width="8" opacity=".7" filter="${url('glow')}"/>`;
  return out+'</g>';
 }
 function character(){return `<g data-component="CareerCharacter">${crop('avatars',[(avatar%6)*256,Math.floor(avatar/6)*256,256,256],mobile?30:25,capY+15,mobile?280:300,mobile?280:300,'human-chibi')}</g>`}
 function capability(s,i){
  const gap=18,available=mobile?680:1215,w=mobile?680:(available-gap*(k-1))/k,x=mobile?40:355+i*(w+gap),y=mobile?capY+300+i*(cardH+20):capY+15,h=cardH;
  let out=`<g data-component="CapabilityCard">${rect(x,y,w,h,40,url('card'+i),'#fff','cardShadow')}<rect x="${x+7}" y="${y+7}" width="${w-14}" height="${h-14}" rx="34" fill="none" stroke="#ffffffaa" stroke-width="3"/>`;
  out+=icon(s.icon,mobile?x+28:x+w/2-35,mobile?y+88:y+8,mobile?90:64,s.id+':icon');
  out+=fit(s.label,mobile?x+400:x+w/2,mobile?y+55:y+103,mobile?480:w-38,mobile?80:58,mobile?35:27,800,2,s.id+':label');
  out+=fit(s.description,mobile?x+400:x+w/2,mobile?y+150:y+(hasMethods?170:185),mobile?480:w-42,mobile?108:74,mobile?30:23,500,3,s.id+':description');
  const methods=s.methods||[];
  if(methods.length){
   const mx=mobile?x+155:x+14,mw=mobile?w-170:w-28,my=y+(mobile?205:213),mh=mobile?90:76;
   out+=rect(mx,my,mw,mh,28,'#ffffff9c','#ffffffd9','');
   methods.forEach((m,index)=>{out+=fit(m.label,mx+mw/2,my+mh/2+(index-(methods.length-1)/2)*(mobile?30:23),mw-20,mobile?30:23,mobile?25:20,550,1,s.id+':method'+index)});
  }
  return out+'</g>';
 }
 parts.push(`<svg xmlns="http://www.w3.org/2000/svg" data-world="pm-illustrated-3d" data-theme="${theme.id}" data-avatar="pm_avatar_${String(avatar+1).padStart(2,'0')}" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-labelledby="${id('title')} ${id('desc')}" style="font-family:Arial,sans-serif"><title id="${id('title')}">My PM Career DNA — ${esc(data.career_signature)}</title><desc id="${id('desc')}">${esc(data.superpower)}. One evidence-grounded PM journey and capability map.</desc><defs><image id="${id('world')}" href="${WORLD}" width="1024" height="1536"/><image id="${id('avatars')}" href="${AVATARS}" width="1536" height="1024"/><image id="${id('icons')}" href="${ICONS}" width="1536" height="1024"/>
 <linearGradient id="${id('background')}" x2="1" y2="1"><stop stop-color="${theme.background[0]}"/><stop offset="1" stop-color="${theme.background[1]}"/></linearGradient>
 <linearGradient id="${id('panel')}" x2=".7" y2="1"><stop stop-color="#ffffffcc"/><stop offset="1" stop-color="${tint(theme.primary)}"/></linearGradient>
 <linearGradient id="${id('pill')}" x2="0" y2="1"><stop stop-color="${tint(theme.primary,.3)}"/><stop offset="1" stop-color="${theme.primary}"/></linearGradient>
 <filter id="${id('shadow')}" x="-25%" y="-40%" width="150%" height="185%"><feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="${theme.primary}" flood-opacity=".2"/></filter>
 <filter id="${id('cardShadow')}" x="-25%" y="-20%" width="150%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="${theme.primary}" flood-opacity=".23"/></filter>
 <filter id="${id('glow')}" x="-30%" y="-150%" width="160%" height="400%"><feGaussianBlur stdDeviation="6"/></filter>`);
 [theme.primary,...theme.accents].forEach((color,i)=>parts.push(`<linearGradient id="${id('card'+i)}" x2=".7" y2="1"><stop stop-color="#fff"/><stop offset="1" stop-color="${tint(color,.78)}"/></linearGradient>`));
 parts.push('</defs>',background(),rect(mobile?30:390,22,mobile?700:820,100,35,'#ffffffeb','#fff'),`<image ${zone('brand',mobile?50:420,37,72,72,'illustration')} href="${BRAND}" x="${mobile?50:420}" y="37" width="72" height="72"/>`,fit('My PM Career DNA',mobile?450:900,74,mobile?490:600,78,mobile?42:54,800,1,'title'),fit(data.career_signature,W/2,158,W-140,36,mobile?25:25,600,1,'signature'));
 parts.push(rect(10,journeyY,W-20,journeyH,60,url('panel'),'#fff'),connections());data.journey.forEach((j,i)=>parts.push(role(j,i)));
 parts.push(decor('garden',0,journeyY+journeyH-70,mobile?25:90,70),decor('garden',W-(mobile?25:90),journeyY+journeyH-70,mobile?25:90,70),pill('My PM Journey',mobile?30:36,journeyY-30,mobile?330:350));
 parts.push(rect(10,capY,W-20,capH,60,url('panel'),'#fff'),character());
 if(mobile)parts.push(fit(data.superpower,530,capY+155,360,180,30,500,5,'superpower'));
 data.strengths.forEach((s,i)=>parts.push(capability(s,i)));parts.push(pill('Shape My PM DNA',W/2-240,bridgeY,480));
 if(!mobile)parts.push(fit(data.superpower,W/2,H-55,W-180,32,23,500,1,'superpower'));
 parts.push(text('PM Career DNA',W/2,H-24,15,500,'#6a7d88'),'</svg>');
 const collisions=[];
 for(let i=0;i<foreground.length;i++)for(let j=i+1;j<foreground.length;j++){
  const a=foreground[i],b=foreground[j];if(Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>.5&&Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>.5)collisions.push([a.id,b.id]);
 }
 if(collisions.length)issues.push('Foreground regions overlap.');
 return {svg:parts.join(''),metrics:{ok:!issues.length,issues,boxes,foreground,collisions,width:W,height:H,theme_id:theme.id,avatar_id:'pm_avatar_'+String(avatar+1).padStart(2,'0'),oneResult:true}};
}
window.buildDNAScene=build;
let current=null;const query=matchMedia('(max-width:700px)');
window.renderDNAMap=(target,data,variant)=>{current={target,data,variant};const scene=build(data,query.matches,variant);target.innerHTML=scene.svg;target.dataset.layout=query.matches?'mobile':'desktop';target.renderMetrics=scene.metrics;return scene.metrics};
query.addEventListener('change',()=>{if(current)window.renderDNAMap(current.target,current.data,current.variant)});
window.renderDNAPoster=async(canvas,data,variant)=>{
 const scene=build(data,false,variant);await document.fonts.ready;
 const blob=new Blob([scene.svg],{type:'image/svg+xml;charset=utf-8'}),url=URL.createObjectURL(blob);
 try{const img=new Image();await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=()=>reject(Error('PM illustration assets could not load.'));img.src=url});canvas.width=scene.metrics.width*2;canvas.height=scene.metrics.height*2;canvas.getContext('2d').drawImage(img,0,0,canvas.width,canvas.height);canvas.renderMetrics=scene.metrics;return scene.metrics}finally{URL.revokeObjectURL(url)}
};
})();
