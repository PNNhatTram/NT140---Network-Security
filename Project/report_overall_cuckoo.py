import json


final_report={}
with open("D:\\ATMMT_Nangcao\\DoAn\\rantro_report.json", "r") as file:
    data = json.load(file)

final_report["info"] = data["info"]
if "procmemory" in data:
#procmemory
    procdump_urls = []
    for item in data["procmemory"]:
        val = item["extracted"]
        for item_1 in val:
            tmp = item_1["urls"]
            procdump_urls = procdump_urls + tmp
    final_report["procmemory"] = {}
    final_report["procmemory"]["urls"] = procdump_urls
if "network" in data:
#network
    network_http_uri = []
    network_tcp_host = []
    network_dns = []
    for item in data["network"]["http"]:
        if "microsoft.com" not in item["uri"] or "windowsupdate" not in item["uri"] or "c.pki.goog" not in item["uri"]:
            network_http_uri.append(item["uri"])
    for item in data["network"]["tcp"]:
        tmp = {}
        dst_ip = item["dst"]
        dst_port = item["dport"]
        tmp["dst_ip"] = dst_ip
        tmp["dport"] = dst_port
        network_tcp_host.append(tmp)

    for item in data["network"]["dns"]:
        tmp = {}
        if "microsoft" not in item["request"] and "windowsupdate" not in item["request"] and "c.pki.goog" not in item["request"]:
            tmp["type"] = item["type"]
            tmp["request"] = item["request"]
            tmp["answers"] = item["answers"]
            network_dns.append(tmp)
    final_report["network"] = {}
    final_report["network"]["http_uri"] = network_http_uri
    final_report["network"]["tcp"] = network_tcp_host
    final_report["network"]["dns"] = network_dns
if "behavior" in data:
#behavior
    behavior = {}
    behavior["processtree"] = data["behavior"]["processtree"]
    behavior["summary"] = {}
    list_fields_summary = ["file_created","file_opened","regkey_opened","command_line","file_written","file_deleted","file_read","regkey_written","dll_loaded"]
    for field in list_fields_summary:
        behavior["summary"][field] = []
        if field in data["behavior"]["summary"]:
            for item in data["behavior"]["summary"][field]:
                #print(item)
                tmp = item.lower()
                if "c:\\python" not in tmp:
                    behavior["summary"][field].append(item)
    final_report["behavior"] = behavior
#dump = json.dumps(final_report,indent=4)
output_path="D:\\ATMMT_Nangcao\\DoAn\\temp.json"
with open(output_path,"w") as file:
    json.dump(final_report, file,indent=4)


