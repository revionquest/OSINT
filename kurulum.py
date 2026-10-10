import ast
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid


SUPPORTED = {(3, 11), (3, 12)}
WINDOWS = os.name == "nt"
PROBE = (
    "import sys,struct,json;print(json.dumps(dict("
    "version=list(sys.version_info[:2]),bits=struct.calcsize('P')*8,"
    "implementation=sys.implementation.name,executable=sys.executable,"
    "base_executable=getattr(sys,'_base_executable',sys.executable),"
    "prefix=sys.prefix,base_prefix=sys.base_prefix)))"
)


class SetupError(Exception):
    pass


def clean_environment():
    env = dict(os.environ)
    for key in list(env):
        upper = key.upper()
        if upper.startswith("PYTHON") or upper.startswith("PIP_") or upper in {
            "VIRTUAL_ENV", "__PYVENV_LAUNCHER__", "PYLAUNCHER_ALLOW_INSTALL", "PYLAUNCHER_ALWAYS_INSTALL"
        }:
            env.pop(key, None)
    return env


def probe(command):
    try:
        result = subprocess.run(list(map(str, command)) + ["-I", "-c", PROBE],
                                capture_output=True, text=True, encoding="utf-8", errors="replace",
                                timeout=10, env=clean_environment())
        if result.returncode:
            return None
        info = json.loads(result.stdout.strip())
        if not isinstance(info, dict) or not isinstance(info.get("version"), list):
            return None
        return info
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def compatible(info):
    return bool(info and tuple(info.get("version", [])) in SUPPORTED
                and info.get("bits") == 64 and info.get("implementation") == "cpython")


def registry_pythons():
    if os.name != "nt":
        return
    import winreg
    for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
            access = winreg.KEY_READ | view
            try:
                with winreg.OpenKey(hive, r"Software\Python", 0, access) as root:
                    companies = [winreg.EnumKey(root, i) for i in range(min(winreg.QueryInfoKey(root)[0], 100))]
            except OSError:
                continue
            for company in companies:
                try:
                    with winreg.OpenKey(hive, "Software\\Python\\" + company, 0, access) as parent:
                        tags = [winreg.EnumKey(parent, i) for i in range(min(winreg.QueryInfoKey(parent)[0], 100))]
                except OSError:
                    continue
                for tag in tags:
                    try:
                        key = "Software\\Python\\" + company + "\\" + tag + "\\InstallPath"
                        with winreg.OpenKey(hive, key, 0, access) as install:
                            try:
                                executable = winreg.QueryValueEx(install, "ExecutablePath")[0]
                            except OSError:
                                executable = str(Path(winreg.QueryValueEx(install, "")[0]) / "python.exe")
                            if isinstance(executable, str) and Path(executable).is_file():
                                yield [executable]
                    except (OSError, TypeError):
                        continue


def candidates():
    yield [getattr(sys, "_base_executable", sys.executable)]
    launcher = shutil.which("py")
    if launcher:
        yield [launcher, "-3.12"]
        yield [launcher, "-3.11"]
    yield from registry_pythons()
    for name in ("python3.12", "python3.11", "python", "python3"):
        executable = shutil.which(name)
        if executable and Path(executable).parent.name.casefold() != "windowsapps":
            yield [executable]
    for folder in (os.environ.get("LOCALAPPDATA"), os.environ.get("ProgramFiles"),
                   os.environ.get("ProgramW6432"), os.environ.get("ProgramFiles(x86)")):
        if not folder:
            continue
        for suffix in ("Programs/Python/Python312/python.exe", "Programs/Python/Python311/python.exe",
                       "Python312/python.exe", "Python311/python.exe"):
            path = Path(folder) / suffix
            if path.is_file():
                yield [str(path)]


def select_python():
    seen = set()
    for command in candidates():
        key = tuple(map(str, command))
        if key in seen:
            continue
        seen.add(key)
        info = probe(command)
        if compatible(info):
            base = info.get("base_executable") or info["executable"]
            checked = probe([base])
            if compatible(checked):
                return Path(checked["executable"])
    raise SetupError("Calisan 64-bit Python 3.11 veya 3.12 bulunamadi. "
                     "Python'u https://www.python.org/downloads/windows/ adresinden kurup tekrar ac. "
                     "Yalnizca 3.13/3.14 kuruluysa 3.12'yi yanina kurabilirsin; mevcut Python'u silme.")


