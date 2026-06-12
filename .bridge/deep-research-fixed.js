export const meta = {
  name: 'deep-research',
  description: 'Deep multi-source research with verify-synthesize',
  phases: [{title:'Search'},{title:'Verify'},{title:'Synthesize'}],
};

const Q = 'Decompose into 5 search angles. Return JSON: {"angles":[5 search strings]}. No other text:\n';

phase('Search');
const scope = await agent(Q + args, {
  label:'scope',
  schema: {type:'object', properties:{angles:{type:'array',items:{type:'string'},minItems:3,maxItems:5}}, required:['angles']}
});
let angles = scope.angles;
if (!angles || angles.length < 3) angles = [args];

const results = await Promise.all(angles.map((a,i) => agent(`Search: ${a}`, {
  label:`search:${i+1}`,
  schema: {type:'object', properties:{findings:{type:'string'}}, required:['findings']}
})));

phase('Verify');
const allText = results.map(r => r.findings || r).join('\n\n---\n\n');
const summary = await agent(`Extract the key factual claims. List 5-10 with sources:\n\n${allText.slice(0,8000)}`, {
  label:'summarize', phase:'Verify'
});

const syn = await agent(`Synthesize into a report.\nFindings:\n${summary}\n\nStructure: 1)Executive summary 2)Key findings with evidence 3)Sources cited.`, {
  label:'synthesize', phase:'Synthesize',
  schema: {type:'object', properties:{report:{type:'string'}}, required:['report']}
});
return syn.report;
