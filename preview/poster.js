/* PM Career DNA: one illustrated world, fixed geometry, stable per-result variant. */
(function(){
'use strict';
const WORLD='/assets/career-world-atlas.png',BRAND='/assets/pm-career-dna-logo.png',AVATARS='/assets/pm-characters-24.png',ICONS='/assets/pm-icons-24.png';
const lib=window.PM_LIBRARY,fonts=window.PM_DNA_FONTS,catalog=window.PM_VISUALS;
const hash=s=>[...s].reduce((h,c)=>(Math.imul(h,31)+c.charCodeAt(0))>>>0,17);
function platformChoices(data){const choice=catalog.platforms[hash(data.career_signature||'PM')%catalog.platforms.length].id;return Object.fromEntries(data.journey.map(j=>[j.id,choice]))}
let fontsLoaded=false;
window.pmFontsReady=(window.uiFontsReady||Promise.all(Object.values(fonts).map(async f=>{const face=await new FontFace(f.family,'url('+f.url+')',{weight:'600'}).load();document.fonts.add(face)}))).then(()=>fontsLoaded=true,()=>false);
const fontFor=weight=>weight>=700?'heading':'body';
document.querySelector('.brand-symbol').src=BRAND;
const favicon=document.createElement('link');favicon.rel='icon';favicon.href=BRAND;document.head.append(favicon);
const names=['growth','conversion','platform','api','operations','ai','analytics','experimentation','trust_safety','user_insight','strategy','roadmap','ux','commerce','mobile','saas','enterprise','content','marketplace','recommendation','monetization','collaboration','delivery','automation'];
const aliases={chart:'analytics','trending-up':'growth',layers:'platform',brain:'ai',shield:'trust_safety',code:'api',users:'user_insight',finance:'monetization',compass:'strategy',globe:'marketplace',spark:'strategy'};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const measure=document.createElement('canvas').getContext('2d');measure.fontKerning='none';
let themeBag=[],avatarBag=[],layoutBag=[],lastTheme=-1,lastAvatar=-1,lastLayout=-1;
function refill(size,previous){const a=Array.from({length:size},(_,i)=>i);for(let i=a.length-1;i>0;i--){const v=new Uint32Array(1);crypto.getRandomValues(v);const j=v[0]%(i+1);[a[i],a[j]]=[a[j],a[i]]}if(a[a.length-1]===previous)[a[0],a[a.length-1]]=[a[a.length-1],a[0]];return a}
window.nextPMVariant=(data)=>{if(!themeBag.length)themeBag=refill(lib.themes.length,lastTheme);if(!avatarBag.length)avatarBag=refill(24,lastAvatar);if(!layoutBag.length)layoutBag=refill(2,lastLayout);lastLayout=layoutBag.pop();lastTheme=themeBag.pop();lastAvatar=avatarBag.pop();return Object.freeze({theme_id:lib.themes[lastTheme].id,avatar_id:'pm_avatar_'+String(lastAvatar+1).padStart(2,'0'),character_side:'left',template_version:'pm-studio-handoff',density:'compact',contrast:'standard',softness:'standard',mascot_visible:true,decorations:'garden',icon_overrides:{},pathway_id:data?.journey_type==='chronological'?'stones':data?.strengths.some(s=>['analytics','operations','automation'].includes(s.icon))?'streams':data?.strengths.some(s=>['experimentation','ux','user_insight'].includes(s.icon))?'constellation':'glow',platform_overrides:data?platformChoices(data):{}})};
function resolveVariant(v){return {theme:lib.themes.find(t=>t.id===v?.theme_id)||lib.themes[0],avatar:/^pm_avatar_(0[1-9]|1[0-9]|2[0-4])$/.test(v?.avatar_id)?Number(v.avatar_id.slice(-2))-1:0}}
function tint(hex,white=.85){const rgb=hex.slice(1).match(/../g).map(v=>Math.round(parseInt(v,16)*(1-white)+255*white));return '#'+rgb.map(v=>v.toString(16).padStart(2,'0')).join('')}
function build(data,mobile=false,variant){
 if(data.status!=='ready'||!data.journey.length||data.journey.length>5||!data.strengths.length||data.strengths.length>4)throw Error('A PM map needs 1–5 supported roles and 1–4 capabilities.');
 const resolved=resolveVariant(variant),base=resolved.theme,theme={...base,background:[...base.background],accents:[...base.accents]},avatar=resolved.avatar,W=mobile?760:1600,n=data.journey.length,k=data.strengths.length;
 // Warm dimensional surfaces adapt to the accepted palette; positions never depend on copy.
 const peach=theme.id==='peach_coral'||theme.id==='warm_yellow',ink='#171333',secondary='#514565',accent=peach?'#f39d83':theme.primary;
 const hasDates=data.journey.some(j=>j.date_label),journeyY=mobile?220:205,unit=(W-160)/n,mobileRows=data.journey.map(()=>300),journeyH=mobile?80+n*300:400,bridgeY=mobile?journeyY+journeyH+15:620,capY=mobile?bridgeY+104:704,cardH=mobile?446:360,capH=mobile?40+k*(cardH+22):375,summaryY=capY+capH+30,H=mobile?summaryY+200:1200;
 const parts=[],issues=[],boxes=[],foreground=[],artBounds=[],overflowFields=[],prefix='pm-world-',platforms=Object.fromEntries(data.journey.map(j=>[j.id,'sculptural_bowl'])),characterSide='left',titleCenter=W/2,logoGap=20;
 const id=s=>prefix+s,url=s=>'url(#'+id(s)+')';
 const zone=(key,x,y,width,height,kind)=>{if(key)foreground.push({id:key,x,y,width,height,kind});return key?`data-foreground="${esc(key)}"`:''};
 function rect(x,y,w,h,r,fill,stroke='#ffffffdd',filter='shadow'){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2.5"${filter?` filter="${url(filter)}"`:''}/>`}
 function text(s,x,y,size=26,weight=500,color=ink){return `<text x="${x}" y="${y}" text-anchor="middle" dominant-baseline="middle" data-font="${fontFor(weight)}" font-family="${fonts[fontFor(weight)].family}" font-kerning="none" font-size="${size}" font-weight="600" fill="${color}">${esc(s)}</text>`}
 function fit(s,x,y,w,h,size=26,weight=500,maxLines=3,key='',color=ink){
  let f=size,rows=[];const min=key.includes(':date')?(mobile?23:18):mobile?23:key==='title'?48:key.includes(':method')?18:key==='signature'?19:22;
  for(;f>=min;f--){measure.font=`600 ${f}px ${fonts[fontFor(weight)].family}`;rows=[];let line='';for(const word of String(s).split(/\s+/)){const next=line?line+' '+word:word;if(line&&measure.measureText(next).width>w){rows.push(line);line=word}else line=next}if(line)rows.push(line);if(rows.length<=maxLines&&rows.length*f*1.18<=h&&rows.every(r=>measure.measureText(r).width<=w))break}
  if(f<min){issues.push('Text exceeds its reserved area: '+key);overflowFields.push(key);return ''}
  boxes.push({text:String(s),x:x-w/2,y:y-h/2,width:w,height:h,size:f,lines:rows.length,paintedHeight:rows.length*f*1.18});
  return `<g ${zone(key,x-w/2,y-h/2,w,h,'text')}>`+rows.map((row,i)=>text(row,x,y+(i-(rows.length-1)/2)*f*1.18,f,weight,color)).join('')+'</g>';
 }
 function crop(atlas,view,x,y,w,h,key=''){
  const scale=Math.min(w/view[2],h/view[3]),drawW=view[2]*scale,drawH=view[3]*scale;x+=(w-drawW)/2;y+=(h-drawH)/2;w=drawW;h=drawH;artBounds.push({key:key||atlas,x,y,width:w,height:h});
  return `<svg ${zone(key,x,y,w,h,'illustration')} data-art="${esc(key||atlas)}" x="${x}" y="${y}" width="${w}" height="${h}" viewBox="${view.join(' ')}" preserveAspectRatio="xMidYMid meet" overflow="hidden"><use href="#${id(atlas)}"/></svg>`;
 }
 function icon(name,x,y,size,key=''){let i=names.indexOf(aliases[name]||name);if(i<0)i=names.indexOf('strategy');return `<g data-icon="${names[i]}">`+crop('icons',[(i%6)*256,Math.floor(i/6)*256,256,256],x,y,size,size,key)+'</g>'}
 function decor(name,x,y,w,h){return crop('world',name==='cloud'?[520,1295,222,218]:[774,1286,243,243],x,y,w,h)}
 function spark(x,y,r=12){return `<path d="M${x} ${y-r}q0 ${r} ${r} ${r}q-${r} 0 -${r} ${r}q0 -${r} -${r} -${r}q${r} 0 ${r} -${r}Z" fill="#ffc65d" stroke="#fff" stroke-width="1.5"/>`}
 function pill(s,x,y,w,h=56){return rect(x,y,w,h,h/2,url('peach'),'#fff')+text(s,x+w/2,y+h/2+1,mobile?32:34,800)}
 const islandColors=['#f6b447','#64b9f3','#62cbb2','#b18dec','#f29fa8'];
 function platform(x,y,w,h,index,key){
  const c=islandColors[index%islandColors.length],top=id('bowlTop'+index),side=id('bowlSide'+index);
  artBounds.push({key,x,y,width:w,height:h});
  return `<g ${zone(key,x,y,w,h,'illustration')} data-platform="sculptural_bowl" transform="translate(${x} ${y}) scale(${w/240} ${h/135})"><defs><linearGradient id="${top}" x2=".8" y2="1"><stop stop-color="#fff"/><stop offset=".6" stop-color="${tint(c,.58)}"/><stop offset="1" stop-color="${c}"/></linearGradient><linearGradient id="${side}" x2=".1" y2="1"><stop stop-color="${tint(c,.5)}"/><stop offset=".6" stop-color="${c}"/><stop offset="1" stop-color="${tint(c,.15)}"/></linearGradient></defs><ellipse cx="120" cy="121" rx="91" ry="9" fill="${c}" opacity=".2"/><g filter="${url('platformShadow')}"><path d="M12 36C28 88 72 97 99 101Q120 106 141 101C168 97 212 88 228 36Z" fill="url(#${side})" stroke="#ffffffb0" stroke-width="2"/><path d="M35 52Q120 90 205 52" fill="none" stroke="#ffffff5c" stroke-width="2"/><ellipse cx="120" cy="36" rx="108" ry="28" fill="url(#${top})" stroke="#fff" stroke-width="3"/><path d="m38 33 29-26 25 26m-15 0 28-38 34 38m-12 0 25-27 28 27" fill="${tint(c,.65)}" stroke="#ffffffc0" stroke-width="1.5"/><ellipse cx="122" cy="43" rx="88" ry="12" fill="#ffffff35"/></g></g>`;
 }
 function role(j,i){
  const x=mobile?470:80+unit*(i+.5),row=journeyY+30+i*300,sideIcon=!mobile&&n>=4;
  const labelY=mobile?row+55:hasDates?318:330,iconSize=mobile?80:sideIcon?48:52,iconX=mobile?78:sideIcon?x-unit/2+20:x-iconSize/2,iconY=mobile?row+20:sideIcon?labelY-24:hasDates?230:240,labelX=sideIcon?x+26:x,labelW=mobile?410:sideIcon?unit-100:unit-30;
  let out='<g data-component="CareerJourneyIsland">'+icon(variant?.icon_overrides?.[j.id]||j.icon,iconX,iconY,iconSize,j.id+':icon');
  out+=fit(j.label,labelX,labelY,labelW,mobile?76:hasDates?58:60,mobile?35:n>=4?29:34,800,2,j.id+':label');
  const blocks=j.highlights?.length?j.highlights.map(h=>h.label):[j.description],width=mobile?410:unit-28,size=mobile?29:n===5?24:28;
  let top=mobile?row+95:hasDates?376:374;
  blocks.forEach((s,b)=>{measure.font=`600 ${size}px ${fonts.body.family}`;const height=mobile?64:measure.measureText(s).width<=width?36:54;out+=fit(s,x,top+height/2,width,height,size,500,2,j.id+':'+(j.highlights?.length?'highlight'+b:'description'),secondary);top+=height+(mobile?6:6)});
  if(j.date_label)out+=fit(j.date_label,x,mobile?row+260:359,mobile?400:unit-32,mobile?36:22,mobile?26:18,500,1,j.id+':date',secondary);
  const iw=mobile?165:Math.min(260,unit-38),ix=mobile?48:x-iw/2,iy=mobile?row+140:502,ih=mobile?125:100;
  out+=platform(ix,iy,iw,ih,i,j.id+':island');out+=icon(j.icon,ix+iw*.54,iy+ih*.04,mobile?42:48);
  return out+'</g>';
 }
 function shapedConnections(){
  const target={x:W/2,y:bridgeY+6},anchors=[];let out='<g data-component="JourneyToDNA" fill="none">';
  data.journey.forEach((j,i)=>{
   const x=mobile?130:80+unit*(i+.5),y=mobile?journeyY+30+i*300+255:581,tx=mobile?target.x:target.x+(i-(n-1)/2)*17;
   const d=mobile?`M${x} ${y}C25 ${y+40} 30 ${bridgeY-30} ${tx} ${target.y}`:`M${x} ${y}C${x} ${y+115} ${tx} ${bridgeY-125} ${tx} ${target.y}`;
   anchors.push({id:j.id,start:{x,y},end:{x:tx,y:target.y}});const c=islandColors[i%islandColors.length];
   out+=`<path d="${d}" stroke="${c}" stroke-width="26" opacity=".3" filter="${url('glow')}"/><path d="${d}" stroke="${c}" stroke-width="19" opacity=".8"/><path d="${d}" stroke="#fff9d8" stroke-width="3"/>`;
   if(!mobile)out+=`<circle cx="${x}" cy="${y+18}" r="5" fill="#fff"/><path d="M${tx-6} ${target.y-18}l6 10 6-10" stroke="#fff" stroke-width="3" stroke-linecap="round"/>`;
  });out+='</g>';return {svg:out,anchors};
 }
 function character(){if(mobile||variant?.mascot_visible===false)return '';const x=45,y=capY+10,w=265,h=350;artBounds.push({key:'human-chibi',x,y,width:w,height:h});return `<g data-component="CareerCharacter"><image ${zone('human-chibi',x,y,w,h,'illustration')} href="/assets/pm-explorer-full.png" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet"/></g>`}
 function capability(s,i){
  const mascot=!mobile&&variant?.mascot_visible!==false,gap=14,available=mobile?680:mascot?1215:1480,w=(available-gap*(mobile?0:k-1))/(mobile?1:k),x=mobile?40:(mascot?325:60)+i*(w+gap),y=mobile?capY+20+i*(cardH+22):capY+12;
  let out='<g data-component="CapabilityCard">'+rect(x,y,w,cardH,46,url('card'+i),'#fff','cardShadow');
  out+=icon(variant?.icon_overrides?.[s.id]||s.icon,x+w/2-28,y+10,56,s.id+':icon');
  out+=fit(s.label,x+w/2,y+103,w-30,60,mobile?35:k===4?30:33,800,2,s.id+':label');
  out+=fit(s.description,x+w/2,y+(mobile?219:190),w-36,mobile?110:100,mobile?31:k===4?25:29,500,4,s.id+':description',secondary);
  if(s.methods?.length){const my=y+(mobile?306:256),mh=mobile?124:92;out+=rect(x+16,my,w-32,mh,36,'#ffffffbc','#fff').replace('<rect ','<rect data-component="EvidenceCapsule" data-for="'+esc(s.id)+'" ');s.methods.forEach((m,z)=>{const count=s.methods.length,step=mobile?36:count===3?26:30,height=count===1?mh-20:mobile?32:count===3?24:28;out+=fit(m.label,x+w/2,my+mh/2+(z-(count-1)/2)*step,w-56,height,mobile?24:count===3?18:20,500,count===1?2:1,s.id+':method'+z)});}
  return out+'</g>';
 }
 const paths=shapedConnections();
 parts.push(`<svg xmlns="http://www.w3.org/2000/svg" data-world="pm-illustrated-3d" data-composition="approved-4-3" data-theme="${theme.id}" data-avatar="pm_avatar_${String(avatar+1).padStart(2,'0')}" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-labelledby="${id('title')} ${id('desc')}"><title id="${id('title')}">My PM Career DNA — ${esc(data.career_signature)}</title><desc id="${id('desc')}">${esc(data.superpower)}. One evidence-grounded PM journey and capability map.</desc><defs><image id="${id('world')}" href="${WORLD}" width="1024" height="1536"/><image id="${id('icons')}" href="${ICONS}" width="1536" height="1024"/><linearGradient id="${id('background')}" x2=".8" y2="1"><stop stop-color="${peach?'#ffd6c6':tint(theme.primary,.83)}"/><stop offset=".5" stop-color="#fff8ed"/><stop offset="1" stop-color="${peach?'#ffddce':tint(theme.accents[0],.8)}"/></linearGradient><linearGradient id="${id('panel')}" x2=".7" y2="1"><stop stop-color="#ffffffd9"/><stop offset="1" stop-color="#fff9f780"/></linearGradient><linearGradient id="${id('peach')}" x2=".2" y2="1"><stop stop-color="#ffe4b8"/><stop offset=".5" stop-color="#ffbca8"/><stop offset="1" stop-color="#f9a18c"/></linearGradient><linearGradient id="${id('swoosh')}" x2="1" y2=".5"><stop stop-color="#ffc356"/><stop offset=".5" stop-color="#ffb2c8"/><stop offset="1" stop-color="#c394ff"/></linearGradient><linearGradient id="${id('summary')}" x2="1" y2="1"><stop stop-color="#fff7ed"/><stop offset=".45" stop-color="#f9d5e1"/><stop offset="1" stop-color="#d8bdff"/></linearGradient><filter id="${id('shadow')}" x="-20%" y="-40%" width="140%" height="185%"><feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="${accent}" flood-opacity=".25"/></filter><filter id="${id('cardShadow')}" x="-15%" y="-15%" width="130%" height="135%"><feDropShadow dx="0" dy="8" stdDeviation="7" flood-color="${accent}" flood-opacity=".25"/></filter><filter id="${id('platformShadow')}" x="-20%" y="-30%" width="140%" height="165%"><feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="${accent}" flood-opacity=".23"/></filter><filter id="${id('glow')}" x="-40%" y="-100%" width="180%" height="300%"><feGaussianBlur stdDeviation="7"/></filter>`);
 ['#f8dad4','#d5eeec','#e2d9fa','#ffe9be'].forEach((c,i)=>parts.push(`<linearGradient id="${id('card'+i)}" x2=".8" y2="1"><stop stop-color="#fff9f8"/><stop offset="1" stop-color="${c}"/></linearGradient>`));
 parts.push('</defs>',rect(0,0,W,H,40,url('background'),'none',''));
 // Soft edge ribbons have no text and stay behind all interactive/dynamic content.
 parts.push(`<path d="M0 155Q180 65 390 130T${W} 75V0H0Z" fill="#ffffff35"/><path d="M0 ${H-60}Q320 ${H-145} 700 ${H-55}T${W} ${H-95}" fill="none" stroke="#ffffff66" stroke-width="25"/>`);
 parts.push(rect(mobile?28:60,30,mobile?W-56:W-120,mobile?150:128,64,url('panel'),'#fff'));
 const logoX=mobile?48:83,logoSize=mobile?48:86,logoY=mobile?44:48;parts.push(`<image ${zone('brand',logoX,logoY,logoSize,logoSize,'illustration')} href="${BRAND}" x="${logoX}" y="${logoY}" width="${logoSize}" height="${logoSize}"/>`);
 const brandX=mobile?190:268,brandY=mobile?66:94;parts.push('<g data-component="BrandWatermark" opacity=".68" '+zone('brand-label',brandX-88,brandY-14,176,28,'text')+'>'+text('PM Career Studio',brandX,brandY,18,500,'#8b7b99')+'</g>');
 parts.push(fit('My PM Career DNA',W/2,mobile?130:91,mobile?660:690,mobile?62:76,mobile?42:62,800,1,'title'),`<path d="M${mobile?210:560} ${mobile?166:137}Q${W/2} ${mobile?150:116} ${mobile?550:1040} ${mobile?166:137}" fill="none" stroke="${url('swoosh')}" stroke-width="9" stroke-linecap="round"/>`);
 parts.push(rect(28,journeyY,W-56,journeyH,58,url('panel'),'#fff'),paths.svg,pill('My PM Journey',mobile?46:76,journeyY-24,mobile?345:350));
 data.journey.forEach((j,i)=>parts.push(role(j,i)));
 if(!mobile&&variant?.decorations!=='none'){
  parts.push(decor('garden',35,journeyY+journeyH-105,100,95),decor('garden',W-135,journeyY+journeyH-105,100,95));
  // UI roadmap and the relevant capability icon are reusable semantic ornaments.
  parts.push(icon('roadmap',38,journeyY+245,48,'journey-decoration-left'),icon(data.strengths[k-1].icon,W-86,journeyY+245,48,'journey-decoration-right'));
 }
 parts.push(pill('Shaped My PM DNA',W/2-250,bridgeY,500,66),spark(W/2-272,bridgeY+33,13),spark(W/2+272,bridgeY+33,13));
 parts.push(rect(36,capY,W-72,capH,58,url('panel'),'#fff'),character());data.strengths.forEach((s,i)=>parts.push(capability(s,i)));
 const sy=summaryY,sh=mobile?155:72,sx=mobile?35:220,sw=mobile?W-70:W-440;
 parts.push('<g data-component="CareerDNASummary">',rect(sx,sy,sw,sh,sh/2,url('summary'),'#fff'),spark(sx+36,sy+sh/2),spark(sx+sw-36,sy+sh/2),fit(data.superpower,W/2,sy+sh/2,sw-120,mobile?126:58,mobile?31:29,800,mobile?4:2,'superpower'),'</g>');
 if(!mobile&&variant?.decorations!=='none')parts.push(icon(data.strengths[0].icon,65,summaryY-26,105),icon(data.strengths[k-1].icon,W-170,summaryY-26,105));
 parts.push('</svg>');
 const collisions=[];for(let i=0;i<foreground.length;i++)for(let j=i+1;j<foreground.length;j++){const a=foreground[i],b=foreground[j];if(Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>.5&&Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>.5)collisions.push([a.id,b.id])}
 if(collisions.length)issues.push('Foreground regions overlap.');const clipped=artBounds.filter(b=>b.x<12||b.y<12||b.x+b.width>W-12||b.y+b.height>H-12);if(clipped.length)issues.push('An illustration is outside safe canvas margins.');if(!fontsLoaded)issues.push('Rounded fonts are not ready.');
 return {svg:parts.join(''),metrics:{ok:!issues.length,issues,overflowFields,boxes,foreground,collisions,width:W,height:H,theme_id:theme.id,avatar_id:'pm_avatar_'+String(avatar+1).padStart(2,'0'),oneResult:true,platforms,pathway:variant?.pathway_id||'glow',pathAnchors:paths.anchors,hub:{x:W/2,y:bridgeY,width:500,height:66},summary:{y:summaryY,cardBottom:capY+capH},header:{title_center_x:W/2,logo_gap:logoGap,theme_in_header:false},artBounds,clipped,character_side:characterSide,fontsLoaded,headingFont:fonts.heading.family,bodyFont:fonts.body.family}};
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