def requirements(script):
    try:
        tree = ast.parse(script.read_text(encoding="utf-8-sig"))
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "DEPENDENCIES" for t in node.targets):
                deps = ast.literal_eval(node.value)
                if (isinstance(deps, dict) and deps and "setuptools" in deps
                        and all(isinstance(k, str) and re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?", k)
                                and isinstance(v, str) and re.fullmatch(r"[0-9][A-Za-z0-9_.+-]*", v)
                                for k, v in deps.items())):
                    return deps
                break
    except (OSError, ValueError, SyntaxError):
        pass
    raise SetupError("nickscan.py icindeki kutuphane listesi okunamadi. Paketi tamamen yeniden cikart.")


def state_directory(project):
    parent = os.environ.get("LOCALAPPDATA")
    parent = Path(parent) if parent else Path.home() / "AppData" / "Local"
    identifier = hashlib.sha256(os.path.normcase(str(project.resolve())).encode("utf-8")).hexdigest()[:16]
    root = parent / "NicknameOSINT" / "environments" / identifier
    try:
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=str(root)):
            pass
    except OSError as exc:
        raise SetupError("Kullanici kurulum klasorune yazilamiyor: {} ({})".format(root, exc)) from exc
    return root


@contextlib.contextmanager
def setup_lock(root, timeout=300):
    with (root / "setup.lock").open("a+b") as stream:
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        start = time.monotonic()
        announced = False
        while True:
            try:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() - start >= timeout:
                    raise SetupError("Baska bir kurulum halen calisiyor. Ilk pencere tamamlaninca tekrar dene.")
                if not announced:
                    print("Baska bir kurulumun bitmesi bekleniyor...", flush=True)
                    announced = True
                time.sleep(0.25)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def env_python(folder):
    return folder / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def healthy_environment(folder):
    executable = env_python(folder)
    if not executable.is_file() or not (folder / "pyvenv.cfg").is_file():
        return False
    info = probe([executable])
    if not compatible(info):
        return False
    return (os.path.normcase(os.path.abspath(info.get("prefix", ""))) == os.path.normcase(str(folder.resolve()))
            and info.get("prefix") != info.get("base_prefix"))


def run_step(command, label, log, timeout=600):
    print(label, flush=True)
    with log.open("ab") as output:
        output.write(("\n" + label + "\n").encode("utf-8"))
        output.flush()
        try:
            result = subprocess.run(list(map(str, command)), stdout=output, stderr=subprocess.STDOUT,
                                    env=clean_environment(), timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise SetupError(label + " Zaman asimi; internet ve guvenlik yazilimi izinlerini kontrol et.") from exc
        except OSError as exc:
            raise SetupError(label + " Baslatilamadi: " + str(exc)) from exc
        if result.returncode:
            raise SetupError(label + " Basarisiz; cikis kodu: " + str(result.returncode))


def prepare_environment(base, root, log):
    folder = root / "venv"
    if healthy_environment(folder):
        return env_python(folder)
    if folder.exists():
        backup = root / ("venv-broken-" + time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6])
        try:
            folder.rename(backup)
        except OSError as exc:
            raise SetupError("Eski kurulum klasoru kullanimda. Acik bot pencerelerini kapatip tekrar dene.") from exc
        print("Bozuk kurulum korundu: " + str(backup), flush=True)
    run_step([base, "-I", "-m", "venv", str(folder)], "Sanal ortam olusturuluyor...", log)
    if not healthy_environment(folder):
        raise SetupError("Python komutu bitti fakat calisan sanal ortam olusmadi. "
                         "Bu nedenle kutuphane kurulumuna gecilmedi. Gunlukteki venv hatasini kontrol et.")
    return env_python(folder)


