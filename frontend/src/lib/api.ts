const API = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
export function token(){ if(typeof window==='undefined') return ''; return localStorage.getItem('assistant_token') || ''; }
export async function api(path:string, init:RequestInit={}) {
 const headers = new Headers(init.headers); headers.set('Content-Type','application/json'); const t=token(); if(t) headers.set('Authorization',`Bearer ${t}`);
 const response=await fetch(`${API}${path}`,{...init,headers}); if(!response.ok){const body=await response.json().catch(()=>({})); throw new Error(body.detail || `Request failed (${response.status})`);} return response.json();
}
