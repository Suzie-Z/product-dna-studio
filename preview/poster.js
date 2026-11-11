/* One controlled SVG illustration system. AI supplies validated content, never markup. */
(function(){
'use strict';
const palette=[['#35c9ba','#ddfaf3','#189c9b'],['#4b9bf2','#e2f1ff','#367cc9'],['#f6ad38','#fff0d9','#de8a2e'],['#a773e5','#efe1ff','#8050bd']];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const measure=document.createElement('canvas').getContext('2d');
function build(data,mobile=false){
 if(data.status!=='ready'||!data.journey.length||data.journey.length>4||!data.strengths.length||data.strengths.length>4)throw Error('A map needs 1–4 evidence-supported stages and strengths.');
 const W=mobile?760:1600,n=data.journey.length,k=data.strengths.length;
 const journeyTop=mobile?220:215,journeyH=mobile?n*235+55:295;
 const bridgeY=journeyTop+journeyH+18,capTop=bridgeY+56,capH=mobile?290+k*245:330;
 const H=capTop+capH+90,prefix=mobile?'m':'d',issues=[],boxes=[];
 let parts=[];
 const id=s=>prefix+s,url=s=>'url(#'+id(s)+')';
 function rect(x,y,w,h,r,fill,stroke='#ffffffcc',filter='shadow'){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2"${filter?` filter="${url(filter)}"`:''}/>`}
 function ellipse(x,y,rx,ry,fill){return `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${fill}"/>`}
 function text(s,x,y,size=26,fill='#171333',weight=500){return `<text x="${x}" y="${y}" text-anchor="middle" dominant-baseline="middle" fill="${fill}" font-size="${size}" font-weight="${weight}">${esc(s)}</text>`}
 function fit(s,x,y,w,h,size=26,weight=500,maxLines=3){
  let rows=[],f=size;
  for(;f>=16;f--){
   measure.font=`${weight} ${f}px Arial`;rows=[];let row='';
   for(const word of String(s).split(/\s+/)){let next=row?row+' '+word:word;if(row&&measure.measureText(next).width>w){rows.push(row);row=word}else row=next}if(row)rows.push(row);
   if(rows.length<=maxLines&&rows.length*f*1.22<=h&&rows.every(r=>measure.measureText(r).width<=w))break;
  }
  if(f<16){issues.push(String(s));return text('Regenerate for shorter wording',x,y,16,'#735b86')}
  boxes.push({text:String(s),width:w,height:h,size:f,lines:rows.length,paintedHeight:rows.length*f*1.22});
  return rows.map((r,i)=>text(r,x,y+(i-(rows.length-1)/2)*f*1.22,f,'#211735',weight)).join('');
 }
 function icon(kind,x,y,size,p){
  kind=({'trending-up':'chart',users:'people',brain:'ai'})[kind]||kind;
  const shapes={chart:'<rect x="-29" y="6" width="14" height="24" rx="4"/><rect x="-7" y="-9" width="14" height="39" rx="4"/><rect x="15" y="-29" width="14" height="59" rx="4"/>',layers:'<path d="M0-29 34-12 0 5-34-12Z"/><path d="m-32 3 32 17 32-17M-32 18 0 35 32 18" fill="none"/>',shield:'<path d="m0-33 29 10-4 33Q21 27 0 36-21 27-25 10l-4-33Z"/><path d="m-13 0 9 10 20-23" stroke="white" fill="none"/>',code:'<path d="m-13-22-21 22 21 22m26-44 21 22-21 22M8-31-8 31" fill="none"/>',people:'<circle cx="-17" cy="-15" r="12"/><circle cx="17" cy="-15" r="12"/><rect x="-33" y="5" width="29" height="29" rx="12"/><rect x="4" y="5" width="29" height="29" rx="12"/>',compass:'<circle r="33"/><path d="m14-19-6 27-22 11 6-27Z" fill="white" stroke="white"/>',globe:'<circle r="32" fill="none"/><ellipse rx="14" ry="32" fill="none"/><path d="M-31 0h62M-24-19h48M-24 19h48" fill="none"/>',healthcare:'<rect x="-30" y="-30" width="60" height="60" rx="15"/><path d="M-17 0h34M0-17v34" fill="none" stroke="white"/>',hospitality:'<path d="M-31 8a31 31 0 0 1 62 0M-36 10h72M-23 28h46M0-24v-7" fill="none"/>',education:'<path d="M0-24q-20-13-34-1v52q20-10 34 1 14-11 34-1v-52Q20-37 0-24Zm0 0v52" fill="none"/>',finance:'<ellipse cy="19" rx="30" ry="13"/><ellipse cy="3" rx="30" ry="13"/><ellipse cy="-13" rx="30" ry="13"/>',operations:'<rect x="-32" y="-29" width="27" height="24" rx="6"/><rect x="5" y="5" width="27" height="24" rx="6"/><path d="M-18-3v21H0M18 3v-21H0" fill="none"/>',spark:'<path d="M0-34Q5-6 32 0 5 6 0 34-5 6-32 0-5-6 0-34Z"/>',ai:'<rect x="-27" y="-27" width="54" height="54" rx="10"/><path d="M-16-38v10M0-38v10M16-38v10M-16 28v10M0 28v10M16 28v10M-38-16h10M-38 0h10M-38 16h10M28-16h10M28 0h10M28 16h10" fill="none"/><path d="M-13 13-4-12 5 13M-10 4H2M15-12v25" fill="none" stroke="white" stroke-width="4"/>'};
  return `<g transform="translate(${x} ${y}) scale(${size/80})" fill="${p[0]}" stroke="${p[2]}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" filter="${url('iconShadow')}">${shapes[kind]||shapes.spark}</g>`;
 }
 function cloud(x,y,scale){return `<path transform="translate(${x} ${y}) scale(${scale})" d="M-100 25Q-120-15-75-18-66-70-15-48 20-90 58-35 96-53 111-13 145-9 135 25Z" fill="${url('cloud')}"/>`}
 function spark(x,y,s){return `<path transform="translate(${x} ${y}) scale(${s})" d="M0-16Q3-3 16 0 3 3 0 16-3 3-16 0-3-3 0-16Z" fill="#fff7ca" stroke="#f6d789"/>`}
 function foliage(x,y,s,flip=1){return `<g transform="translate(${x} ${y}) scale(${s*flip} ${s})"><path d="M0 0Q-20-25-19-60M0 0Q20-40 35-65M0 0Q-10-38 5-85" stroke="#90be91" stroke-width="7" fill="none"/><ellipse cx="-26" cy="-43" rx="13" ry="25" fill="#b2d68b" transform="rotate(-35 -26 -43)"/><ellipse cx="23" cy="-38" rx="14" ry="27" fill="#78c2a1" transform="rotate(30 23 -38)"/><ellipse cx="4" cy="-64" rx="12" ry="22" fill="#c3dc96"/><circle cx="-3" cy="-32" r="7" fill="#fff7db"/><circle cx="-3" cy="-32" r="3" fill="#efc76a"/></g>`}
 function island(x,y,rx,p,i){return `<g filter="${url('shadow')}"><path d="M${x-rx} ${y}Q${x-rx-5} ${y+32} ${x-rx*.66} ${y+40}L${x-rx*.36} ${y+34} ${x-rx*.1} ${y+46} ${x+rx*.18} ${y+38} ${x+rx*.48} ${y+44}Q${x+rx} ${y+36} ${x+rx} ${y}Z" fill="${url('rock'+i)}" stroke="${p[2]}" stroke-width="1.5"/>${ellipse(x,y,rx,18,url('top'+i))}<ellipse cx="${x}" cy="${y-1}" rx="${rx-7}" ry="13" fill="none" stroke="#ffffffcc" stroke-width="2"/><path d="m${x-rx*.5} ${y+18} 5 18m${rx*.4} -18-3 25m${rx*.45} -23-6 18" stroke="${p[2]}" opacity=".35" stroke-width="3"/></g>`}
 function character(x,y,scale,domain){
  // Abstract toy explorer: fixed non-human face, no inferred identity or appearance.
  const prop=['code','brain','layers'].includes(domain)?'code':['chart','finance'].includes(domain)?'chart':['healthcare','shield'].includes(domain)?'shield':domain==='education'?'education':domain==='hospitality'?'hospitality':'operations';
  return `<g transform="translate(${x} ${y}) scale(${scale})">${ellipse(0,185,110,17,'#8c71b52a')}${rect(-83,13,51,114,20,url('toyPurple'),'#ecddff', 'shadow')}<path d="M-42 114-69 164M32 119 64 163" stroke="#b79bd9" stroke-width="30" stroke-linecap="round"/>${rect(-92,155,59,24,11,url('toyPurple'),'#fff','')}${rect(39,155,59,24,11,url('toyPurple'),'#fff','')}${rect(-57,0,114,129,34,url('toy'),'#fff','shadow')}<path d="m-49 28-33 59 44 23M49 28l33 59-44 23" fill="none" stroke="#ddd0ef" stroke-width="25" stroke-linecap="round"/><path d="m-49 28-33 59 44 23M49 28l33 59-44 23" fill="none" stroke="#f4edfc" stroke-width="17" stroke-linecap="round"/>${rect(-79,-119,158,128,48,url('toy'),'#fff','shadow')}${rect(-61,-96,122,78,30,url('face'),'#d6f8f2','')}<ellipse cx="-23" cy="-60" rx="8" ry="10" fill="#b6fff2"/><ellipse cx="23" cy="-60" rx="8" ry="10" fill="#b6fff2"/><path d="M-11-37q11 9 22 0" fill="none" stroke="#b6fff2" stroke-width="4" stroke-linecap="round"/><path d="M-46-86h68" stroke="#ffffff66" stroke-width="6" stroke-linecap="round"/><path d="M0-119v-22" stroke="#b898db" stroke-width="6"/><circle cy="-148" r="11" fill="#71d9c5" stroke="#fff" stroke-width="3"/><g transform="translate(-4 68) rotate(-5)">${rect(-68,-19,136,85,10,url('laptop'),'#cfc0ef','')}<path d="M-81 67H78l-13 10H-65Z" fill="#a08bbd"/>${icon(prop,0,22,35,palette[0])}</g></g>`;
 }
 parts.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-labelledby="${id('title')} ${id('desc')}" style="font-family:Arial,sans-serif"><title id="${id('title')}">My Career DNA — ${esc(data.career_signature)}</title><desc id="${id('desc')}">${esc(data.superpower)}. ${data.journey_type==='chronological'?'Career progression':'Experience areas, without an implied sequence'}. All text is based on the experience provided.</desc><defs>
 <linearGradient id="${id('bg')}" x2="1" y2="1"><stop stop-color="#e8dffc"/><stop offset=".47" stop-color="#fff5f8"/><stop offset="1" stop-color="#e7e4fc"/></linearGradient>
 <linearGradient id="${id('panel')}" x2="0" y2="1"><stop stop-color="#ffffffb5"/><stop offset="1" stop-color="#dfd3f28c"/></linearGradient>
 <linearGradient id="${id('pill')}" x2="0" y2="1"><stop stop-color="#c598ef"/><stop offset=".5" stop-color="#a06bd6"/><stop offset="1" stop-color="#8353bf"/></linearGradient>
 <linearGradient id="${id('cloud')}" x2="0" y2="1"><stop stop-color="#fff9"/><stop offset="1" stop-color="#cbb7f0aa"/></linearGradient>
 <linearGradient id="${id('toy')}" x2=".7" y2="1"><stop stop-color="#fff"/><stop offset=".5" stop-color="#f5efff"/><stop offset="1" stop-color="#baa0de"/></linearGradient>
 <linearGradient id="${id('toyPurple')}" x2="1" y2="1"><stop stop-color="#d8c6ef"/><stop offset="1" stop-color="#9474b8"/></linearGradient>
 <linearGradient id="${id('face')}" x2="0" y2="1"><stop stop-color="#6f9caa"/><stop offset="1" stop-color="#29394e"/></linearGradient>
 <linearGradient id="${id('laptop')}" x2="1" y2="1"><stop stop-color="#ece4f9"/><stop offset="1" stop-color="#b3a1cf"/></linearGradient>
 <filter id="${id('shadow')}" x="-25%" y="-40%" width="150%" height="190%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#8056a1" flood-opacity=".22"/></filter>
 <filter id="${id('iconShadow')}" x="-40%" y="-40%" width="180%" height="190%"><feDropShadow dx="0" dy="5" stdDeviation="3" flood-color="#72549e" flood-opacity=".22"/></filter>`);
 palette.forEach((p,i)=>parts.push(`<linearGradient id="${id('rock'+i)}" x2="0" y2="1"><stop stop-color="${p[0]}"/><stop offset="1" stop-color="${p[2]}"/></linearGradient><linearGradient id="${id('top'+i)}" x2="0" y2="1"><stop stop-color="#fff"/><stop offset=".5" stop-color="${p[1]}"/><stop offset="1" stop-color="${p[0]}"/></linearGradient><linearGradient id="${id('card'+i)}" x2=".8" y2="1"><stop stop-color="#fffffff0"/><stop offset="1" stop-color="${p[1]}"/></linearGradient>`));
 parts.push(`</defs>`,rect(0,0,W,H,32,url('bg'),'none',''),cloud(90,127,.7),cloud(W-85,125,.9),spark(W/2-310,78,.8),spark(W/2+310,81,.8),rect(W/2-(mobile?270:370),37,mobile?540:740,104,32,'#ffffffa8','#fff'),text('My Career DNA',W/2,88,mobile?45:56,'#171333',800),fit(data.career_signature,W/2,169,W-120,40,mobile?25:27,600,1));
 parts.push(rect(22,journeyTop,W-44,journeyH,43,url('panel'),'#fff'),rect(43,journeyTop-25,mobile?310:330,50,25,url('pill'),'#dfc8f3'),text('My Career Journey',mobile?198:208,journeyTop+1,26,'white',700));
 if(mobile){
  parts.push(`<path d="M109 ${journeyTop+65}V${journeyTop+journeyH-40}" stroke="#fff5c3" stroke-width="9" fill="none"/>`);
 }else parts.push(`<path d="M65 ${journeyTop+235}C380 ${journeyTop+192} 480 ${journeyTop+274} 760 ${journeyTop+233}S1280 ${journeyTop+218} 1535 ${journeyTop+232}" fill="none" stroke="#fff1af" stroke-width="8"/><path d="M65 ${journeyTop+235}C380 ${journeyTop+192} 480 ${journeyTop+274} 760 ${journeyTop+233}S1280 ${journeyTop+218} 1535 ${journeyTop+232}" fill="none" stroke="#fff" stroke-width="3"/>`);
 data.journey.forEach((j,i)=>{
  const p=palette[i],unit=(W-140)/n,x=mobile?410:70+unit*(i+.5),y=mobile?journeyTop+95+i*235:journeyTop+70;
  parts.push(`<g><title>${esc(j.evidence_note)}</title>`,icon(j.icon,mobile?110:x,y,mobile?65:63,p),fit(j.label,x,mobile?y-5:y+63,mobile?410:unit-26,65,mobile?31:29,750,2),fit(j.description,x,mobile?y+63:y+122,mobile?410:unit-30,62,mobile?27:23,500,2));
  if(j.date_label)parts.push(text(j.date_label,x,mobile?y+112:y+170,18,'#765e8d'));
  parts.push(island(mobile?110:x,mobile?y+85:journeyTop+235,mobile?62:Math.min(unit*.34,126),p,i),'</g>');
  if(data.journey_type==='chronological'&&i<n-1)parts.push(mobile?`<path d="m99 ${y+153} 11 11 11-11" fill="none" stroke="#b087df" stroke-width="5" stroke-linecap="round"/>`:`<path d="m${x+unit/2-9} ${y+76} 10 11-10 11" fill="none" stroke="#b087df" stroke-width="5" stroke-linecap="round"/>`);
 });
 parts.push(foliage(49,journeyTop+journeyH-10,.7),foliage(W-49,journeyTop+journeyH-10,.7,-1));
 parts.push(`<path d="M${W/2} ${bridgeY-16}v44" stroke="#fff" stroke-width="6"/>`,rect(W/2-235,bridgeY,470,53,27,url('pill'),'#e8d6fc'),text('Shape My Career DNA',W/2,bridgeY+28,29,'white',700),rect(22,capTop,W-44,capH,45,url('panel'),'#fff'));
 const charX=mobile?163:165,charY=mobile?capTop+124:capTop+163;
 parts.push(character(charX,charY,mobile?.78:.85,data.strengths[0].icon));
 if(mobile){parts.push(fit(data.superpower,480,capTop+128,370,145,27,500,4))}else parts.push(fit(data.superpower,W/2,H-61,W-160,38,23,500,1));
 data.strengths.forEach((s,i)=>{
  const p=palette[i],gap=14,available=mobile?W-90:W-343-47,col=mobile?0:i,row=mobile?i:0,cols=mobile?1:k,w=(available-gap*(cols-1))/cols,h=mobile?224:278;
  const x=(mobile?45:343)+col*(w+gap),y=mobile?capTop+281+row*245:capTop+27;
  parts.push(`<g><title>${esc(s.evidence_note)}</title>`,rect(x,y,w,h,32,url('card'+i),'#fff'),icon(s.icon,mobile?x+80:x+w/2,mobile?y+110:y+58,mobile?76:66,p),fit(s.label,mobile?x+w/2+40:x+w/2,mobile?y+65:y+126,mobile?w-205:w-30,65,mobile?36:27,750,2),fit(s.description,mobile?x+w/2+40:x+w/2,mobile?y+151:y+211,mobile?w-205:w-30,86,mobile?31:23,500,3),'</g>');
 });
 parts.push(spark(W-50,capTop+20,.6),text('Career DNA Studio',W/2,H-28,16,'#8f78aa',500),'</svg>');
 return {svg:parts.join(''),metrics:{ok:!issues.length,issues,boxes,width:W,height:H}};
}
window.buildDNAScene=build;
window.renderDNAMap=function(target,data){
 const desktop=build(data),mobile=build(data,true);
 target.innerHTML=`<div class="map-desktop">${desktop.svg}</div><div class="map-mobile">${mobile.svg}</div>`;
 return desktop.metrics;
};
window.renderDNAPoster=async function(canvas,data){
 const scene=build(data);await document.fonts.ready;
 const blob=new Blob([scene.svg],{type:'image/svg+xml;charset=utf-8'}),url=URL.createObjectURL(blob);
 try{
  const img=new Image();await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=()=>reject(Error('Image rendering failed.'));img.src=url});
  canvas.width=scene.metrics.width*2;canvas.height=scene.metrics.height*2;
  canvas.getContext('2d').drawImage(img,0,0,canvas.width,canvas.height);canvas.renderMetrics=scene.metrics;return scene.metrics;
 }finally{URL.revokeObjectURL(url)}
};
})();
