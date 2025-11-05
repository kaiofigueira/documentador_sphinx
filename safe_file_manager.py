import os
import shutil
import stat
import time
import errno
from pathlib import Path

class SafeFileManager:
    """Classe utilitária para operações seguras de arquivos e diretórios em Windows/Linux."""

    @staticmethod
    def unlock_and_retry(func, path, exc_info):
        """Remove permissão somente-leitura e reexecuta a operação."""
        exc = exc_info[1]
        try:
            if isinstance(exc, PermissionError) or getattr(exc, "errno", None) in (errno.EACCES, errno.EPERM):
                try:
                    st = os.stat(path)
                    if stat.S_ISDIR(st.st_mode):
                        # 700 → rwx para o dono (Linux) / libera travas (Windows)
                        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                    else:
                        # 600 → rw para o dono
                        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
                except OSError:
                    pass
                func(path)
            else:
                raise exc
        except PermissionError:
            # se ainda travar, espera um pouco e tenta mais uma
            time.sleep(0.2)
            try:
                os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            except OSError:
                pass
            func(path)

    @staticmethod
    def rmtree_safe(path: Path, attempts: int = 5):
        """Remove diretórios com segurança, funciona no Windows e Linux."""
        path = Path(path)
        if not path.exists():
            return
        for i in range(attempts):
            try:
                shutil.rmtree(path, onerror=SafeFileManager.unlock_and_retry)
                return
            except PermissionError:
                time.sleep(0.3 * (i + 1))
        shutil.rmtree(path, onerror=SafeFileManager.unlock_and_retry)

    @staticmethod
    def ensure_abs(p: str | Path) -> Path:
        """Garante caminho absoluto."""
        return Path(p).resolve()

    @staticmethod
    def mkdir(p: Path):
        """Cria diretório, se não existir."""
        p.mkdir(parents=True, exist_ok=True)
