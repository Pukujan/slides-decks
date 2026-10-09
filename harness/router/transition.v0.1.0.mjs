// Versioned routing validator. Enforces *machine-readable transitions*, not LLM behavior.
// Usage: node harness/router/transition.v0.1.0.mjs intake narrative_options
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const folder=path.dirname(fileURLToPath(import.meta.url));
export const router=JSON.parse(fs.readFileSync(path.join(folder,'state-machine.v0.1.0.json'),'utf8'));
export function evaluateTransition({from,to,approvals=[],defect_ticket=null,human_rejection=false,answered=false}) {
  const src=router.states[from];
  if (!src) return {ok:false,reason:'Unknown source state: '+from};
  if (!router.states[to] || !src.next.includes(to)) return {ok:false,reason:'Illegal transition '+from+' -> '+to};
  const a=new Set(approvals);
  const need=router.transition_constraints.approvals_required_for_target[to]||[];
  const missing=need.filter(x=>!a.has(x));
  if(missing.length) return {ok:false,reason:'Missing approval/evidence: '+missing.join(', ')};
  const edge=from+'->'+to;
  if(router.transition_constraints.human_rejection_required.includes(edge)&&!human_rejection)
    return {ok:false,reason:'Explicit human rejection is required to reopen gate'};
  if(router.transition_constraints.unblocking_input_required.includes(edge)&&!answered)
    return {ok:false,reason:'User answers or explicit approved assumptions required'};
  if(router.transition_constraints.ticket_required_on_backward_from.includes(from) && to!=='regression' && to!=='human_release_gate'
      && (!defect_ticket || !defect_ticket.id || !defect_ticket.observed_evidence || !defect_ticket.owning_state))
    return {ok:false,reason:'Documented defect ticket required for lookback'};
  return {ok:true,from,to};
}
if(process.argv[1]===fileURLToPath(import.meta.url)) {
 const [from,to]=process.argv.slice(2);
 const result=evaluateTransition({from,to});
 console.log(JSON.stringify(result,null,2));
 process.exit(result.ok?0:1);
}
