# Pi Zero/1/2: Minimal build, minimal dependencies
block_cipher = None
a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt5'],
    excludes=['numpy', 'scipy', 'matplotlib', 'yaml'],
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='GHST-Pi-Tier1', console=True)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, name='GHST-Pi-Tier1')
