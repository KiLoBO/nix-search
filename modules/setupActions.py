from pathlib import Path

from modules.configmgr import ConfigManager

class SetupActions():

    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config = config_manager


    def check_existing(self):
        db_path = Path(self.config.get("general.db_path"))

        is_db: bool = db_path.exists()
        is_nix: bool = Path(db_path.parent / "NixOS_options.json").exists()
        is_hm: bool = Path(db_path.parent / "Home-Manager_options.json").exists()
        is_pkgs: bool = Path(db_path.parent / "packages.json").exists()

        result = {
            "db_exists": ["Database exists", is_db],
            "nixOpts_exists": ["Nix Options dumped", is_nix],
            "hmOpts_exists": ["Home-Manager Options dumped", is_hm],
            "pkgs_exists": ["Packages dumped", is_pkgs],
        }

        passed = all(result[key][1] for key in result)
        result["passed"] = passed

        return result
