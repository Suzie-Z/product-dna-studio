/* One illustrated world. AI chooses evidence-grounded content; approved art stays fixed. */
(function(){
'use strict';
const ART='/assets/career-world-atlas.png',BRAND='/assets/career-dna-logo.png';
const palette=[['#35c9ba','#dcfaf3'],['#4b9bf2','#e2f1ff'],['#f6ad38','#fff0db'],['#a773e5','#eee0ff']];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const measure=document.createElement('canvas').getContext('2d');
const sprites={chart:[0,1],layers:[1,1],brain:[2,1],shield:[3,1],code:[0,2],users:[1,2],finance:[2,2],healthcare:[3,2],education:[0,3],hospitality:[1,3],operations:[2,3],compass:[3,3],globe:[2,4],spark:[3,4],cloud:[2,5],garden:[3,5]};
function CareerDNAResult(data,mobile=false){
 if(data.status!=='ready'||!data.journey.length||data.journey.length>4||!data.strengths.length||data.strengths.length>4)throw Error('A map needs 1–4 evidence-supported career categories and strengths.');
 const W=mobile?760:1600,n=data.journey.length,k=data.strengths.length;
 const journeyY=mobile?235:260,journeyH=mobile?n*255+65:365;
 const bridgeY=journeyY+journeyH+15,capY=bridgeY+80,capH=mobile?360+k*245:340,H=mobile?capY+capH+100:1180;
 const prefix='career-world-',issues=[],boxes=[],parts=[];
 const id=s=>prefix+s,url=s=>'url(#'+id(s)+')';
 function rect(x,y,w,h,r,fill,stroke='#ffffffe6',filter='shadow'){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="3"${filter?` filter="${url(filter)}"`:''}/>`}
 function text(s,x,y,size=26,weight=500,color='#171333'){return `<text x="${x}" y="${y}" text-anchor="middle" dominant-baseline="middle" font-size="${size}" font-weight="${weight}" fill="${color}">${esc(s)}</text>`}
 function fit(s,x,y,w,h,size=26,weight=500,maxLines=3){
  let rows=[],f=size;
  for(;f>=16;f--){measure.font=`${weight} ${f}px Arial`;rows=[];let row='';for(const word of String(s).split(/\s+/)){const next=row?row+' '+word:word;if(row&&measure.measureText(next).width>w){rows.push(row);row=word}else row=next}if(row)rows.push(row);if(rows.length<=maxLines&&rows.length*f*1.2<=h&&rows.every(r=>measure.measureText(r).width<=w))break}
  if(f<16){issues.push(String(s));return text('Regenerate for shorter wording',x,y,16,500,'#77578d')}
  boxes.push({text:String(s),width:w,height:h,size:f,lines:rows.length,paintedHeight:rows.length*f*1.2});
  return rows.map((row,i)=>text(row,x,y+(i-(rows.length-1)/2)*f*1.2,f,weight)).join('');
 }
 function crop(view,x,y,w,h,name){return `<svg data-art="${name}" x="${x}" y="${y}" width="${w}" height="${h}" viewBox="${view.join(' ')}" preserveAspectRatio="none" overflow="hidden"><use href="#${id('atlas')}"/></svg>`}
 function asset(name,x,y,w,h=w){const key=name==='trending-up'?'chart':name;const [col,row]=sprites[key]||sprites.spark;const view=key==='cloud'?[520,1295,222,218]:key==='garden'?[774,1286,243,243]:[col*256+8,row*256+8,240,240];return crop(view,x,y,w,h,key)}
 function pill(label,x,y,w,size=29){return rect(x,y,w,58,29,url('pill'),'#e2c7fc')+`<path d="M${x+28} ${y+7}H${x+w-28}" stroke="#ffffff65" stroke-width="3" stroke-linecap="round"/>`+text(label,x+w/2,y+31,size,750,'white')}
 function DecorativeBackground(){return rect(0,0,W,H,36,url('background'),'none','')+asset('cloud',-10,62,mobile?200:330,mobile?120:185)+asset('cloud',W-(mobile?188:320),37,mobile?210:355,mobile?125:210)+asset('cloud',W-260,journeyY+85,300,225)+`<g fill="#ffe072" stroke="#ffbc2e" stroke-width="7" stroke-linecap="round"><path d="m${W/2-430} 102-15-23m14 45-23-4m${W/2+428} 109 17-25m-10 46 23-5"/></g>`}
 function JourneyConnection(){
  const y=journeyY+270;
  const path=mobile?`M112 ${journeyY+100}C85 ${journeyY+290} 140 ${journeyY+400} 112 ${journeyY+journeyH-45}`:`M40 ${y+28}C240 ${y-39} 340 ${y+28} 465 ${y+15}S705 ${y-12} 830 ${y+24}S1100 ${y-30} 1250 ${y+16} 1450 ${y-30} 1560 ${y+5}`;
  return `<g data-component="JourneyConnection"><path d="${path}" fill="none" stroke="#ffd66e" stroke-width="17" opacity=".58" filter="${url('glow')}"/><path d="${path}" fill="none" stroke="#ffe390" stroke-width="9"/><path d="${path}" fill="none" stroke="#fffdf1" stroke-width="4"/></g>`;
 }
 function CareerJourneyIsland(j,i){
  const unit=(W-160)/n,x=mobile?440:80+unit*(i+.5),y=mobile?journeyY+90+i*255:journeyY+60;
  let out=`<g data-component="CareerJourneyIsland"><title>${esc(j.evidence_note)}</title>`;
  out+=asset(j.icon,mobile?65:x-47,mobile?y-32:y-52,mobile?94:94);
  out+=fit(j.label,x,mobile?y-3:y+63,mobile?440:unit-26,mobile?73:65,mobile?33:31,800,2);
  out+=fit(j.description,x,mobile?y+69:y+125,mobile?430:unit-30,66,mobile?29:25,500,2);
  if(j.date_label)out+=text(j.date_label,x,mobile?y+120:y+167,18,500,'#705889');
  const islandX=mobile?22:x-150,islandY=mobile?y+72:journeyY+222;
  out+=crop([i*256,32,256,211],islandX,islandY,mobile?180:300,mobile?125:188,'island-'+i);
  if(data.journey_type==='chronological'&&i<n-1){const xx=mobile?112:x+unit/2,yy=mobile?y+220:y+113;out+=`<path d="${mobile?`m${xx-9} ${yy-7} 9 9 9-9`:`m${xx-7} ${yy-10} 10 10-10 10`}" fill="none" stroke="#af78ed" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`}
  if(!mobile)out+=`<path d="M${x} ${journeyY+345}Q${x} ${bridgeY+34} ${W/2} ${bridgeY+34}" fill="none" stroke="#ffdfa0" stroke-width="8" opacity=".6" filter="${url('glow')}"/><path d="M${x} ${journeyY+345}Q${x} ${bridgeY+34} ${W/2} ${bridgeY+34}" fill="none" stroke="#fff8dc" stroke-width="3"/>`;
  return out+'</g>';
 }
 function CareerCharacter(){
  const x=mobile?15:8,y=mobile?capY-25:capY-27,w=mobile?340:360;
  let out=`<g data-component="CareerCharacter">${crop([0,1020,512,516],x,y,w,w,'human-chibi')}`;
  const domain=data.journey.find(j=>['code','brain','healthcare','education','finance','hospitality','operations'].includes(j.icon))?.icon||data.strengths[0].icon;
  // A symbolic work prop is selected from professional context, never appearance.
  out+=asset(domain,mobile?260:264,mobile?capY+231:capY+236,67);
  return out+'</g>';
 }
 function CapabilityCard(s,i){
  const gap=14,available=mobile?W-80:W-390,col=mobile?0:i,row=mobile?i:0,cols=mobile?1:k,w=(available-gap*(cols-1))/cols,h=mobile?225:304,x=(mobile?40:355)+col*(w+gap),y=mobile?capY+335+row*245:capY+18;
  const iconX=mobile?x+85:x+w/2,iconY=mobile?y+108:y+53;
  return `<g data-component="CapabilityCard"><title>${esc(s.evidence_note)}</title>${rect(x,y,w,h,45,url('card'+i),'#fff','cardShadow')}<rect x="${x+7}" y="${y+7}" width="${w-14}" height="${h-14}" rx="39" fill="none" stroke="#ffffff94" stroke-width="3"/>${asset(s.icon,iconX-(mobile?47:53),iconY-(mobile?47:53),mobile?94:106)}${fit(s.label,mobile?x+w/2+49:x+w/2,mobile?y+66:y+140,mobile?w-205:w-32,75,mobile?35:29,800,2)}${fit(s.description,mobile?x+w/2+49:x+w/2,mobile?y+153:y+235,mobile?w-205:w-34,91,mobile?30:24,500,3)}</g>`;
 }
 parts.push(`<svg xmlns="http://www.w3.org/2000/svg" data-world="illustrated-3d" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-labelledby="${id('title')} ${id('desc')}" style="font-family:Arial,sans-serif"><title id="${id('title')}">My Career DNA — ${esc(data.career_signature)}</title><desc id="${id('desc')}">${esc(data.superpower)}. ${data.journey_type==='chronological'?'Career progression':'Professional experience areas without an implied chronological sequence'}. One personalised illustrated map based on your experience.</desc><defs><image id="${id('atlas')}" width="1024" height="1536" href="${ART}"/>
 <linearGradient id="${id('background')}" x2="1" y2="1"><stop stop-color="#e8ddff"/><stop offset=".48" stop-color="#fff5fa"/><stop offset="1" stop-color="#dedbff"/></linearGradient>
 <linearGradient id="${id('panel')}" x2=".6" y2="1"><stop stop-color="#ffffff91"/><stop offset="1" stop-color="#c3a8f35c"/></linearGradient>
 <linearGradient id="${id('pill')}" x2="0" y2="1"><stop stop-color="#d6a2f2"/><stop offset=".45" stop-color="#b66fe2"/><stop offset="1" stop-color="#7d3fc1"/></linearGradient>
 <filter id="${id('shadow')}" x="-25%" y="-40%" width="150%" height="185%"><feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="#8050ab" flood-opacity=".24"/></filter>
 <filter id="${id('cardShadow')}" x="-25%" y="-20%" width="150%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#8965bc" flood-opacity=".26"/></filter>
 <filter id="${id('glow')}" x="-30%" y="-150%" width="160%" height="400%"><feGaussianBlur stdDeviation="7"/></filter>`);
 palette.forEach((p,i)=>parts.push(`<linearGradient id="${id('card'+i)}" x2=".6" y2="1"><stop stop-color="#ffffffe8"/><stop offset=".48" stop-color="${p[1]}"/><stop offset="1" stop-color="${p[1]}"/></linearGradient>`));
 parts.push('</defs>',DecorativeBackground(),rect(W/2-(mobile?280:405),62,mobile?560:810,134,36,'#fff9','#ffffffc9'),`<image href="${BRAND}" x="${W/2-(mobile?265:375)}" y="89" width="79" height="79"/>`,text('My Career DNA',W/2+38,128,mobile?45:58,800));
 parts.push(fit(data.career_signature,W/2,222,W-130,31,mobile?23:25,600,1));
 parts.push(rect(10,journeyY,W-20,journeyH,65,url('panel'),'#fff'),asset('cloud',W-(mobile?207:310),journeyY+105,mobile?200:340,mobile?150:245),JourneyConnection());
 data.journey.forEach((j,i)=>parts.push(CareerJourneyIsland(j,i)));
 parts.push(asset('garden',-15,journeyY+journeyH-(mobile?140:177),mobile?165:220,mobile?145:195),asset('garden',W-(mobile?142:196),journeyY+journeyH-(mobile?115:138),mobile?160:210,mobile?138:160));
 parts.push(pill('My Career Journey',36,journeyY-27,mobile?335:375,29));
 parts.push(rect(10,capY,W-20,capH,65,url('panel'),'#fff'),asset('cloud',W-210,capY+capH-125,220,146),asset('garden',-12,capY+capH-170,200,170),CareerCharacter());
 if(mobile)parts.push(fit(data.superpower,515,capY+126,355,160,29,500,4));
 data.strengths.forEach((s,i)=>parts.push(CapabilityCard(s,i)));
 parts.push(pill('Shape My Career DNA',W/2-(mobile?245:250),bridgeY,mobile?490:500,mobile?29:31));
 if(!mobile)parts.push(fit(data.superpower,W/2,1120,W-200,37,23,500,1));
 parts.push(text('Career DNA Studio',W/2,H-23,15,500,'#9072b0'),'</svg>');
 return {svg:parts.join(''),metrics:{ok:!issues.length,issues,boxes,width:W,height:H,illustrated:true,oneResult:true}};
}
window.buildDNAScene=CareerDNAResult;
let current=null;const mobileQuery=matchMedia('(max-width:700px)');
window.renderDNAMap=function(target,data){current={target,data};const scene=CareerDNAResult(data,mobileQuery.matches);target.innerHTML=scene.svg;target.dataset.layout=mobileQuery.matches?'mobile':'desktop';return scene.metrics};
mobileQuery.addEventListener('change',()=>{if(current)window.renderDNAMap(current.target,current.data)});
window.renderDNAPoster=async function(canvas,data){
 const scene=CareerDNAResult(data);await document.fonts.ready;
 const blob=new Blob([scene.svg],{type:'image/svg+xml;charset=utf-8'}),url=URL.createObjectURL(blob);
 try{const img=new Image();await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=()=>reject(Error('Illustration assets could not load.'));img.src=url});canvas.width=scene.metrics.width*2;canvas.height=scene.metrics.height*2;canvas.getContext('2d').drawImage(img,0,0,canvas.width,canvas.height);canvas.renderMetrics=scene.metrics;return scene.metrics}finally{URL.revokeObjectURL(url)}
};
})();
