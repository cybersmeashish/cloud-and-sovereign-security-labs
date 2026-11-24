"""Loopback-only synthetic HTTP service; no enterprise identity implementation."""
import json,threading,urllib.request,urllib.error
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

def decision(state,actor):
    if actor not in {"staff-A","staff-B"}:return 403,"unrecognised_synthetic_actor"
    if state.get("policy_present") is not True:return 503,"no_local_policy"
    if type(state.get("now")) is not int or type(state.get("expires")) is not int or state["now"]>=state["expires"]:return 503,"expired_or_invalid_policy_time"
    if type(state.get("bundle_epoch")) is not int or type(state.get("required_epoch")) is not int or state["bundle_epoch"]!=state["required_epoch"]:return 503,"policy_epoch_mismatch"
    if actor!="staff-A":return 403,"case_boundary"
    return 200,"SYN case-A record"


def serve_cases():
    state={"policy_present":True,"now":10,"expires":60,"bundle_epoch":7,"required_epoch":7,"central_available":False}
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path!="/document/A":code,msg=404,"not_found"
            else:code,msg=decision(state,self.headers.get("X-Synthetic-Actor"))
            body=json.dumps({"result":msg}).encode();self.send_response(code);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(("127.0.0.1",0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=dict(state);rows=[]
    scenarios=[("valid_local_policy","staff-A",{},200),("cross_case","staff-B",{},403),("missing_policy","staff-A",{"policy_present":False},503),("expired_policy","staff-A",{"now":60},503),("revoked_epoch","staff-A",{"required_epoch":8},503),("old_restore","staff-A",{"bundle_epoch":6},503),("unknown_actor","unknown",{},403)]
    try:
        for name,actor,patch,expected in scenarios:
            state.clear();state.update(base);state.update(patch)
            req=urllib.request.Request(f"http://127.0.0.1:{server.server_port}/document/A",headers={"X-Synthetic-Actor":actor})
            try:
                with urllib.request.urlopen(req,timeout=3) as response:status=response.status;body=json.load(response)
            except urllib.error.HTTPError as response:status=response.code;body=json.load(response)
            assert status==expected,(name,status,expected)
            rows.append({"scenario":name,"http_status":status,"result":body["result"],"central_available":False})
    finally:server.shutdown();server.server_close();thread.join(timeout=3)
    return rows
