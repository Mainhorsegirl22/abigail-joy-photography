import { existsSync } from 'node:fs';
const [url, width] = process.argv.slice(2);
const puppeteer = (await import('/home/user/abigail-joy-photography/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js')).default;
const executablePath = existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
const b = await puppeteer.launch({ ...(executablePath?{executablePath}:{}), args:['--no-sandbox','--disable-setuid-sandbox'] });
try{
  const p = await b.newPage();
  await p.setViewport({ width:Number(width||1440), height:900, deviceScaleFactor:1 });
  await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
  await p.evaluate(()=>document.fonts.ready);
  await new Promise(r=>setTimeout(r,500));
  const out = await p.evaluate(()=>{
    const q = (sel,props)=>{
      const el = document.querySelector(sel);
      if(!el) return {sel, MISSING:true};
      const c = getComputedStyle(el), r = el.getBoundingClientRect();
      const o = {sel, w:Math.round(r.width), h:Math.round(r.height)};
      for(const pr of props) o[pr]=c[pr];
      return o;
    };
    return [
      q('.ph-hero',['minHeight','justifyContent','paddingLeft']),
      q('.ph-hero .elementor-heading-title',['fontSize','color','fontFamily']),
      q('.ph-hero .ph-script p',['fontSize','color','fontFamily']),
      q('.ph-hero__in',['maxWidth']),
      q('.ph-trust__row',['flexDirection','justifyContent']),
      q('.ph-split',['flexDirection','maxWidth','alignItems']),
      q('.ph-frame img',['height','objectFit']),
      q('.ph-strip__row',['flexDirection','gap']),
      q('.ph-strip__img',['flexBasis','flexGrow']),
      q('.ph-strip__img img',['height','width','objectFit']),
      q('.ph-band__card',['maxWidth','backgroundColor','marginLeft']),
      q('.ph-sec',['paddingTop','paddingLeft','backgroundColor']),
      q('.ph-linen',['backgroundColor']),
      q('.ph-white',['backgroundColor']),
      q('.ph-script p',['fontSize','fontFamily']),
      q('.ph-quote p',['fontSize','fontStyle']),
      q('.ph-list ul',['display','gridTemplateColumns']),
      q('.ph-step .elementor-icon',['width','height','borderRadius','backgroundColor']),
      q('.elementor-button',['backgroundColor','color','fontSize','letterSpacing']),
      q('.ph-edge__text',['maxWidth','marginLeft']),
      q('.ph-dog:nth-child(2)',['marginTop']),
      q('.ph-narrow',['maxWidth','textAlign','alignItems']),
    ];
  });
  const scroll = await p.evaluate(()=>({docW:document.documentElement.scrollWidth, winW:window.innerWidth}));
  console.log(JSON.stringify({scroll, out}, null, 1));
} finally { await b.close(); }
