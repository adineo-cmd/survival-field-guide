/* ---------- FAQ ---------- */
const FAQ=[
  ['What is the single most important survival skill?','Not a technique — a habit: preparation. Telling someone your route and return time, carrying the chapter-09 kit, and knowing the Rule of Threes before you leave. In real rescues, calm decision-making in the first hour outweighs every gadget in the pack.'],
  ['How long can a person actually go without water?','The "three days" is a rough average, not a target. In desert heat with exertion, incapacitation can come in hours; at rest in cool shade, people have lasted a week. Performance degrades at just 2% dehydration — drink on a schedule, not on thirst.'],
  ['Is rainwater safe to drink?','Freshly collected rain is among the safest water there is. Avoid the first minutes of runoff off a dirty surface, any puddle that has stood overnight, and water that has touched decaying matter — then you are in the "still treat it" zone.'],
  ['If I could carry only one item, what should it be?','The classic and correct answer is a fixed-blade knife — fire, shelter, cordage, and food all run through it. The honest modern answer: a working phone with a charged power bank, since it converts a survival situation into an inconvenience. Carry both.'],
  ['Are berries safe to eat if birds and animals are eating them?','No — this myth sends people to hospital. Birds tolerate plant toxins that seriously harm humans, and animals eat things that make them sick too. Positive identification or nothing; the universal edibility test in chapter 05 is the only field test that counts.'],
  ['What should I teach my children first?','Four things: if lost, stay put and stay loud (the "hug a tree" rule); keep a whistle on them and teach three blasts; know your real names and phone number — not just "Mum" and "Dad"; and bright clothing. A child who stays put is usually found within hours.'],
  ['Does reading this page make me prepared?','It makes you informed — that is step one of about five. Book a certified first-aid course, practice fire and shelter in benign weather, forage with a local expert, and check the laws where you roam. The page gets you from zero to dangerous-with-yourself; training gets you the rest of the way.']
];
$('#faqList').innerHTML=FAQ.map(([q,a])=>`
  <div class="faq-item">
    <button class="faq-q" aria-expanded="false"><span>${q}</span><span class="pm"></span></button>
    <div class="faq-a"><p>${a}</p></div>
  </div>`).join('');
$$('.faq-item').forEach(item=>{
  const panel=item.querySelector('.faq-a');
  item.querySelector('.faq-q').addEventListener('click',()=>{
    const open=item.classList.contains('open');
    $$('.faq-item.open').forEach(o=>{
      o.classList.remove('open');
      o.querySelector('.faq-a').style.maxHeight='0px';
      o.querySelector('.faq-q').setAttribute('aria-expanded','false');
    });
    if(!open){
      item.classList.add('open');
      panel.style.maxHeight=panel.scrollHeight+'px';
      item.querySelector('.faq-q').setAttribute('aria-expanded','true');
    }
  });
});

