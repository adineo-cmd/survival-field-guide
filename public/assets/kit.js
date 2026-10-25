/* ---------- gear checklist ---------- */
const KIT=[
  {g:'Fire & Light',icon:'i-flame',items:['Lighter (primary)','Stormproof matches','Ferrocerium rod','Tinder cubes or dryer lint','Headlamp + spare batteries']},
  {g:'Water',icon:'i-drop',items:['Metal bottle (for boiling)','Squeeze or straw filter','Purification tablets','Collapsible container']},
  {g:'Shelter',icon:'i-tent',items:['Emergency bivy or tarp','550 paracord — 30 m','Space blanket','Rain shell']},
  {g:'Cutting & Repair',icon:'i-shield',items:['Fixed-blade knife','Folding saw or axe','Multitool','Duct-tape wrap']},
  {g:'First Aid',icon:'i-med',items:['Trauma dressing','Adhesive bandages','Antiseptic wipes','Painkillers','Personal medication','Blister pads']},
  {g:'Navigation & Signal',icon:'i-compass',items:['Baseplate compass','Map in waterproof bag','Pealess whistle','Signal mirror','Power bank + cable']},
  {g:'Food & Extras',icon:'i-leaf',items:['3 days no-cook rations','Electrolyte tablets','Fishing kit','Work gloves','Garbage bags ×2','ID copies + emergency cash']}
];
const KEY='fieldguide-kit-v1';
let packed=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));
const kitGrid=$('#kitGrid');
kitGrid.innerHTML=KIT.map((grp,gi)=>`
  <div class="kit-group">
    <h4><svg class="icon"><use href="#${grp.icon}"/></svg>${grp.g}</h4>
    ${grp.items.map((it,ii)=>`
      <label class="kit-item"><input type="checkbox" data-id="${gi}-${ii}" ${packed.has(gi+'-'+ii)?'checked':''}><span>${it}</span></label>`).join('')}
  </div>`).join('');
function kitUI(){
  const total=KIT.reduce((n,g)=>n+g.items.length,0);
  const done=kitGrid.querySelectorAll('input:checked').length;
  $('#kitCount').innerHTML=`<b>${done}</b> / ${total} PACKED`;
  $('#kitBar').style.width=(done/total*100)+'%';
}
kitGrid.addEventListener('change',e=>{
  const id=e.target.dataset.id;
  e.target.checked?packed.add(id):packed.delete(id);
  localStorage.setItem(KEY,JSON.stringify([...packed]));
  kitUI();
});
$('#kitReset').addEventListener('click',()=>{
  packed.clear();localStorage.removeItem(KEY);
  kitGrid.querySelectorAll('input').forEach(i=>i.checked=false);
  kitUI();
});
kitUI();

