"""Build a Launcher-friendly ZIP without development/old/generated-cache files."""
from pathlib import Path
import hashlib
import json
import zipfile
from generate import ROOT, VERSION

def main():
    report=json.loads((ROOT/'docs/static_validation.json').read_text(encoding='utf-8'))
    if report['status']!='PASS' or report['version']!=VERSION:
        raise ValueError('Run static validation before packaging')
    out=ROOT/'dist'
    out.mkdir(exist_ok=True)
    name=f'GiveTechnologyFleets_{VERSION}_Stellaris_4.5.2_UNVERIFIED.zip'
    files=[ROOT/'descriptor.mod',ROOT/'thumbnail.png',ROOT/'README.md',ROOT/'CHANGELOG.md']
    for folder in ['common','events','localisation','docs']:
        files+=sorted(p for p in (ROOT/folder).rglob('*') if p.is_file())
    with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED) as z:
        z.write(ROOT/'GiveTechnologyFleets.mod','GiveTechnologyFleets.mod')
        for p in files:z.write(p,'GiveTechnologyFleets/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(out/name) as z:
        assert z.testzip() is None
        entries=z.namelist()
        assert len(entries)==len(set(entries))
        assert not any('.git/' in n or '__pycache__' in n for n in entries)
        assert not any(n.endswith(('GFT_tech_l_japanese.yml','GFT_fleet_l_japanese.yml')) for n in entries)
    print(str(out/name))
    print('SHA256 '+hashlib.sha256((out/name).read_bytes()).hexdigest())

if __name__=='__main__':main()
