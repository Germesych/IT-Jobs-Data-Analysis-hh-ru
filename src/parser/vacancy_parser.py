from src.parser.category_manager import parser_links

from src.utils.main_logger import setup_logger
logger = setup_logger(__name__)

def parser():
    parser_links()


if __name__ == "__main__":
    parser_links()
