import asyncio
import os
import shutil
import urllib.request
import brotli
from pathlib import Path


class generateDumps:
    def __init__(self):
        super().__init__()

    async def genNixOptions(self, cache_dir):
        nix_opts = await asyncio.create_subprocess_exec(
            "nix-build",
            "<nixpkgs/nixos/release.nix>",
            "-A",
            "options",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await nix_opts.communicate()

        if nix_opts.returncode != 0:
            print(f"Error generating nix options. Exit code: {nix_opts.returncode}")
            return None
        try:
            src = Path.cwd() / "result" / "share" / "doc" / "nixos" / "options.json"
            dest = cache_dir / "NixOS_options.json"
            dmp = shutil.copy(src, dest)

            os.unlink("result")

            return Path(dmp)
        except Exception as e:
            print(f"Error copying dumped options: {e}")

    async def genHmOptions(self, cache_dir):
        hm_opts = await asyncio.create_subprocess_exec(
            "nix-build",
            "https://github.com/nix-community/home-manager/archive/master.tar.gz",
            "-A",
            "docs.json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await hm_opts.communicate()

        if hm_opts.returncode != 0:
            print(
                f"Error generating Home-Manager options. Exit code: {hm_opts.returncode}"
            )
            return None

        try:
            src = (
                Path.cwd()
                / "result"
                / "share"
                / "doc"
                / "home-manager"
                / "options.json"
            )
            dest = cache_dir / "Home-Manager_options.json"
            dmp = shutil.copy(src, dest)

            os.unlink("result")

            return Path(dmp)
        except Exception as e:
            print(f"Error copying dumped options: {e}")

    async def genPackages(self, cache_dir, nixpkgs_version):
        url = f"https://channels.nixos.org/{nixpkgs_version}/packages.json.br"
        dest = cache_dir / "packages.json"

        with urllib.request.urlopen(url) as response:
            compressed = response.read()

        decompressed = brotli.decompress(compressed)

        with open(dest, "wb") as f:
            f.write(decompressed)
