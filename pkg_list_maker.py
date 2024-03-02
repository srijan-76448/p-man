#! /usr/bin/python3

import json, subprocess as sp, os


message_type = {
    "success": 32,
    "worning": 33,
    "error": 31
}

mainDir = os.path.dirname(os.path.abspath(__file__))
user = sp.check_output("echo $USER", shell=True).decode().replace('\n', '')

norms_file_path = os.path.join(mainDir, "norms.json")
settings_file_path = os.path.join(mainDir, "settings.json")


def print_message(msg_type: str, message, error_code: int = False):
    print(f"\033[1;{message_type[msg_type]}m[pan {msg_type}]\033[0m: {message}\033[0m", end='')

    if error_code:
        print(f"[error code {error_code}]")
        print("Exetting...")

    else:
        print('')

    if msg_type != "success":
        exit()


pkgs_path = {
    "installed": os.path.join("/", "home", user, ".installed-pkgs.json"),
    "excluded": os.path.join("/", "home", user, ".excluded-pkgs.json")
}


for p in list(pkgs_path.values()):
    if not os.path.exists(p):
        print_message("worning", f"\'\033[1m{p}\033[0m\' not found\nCreating \'\033[1m{p}\033[0m\'")
        os.system(f"touch {p}")


def get_norms():
    with open(norms_file_path) as f:
        norms = dict(json.load(f))

    return norms


def update_norms():
    norms = get_norms()
    excluded_pkgs = norms["exclude"]
    present_pkgs = get_installed_pkgs()

    for i in excluded_pkgs:
        if i not in list(present_pkgs.keys()):
            del excluded_pkgs[excluded_pkgs.index(i)]

    norms["exclude"] = excluded_pkgs

    with open(pkgs_path["excluded"], 'w') as f:
        json.dump(norms, f, indent=4)


def get_app_name():
    with open(settings_file_path) as f:
        return dict(json.load(f))["App-Settings"]["name"]


def get_installed_pkgs() -> dict:
    pkgman = get_norms()["package-maneger"]
    getpkgarg = get_norms()["get-package-argument"]
    ret = {}
    pkgs = [p.split(' ') for p in sp.check_output(f"{pkgman} {getpkgarg}", shell=True).decode().split('\n') if p != '']

    for p in pkgs:
        ret[p[0]] = p[1]

    return ret


def update_installed_pkgs(pkgs: dict):
    excluded_pkgs = {}
    exclude = get_norms()["exclude"]

    for i in list(pkgs.keys()):
        if i in exclude:
            excluded_pkgs[i] = pkgs[i]
            del pkgs[i]

    with open(pkgs_path["installed"], 'w') as f:
        json.dump(pkgs, f, indent=4)
        print_message("success", f"Updated installed pkgs database at '\033[1m{pkgs_path['installed']}\033[0m' successfully")

    with open(pkgs_path["excluded"], 'w') as f:
        json.dump(excluded_pkgs, f, indent=4)
        print_message("success", f"Updated installed pkgs database at '\033[1m{pkgs_path['excluded']}\033[0m' successfully")


def main():
    try:
        installed_pkgs = get_installed_pkgs()
        update_installed_pkgs(installed_pkgs)
        # update_norms()

    except KeyboardInterrupt:
        print_message("error", "Keyboard Interruption Error")