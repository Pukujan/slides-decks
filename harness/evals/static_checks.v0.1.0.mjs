import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const data=JSON.parse(fs.readFileSync(path.join(root,'harness/lock.json'),'utf8'));
assert.equal(data.version,'0.1.0');
const gitBlob=(buf)=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+buf.length+'\\0'.replace('\\0','\0')),buf])).digest('hex');
for(const entry of data.packages){
 assert.match(entry.version,/^\d+\.\d+\.\d+$/);
 assert(entry.path.includes('v'+entry.version+'.'),'Unversioned package '+entry.path);
 const file=path.join(root,entry.path);
 assert(fs.existsSync(file),'Missing '+entry.path);
 const actual=gitBlob(fs.readFileSync(file));
 assert.equal(actual,entry.git_blob_sha,'Modified pinned package '+entry.path);
}
const gold=path.join(root,data.golden.path);
assert(fs.existsSync(gold),'Missing golden PDF');
assert.equal(gitBlob(fs.readFileSync(gold)),data.golden.git_blob_sha,'Golden PDF mutated');
const router=JSON.parse(fs.readFileSync(path.join(root,'harness/router/state-machine.v0.1.0.json'),'utf8'));
assert.equal(router.version,'0.1.0');
for(const [state,s] of Object.entries(router.states)){
 assert(router.roles[s.owner],state+' has unknown owner '+s.owner);
 for(const next of s.next)assert(router.states[next],'Bad edge '+state+'->'+next);
}
console.log('locked modules/prompts/router + golden + transition graph: PASS ('+data.packages.length+' version-pinned packages)');
