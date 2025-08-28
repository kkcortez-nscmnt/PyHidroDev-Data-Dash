from pathlib import Path


def get_path_files(target_folder="files", extensions=None):
    """
    Retorna uma lista com os caminhos de arquivos com extenção expecificada.
    Args:
      target_folder - str : Nome da pasta onde buscar os arquivos (padrão: files)
      extension - list : Lista com extensões como padrão de busca.
    Return:
      list: lista de Path para os arquivos encontrados.
    """
    if extensions is None:
        extensions = [".csv"]

    project_root = Path.cwd()

    files_dir = project_root / target_folder

    if not files_dir.is_dir():
        raise FileNotFoundError(
            f"A pasta {target_folder} não foi encontrada em {project_root}"
        )

    founded_files = []
    for extension in extensions:
        cleaned_extension = extension if extension.startswith(".") else f".{extension}"
        founded_files.extend(
            [f.resolve() for f in files_dir.rglob(f"*{cleaned_extension}")]
        )

    founded_files = list(set(founded_files))
    founded_files.sort()
    return founded_files
