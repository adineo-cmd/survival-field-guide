/* ---------- quiz ---------- */
const QUIZ=[
  {q:'Stranded at dusk — cold, damp, and losing light. What do you handle first?',
   opts:['Find drinking water','Build or find shelter','Start looking for food','Light a big signal fire now'],a:1,
   why:'The Rule of Threes: exposure can kill in three hours, water in three days, food in three weeks. Warm and dry first.'},
  {q:'How long must water boil to be safe at sea level?',
   opts:['30 seconds','1 minute at a rolling boil','5 minutes','10 minutes'],a:1,
   why:'One minute at a rolling boil — three minutes above 2,000 m / 6,500 ft, where water boils cooler.'},
  {q:'A companion is bleeding heavily through your first cloth dressing. You should:',
   opts:['Remove it and clean the wound','Add more layers and keep pressing','Apply a tourniquet immediately','Elevate and wait'],a:1,
   why:'Never remove soaked dressings — they hold the clot. Add layers on top and maintain firm pressure; a tourniquet is for uncontrolled limb bleeding only.'},
  {q:'You are lost, but you told someone your route and return time. Best move?',
   opts:['Walk downhill — rivers lead to people','Follow the sun west','Stay put and make yourself findable','Head for the tallest ridge'],a:2,
   why:'If searchers know where to look, a stationary, signalled position is the fastest rescue. Walking turns a search into a hunt.'},
  {q:'In the backcountry, "three of anything" means:',
   opts:['A meeting point','Distress — need help','A trail marker','Dangerous animals ahead'],a:1,
   why:'Three whistle blasts, three fires, three flashes — three is the universal distress signal worldwide.'},
  {q:'Correct response to a venomous snakebite?',
   opts:['Cut the wound and suck out venom','Ice the bite area','Keep calm and immobilise the limb at heart level','Run back to the trailhead'],a:2,
   why:'Stillness slows venom spread. Remove rings before swelling, immobilise below heart level, and get help moving toward you. Cutting, sucking, icing, and tourniquets all make it worse.'}
];
let qi=0,score=0;
const KEYS='ABCD';
function qShow(){
  const t=QUIZ[qi];
  $('#qTrack').textContent=`QUESTION ${qi+1} / ${QUIZ.length}`;
  $('#qText').textContent=t.q;
  $('#qExplain').className='q-explain';
  $('#qNext').style.display='none';
  $('#qOpts').innerHTML=t.opts.map((o,i)=>`<button class="q-opt" data-i="${i}"><span class="key">${KEYS[i]}</span>${o}</button>`).join('');
  $$('#qOpts .q-opt').forEach(b=>b.addEventListener('click',()=>qAnswer(+b.dataset.i)));
}
function qAnswer(i){
  const t=QUIZ[qi];
  $$('#qOpts .q-opt').forEach(b=>{
    b.disabled=true;
    const bi=+b.dataset.i;
    if(bi===t.a)b.classList.add('ok');
    if(bi===i&&i!==t.a)b.classList.add('bad');
  });
  if(i===t.a)score++;
  const ex=$('#qExplain');
  ex.textContent=(i===t.a?'Correct. ':'Not quite. ')+t.why;
  ex.classList.add('show');
  const next=$('#qNext');
  next.textContent=qi<QUIZ.length-1?'Next question':'See the verdict';
  next.style.display='inline-flex';
}
$('#qNext').addEventListener('click',()=>{
  qi++;
  if(qi<QUIZ.length)qShow();
  else{
    $('#qLive').style.display='none';
    $('#qResult').style.display='block';
    $('#qScore').textContent=`${score}/${QUIZ.length}`;
    const [v,b]=score===6?['FIELD-READY','You could teach this page. Keep the knowledge sharp — skills fade faster than gear wears out.']:
      score>=4?['SOLID BASE CAMP','Strong instincts. Revisit the chapters you missed and the gaps close fast.']:
      score>=2?['PACK MORE KNOWLEDGE','The foundations are there. Reread priorities, water and first aid — then run this again.']:
      ['READ THE MANUAL','Good thing you found this page. Start at chapter 01 and take the exam again.'];
    $('#qVerdict').textContent=v;
    $('#qBlurb').textContent=b;
  }
});
$('#qRestart').addEventListener('click',()=>{qi=0;score=0;$('#qResult').style.display='none';$('#qLive').style.display='block';qShow()});
qShow();

