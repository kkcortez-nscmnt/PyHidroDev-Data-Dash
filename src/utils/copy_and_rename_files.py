import shutil
from pathlib import Path


def copy_and_rename_files(file_paths, source_folder="files", target_folder="dist"):
    """
    Copia arquivos da pasta 'files' para a pasta 'target', renomeando-os.
    Mantem a estrutura de subpastas.
    Args:
      file_paths - list: Lista de paths para os arquivos a serem processados
      source_folder - str: Pasta de origem (padrão: "files")
      target_folder - str: Pasta de destino(padrão: "dist")
    Return:
      dict: Dicionário com mapeamento dos arquivos originais.
    """
    if not file_paths:
        return {}

    dist_dir = Path.cwd() / target_folder
    dist_dir.mkdir(exist_ok=True)

    mapping = {}

    for original_file in file_paths:
        try:
            relative_path = original_file.relative_to(Path.cwd() / source_folder)
        except ValueError:
            relative_path = Path(original_file.name)

        relative_parent_folder = relative_path.parent

        original_name = relative_path.name
        clean_tbl_name = (
            original_name.lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace(r"/", "_")
            .replace("\\", "_")
            .replace("$", "")
            .replace("%", "")
            .replace("__", "_")
            .strip("_")
        )
        updated_name = f'{clean_tbl_name.split(".")[0]}{original_file.suffix}'

        dist_folder = dist_dir / relative_parent_folder
        dist_folder.mkdir(parents=True, exist_ok=True)

        dist_file = dist_folder / updated_name

        shutil.copy2(original_file, dist_file)

        mapping[str(original_file)] = str(dist_file)
    return mapping
