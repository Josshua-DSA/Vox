import logging
import sys


class Logger:
    """
    Wrapper logger terpusat dengan format standar untuk tracking pipeline eksperimen.
    """

    @staticmethod
    def get_logger(name: str = "IndoToxic") -> logging.Logger:
        """
        Inisialisasi dan kembalikan instance logger.

        Args:
            name (str): Nama scope logger.

        Returns:
            logging.Logger: Instance logger yang sudah terkonfigurasi.
        """
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