def dependencies_ready(executable, deps):
    code = (
        "import importlib.metadata as m,sys;d=" + repr(deps) + ";"
        "sys.exit(0 if all(m.version(k)==v for k,v in d.items()) else 1)"
    )
    try:
        result = subprocess.run([str(executable), "-I", "-c", code], capture_output=True,
                                env=clean_environment(), timeout=20)
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def imports_ready(executable, log=None):
    try:
        result = subprocess.run([str(executable), "-I", "-c",
                                 "import setuptools; import undetected_chromedriver,selenium,bs4"],
                                capture_output=True, env=clean_environment(), timeout=30)
        if result.returncode and log is not None:
            with log.open("ab") as output:
                output.write(b"\nKutuphane import hatasi:\n" + result.stdout[-6000:] + result.stderr[-6000:])
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired) as exc:
        if log is not None:
            with log.open("a", encoding="utf-8") as output:
                output.write("\nKutuphane import kontrolu: " + str(exc) + "\n")
        return False


def install_dependencies(executable, deps, log):
    versions_ok = dependencies_ready(executable, deps)
    if versions_ok and imports_ready(executable, log):
        print("Kutuphaneler ve surumleri dogrulandi.", flush=True)
        return
    run_step([executable, "-I", "-m", "ensurepip", "--upgrade"], "pip kontrol ediliyor...", log)
    pip = [executable, "-I", "-m", "pip", "--isolated", "--disable-pip-version-check",
           "--no-input", "--retries", "2", "--timeout", "30", "install",
           "--index-url", "https://pypi.org/simple"]
    if versions_ok:
        pip.extend(["--force-reinstall", "--no-cache-dir"])
    run_step(pip + ["setuptools==" + deps["setuptools"]], "Kurulum altyapisi hazirlaniyor...", log)
    remaining = [name + "==" + version for name, version in deps.items() if name != "setuptools"]
    if remaining:
        run_step(pip + remaining, "Gerekli kutuphaneler kuruluyor; ilk kurulum biraz surebilir...", log)
    if not dependencies_ready(executable, deps) or not imports_ready(executable, log):
        raise SetupError("Kutuphane kurulumundan sonra dogrulama basarisiz. "
                         "Basarili kurulmus gibi devam edilmedi.")


def install(project):
    script = project / "nickscan.py"
    if not script.is_file():
        raise SetupError("nickscan.py bulunamadi. ZIP'in tamamini bir klasore cikart; BAT dosyasini tek basina tasima.")
    deps = requirements(script)
    root = state_directory(project)
    log = root / "kurulum.log"
    try:
        with setup_lock(root):
            log.write_text("Nickname OSINT Windows kurulumu\n", encoding="utf-8")
            base = select_python()
            print("Python: " + str(base), flush=True)
            executable = prepare_environment(base, root, log)
            print("Sanal ortam: " + str(executable.parent.parent), flush=True)
            install_dependencies(executable, deps, log)
            return executable
    except (SetupError, OSError) as exc:
        if log.exists():
            tail = log.read_text(encoding="utf-8", errors="replace").splitlines()[-60:]
            if tail:
                print("\nKurulum gunlugunun son bolumu:\n" + "\n".join(tail), flush=True)
        raise SetupError(str(exc) + "\nAyrintili gunluk: " + str(log)) from exc


def main(argv=None, project=None):
    args = list(sys.argv[1:] if argv is None else argv)
    mode = args.pop(0) if args else "install"
    if mode not in {"install", "run"}:
        print("Kullanim: python kurulum.py install veya python kurulum.py run -- [bot secenekleri]", flush=True)
        return 2
    if args and args[0] == "--":
        args.pop(0)
    project = Path(project).resolve() if project is not None else Path(__file__).resolve().parent
    try:
        if not WINDOWS:
            raise SetupError("Bu baslatici Windows 10/11 64-bit icindir. Diger sistemlerde nickscan.py dogrudan kullanilir.")
        executable = install(project)
        if mode == "install":
            print("\nKurulum tamamlandi. Artik baslat.bat dosyasini acabilirsin.", flush=True)
            return 0
        print("\nProgram klasoru: " + str(project), flush=True)
        return subprocess.call([str(executable), "-I", str(project / "nickscan.py")] + args,
                               cwd=str(project), env=clean_environment())
    except KeyboardInterrupt:
        print("\nIslem durduruldu. Sonraki acilista kurulum tekrar kontrol edilecek.", flush=True)
        return 130
    except (SetupError, OSError) as exc:
        print("\nKurulum tamamlanamadi: " + str(exc), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
