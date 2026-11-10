/* Controlled vector scene; only validated English display fields reach the canvas. */
window.renderDNAPoster=function(canvas,data,format='portrait'){
 if(data.status!=='ready'||!data.journey.length||data.journey.length>5||!data.strengths.length||data.strengths.length>5)throw Error('A ready map needs 1–5 journey stages and strengths.');
 const W=format==='square'?1400:1200,H=format==='square'?1400:1500,scale=2;
 canvas.width=W*scale;canvas.height=H*scale;const c=canvas.getContext('2d');c.scale(scale,scale);
 const issues=[],metrics=[];
const palette=[{main:'#42cbb7',light:'#dcfaf3',deep:'#139e99'},{main:'#60b3f6',light:'#e1f1ff',deep:'#4189da'},{main:'#f6b761',light:'#fff0d8',deep:'#e99542'},{main:'#ae7aed',light:'#f0e1ff',deep:'#8c54d5'}];
function grad(x,y,x2,y2,stops){let g=c.createLinearGradient(x,y,x2,y2);stops.forEach(([p,col])=>g.addColorStop(p,col));return g}
function round(x,y,w,h,r,fill,stroke,shadow=0){c.save();if(shadow){c.shadowColor='#7754a333';c.shadowBlur=shadow;c.shadowOffsetY=8}c.beginPath();c.roundRect(x,y,w,h,r);c.fillStyle=fill;c.fill();if(stroke){c.lineWidth=3;c.strokeStyle=stroke;c.stroke()}c.restore()}
function line(x,y,x2,y2,color,width=3){c.beginPath();c.moveTo(x,y);c.lineTo(x2,y2);c.strokeStyle=color;c.lineWidth=width;c.lineCap='round';c.stroke()}
function circle(x,y,r,color){c.beginPath();c.arc(x,y,r,0,Math.PI*2);c.fillStyle=color;c.fill()}
function label(text,x,y,size=30,color='#291a43',weight=600,align='center'){c.fillStyle=color;c.font=weight+' '+size+'px "DM Sans", system-ui, sans-serif';c.textAlign=align;c.textBaseline='middle';c.fillText(String(text),x,y)}
function lines(text,maxWidth,size,weight){c.font=weight+' '+size+'px "DM Sans", system-ui, sans-serif';let words=String(text).split(/\s+/),out=[],row='';for(let word of words){while(c.measureText(word).width>maxWidth){let n=1;while(n<word.length&&c.measureText(word.slice(0,n+1)).width<=maxWidth)n++;if(row){out.push(row);row=''}out.push(word.slice(0,n));word=word.slice(n)}const next=row?row+' '+word:word;if(c.measureText(next).width>maxWidth&&row){out.push(row);row=word}else row=next}if(row)out.push(row);return out}
function fitted(text,x,y,w,h,maxSize=28,weight=600,color='#302040',maxLines=3){
 let size=maxSize,rows=[];for(;size>=15;size--){rows=lines(text,w,size,weight);if(rows.length<=maxLines&&rows.length*size*1.25<=h)break}
 if(size<15){issues.push(String(text));label('Shorten this text in the editor',x,y,14,'#826592',500);return false}
 const lineH=size*1.25,total=rows.length*lineH;
 metrics.push({text:String(text),x,y,width:w,height:h,size,lines:rows.length,paintedHeight:total});
 rows.forEach((row,i)=>label(row,x,y-total/2+lineH*(i+.5),size,color,weight));return true;
}
function cloud(x,y,scale,color){c.save();c.translate(x,y);c.scale(scale,scale);c.beginPath();c.moveTo(-100,30);c.bezierCurveTo(-130,-10,-75,-25,-58,-10);c.bezierCurveTo(-65,-65,10,-75,35,-30);c.bezierCurveTo(70,-60,120,-25,103,5);c.bezierCurveTo(140,-5,150,25,130,35);c.closePath();c.fillStyle=color;c.fill();c.restore()}
function spark(x,y,r,col){c.save();c.translate(x,y);c.beginPath();c.moveTo(0,-r);c.quadraticCurveTo(r*.2,-r*.15,r,0);c.quadraticCurveTo(r*.2,r*.15,0,r);c.quadraticCurveTo(-r*.2,r*.15,-r,0);c.quadraticCurveTo(-r*.2,-r*.15,0,-r);c.fillStyle=col;c.fill();c.restore()}
function icon(kind,x,y,s,color){kind=({'trending-up':'chart',users:'people',brain:'ai'})[kind]||kind;c.save();c.translate(x,y);c.scale(s/80,s/80);c.strokeStyle=color;c.fillStyle=color;c.lineWidth=6;c.lineCap='round';c.lineJoin='round';if(kind==='chart'){round(-30,8,13,25,4,color);round(-7,-7,13,40,4,color);round(16,-30,13,63,4,color)}else if(kind==='layers'){for(let k=2;k>=0;k--){let yy=k*15-15;c.beginPath();c.moveTo(0,yy-22);c.lineTo(34,yy-7);c.lineTo(0,yy+10);c.lineTo(-34,yy-7);c.closePath();c.fillStyle=k===2?color:k===1?'#ffffff':color;c.fill();c.stroke()}}else if(kind==='shield'){c.beginPath();c.moveTo(0,-35);c.lineTo(30,-23);c.lineTo(25,10);c.quadraticCurveTo(22,25,0,38);c.quadraticCurveTo(-22,25,-25,10);c.lineTo(-30,-23);c.closePath();c.fill();c.strokeStyle='white';line(-12,0,-2,11,'white',6);line(-2,11,16,-12,'white',6)}else if(kind==='code'){line(-14,-18,-31,0,color,6);line(-31,0,-14,18,color,6);line(14,-18,31,0,color,6);line(31,0,14,18,color,6);line(7,-28,-7,28,color,5)}else if(kind==='people'){circle(-16,-14,12,color);circle(16,-14,12,color);round(-34,6,29,28,12,color);round(5,6,29,28,12,color)}else if(kind==='compass'){circle(0,0,34,color);c.fillStyle='white';c.beginPath();c.moveTo(15,-18);c.lineTo(6,9);c.lineTo(-15,18);c.lineTo(-6,-9);c.closePath();c.fill()}else if(kind==='globe'){circle(0,0,33,color);c.strokeStyle='white';c.lineWidth=3;c.beginPath();c.ellipse(0,0,14,31,0,0,Math.PI*2);c.stroke();line(-30,0,30,0,'white',3);line(-23,-18,23,-18,'white',3);line(-23,18,23,18,'white',3)}else if(kind==='healthcare'){round(-28,-28,56,56,15,color);line(-17,0,17,0,'white',10);line(0,-17,0,17,'white',10)}else if(kind==='hospitality'){c.beginPath();c.arc(0,5,30,Math.PI,0);c.stroke();line(-36,8,36,8,color,5);line(-22,24,22,24,color,5);circle(0,-30,4,color)}else if(kind==='education'){c.beginPath();c.moveTo(0,-23);c.quadraticCurveTo(-18,-34,-34,-22);c.lineTo(-34,25);c.quadraticCurveTo(-16,14,0,27);c.quadraticCurveTo(16,14,34,25);c.lineTo(34,-22);c.quadraticCurveTo(18,-34,0,-23);c.closePath();c.stroke();line(0,-22,0,27,color,3)}else if(kind==='finance'){for(let i=2;i>=0;i--){c.beginPath();c.ellipse(0,i*13-8,29,13,0,0,Math.PI*2);c.fillStyle=i===0?color:'#fff';c.fill();c.stroke()}}else if(kind==='operations'){round(-32,-29,27,24,6,color);round(5,5,27,24,6,color);line(-18,-4,-18,17,color,5);line(-18,17,0,17,color,5);line(18,4,18,-17,color,5);line(18,-17,0,-17,color,5)}else if(kind==='spark'){spark(0,0,31,color)}else{round(-27,-27,54,54,12,color);for(let i=-18;i<=18;i+=18){line(i,-38,i,-29,color,5);line(i,29,i,38,color,5);line(-38,i,-29,i,color,5);line(29,i,38,i,color,5)}if(kind==='spark'){spark(0,0,18,'white')}else spark(0,0,16,'white')}c.restore()}
function bot(x,y,s,color,walking=true){c.save();c.translate(x,y);c.scale(s,s);c.save();c.scale(1,.25);circle(0,390,85,'#9480bd26');c.restore();round(-69,-26,35,90,13,'#b392df','#e7dcff',6);c.save();c.translate(-24,66);c.rotate(walking?.28:0);round(-16,0,30,55,11,'#cbb7e9','#f3eaff');round(-23,43,48,21,9,'#7e63a8','#d9c9ef');c.restore();c.save();c.translate(25,68);c.rotate(walking?-.33:0);round(-15,0,30,58,11,'#ded1f0','#fff');round(-17,45,48,21,9,'#8d70b9','#dfd0f2');c.restore();round(-52,-16,104,98,27,grad(-50,0,50,75,[[0,'#ffffff'],[.5,'#eee7fc'],[1,'#b9a0dc']]),'#fff',12);round(-34,0,68,42,17,color,'#ffffff');spark(0,21,12,'#fff');c.save();c.translate(-46,10);c.rotate(.45);round(-20,0,23,67,12,'#e7d8f6','#fff');c.restore();c.save();c.translate(49,9);c.rotate(walking?-.9:-.3);round(0,0,22,62,11,'#e7d8f6','#fff');c.restore();round(-67,-112,134,108,40,grad(-60,-110,65,-5,[[0,'#fff'],[.5,'#e9ddf9'],[1,'#b69ad8']]),'#fff',14);round(-51,-91,102,63,24,grad(-50,-90,50,-20,[[0,'#87b9bf'],[.5,'#42556e'],[1,'#283952']]),'#d7f7ef');circle(-17,-60,7,'#b7fff2');circle(17,-60,7,'#b7fff2');line(-9,-42,9,-42,'#a3dcd9',3);c.save();c.globalAlpha=.35;round(-43,-84,80,9,5,'#fff');c.restore();line(0,-115,0,-135,'#b295d2',5);circle(0,-138,9,color);c.restore()}

const bg=grad(0,0,W,H,[[0,'#e9e0fc'],[.45,'#fbf5fb'],[1,'#e7e6fc']]);c.fillStyle=bg;c.fillRect(0,0,W,H);
cloud(90,150,.9,'#d4c2f550');cloud(W-90,145,1.1,'#d9c9f555');
round(W/2-375,42,750,108,36,'#fff9','#ffffffb0',16);label('My Career DNA',W/2,98,49,'#29183f',800);
round(38,214,W-76,322,46,grad(0,214,W,536,[[0,'#ffffffb9'],[1,'#e8dff8a9']]),'#ffffff',15);
const journeyLabel=data.journey_type==='chronological'?'Career Journey':'Experience Areas';
round(64,190,285,51,24,grad(64,190,340,240,[[0,'#ba93e2'],[1,'#9a6bc7']]),'#f2e5ff',7);label(journeyLabel,206,216,24,'#fff',700);
const n=data.journey.length,unit=(W-180)/n;
const trail=grad(70,0,W-60,0,[[0,'#f2cb88'],[.8,'#e5c4a8'],[1,'#ffffff00']]);
c.beginPath();c.moveTo(70,493);c.bezierCurveTo(W*.35,455,W*.6,530,W-65,487);c.lineWidth=6;c.strokeStyle=trail;c.stroke();
data.journey.forEach((j,i)=>{const x=90+unit*(i+.5),p=palette[i%palette.length];icon(j.icon,x,293,48,p.main);fitted(j.label,x,350,unit-23,62,24,750,'#38234c',2);fitted(j.description,x,419,unit-22,67,19,500,'#685174',3);if(j.date_label)fitted(j.date_label,x,463,unit-25,24,15,500,'#8a709d',1);c.beginPath();c.ellipse(x,495,Math.min(unit*.34,100),14,0,0,Math.PI*2);c.fillStyle=grad(x,481,x,510,[[0,'#fff'],[.5,p.light],[1,p.main]]);c.fill();c.strokeStyle='#fff';c.lineWidth=2;c.stroke();});
for(let i=0;i<3;i++){c.save();c.globalAlpha=.65-i*.18;circle(W-64+i*11,486-i*3,3.5,'#ae91ce');c.restore()}
for(let i=0;i<n;i++){const x=90+unit*(i+.5);c.beginPath();c.moveTo(x,525);c.bezierCurveTo(x,566,W/2,563,W/2,590);c.strokeStyle=palette[i%palette.length].main+'77';c.lineWidth=3;c.stroke()}
round(W/2-133,554,266,39,18,'#fbf7fff0','#ffffff');label('Shaped by your journey',W/2,574,18,'#9e80b7',500);
// One abstract, gender-neutral explorer, with no inferred appearance.
round(38,609,W-76,220,42,'#ffffffb3','#ffffff',14);bot(142,720,.59,'#a5d7c9',true);
const signatureX=W/2+65,signatureW=W-365;
label('MY CAREER SIGNATURE',signatureX,646,13,'#9678b0',700);
fitted(data.career_signature,signatureX,699,signatureW,74,35,750,'#402450',2);
fitted(data.superpower,signatureX,774,signatureW,58,23,500,'#7b608b',2);
const count=data.strengths.length,top=H===1500?900:855,available=H-top-62,gap=20,margin=65,totalW=W-margin*2;
let rows=count>=4?2:1,cols=count===1?1:count===2||count===4?2:3;
let cardH=Math.min(rows===1?310:260,(available-gap*(rows-1))/rows),cardW=(totalW-gap*(cols-1))/cols;
if(count===1)cardW=Math.min(850,totalW);
const allH=rows*cardH+(rows-1)*gap,offsetY=top+(available-allH)/2;
const cards=data.strengths.map((strength,i)=>{
 const row=Math.floor(i/cols),itemsInRow=Math.min(cols,count-row*cols),rowW=itemsInRow*cardW+(itemsInRow-1)*gap;
 const x=(W-rowW)/2+(i%cols)*(cardW+gap),y=offsetY+row*(cardH+gap),p=palette[i%palette.length];
 return {strength,i,x,y,p};
});
for(const {x,y,p}of cards){ c.beginPath();c.moveTo(W/2,829);c.bezierCurveTo(W/2,y-25,x+cardW/2,y-25,x+cardW/2,y);c.strokeStyle=p.main+'33';c.lineWidth=2;c.stroke();
}
cards.forEach(({strength,i,x,y,p})=>{
 round(x,y,cardW,cardH,33,grad(x,y,x+cardW,y+cardH,[[0,'#ffffffee'],[1,p.light]]),'#ffffff',12);
 icon(strength.icon,x+cardW/2,y+43,43,p.main);
 fitted(strength.label,x+cardW/2,y+100,cardW-36,64,count===1?34:26,750,'#352046',2);
 fitted(strength.description,x+cardW/2,y+cardH*.71,cardW-38,cardH*.29,count===1?26:21,500,'#705381',3);
 const linked=strength.journey_ids.map(j=>data.journey.findIndex(v=>v.id===j)).filter(index=>index>=0);
 linked.forEach((index,k)=>circle(x+cardW/2+(k-(linked.length-1)/2)*13,y+cardH-18,3.5,palette[index%palette.length].main));
});
label('Career DNA Studio',W/2,H-22,12,'#a38bb6',500);
canvas.renderMetrics={ok:!issues.length,issues,boxes:metrics,width:W,height:H};return canvas.renderMetrics;
};
