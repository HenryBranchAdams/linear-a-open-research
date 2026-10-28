export const reserveSQL = `INSERT INTO slots(mission,user,handle,expires,state,note,version)
 SELECT ?,?,?,?,'claimed','',1 WHERE
 (SELECT count(*) FROM slots WHERE user=? AND (state='submitted' OR (state='claimed' AND expires>?))) < 2
 ON CONFLICT(mission) DO UPDATE SET user=excluded.user,handle=excluded.handle,expires=excluded.expires,state='claimed',note='',version=slots.version+1
 WHERE (slots.state='available' OR (slots.state='claimed' AND slots.expires<=?)) AND
 (SELECT count(*) FROM slots WHERE user=? AND (state='submitted' OR (state='claimed' AND expires>?))) < 2`;
export function dbFor(env) {
 if (!env.DB) throw new Error('Coordination service unavailable');
 return {q:(sql,...args)=>env.DB.prepare(sql).bind(...args),all:async(sql,...args)=>(await env.DB.prepare(sql).bind(...args).all()).results,first:(sql,...args)=>env.DB.prepare(sql).bind(...args).first()};
}
export function publicSlot(s,now=Date.now()) {
 if (!s || s.state==='available' || (s.state==='claimed' && s.expires<=now)) return {state:'available',handle:null,expires:null};
 return {state:s.state,handle:s.handle,expires:s.expires};
}
