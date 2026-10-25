/* ---------- helpers ---------- */
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- scroll: progress bar, nav state, back-to-top ---------- */
const nav=$('#nav'), bar=$('#progress'), totop=$('#totop');
addEventListener('scroll',()=>{
  const h=document.documentElement, max=h.scrollHeight-innerHeight;
  bar.style.width=(max>0?(h.scrollTop/max)*100:0)+'%';
  nav.classList.toggle('solid',h.scrollTop>40);
  totop.classList.toggle('show',h.scrollTop>900);
},{passive:true});
totop.addEventListener('click',()=>scrollTo({top:0,behavior:reduced?'auto':'smooth'}));

/* ---------- mobile menu ---------- */
const burger=$('#burger'), links=$('#navLinks');
burger.addEventListener('click',()=>{
  const open=links.classList.toggle('open');
  burger.setAttribute('aria-expanded',open);
});
links.addEventListener('click',e=>{if(e.target.tagName==='A')links.classList.remove('open')});

/* ---------- reveal section headers ---------- */
const io=new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}
}),{threshold:.15});
$$('.rv').forEach(el=>io.observe(el));

/* ---------- current-page nav highlight ---------- */
(function(){
  const here=location.pathname.split('/').pop()||'index.html';
  $$('.nav-links a').forEach(a=>{
    const target=(a.getAttribute('href')||'').split('#')[0];
    if(target===here)a.classList.add('active');
  });
})();

/* ---------- "More" dropdown ---------- */
const more=$('.nav-more');
if(more){
  const btn=more.querySelector('button');
  btn.addEventListener('click',e=>{e.stopPropagation();more.classList.toggle('drop')});
  addEventListener('click',e=>{if(!more.contains(e.target))more.classList.remove('drop')});
  addEventListener('keydown',e=>{if(e.key==='Escape')more.classList.remove('drop')});
}

/* ---------- tabs ---------- */
$$('.tab-btn').forEach(btn=>btn.addEventListener('click',()=>{
  const group=btn.parentElement;
  group.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  const panels=btn.closest('.panel');
  panels.querySelectorAll('.tab-panel').forEach(p=>p.classList.toggle('active',p.id===btn.dataset.tab));
}));

/* ---------- ember particles ---------- */
const cv=$('#embers');
if(cv&&!reduced){
  const ctx=cv.getContext('2d');
  let W,H,ps=[];
  const N=()=>innerWidth<700?28:64;
  function size(){W=cv.width=cv.offsetWidth;H=cv.height=cv.offsetHeight}
  function spawn(y){return{x:Math.random()*W,y:y!==undefined?y:H+10,r:.6+Math.random()*1.9,s:.2+Math.random()*.7,w:Math.random()*6.28,a:.12+Math.random()*.45,c:Math.random()<.25?'#ffc27a':'#f07d33'}}
  size();addEventListener('resize',size);
  for(let i=0;i<N();i++)ps.push(spawn(Math.random()*H));
  (function loop(){
    ctx.clearRect(0,0,W,H);
    for(const p of ps){
      p.y-=p.s;p.w+=.009;p.x+=Math.sin(p.w)*.35;
      const fade=Math.min(1,p.y/(H*.3));
      ctx.globalAlpha=p.a*fade*(.65+.35*Math.sin(p.w*4));
      ctx.fillStyle=p.c;
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,7);ctx.fill();
      if(p.y<-12)Object.assign(p,spawn());
    }
    ctx.globalAlpha=1;requestAnimationFrame(loop);
  })();
}

/* ---------- footer year ---------- */
$('#year').textContent=new Date().getFullYear();
