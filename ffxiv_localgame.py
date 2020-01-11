import os
import sys
import logging
import subprocess
import xml.etree.ElementTree as ElementTree
import ffxiv_tools

from typing import List

class FFXIVLocalGame(object):
    def __init__(self, game_dir, game_executable):
        self._dir = game_dir.lower()
        self._executable = game_executable.lower()

    def exe_name(self) -> str:
        return self._executable

    def run_game(self) -> None:
        subprocess.Popen([os.path.join(self._dir, self._executable)], creationflags=0x00000008, cwd = self._dir)

    def delete_game(self) -> None:
        subprocess.Popen(ffxiv_tools.get_uninstall_exe(), creationflags=0x00000008, cwd = self._dir, shell=True)

def get_game_instances() -> List[FFXIVLocalGame]:
    result = list()

    # Try to use XIVLauncher first if it's installed
    install_folder = ffxiv_tools.get_xivlauncher_folder()
    if (
        install_folder is not None and
        os.path.exists(install_folder)
    ):
        result.append(FFXIVLocalGame(install_folder + "\\", "xivlauncher.exe"))

    # Fallback to vanilla launcher
    if len(result) == 0:
        install_folder = ffxiv_tools.get_installation_folder()
        if (
                install_folder is not None and
                os.path.exists(install_folder)
        ):
            result.append(FFXIVLocalGame(install_folder + "\\boot\\", "ffxivboot.exe"))

    return result
