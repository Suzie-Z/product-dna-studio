/* PM Career DNA: one illustrated world, fixed geometry, stable per-result variant. */
(function(){
'use strict';
const WORLD='/assets/career-world-atlas.png',BRAND='/assets/pm-career-dna-logo.png',AVATARS='/assets/pm-characters-24.png',ICONS='/assets/pm-icons-24.png';
const lib=window.PM_LIBRARY,fonts=window.PM_DNA_FONTS,catalog=window.PM_VISUALS;
const hash=s=>[...s].reduce((h,c)=>(Math.imul(h,31)+c.charCodeAt(0))>>>0,17);
function platformChoices(data){const used=new Set(),out={};for(const j of data.journey){const scored=catalog.platforms.map(p=>({p,score:p.semantics.includes(j.icon)?10:0,tie:hash(j.label+j.description+p.id)})).sort((a,b)=>b.score-a.score||a.tie-b.tie);const choice=scored.find(x=>!used.has(x.p.id))||scored[0];out[j.id]=choice.p.id;used.add(choice.p.id)}return out}
let fontsLoaded=false;
window.pmFontsReady=Promise.all(Object.values(fonts).map(async f=>{const face=await new FontFace(f.family,'url('+f.url+')',{weight:'600'}).load();document.fonts.add(face)})).then(()=>fontsLoaded=true,()=>false);
const fontFor=weight=>weight>=700?'heading':'body';
document.querySelector('.brand-symbol').src=BRAND;
const favicon=document.createElement('link');favicon.rel='icon';favicon.href=BRAND;document.head.append(favicon);
const names=['growth','conversion','platform','api','operations','ai','analytics','experimentation','trust_safety','user_insight','strategy','roadmap','ux','commerce','mobile','saas','enterprise','content','marketplace','recommendation','monetization','collaboration','delivery','automation'];
const aliases={chart:'analytics','trending-up':'growth',layers:'platform',brain:'ai',shield:'trust_safety',code:'api',users:'user_insight',finance:'monetization',compass:'strategy',globe:'marketplace',spark:'strategy'};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const measure=document.createElement('canvas').getContext('2d');measure.fontKerning='none';
let themeBag=[],avatarBag=[],layoutBag=[],lastTheme=-1,lastAvatar=-1,lastLayout=-1;
function refill(size,previous){const a=Array.from({length:size},(_,i)=>i);for(let i=a.length-1;i>0;i--){const v=new Uint32Array(1);crypto.getRandomValues(v);const j=v[0]%(i+1);[a[i],a[j]]=[a[j],a[i]]}if(a[a.length-1]===previous)[a[0],a[a.length-1]]=[a[a.length-1],a[0]];return a}
window.nextPMVariant=(data)=>{if(!themeBag.length)themeBag=refill(lib.themes.length,lastTheme);if(!avatarBag.length)avatarBag=refill(24,lastAvatar);if(!layoutBag.length)layoutBag=refill(2,lastLayout);lastLayout=layoutBag.pop();lastTheme=themeBag.pop();lastAvatar=avatarBag.pop();return Object.freeze({theme_id:lib.themes[lastTheme].id,avatar_id:'pm_avatar_'+String(lastAvatar+1).padStart(2,'0'),character_side:lastLayout?'right':'left',template_version:'pm-studio-handoff',density:'compact',contrast:'standard',softness:'standard',mascot_visible:true,decorations:'garden',icon_overrides:{},pathway_id:data?.journey_type==='chronological'?'stones':data?.strengths.some(s=>['analytics','operations','automation'].includes(s.icon))?'streams':data?.strengths.some(s=>['experimentation','ux','user_insight'].includes(s.icon))?'constellation':'glow',platform_overrides:data?platformChoices(data):{}})};
function resolveVariant(v){return {theme:lib.themes.find(t=>t.id===v?.theme_id)||lib.themes[0],avatar:/^pm_avatar_(0[1-9]|1[0-9]|2[0-4])$/.test(v?.avatar_id)?Number(v.avatar_id.slice(-2))-1:0}}
function tint(hex,white=.85){const rgb=hex.slice(1).match(/../g).map(v=>Math.round(parseInt(v,16)*(1-white)+255*white));return '#'+rgb.map(v=>v.toString(16).padStart(2,'0')).join('')}
function build(data,mobile=false,variant){
 if(data.status!=='ready'||!data.journey.length||data.journey.length>4||!data.strengths.length||data.strengths.length>4)throw Error('A PM map needs 1–4 supported roles and capabilities.');
 const resolved=resolveVariant(variant),theme={...resolved.theme,background:[...resolved.theme.background],accents:[...resolved.theme.accents]},avatar=resolved.avatar,W=mobile?760:1600,n=data.journey.length,k=data.strengths.length;
 if(variant?.softness==='soft'){theme.background=theme.background.map(c=>tint(c,.4));theme.primary=tint(theme.primary,.15)}if(variant?.contrast==='high'){theme.ink='#100c24';theme.primary={sky_blue:'#226db3',mint_green:'#187a62',warm_yellow:'#9a6716',peach_coral:'#a64c48',teal_sage:'#24716d',lilac_light:'#7240ae'}[theme.id]}
 const platforms={...platformChoices(data),...(variant?.platform_overrides||{})},mascot=variant?.mascot_visible!==false;
 const unit=(W-160)/n,roleWidth=mobile?400:unit-32,characterSide=mobile?'left':variant?.character_side==='right'?'right':'left';
 function linesFor(s,width,size,kind='body'){const f=fonts[kind];let rows=1,line='';for(const word of String(s).split(/\s+/)){const next=line?line+' '+word:word,w=[...next].reduce((sum,ch)=>sum+(f.glyphs[ch]?.advance||0),0)*size/f.units;if(line&&w>width){rows++;line=word}else line=next}return rows}
 const roleBlocks=data.journey.map(j=>(j.highlights?.length?j.highlights.map(h=>({text:h.label,key:'highlight',lines:mobile?Math.min(3,linesFor(h.label,roleWidth,29)):1})): [{text:j.description,key:'description',lines:Math.min(3,linesFor(j.description,roleWidth,mobile?30:25))}]).map(b=>({...b,height:mobile?b.lines*36+4:30})));
 const blockHeights=roleBlocks.map(bs=>bs.reduce((sum,b)=>sum+b.height,0)+Math.max(0,bs.length-1)*6),hasDates=data.journey.some(j=>j.date_label),hasMethods=data.strengths.some(s=>s.methods?.length),journeyY=mobile?190:144;
 const mobileRows=data.journey.map((j,i)=>Math.max(280,102+blockHeights[i]+(j.date_label?54:12)+22)),islandY=mobile?346:338,islandH=mobile?170:92;
 const journeyH=mobile?mobileRows.reduce((sum,h)=>sum+h,0)+50:296,bridgeY=mobile?journeyY+journeyH+12:442,capY=mobile?bridgeY+72:492,cardH=mobile?340:318,capH=mobile?(mascot?300:130)+k*(cardH+(variant?.density==='comfortable'?32:20)):342,H=mobile?capY+capH+70:900;
 const prefix='pm-world-',parts=[],issues=[],boxes=[],foreground=[],artBounds=[],overflowFields=[];
 if(!fontsLoaded)issues.push('Rounded fonts are not ready.');
 const id=s=>prefix+s,url=s=>'url(#'+id(s)+')';
 function zone(key,x,y,w,h,kind){foreground.push({id:key,x,y,width:w,height:h,kind});return `data-foreground="${esc(key)}"`}
 function rect(x,y,w,h,r,fill,stroke='#ffffffe6',filter='shadow'){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="3"${filter?` filter="${url(filter)}"`:''}/>`}
 function text(s,x,y,size=26,weight=500,color=theme.ink){return `<text x="${x}" y="${y}" text-anchor="middle" dominant-baseline="middle" data-font="${fontFor(weight)}" font-family="${fonts[fontFor(weight)].family}" font-kerning="none" font-size="${size}" font-weight="600" fill="${color}">${esc(s)}</text>`}
 function fit(s,x,y,w,h,size=26,weight=500,maxLines=3,key=''){
  let f=size,rows=[];const min=key.includes(':method')?(mobile?24:20):key.includes(':highlight')?(mobile?27:23):key.includes(':date')?(mobile?30:20):mobile?(key==='signature'?22:30):key==='signature'?22:23;
  for(;f>=min;f--){measure.font=`600 ${f}px ${fonts[fontFor(weight)].family}`;rows=[];let line='';for(const word of String(s).split(/\s+/)){const next=line?line+' '+word:word;if(line&&measure.measureText(next).width>w){rows.push(line);line=word}else line=next}if(line)rows.push(line);if(rows.length<=maxLines&&rows.length*f*1.2<=h&&rows.every(r=>measure.measureText(r).width<=w))break}
  if(f<min){issues.push('Text exceeds its reserved area: '+(key||'copy'));overflowFields.push(key);return ''}
  boxes.push({text:String(s),x:x-w/2,y:y-h/2,width:w,height:h,size:f,lines:rows.length,paintedHeight:rows.length*f*1.2});
  const attr=key?zone(key,x-w/2,y-h/2,w,h,'text'):'';
  return `<g ${attr}>`+rows.map((row,i)=>text(row,x,y+(i-(rows.length-1)/2)*f*1.2,f,weight)).join('')+'</g>';
 }
 function crop(atlas,view,x,y,w,h,key=''){
  const scale=Math.min(w/view[2],h/view[3]),drawW=view[2]*scale,drawH=view[3]*scale;x+=(w-drawW)/2;y+=(h-drawH)/2;w=drawW;h=drawH;
  artBounds.push({key:key||atlas,x,y,width:w,height:h});const attr=key?zone(key,x,y,w,h,'illustration'):'';
  return `<svg ${attr} data-art="${esc(key||atlas)}" x="${x}" y="${y}" width="${w}" height="${h}" viewBox="${view.join(' ')}" preserveAspectRatio="xMidYMid meet" overflow="hidden"><use href="#${id(atlas)}"/></svg>`;
 }
 function icon(name,x,y,size,key){let i=names.indexOf(aliases[name]||name);if(i<0)i=names.indexOf('strategy');return `<g data-icon="${names[i]}"><circle cx="${x+size/2}" cy="${y+size/2}" r="${size/2}" fill="${tint(theme.primary,.8)}" opacity=".5"/>`+crop('icons',[(i%6)*256,Math.floor(i/6)*256,256,256],x,y,size,size,key)+'</g>'}
 function decor(name,x,y,w,h){const view=name==='cloud'?[520,1295,222,218]:[774,1286,243,243];return crop('world',view,x,y,w,h)}
 function pill(s,x,y,w){const rgb=tint(theme.primary,.3).slice(1).match(/../g).map(v=>{const n=parseInt(v,16)/255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4}),l=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2],ink=1.05/(l+.05)>=4.5?'#fff':theme.ink;const h=mobile?58:42;return rect(x,y,w,h,h/2,url('pill'),'#fff9')+text(s,x+w/2,y+h/2+1,mobile?31:27,750,ink)}
 function background(){return rect(0,0,W,H,36,url('background'),'none','')}
 function connections(){
  const path=variant?.pathway_id||'glow',y=mobile?journeyY+160:islandY+48,d=mobile?`M112 ${y}V${journeyY+journeyH-40}`:`M60 ${y}C300 ${y-25} 400 ${y+15} 650 ${y}S1200 ${y-10} 1540 ${y}`;
  if(path==='stones')return `<g data-component="JourneyConnection" data-pathway="stones">`+Array.from({length:mobile?6:15},(_,i)=>`<ellipse cx="${mobile?112:70+i*104}" cy="${mobile?y+i*40:y+Math.sin(i)*7}" rx="${mobile?12:23}" ry="7" fill="${tint(theme.primary,.45)}" stroke="#fff" stroke-width="2"/>`).join('')+'</g>';
  if(path==='constellation')return `<g data-component="JourneyConnection" data-pathway="constellation"><path d="${d}" stroke="${theme.primary}" opacity=".35" stroke-width="3" stroke-dasharray="3 13" fill="none"/>`+Array.from({length:mobile?7:19},(_,i)=>`<circle cx="${mobile?112:65+i*81}" cy="${mobile?y+i*35:y+Math.sin(i)*8}" r="${i%3?3:5}" fill="#fff" stroke="${theme.primary}" stroke-width="2"/>`).join('')+'</g>';
  if(path==='streams')return `<g data-component="JourneyConnection" data-pathway="streams">`+[-9,0,9].map((offset,i)=>`<path d="${d}" transform="translate(0 ${offset})" fill="none" stroke="${i===1?'#fff6ce':theme.accents[i]}" stroke-width="${i===1?5:3}" opacity=".7"/>`).join('')+'</g>';
  return `<g data-component="JourneyConnection" data-pathway="glow"><path d="${d}" stroke="#ffda7e" stroke-width="12" opacity=".5" fill="none" filter="${url('glow')}"/><path d="${d}" stroke="#fff1b9" stroke-width="5" fill="none"/><path d="${d}" stroke="#fffef3" stroke-width="2" fill="none"/></g>`;
 }
 function platform(key,x,y,w,h,ident){
  if(!catalog.platforms.some(p=>p.id===key))key='garden';
  let art='';const top=tint(theme.primary,.6),edge=theme.primary,accent=theme.accents[0];
  if(key==='garden')art=`<path d="M22 45 54 84 116 113 177 85 218 45Z" fill="${url('earth')}"/><path d="m54 84 29-29 33 58 23-59 38 31" fill="none" stroke="#9e6fc255" stroke-width="3"/><ellipse cx="120" cy="43" rx="100" ry="25" fill="${top}" stroke="#fff4d8" stroke-width="4"/><ellipse cx="120" cy="41" rx="72" ry="13" fill="#fff5cb" stroke="#fff" stroke-width="3"/><g fill="#8bbd64"><ellipse cx="32" cy="31" rx="9" ry="16" transform="rotate(-35 32 31)"/><ellipse cx="211" cy="32" rx="8" ry="15" transform="rotate(30 211 32)"/><ellipse cx="48" cy="24" rx="7" ry="12"/></g><circle cx="32" cy="44" r="5" fill="#fff6cf"/>`;
  if(key==='crystal')art=`<path d="m20 54 55-26 104 2 44 24-49 37-61 22-49-25Z" fill="${edge}" stroke="${top}" stroke-width="3"/><path d="m20 54 93 59 13-59 97 0-96-24-14 83" fill="${top}" opacity=".8"/><path d="m80 49 9-31 21-12 22 19-4 25m16 0 12-29 22-6 17 27-16 13" fill="${url('prism')}" stroke="#fff" stroke-width="3"/><ellipse cx="120" cy="57" rx="84" ry="13" fill="#ffffff99"/>`;
  if(key==='modular')art=[78,56,34].map((yy,i)=>`<path d="m25 ${yy} 92-23 99 23v17l-99 25-92-25Z" fill="${i%2?accent:edge}" stroke="#fff9" stroke-width="2"/><path d="m25 ${yy} 92-23 99 23-99 23Z" fill="${i===2?top:tint(edge,.3)}"/>`).join('');
  if(key==='steps')art=`<g stroke="#fff9" stroke-width="2"><rect x="26" y="73" width="61" height="29" rx="9" fill="${edge}"/><rect x="87" y="53" width="61" height="49" rx="9" fill="${accent}"/><rect x="148" y="32" width="61" height="70" rx="9" fill="${edge}"/><ellipse cx="57" cy="73" rx="29" ry="7" fill="${top}"/><ellipse cx="117" cy="53" rx="29" ry="7" fill="#e8f6ff"/><ellipse cx="178" cy="32" rx="29" ry="7" fill="${top}"/></g><path d="M178 31V7l25 7-25 8" fill="#ffca88" stroke="#fff" stroke-width="2"/>`;
  if(key==='nebula')art=`<ellipse cx="120" cy="87" rx="98" ry="19" fill="${edge}" opacity=".35"/><g fill="${url('prism')}" stroke="#fff9" stroke-width="2"><ellipse cx="51" cy="65" rx="32" ry="24"/><ellipse cx="92" cy="47" rx="42" ry="36"/><ellipse cx="142" cy="51" rx="41" ry="32"/><ellipse cx="186" cy="67" rx="35" ry="23"/><ellipse cx="119" cy="77" rx="80" ry="24"/></g><path d="m121 15 5 10 11 2-8 8 1 11-10-5-10 5 2-11-8-8 11-2Z" fill="#fff3bc" stroke="#fff" stroke-width="2"/>`;
  if(key==='circuit')art=`<path d="M24 46v36c0 31 192 31 192 0V46Z" fill="${edge}"/><ellipse cx="120" cy="47" rx="96" ry="29" fill="${top}" stroke="#fff" stroke-width="4"/><ellipse cx="120" cy="47" rx="76" ry="19" fill="${accent}" stroke="#dffeff" stroke-width="4"/><g fill="none" stroke="#e6ffff" stroke-width="3"><path d="M70 47h28v-12m72 12h-28v12m-24-26v30"/></g><g fill="#c8ffed"><rect x="48" y="80" width="21" height="6" rx="3"/><rect x="107" y="88" width="25" height="6" rx="3"/><rect x="174" y="80" width="21" height="6" rx="3"/></g>`;
  art=art.replaceAll('fill="'+edge+'"','fill="'+url('platformSide')+'"').replaceAll('fill="'+top+'"','fill="'+url('platformTop')+'"');
  artBounds.push({key:ident,x,y,width:w,height:h});return `<g ${zone(ident,x,y,w,h,'illustration')} data-platform="${key}" transform="translate(${x} ${y}) scale(${w/240} ${h/120})"><ellipse cx="120" cy="105" rx="90" ry="9" fill="${edge}" opacity=".12"/><g filter="${url('platformShadow')}">${art}</g></g>`;
 }

 function role(j,i){
  const x=mobile?485:80+unit*(i+.5),row=mobile?journeyY+25+mobileRows.slice(0,i).reduce((sum,h)=>sum+h,0):0;
  const symbol=variant?.icon_overrides?.[j.id]||j.icon||lib.roles.find(r=>r.display_label===j.label)?.preferred_icon_id||'strategy';
  let out=`<g data-component="CareerJourneyIsland">`+icon(symbol,mobile?70:x-40,mobile?row+22:166,mobile?88:52,j.id+':icon');
  out+=fit(j.label,x,mobile?row+55:238,mobile?400:unit-56,mobile?76:34,mobile?34:28,800,2,j.id+':label');
  let textY=mobile?row+102:hasDates?286:266;
  roleBlocks[i].forEach((block,index)=>{out+=fit(block.text,x,textY+block.height/2,roleWidth,block.height,mobile?(block.key==='description'?30:29):23,500,mobile?3:1,j.id+':'+block.key+index);textY+=block.height+6});
  if(j.date_label)out+=fit(j.date_label,x,mobile?textY+20:270,mobile?400:unit-64,mobile?36:24,mobile?30:20,500,1,j.id+':date');
  out+=platform(platforms[j.id],mobile?48:x-100,mobile?row+145:islandY+(hasDates?20:0),mobile?135:200,mobile?100:islandH-(hasDates?20:0),j.id+':island');
  if(data.journey_type==='chronological'&&i<n-1){const xx=mobile?112:x+unit/2,yy=mobile?row+mobileRows[i]-15:385;out+=`<path d="${mobile?`m${xx-8} ${yy-7} 8 8 8-8`:`m${xx-7} ${yy-10} 10 10-10 10`}" fill="none" stroke="${theme.primary}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`}
  if(!mobile&&variant?.pathway_id==='streams')out+=`<path d="M${x} ${journeyY+journeyH-10}Q${x} ${bridgeY+32} ${W/2} ${bridgeY+32}" fill="none" stroke="#ffe8ad" stroke-width="8" opacity=".7" filter="${url('glow')}"/>`;
  return out+'</g>';
 }
 function character(){if(!mascot)return '';return `<g data-component="CareerCharacter">${crop('avatars',[(avatar%6)*256,Math.floor(avatar/6)*256,256,256],mobile?30:characterSide==='right'?W-235:25,capY+(mobile?15:60),mobile?280:210,mobile?280:210,'human-chibi')}</g>`}
 function capability(s,i){
  const gap=variant?.density==='comfortable'?24:18,available=mobile?680:mascot?(variant?.density==='comfortable'?1270:1310):1540,w=mobile?680:(available-gap*(k-1))/k,x=mobile?40:(!mascot?30:characterSide==='right'?25:(variant?.density==='comfortable'?285:265))+i*(w+gap),y=mobile?capY+(mascot?300:130)+i*(cardH+(variant?.density==='comfortable'?32:20)):capY+15,h=cardH;
  let out=`<g data-component="CapabilityCard">${rect(x,y,w,h,40,url('card'+i),'#fff','cardShadow')}`;
  out+=icon(variant?.icon_overrides?.[s.id]||s.icon,mobile?x+28:x+w/2-26,mobile?y+88:y+8,mobile?90:52,s.id+':icon');
  out+=fit(s.label,mobile?x+400:x+w/2,mobile?y+55:y+98,mobile?480:w-32,mobile?80:70,mobile?35:28,800,mobile?3:2,s.id+':label');
  out+=fit(s.description,mobile?x+400:x+w/2,mobile?y+155:y+(hasMethods?176:184),mobile?480:w-32,mobile?108:84,mobile?30:23,500,3,s.id+':description');
  const methods=s.methods||[];
  if(methods.length){
   const mx=mobile?x+155:x+14,mw=mobile?w-170:w-28,my=y+(mobile?225:226),mh=mobile?108:84;
   out+=rect(mx,my,mw,mh,28,'#ffffff9c','#ffffffd9','');
   methods.forEach((m,index)=>{out+=fit(m.label,mx+mw/2,my+mh/2+(index-(methods.length-1)/2)*(mobile?36:28),mw-20,mobile?36:26,mobile?25:20,550,1,s.id+':method'+index)});
  }
  return out+'</g>';
 }
 parts.push(`<svg xmlns="http://www.w3.org/2000/svg" data-world="pm-illustrated-3d" data-theme="${theme.id}" data-avatar="pm_avatar_${String(avatar+1).padStart(2,'0')}" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-labelledby="${id('title')} ${id('desc')}" style="font-family:Arial,sans-serif"><title id="${id('title')}">My PM Career DNA — ${esc(data.career_signature)}</title><desc id="${id('desc')}">${esc(data.superpower)}. One evidence-grounded PM journey and capability map.</desc><defs><image id="${id('world')}" href="${WORLD}" width="1024" height="1536"/><image id="${id('avatars')}" href="${AVATARS}" width="1536" height="1024"/><image id="${id('icons')}" href="${ICONS}" width="1536" height="1024"/>
 <filter id="${id('platformShadow')}" x="-15%" y="-25%" width="130%" height="150%"><feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="${theme.primary}" flood-opacity=".22"/></filter><linearGradient id="${id('platformTop')}" x2=".8" y2="1"><stop stop-color="#fffaff"/><stop offset=".45" stop-color="${tint(theme.primary,.7)}"/><stop offset="1" stop-color="${tint(theme.primary,.3)}"/></linearGradient><linearGradient id="${id('platformSide')}" x2=".2" y2="1"><stop stop-color="${tint(theme.primary,.35)}"/><stop offset="1" stop-color="${theme.primary}"/></linearGradient><linearGradient id="${id('earth')}" x2="0" y2="1"><stop stop-color="#f3c28c"/><stop offset="1" stop-color="#b37992"/></linearGradient><linearGradient id="${id('prism')}" x2=".8" y2="1"><stop stop-color="#fff7ff"/><stop offset="1" stop-color="${theme.primary}"/></linearGradient><linearGradient id="${id('background')}" x2="1" y2="1"><stop stop-color="${theme.background[0]}"/><stop offset="1" stop-color="${theme.background[1]}"/></linearGradient>
 <linearGradient id="${id('panel')}" x2=".7" y2="1"><stop stop-color="#ffffffcc"/><stop offset="1" stop-color="${tint(theme.primary)}"/></linearGradient>
 <linearGradient id="${id('pill')}" x2="0" y2="1"><stop stop-color="${tint(theme.primary,.3)}"/><stop offset="1" stop-color="${theme.primary}"/></linearGradient>
 <filter id="${id('shadow')}" x="-25%" y="-40%" width="150%" height="185%"><feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="${theme.primary}" flood-opacity=".2"/></filter>
 <filter id="${id('cardShadow')}" x="-25%" y="-20%" width="150%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="${theme.primary}" flood-opacity=".23"/></filter>
 <filter id="${id('glow')}" x="-30%" y="-150%" width="160%" height="400%"><feGaussianBlur stdDeviation="6"/></filter>`);
 [theme.primary,...theme.accents].forEach((color,i)=>parts.push(`<linearGradient id="${id('card'+i)}" x2=".7" y2="1"><stop stop-color="#fff"/><stop offset="1" stop-color="${tint(color,.78)}"/></linearGradient>`));
 const titleSize=mobile?42:48,titleText='My PM Career DNA',titleWidth=[...titleText].reduce((sum,ch)=>sum+(fonts.heading.glyphs[ch]?.advance||0),0)*titleSize/fonts.heading.units,logoSize=mobile?52:54,logoGap=mobile?12:16,headerWidth=Math.min(W-32,titleWidth+2*(logoSize+logoGap+22)),logoX=W/2-titleWidth/2-logoGap-logoSize;
 parts.push('</defs>',background(),rect(W/2-headerWidth/2,mobile?22:16,headerWidth,mobile?100:82,35,'#ffffffeb','#fff'),`<image ${zone('brand',logoX,(mobile?74:58)-logoSize/2,logoSize,logoSize,'illustration')} href="${BRAND}" x="${logoX}" y="${(mobile?74:58)-logoSize/2}" width="${logoSize}" height="${logoSize}"/>`,fit(titleText,W/2,mobile?74:58,titleWidth+2,mobile?78:64,titleSize,800,1,'title'),fit(data.career_signature,W/2,mobile?158:118,W-140,mobile?36:28,mobile?25:22,600,1,'signature'));
 parts.push(rect(10,journeyY,W-20,journeyH,60,url('panel'),'#fff'),connections());data.journey.forEach((j,i)=>parts.push(role(j,i)));
 if(!variant?.decorations||variant.decorations==='garden')parts.push(decor('garden',16,journeyY+journeyH-70,mobile?25:90,70),decor('garden',W-16-(mobile?25:90),journeyY+journeyH-70,mobile?25:90,70),'');if(variant?.decorations==='sparkles')parts.push([28,W-28].map(x=>`<path d="M${x} ${journeyY+journeyH-55}l5 10 10 5-10 5-5 10-5-10-10-5 10-5Z" fill="${theme.primary}" opacity=".45"/>`).join(''));parts.push(pill('My PM Journey',mobile?30:36,journeyY-(mobile?30:22),mobile?330:350));
 parts.push(rect(10,capY,W-20,capH,60,url('panel'),'#fff'),character());
 if(mobile)parts.push(fit(data.superpower,mascot?530:W/2,capY+(mascot?155:65),mascot?360:W-100,mascot?180:112,30,500,mascot?5:3,'superpower'));
 data.strengths.forEach((s,i)=>parts.push(capability(s,i)));parts.push(pill('Shaped My PM DNA',W/2-240,bridgeY,480));
 if(!mobile)parts.push(fit(data.superpower,W/2,H-55,W-180,32,23,500,1,'superpower'));
 parts.push(text('PM Career Studio',W/2,H-24,mobile?18:20,500,'#566271'),'</svg>');
 const collisions=[];
 for(let i=0;i<foreground.length;i++)for(let j=i+1;j<foreground.length;j++){
  const a=foreground[i],b=foreground[j];if(Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>.5&&Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>.5)collisions.push([a.id,b.id]);
 }
 if(collisions.length)issues.push('Foreground regions overlap.');
 const clipped=artBounds.filter(b=>b.x<12||b.y<12||b.x+b.width>W-12||b.y+b.height>H-12);if(clipped.length)issues.push('An illustration is outside safe canvas margins.');
 return {svg:parts.join(''),metrics:{ok:!issues.length,issues,overflowFields,boxes,foreground,collisions,width:W,height:H,theme_id:theme.id,avatar_id:'pm_avatar_'+String(avatar+1).padStart(2,'0'),oneResult:true,platforms,pathway:variant?.pathway_id||'glow',header:{title_center_x:W/2,logo_gap:logoGap},artBounds,clipped,character_side:characterSide,fontsLoaded,headingFont:fonts.heading.family,bodyFont:fonts.body.family}};
}
window.buildDNAScene=build;
let current=null;window.clearDNAMap=()=>{current=null};const query=matchMedia('(max-width:1000px)');
window.renderDNAMap=(target,data,variant)=>{current={target,data,variant};const scene=build(data,query.matches,variant);target.innerHTML=scene.svg;target.dataset.layout=query.matches?'mobile':'desktop';target.renderMetrics=scene.metrics;return scene.metrics};
query.addEventListener('change',()=>{if(current)window.renderDNAMap(current.target,current.data,current.variant)});
function outlineText(svg){
 const root=new DOMParser().parseFromString(svg,'image/svg+xml').documentElement,ns='http://www.w3.org/2000/svg';let count=0;
 for(const el of [...root.querySelectorAll('text')]){
  const f=fonts[el.dataset.font||'body'],size=Number(el.getAttribute('font-size')),scale=size/f.units,glyphs=[...el.textContent].map(ch=>f.glyphs[ch]);
  if(glyphs.some(g=>!g))throw Error('A display character is not supported by the rounded font.');
  const width=glyphs.reduce((n,g)=>n+g.advance,0),group=document.createElementNS(ns,'g');group.setAttribute('fill',el.getAttribute('fill'));group.setAttribute('transform',`translate(${Number(el.getAttribute('x'))-width*scale/2} ${Number(el.getAttribute('y'))+f.xHeight*scale/2}) scale(${scale} ${-scale})`);group.setAttribute('data-outlined-text',el.textContent);
  let advance=0;for(const glyph of glyphs){if(glyph.path){const path=document.createElementNS(ns,'path');path.setAttribute('d',glyph.path);path.setAttribute('transform',`translate(${advance} 0)`);group.append(path)}advance+=glyph.advance}el.replaceWith(group);count++;
 }
 return {svg:new XMLSerializer().serializeToString(root),count};
}
window.renderDNAPoster=async(canvas,data,variant)=>{
 await window.pmFontsReady;const scene=build(data,false,variant),outlined=outlineText(scene.svg);scene.metrics.outlinedText=true;scene.metrics.exportTextCount=outlined.count;
 const blob=new Blob([outlined.svg],{type:'image/svg+xml;charset=utf-8'}),url=URL.createObjectURL(blob);
 try{const img=new Image();await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=()=>reject(Error('PM illustration assets could not load.'));img.src=url});canvas.width=scene.metrics.width*2;canvas.height=scene.metrics.height*2;canvas.getContext('2d').drawImage(img,0,0,canvas.width,canvas.height);canvas.renderMetrics=scene.metrics;return scene.metrics}finally{URL.revokeObjectURL(url)}
};
})();
