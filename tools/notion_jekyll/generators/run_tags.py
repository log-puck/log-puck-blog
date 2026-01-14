"""
Entry point for tag generation (tag pages + top tags + cleanup).
"""

from .tags import TagGenerator


def main() -> None:
    generator = TagGenerator()
    generator.generate_tag_pages()
    generator.generate_top_tags_data()
    generator.cleanup_orphan_tag_pages()


if __name__ == "__main__":
    main()
