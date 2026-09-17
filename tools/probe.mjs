import { existsSync } from 'node:fs';
const [url, width] = process.argv.slice(2);
const puppeteer = (await import('/home/user/abigail-joy-photography/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js')).default;
const executablePath = existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
const b = await puppeteer.launch({ ...(executablePath?{executablePath}:{}), args:['--no-sandbox','--disable-setuid-sandbox'] });
try{
  const p = await b.newPage();
  await p.setViewport({ width:Number(width||1440), height:900 });
  await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
  await p.evaluate(()=>document.fonts.ready);
  await new Promise(r=>setTimeout(r,400));
  const out = await p.evaluate(()=>{
    const r=[];
    const box=(label,el)=>{ if(!el){r.push({label,MISSING:true});return;}
      const c=getComputedStyle(el), b=el.getBoundingClientRect();
      r.push({label, x:Math.round(b.x), w:Math.round(b.width), h:Math.round(b.height),
              dir:c.flexDirection, just:c.justifyContent, ai:c.alignItems,
              pad:c.padding.replace(/\s+/g,' '), bg:c.backgroundColor, ta:c.textAlign}); };
    const q=s=>document.querySelector(s);
    box('hero', q('.ph-hero'));
    box('hero-inner', q('.ph-hero__in'));
    box('trust', q('.ph-trust'));
    box('trust-inner', q('.ph-trust > .e-con-inner'));
    const secs=[...document.querySelectorAll('body > .e-con')];
    secs.forEach((s,i)=>box('sec'+i+' '+s.dataset.id, s));
    const inner=secs.map(s=>s.querySelector(':scope > .e-con-inner')).filter(Boolean);
    inner.forEach((s,i)=>box('inner'+i, s));
    box('story-img-col', q('[data-id=phstoryc02]'));
    box('story-txt-col', q('[data-id=phstoryc03]'));
    box('band-card', q('.ph-band__card'));
    box('shep-head', document.querySelectorAll('[data-id^=phshepc]')[0]);
    box('quote-centre', q('[data-id=phquotec02]'));
    r.push({label:'dividers', v:[...document.querySelectorAll('.ph-rule')].map(d=>{
      const s=d.querySelector('.elementor-divider-separator').getBoundingClientRect();
      const w=d.getBoundingClientRect();
      return Math.round(s.x-w.x)+'/'+Math.round(w.width);})});
    r.push({label:'overflow', docW:document.documentElement.scrollWidth, winW:window.innerWidth});
    return r;
  });
  console.log(JSON.stringify(out,null,0).replace(/\},\{/g,'}\n{'));
} finally { await b.close(); }
